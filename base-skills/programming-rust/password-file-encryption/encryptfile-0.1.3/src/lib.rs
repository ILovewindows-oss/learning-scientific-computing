//! This library provides an interface to Rust Crypto([1]) for encrypting and decrypting files.
//! It provides the following features:
//!
//! 1. A high-level configuration interface to specify various options
//!
//! 2. Generation and verification of HMACs([2]) for the encrypted data.
//!
//! In the future, this library may provide:
//!
//! 1. Support for different encryption methods or output formats.
//!
//! 2. Support for encryption libraries other than rust crypto
//!
//! 3. Support for arbitrary user-provided metadata that is included (encrypted)
//!    with the output file.
//!
//! This library is [on GitHub](https://github.com/jmquigs/rs-encryptfile).
//! Feel free to make feature suggestions in the
//!    [issue tracker](https://github.com/jmquigs/rs-encryptfile/issues).
//!
//! ## Example
//!
//!
//! ```rust
//! use encryptfile as ef;
//!
//! // Encrypt
//! let mut in_file = std::env::var("HOME").unwrap();
//! in_file.push_str("/.bash_history");
//! let mut c = ef::Config::new();
//! c.input_stream(ef::InputStream::File(in_file.to_owned()))
//!  .output_stream(ef::OutputStream::File("/tmp/__encrypted_bash_history.ef".to_owned()))
//!  .add_output_option(ef::OutputOption::AllowOverwrite)
//!  .initialization_vector(ef::InitializationVector::GenerateFromRng)
//!  .password(ef::PasswordType::Text("iloveyou".to_owned(), ef::scrypt_defaults()))
//!  .encrypt();
//! let _ = ef::process(&c).map_err(|e| panic!("error encrypting: {:?}", e));
//!
//! // Decrypt
//! let mut c = ef::Config::new();
//! c.input_stream(ef::InputStream::File("/tmp/__encrypted_bash_history.ef".to_owned()))
//!  .output_stream(ef::OutputStream::File("/tmp/__encrypted_bash_history.txt".to_owned()))
//!  .add_output_option(ef::OutputOption::AllowOverwrite)
//!  .password(ef::PasswordType::Text("iloveyou".to_owned(), ef::PasswordKeyGenMethod::ReadFromFile))
//!  .decrypt();
//! let _ = ef::process(&c).map_err(|e| panic!("error decrypting: {:?}", e));
//! ```
//! [1]: https://github.com/DaGenix/rust-crypto
//! [2]: https://en.wikipedia.org/wiki/Hash-based_message_authentication_code
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!
//!

// #![feature(plugin)]
// #![plugin(clippy)]

use std::io::{Read, Write};
use std::fs::{File, rename, OpenOptions};
use std::path::PathBuf;

extern crate rand;
use self::rand::{Rng, OsRng, Isaac64Rng, SeedableRng};

extern crate crypto;
use self::crypto::scrypt::{scrypt, ScryptParams};

pub use config::{Config, PW_KEY_SIZE, IV_SIZE, PwKeyArray, IvArray, ScryptR, ScryptP, ScryptLogN,
                 PasswordType, PasswordKeyGenMethod, InitializationVector, RngMode, InputStream,
                 Mode, OutputStream,
                 scrypt_defaults, scrypt_params_encrypt1, OutputOption};

use config::{SeekRead, SeekWrite};

mod config;
mod crypto_util;
mod crypt;

use crypt::{encrypt, decrypt, TempFileRemover, EncryptState};

extern crate byteorder;

#[derive(Debug)]
pub enum EncryptError {
    ValidateFailed(config::ValidateError),
    OsRngFailed(std::io::Error),
    OutputFileExists,
    PwKeyIsZeroed,
    IvIsZeroed,
    IvEqualsCheckValue,
    HeaderTooSmall,
    ShortIvRead,
    ShortHmacRead,
    BadHeaderMagic,
    UnexpectedVersion(u32, u32),
    InvalidHmacLength,
    HmacMismatch,
    InvalidPasswordGenMethod,
    InvalidKeyMetadataType(u32),
    UnexpectedEnumVariant(String),
    NoKeyMetadataFound(String),
    ByteOrderError(byteorder::Error),
    IoError(std::io::Error),
    CryptoError(crypto_util::CryptoError),
    InternalError(String),
}

impl From<std::io::Error> for EncryptError {
    fn from(e: std::io::Error) -> Self {
        EncryptError::IoError(e)
    }
}
impl From<byteorder::Error> for EncryptError {
    fn from(e: byteorder::Error) -> Self {
        EncryptError::ByteOrderError(e)
    }
}

fn make_scrypt_key(password: &str,
                   salt: &str,
                   logn: &ScryptLogN,
                   r: &ScryptR,
                   p: &ScryptP)
                   -> PwKeyArray {
    let &ScryptLogN(logn) = logn;
    let &ScryptR(r) = r;
    let &ScryptP(p) = p;

    let salt = salt.as_bytes();
    let pw_bytes = password.as_bytes();

    let mut ek: PwKeyArray = [0; PW_KEY_SIZE];

    let params = ScryptParams::new(logn, r, p);
    scrypt(pw_bytes, salt, &params, &mut ek);
    ek
}

fn generate_iv(c: &Config) -> Result<config::IvArray, EncryptError> {
    let init_val = 47;
    let mut iv: IvArray = [init_val; IV_SIZE];
    if let RngMode::Func(ref bf) = *c.get_rng_mode() {
        for item in &mut iv {
            *item = (*bf)();
        }
    } else {
        let mut os_rng = match OsRng::new() {
            Err(e) => return Err(EncryptError::OsRngFailed(e)),
            Ok(rng) => rng,
        };
        let seed = match *c.get_rng_mode() {
            RngMode::Os |
            RngMode::OsIssac => {
                [os_rng.next_u64(), os_rng.next_u64(), os_rng.next_u64(), os_rng.next_u64()]
            }
            RngMode::OsRandIssac => {
                // Use a combination of OsRng and and regular Rand in case OS has been backdoored
                [rand::random::<u64>(), rand::random::<u64>(), os_rng.next_u64(), os_rng.next_u64()]
            }
            RngMode::Func(_) => {
                return Err(EncryptError::UnexpectedEnumVariant("IV Func should have already been \
                                                                handled"
                                                                   .to_owned()))
            }
        };

        // TODO: needs crypto review.
        match *c.get_rng_mode() {
            RngMode::Func(_) => {
                return Err(EncryptError::UnexpectedEnumVariant("IV Func should have already been \
                                                                handled"
                                                                   .to_owned()))
            }
            RngMode::Os => {
                // skip isaac,  Trust os.
                os_rng.fill_bytes(&mut iv);
            }
            RngMode::OsIssac |
            RngMode::OsRandIssac => {
                // According to the rand crate docs, isaac64 is not supposed to be use for this.
                // But the Os RNG may be backdoored (*cough* Windows Dual_EC_DRBG).
                // So in the interests of paranoia, use a mix of both.

                let mut isaac_rng = Isaac64Rng::from_seed(&seed);
                {
                    let mut first = &mut iv[0..IV_SIZE / 2];
                    os_rng.fill_bytes(first);
                }
                {
                    let mut second = &mut iv[IV_SIZE / 2..IV_SIZE];
                    isaac_rng.fill_bytes(second);
                }
            }
        }
    }

    let check: [u8; IV_SIZE] = [init_val; IV_SIZE];
    if check == iv {
        return Err(EncryptError::IvEqualsCheckValue);
    }

    Ok(iv)
}

fn make_key_from_method(pw: &str,
                        salt: &str,
                        m: &PasswordKeyGenMethod)
                        -> Result<PwKeyArray, EncryptError> {
    match m {
        &PasswordKeyGenMethod::ReadFromFile => Err(EncryptError::InvalidPasswordGenMethod),
        &PasswordKeyGenMethod::Scrypt(ref logn, ref r, ref p) => {
            Ok(make_scrypt_key(pw, salt, logn, r, p))
        }
    }
}

fn get_pw_key(c: &Config) -> Result<PwKeyArray, EncryptError> {
    match *c.get_password() {
        PasswordType::Unknown => {
            Err(EncryptError::UnexpectedEnumVariant("Password type unknown not allowed here"
                                                        .to_owned()))
        }
        PasswordType::Text(ref pw, ref method) => make_key_from_method(pw, &c.get_salt(), method),
        PasswordType::Func(ref bf) => Ok((*bf)()),
    }
    .and_then(|pwkey| {
        if config::slice_is_zeroed(&pwkey) {
            // while its technically possible to have zeroed data at this point, its really
            // unlikely and probably indicates a bug.
            Err(EncryptError::PwKeyIsZeroed)
        } else {
            Ok(pwkey)
        }
    })
}

fn get_iv(c: &Config) -> Result<IvArray, EncryptError> {
    match *c.get_initialization_vector() {
        InitializationVector::Unknown =>
            Err(EncryptError::UnexpectedEnumVariant("Unknown IV not allowed here".to_owned())),
        InitializationVector::Func(ref bf) => Ok((*bf)()),
        InitializationVector::GenerateFromRng => generate_iv(c)
    }
    .and_then(|iv| {
        if config::slice_is_zeroed(&iv) {
            // while its technically possible to have zeroed data at this point, its really unlikely and
            // probably indicates a bug.
            Err(EncryptError::IvIsZeroed)
        } else {
            Ok(iv)
        }
    })
}

/// Process the config and produce the result.  This function does not "consume" the config,
/// so it can be reconfigured and reused after `process()` returns.
pub fn process(c: &Config) -> Result<(), EncryptError> {
    match c.validate() {
        Err(e) => return Err(EncryptError::ValidateFailed(e)),
        Ok(_) => (),
    };

    // open streams
    let in_stream: Box<SeekRead> = match *c.get_input_stream() {
        InputStream::Unknown => {
            return Err(EncryptError::UnexpectedEnumVariant("Unknown InputStream not allowed here"
                                                               .to_owned()))
        }
        InputStream::File(ref file) => Box::new(try!(File::open(file))),
    };

    let out_stream: Box<SeekWrite> = match *c.get_output_stream() {
        OutputStream::Unknown => {
            return Err(EncryptError::UnexpectedEnumVariant("Unknown OutputStream not allowed here"
                                                               .to_owned()))
        }
        OutputStream::File(ref file) => {
            if !c.get_output_options().contains(&OutputOption::AllowOverwrite) {
                let pb = PathBuf::from(file);
                if pb.is_file() || pb.is_dir() {
                    return Err(EncryptError::OutputFileExists);
                }
            }
            Box::new(try!(OpenOptions::new().read(true).write(true).create(true).open(file)))
        }
    };

    // heap-alloc buffers
    let mut read_buf: Vec<u8> = vec![0;c.get_buffer_size()];
    let mut write_buf: Vec<u8> = vec![0;c.get_buffer_size()];

    let mut state = EncryptState {
        config: c,
        iv: [0; IV_SIZE],
        read_buf: &mut read_buf,
        write_buf: &mut write_buf,
    };

    match *c.get_mode() {
        Mode::Unknown => {
            return Err(EncryptError::UnexpectedEnumVariant("Unknown Mode not allowed here"
                                                               .to_owned()))
        }
        Mode::Encrypt => {
            let iv = try!(get_iv(c));
            state.iv = iv;
            try!(encrypt(state, in_stream, out_stream))
        }
        Mode::Decrypt => {
            if let OutputStream::File(ref fname) = *c.get_output_stream() {
                // if decrypting to file, since we have to verify the hmac, don't write directly
                // to the target.  write to a temporary
                // file, then move it over the target path if the decryption & hmac check succeed.

                // make a temp path in same directory
                let tmp_outpath = format!("{}.{}.gc_tmp", fname, rand::random::<u64>());
                let remover = TempFileRemover { filename: tmp_outpath.to_owned() };
                let _ = remover; // silence warning
                let tstream = try!(File::create(&tmp_outpath));
                try!(decrypt(state, in_stream, Box::new(tstream)));
                drop(out_stream);
                try!(rename(tmp_outpath, fname));
            } else {
                try!(decrypt(state, in_stream, out_stream))
            }
        }
    }

    Ok(())
}

// ===============================================================================================
#[cfg(test)]
mod tests {
    use config::*;
    use std::env;
    use std::rc::Rc;

    fn check_eq(xs: &[u8], ys: &[u8], failmsg: String) {
        assert!(xs == ys, failmsg);
    }

    #[test]
    fn get_pwkey_scrypt() {
        let skip_long: i32 = env::var("SKIP_LONG").unwrap_or("0".to_owned()).parse().unwrap();

        let mut c = Config::new();

        fn test_ct_combo(c: &mut Config,
                         logn: u8,
                         r: u32,
                         p: u32,
                         pw: &str,
                         salt: &str,
                         ex: PwKeyArray) {
            c.salt(salt);
            c.password(PasswordType::Text(pw.to_owned(),
                                          PasswordKeyGenMethod::Scrypt(ScryptLogN(logn),
                                                                       ScryptR(r),
                                                                       ScryptP(p))));
            let key = super::get_pw_key(&c);
            let key = key.map_err(|e| panic!("Unexpected error: {:?}", e));

            check_eq(&key.unwrap(),
                     &ex,
                     format!("pw key mismatch: pw: {}, salt: {}", pw, salt));
        }
        // this replicates the rust crypto tests just to make sure I didn't break it
        test_ct_combo(&mut c,
                      4,
                      1,
                      1,
                      "",
                      "",
                      [0x77, 0xd6, 0x57, 0x62, 0x38, 0x65, 0x7b, 0x20, 0x3b, 0x19, 0xca, 0x42,
                       0xc1, 0x8a, 0x04, 0x97, 0xf1, 0x6b, 0x48, 0x44, 0xe3, 0x07, 0x4a, 0xe8,
                       0xdf, 0xdf, 0xfa, 0x3f, 0xed, 0xe2, 0x14, 0x42, 0xfc, 0xd0, 0x06, 0x9d,
                       0xed, 0x09, 0x48, 0xf8, 0x32, 0x6a, 0x75, 0x3a, 0x0f, 0xc8, 0x1f, 0x17,
                       0xe8, 0xd3, 0xe0, 0xfb, 0x2e, 0x0d, 0x36, 0x28, 0xcf, 0x35, 0xe2, 0x0c,
                       0x38, 0xd1, 0x89, 0x06]);
        if skip_long == 0 {
            test_ct_combo(&mut c,
                          10,
                          8,
                          16,
                          "password",
                          "NaCl",
                          [0xfd, 0xba, 0xbe, 0x1c, 0x9d, 0x34, 0x72, 0x00, 0x78, 0x56, 0xe7,
                           0x19, 0x0d, 0x01, 0xe9, 0xfe, 0x7c, 0x6a, 0xd7, 0xcb, 0xc8, 0x23,
                           0x78, 0x30, 0xe7, 0x73, 0x76, 0x63, 0x4b, 0x37, 0x31, 0x62, 0x2e,
                           0xaf, 0x30, 0xd9, 0x2e, 0x22, 0xa3, 0x88, 0x6f, 0xf1, 0x09, 0x27,
                           0x9d, 0x98, 0x30, 0xda, 0xc7, 0x27, 0xaf, 0xb9, 0x4a, 0x83, 0xee,
                           0x6d, 0x83, 0x60, 0xcb, 0xdf, 0xa2, 0xcc, 0x06, 0x40]);
        }
    }

    #[test]
    fn get_pwkey_variants() {
        let mut c = Config::new();

        let pwkey: PwKeyArray = [87; PW_KEY_SIZE];
        let expected = pwkey;
        c.password(PasswordType::Func(Rc::new(Box::new(move || pwkey))));
        let key = super::get_pw_key(&c).unwrap();
        check_eq(&expected, &key, format!("Func pwkey variant failed"));

        let pwkey: PwKeyArray = [0; PW_KEY_SIZE];
        c.password(PasswordType::Func(Rc::new(Box::new(move || pwkey))));
        let key = super::get_pw_key(&c);
        let _ = key.map(|_| panic!("Expected error, but got valid key"));
    }

    #[test]
    fn get_iv_generate() {
        // test the various rnd modes.  since we can't really test that the output is
        // random, just make sure the functions return...something
        let mut c = Config::new();

        c.initialization_vector(InitializationVector::GenerateFromRng);
        {
            let mut testmode = |rngmode| {
                c.rng_mode(rngmode);
                match super::get_iv(&c) {
                    Err(e) => panic!("Unexpected error generating iv: {:?}", e),
                    Ok(vec) => {
                        if slice_is_zeroed(&vec) {
                            panic!("got zeroed iv");
                        }
                    }
                };
            };

            testmode(RngMode::OsIssac);
            testmode(RngMode::OsRandIssac);
        }

        // test user-defined rng function
        c.rng_mode(RngMode::Func(Rc::new(Box::new(|| 6))));
        let expected: IvArray = [6; IV_SIZE];
        let geniv = super::get_iv(&c).unwrap();
        check_eq(&expected, &geniv, format!("Data iv variant failed"));
    }

    #[test]
    fn get_iv_variants() {
        let mut c = Config::new();

        let iv: IvArray = [89; IV_SIZE];
        let expected = iv;

        c.initialization_vector(InitializationVector::Func(Rc::new(Box::new(move || iv))));
        let geniv = super::get_iv(&c).unwrap();
        check_eq(&geniv, &expected, format!("Func iv variant failed"));

        let iv: IvArray = [0; IV_SIZE];
        c.initialization_vector(InitializationVector::Func(Rc::new(Box::new(move || iv))));
        let geniv = super::get_iv(&c);
        let _ = geniv.map(|_| panic!("Expected error, but got valid iv"));
    }
}
