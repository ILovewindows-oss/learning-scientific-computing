use std::io::{Cursor, Read, Write, Seek, SeekFrom};
use std::path::PathBuf;
use std::fs::remove_file;
use std::mem;

extern crate crypto;
use self::crypto::mac::{Mac, MacResult};

extern crate byteorder;
use self::byteorder::{ReadBytesExt, WriteBytesExt, LittleEndian};

pub use super::EncryptError;
pub use super::process;
use config::*;

use config;
use crypto_util;

const MAGIC: u64 = 0xDEADBEEEEEEFCAFE;
const FORMAT_VERSION: u32 = 1;

const MD_TYPE_SCRYPT: u32 = 1;

pub struct EncryptState<'a> {
    pub config: &'a Config,
    pub iv: config::IvArray,
    pub read_buf: &'a mut [u8],
    pub write_buf: &'a mut [u8],
}

pub struct TempFileRemover {
    pub filename: String,
}

impl Drop for TempFileRemover {
    fn drop(&mut self) {
        let pb = PathBuf::from(&self.filename);
        if pb.is_file() {
            match remove_file(&self.filename) {
                Err(e) => println!("Failed to remove temporary file: {}: {}", &self.filename, e),
                Ok(_) => (),
            }
        }
    }
}

struct FileHeader {
    magic: u64,
    fversion: u32,
    hmac_len: u32,
    key_md_size: u32,
    iv: IvArray,
}

const HMAC_RESERVED: usize = 40; // reserved space after FileHeader

impl FileHeader {
    pub fn write(&self, s: &mut Write) -> Result<(), EncryptError> {
        try!(s.write_u64::<LittleEndian>(self.magic));
        try!(s.write_u32::<LittleEndian>(self.fversion));
        try!(s.write_u32::<LittleEndian>(self.hmac_len));
        try!(s.write_u32::<LittleEndian>(self.key_md_size));
        try!(s.write_all(&self.iv));
        Ok(())
    }

    pub fn verify(&self) -> Result<(), EncryptError> {
        if self.magic != MAGIC {
            return Err(EncryptError::BadHeaderMagic);
        }
        if self.fversion != FORMAT_VERSION {
            return Err(EncryptError::UnexpectedVersion(self.fversion, FORMAT_VERSION));
        }
        if self.hmac_len == 0 {
            return Err(EncryptError::InvalidHmacLength);
        }
        if config::slice_is_zeroed(&self.iv) {
            return Err(EncryptError::IvIsZeroed);
        }
        Ok(())
    }

    pub fn read(s: &mut Read) -> Result<FileHeader, EncryptError> {
        let mut header = FileHeader {
            magic: try!(s.read_u64::<LittleEndian>()),
            fversion: try!(s.read_u32::<LittleEndian>()),
            hmac_len: try!(s.read_u32::<LittleEndian>()),
            key_md_size: try!(s.read_u32::<LittleEndian>()),
            iv: [0; IV_SIZE],
        };

        // TODO: use read_exact when it is stable
        let nread = try!(s.read(&mut header.iv));
        if nread != IV_SIZE {
            return Err(EncryptError::ShortIvRead);
        }

        try!(header.verify());

        Ok(header)
    }
}

fn get_key_metadata(c: &Config) -> Result<Vec<u8>, EncryptError> {
    let mut md: Vec<u8> = Vec::new();
    if !c.get_output_options().contains(&OutputOption::IncludeKeyMetadata) {
        return Ok(md);
    }

    match c.get_password() {
        &PasswordType::Unknown |
        &PasswordType::Func(_) |
        &PasswordType::Text(_, PasswordKeyGenMethod::ReadFromFile) => (),
        &PasswordType::Text(_,
                            PasswordKeyGenMethod::Scrypt(ScryptLogN(logn),
                                                         ScryptR(r),
                                                         ScryptP(p))) => {
            try!(md.write_u32::<LittleEndian>(MD_TYPE_SCRYPT));
            try!(md.write_u8(logn));
            try!(md.write_u32::<LittleEndian>(r));
            try!(md.write_u32::<LittleEndian>(p));
        }
    }

    Ok(md)
}

fn read_key_metadata(s: &mut Read,
                     key_md_size: usize)
                     -> Result<(PasswordKeyGenMethod, Vec<u8>), EncryptError> {
    if key_md_size == 0 {
        return Err(EncryptError::InternalError("Key md size is zero, can't read metadata"
                                                   .to_owned()));
    };

    let mut raw_bytes: Vec<u8> = vec![0;key_md_size];
    // TODO: use read_exact when it is stable
    let nread = try!(s.read(&mut raw_bytes));
    if nread != key_md_size {
        return Err(EncryptError::InternalError("short metadata read".to_owned()));
    }

    let method = {
        let mut s = Cursor::new(&raw_bytes);
        let ktype = try!(s.read_u32::<LittleEndian>());
        match ktype {
            MD_TYPE_SCRYPT => {
                let logn = ScryptLogN(try!(s.read_u8()));
                let r = ScryptR(try!(s.read_u32::<LittleEndian>()));
                let p = ScryptP(try!(s.read_u32::<LittleEndian>()));
                PasswordKeyGenMethod::Scrypt(logn, r, p)
            }
            x => return Err(EncryptError::InvalidKeyMetadataType(x)),
        }
    };

    Ok((method, raw_bytes))
}



pub fn encrypt(state: EncryptState,
               mut in_stream: Box<SeekRead>,
               mut out_stream: Box<SeekWrite>)
               -> Result<(), EncryptError> {

    let pwkey = try!(super::get_pw_key(state.config));

    if config::slice_is_zeroed(&pwkey) {
        return Err(EncryptError::PwKeyIsZeroed);
    }

    let mut crypto = crypto_util::CryptoHelper::new(&pwkey, &state.iv, true);
    let mut buf = state.read_buf;

    // obtain key metadata
    let key_md = try!(get_key_metadata(state.config));

    // reserve space for header + hmac
    let header_size = mem::size_of::<FileHeader>();
    let header_capacity = header_size + key_md.len() + HMAC_RESERVED;
    let header: Vec<u8> = vec![0;header_capacity];
    try!(out_stream.write_all(&header));

    loop {
        let num_read = try!(in_stream.read(buf));
        let enc_bytes = &buf[0..num_read];
        let eof = num_read == 0;
        let res = crypto.encrypt(enc_bytes, eof);
        match res {
            Err(e) => return Err(EncryptError::CryptoError(e)),
            Ok(d) => try!(out_stream.write_all(&d)),
        }
        if eof {
            break;
        }
    }

    // include some metadata in the hmac
    crypto.hmac.input(&key_md);
    crypto.hmac.input(&state.iv);
    // TODO: include format version, sizes?

    let hmac = crypto_util::hmac_to_vec(&mut crypto.hmac);
    if hmac.len() >= HMAC_RESERVED {
        return Err(EncryptError::HeaderTooSmall);
    }

    let header = FileHeader {
        magic: MAGIC,
        fversion: FORMAT_VERSION,
        iv: state.iv.clone(),
        hmac_len: hmac.len() as u32,
        key_md_size: key_md.len() as u32,
    };
    try!(out_stream.seek(SeekFrom::Start(0)));
    try!(header.write(&mut out_stream));
    // hmac and md go after the header
    try!(out_stream.write_all(&hmac));
    let hmac_unused = HMAC_RESERVED - hmac.len();
    try!(out_stream.seek(SeekFrom::Current(hmac_unused as i64)));
    try!(out_stream.write_all(&key_md));

    let pos = try!(out_stream.seek(SeekFrom::Current(0)));
    if pos >= header_capacity as u64 {
        // faaack
        return Err(EncryptError::InternalError(format!("Stomped data with header stuff: {} {}",
                                                       pos,
                                                       header_capacity)));
    }

    Ok(())
}

pub fn decrypt(state: EncryptState,
               mut in_stream: Box<SeekRead>,
               mut out_stream: Box<SeekWrite>)
               -> Result<(), EncryptError> {
    let mut buf = state.read_buf;
    let header = try!(FileHeader::read(&mut in_stream));

    // TODO: use read_exact when it is stable
    let hmac_len = header.hmac_len as usize;
    let mut hmac_bytes: Vec<u8> = vec![0;hmac_len];
    let nread = try!(in_stream.read(&mut hmac_bytes));
    if nread != hmac_len {
        return Err(EncryptError::ShortHmacRead);
    }
    let hmac_unused = HMAC_RESERVED - nread;
    try!(in_stream.seek(SeekFrom::Current(hmac_unused as i64)));

    let (pwkey, raw_md_bytes) = if header.key_md_size > 0 {
        let (method, raw_md_bytes) = try!(read_key_metadata(&mut in_stream,
                                                            header.key_md_size as usize));
        let key = try!(match *state.config.get_password() {
            PasswordType::Unknown |
            PasswordType::Func(_) => {
                Err(EncryptError::UnexpectedEnumVariant(format!("Illegal password type (unknown \
                                                                 or func)")))
            }
            PasswordType::Text(ref pw, _) => {
                super::make_key_from_method(pw, state.config.get_salt(), &method)
            }
        });
        (key, raw_md_bytes)
    } else {
        // no metadata in file; this is an error if the method requires it
        match *state.config.get_password() {
            PasswordType::Text(_, PasswordKeyGenMethod::ReadFromFile) => {
                return Err(EncryptError::NoKeyMetadataFound("Metadata not found; you must supply \
                                                             a key gen method that matches the \
                                                             encrypted file"
                                                                .to_owned()))
            }
            PasswordType::Unknown |
            PasswordType::Func(_) |
            PasswordType::Text(_, _) => (),
        }

        let key = try!(super::get_pw_key(state.config));

        (key, vec![0;0])
    };

    let mut crypto = crypto_util::CryptoHelper::new(&pwkey, &header.iv, false);
    // seek to data pos
    let header_size = mem::size_of::<FileHeader>();
    let header_capacity = header_size + header.key_md_size as usize + HMAC_RESERVED;
    try!(in_stream.seek(SeekFrom::Start(header_capacity as u64)));

    loop {
        let num_read = try!(in_stream.read(buf));
        let enc_bytes = &buf[0..num_read];
        let eof = num_read == 0;
        let res = crypto.decrypt(enc_bytes, eof);
        match res {
            Err(e) => return Err(EncryptError::CryptoError(e)),
            Ok(d) => try!(out_stream.write_all(&d)),
        }
        if eof {
            break;
        }
    }

    crypto.hmac.input(&raw_md_bytes);
    crypto.hmac.input(&header.iv);

    let mut computed_hmac = crypto.hmac;
    let expected_hmac = MacResult::new(&hmac_bytes);
    if computed_hmac.result() != expected_hmac {
        return Err(EncryptError::HmacMismatch);
    }

    Ok(())
}

// ===============================================================================================
#[cfg(test)]
mod tests {
    // extern crate tempfile;
    // use self::tempfile::TempFile;
    use std::fs::{remove_file, File, OpenOptions};
    use std::io::{Read, Write, Seek, SeekFrom};

    extern crate tempdir;
    use self::tempdir::TempDir;

    use super::EncryptError;
    use super::FileHeader;

    use config::*;

    fn write_test_file(dir: &TempDir, name: &str, contents: &str) -> String {
        let tdp = dir.path().to_path_buf();
        let mut fname = tdp.clone();
        fname.push(name);
        let fname = fname.to_str().unwrap();
        let mut fstream = File::create(&fname).unwrap();
        let _ = write!(fstream, "{}", contents);
        fname.to_owned()
    }

    fn encrypt_file(td: &TempDir,
                    in_name: &str,
                    out_name: &str,
                    pw: &str,
                    contents: &str)
                    -> (Result<(), EncryptError>, String, String) {
        let in_fname = write_test_file(&td, in_name, contents);
        let out_fname = write_test_file(&td, out_name, "");
        remove_file(&out_fname).unwrap();

        let mut c = Config::new();
        c.input_stream(InputStream::File(in_fname.to_owned()));
        c.output_stream(OutputStream::File(out_fname.to_owned()));
        c.initialization_vector(InitializationVector::GenerateFromRng);
        c.password(PasswordType::Text(pw.to_owned(), scrypt_defaults()));
        c.encrypt();

        let res = super::process(&c).map_err(|e| panic!("error encrypting: {:?}", e));

        (res, in_fname, out_fname)
    }

    #[test]
    fn crypt_basic() {
        let td = TempDir::new("crypt_basic").unwrap();

        let expected = "Hello World!";

        let (res, _, out_fname) = encrypt_file(&td, "in_file", "out_file", "Swordfish", expected);
        let _ = res.map_err(|e| panic!("error encrypting: {:?}", e));

        let in_fname = out_fname;
        let out_fname = write_test_file(&td, "out_file.dec", "");
        remove_file(&out_fname).unwrap();

        let mut c = Config::new();
        c.password(PasswordType::Text("Swordfish".to_owned(), scrypt_defaults()));
        c.input_stream(InputStream::File(in_fname.to_owned()));
        c.output_stream(OutputStream::File(out_fname.to_owned()));
        c.decrypt();

        let _ = super::process(&c).map_err(|e| panic!("error decrypting: {:?}", e));

        let mut fout_stream = File::open(out_fname).unwrap();
        let mut s = String::new();
        fout_stream.read_to_string(&mut s).unwrap();
        assert!(s == expected,
                format!("Expected '{}', got '{}'", expected, s));
    }

    #[test]
    fn crypt_wrong_pw() {
        let td = TempDir::new("crypt_wrong_pw").unwrap();
        let (res, _, out_fname) = encrypt_file(&td, "in_file", "out_file", "Swordfish", "stuff");
        let _ = res.map_err(|e| panic!("error encrypting: {:?}", e));

        let in_fname = out_fname;
        let out_fname = write_test_file(&td, "out_file.dec", "");
        remove_file(&out_fname).unwrap();

        let mut c = Config::new();
        c.password(PasswordType::Text("Clownfish".to_owned(), scrypt_defaults()));
        c.input_stream(InputStream::File(in_fname.to_owned()));
        c.output_stream(OutputStream::File(out_fname.to_owned()));
        c.decrypt();
        match super::process(&c) {
            Err(EncryptError::CryptoError(_)) => (),
            x => panic!("Unexpected result: {:?}", x),
        }
    }

    #[test]
    fn crypt_change_iv() {
        let td = TempDir::new("crypt_change_iv").unwrap();
        let (res, _, out_fname) = encrypt_file(&td, "in_file", "out_file", "Swordfish", "stuff");
        let _ = res.map_err(|e| panic!("error encrypting: {:?}", e));

        let mut fout_stream = OpenOptions::new().read(true).write(true).open(&out_fname).unwrap();
        let mut header = FileHeader::read(&mut fout_stream).unwrap();
        header.iv = [6; IV_SIZE];
        fout_stream.seek(SeekFrom::Start(0)).unwrap();
        header.write(&mut fout_stream).unwrap();
        drop(fout_stream);

        let in_fname = out_fname;
        let out_fname = write_test_file(&td, "out_file.dec", "");
        remove_file(&out_fname).unwrap();

        let mut c = Config::new();
        c.password(PasswordType::Text("Swordfish".to_owned(), scrypt_defaults()));
        c.input_stream(InputStream::File(in_fname.to_owned()));
        c.output_stream(OutputStream::File(out_fname.to_owned()));
        c.decrypt();
        match super::process(&c) {
            Err(EncryptError::HmacMismatch) => (),
            Err(EncryptError::CryptoError(_)) => (),
            x => panic!("Unexpected result: {:?}", x),
        }
    }

    #[test]
    fn crypt_change_hmac() {
        let td = TempDir::new("crypt_change_hmac").unwrap();
        let (res, _, out_fname) = encrypt_file(&td, "in_file", "out_file", "Swordfish", "stuff");
        let _ = res.map_err(|e| panic!("error encrypting: {:?}", e));

        let mut fout_stream = OpenOptions::new().read(true).write(true).open(&out_fname).unwrap();
        let _ = FileHeader::read(&mut fout_stream).unwrap();
        write!(fout_stream, "badhmac").unwrap();
        drop(fout_stream);

        let in_fname = out_fname;
        let out_fname = write_test_file(&td, "out_file.dec", "");
        remove_file(&out_fname).unwrap();

        let mut c = Config::new();
        c.password(PasswordType::Text("Swordfish".to_owned(), scrypt_defaults()));
        c.input_stream(InputStream::File(in_fname.to_owned()));
        c.output_stream(OutputStream::File(out_fname.to_owned()));
        c.decrypt();
        match super::process(&c) {
            Err(EncryptError::HmacMismatch) => (),
            x => panic!("Unexpected result: {:?}", x),
        }
    }

    #[test]
    fn crypt_change_data() {
        let td = TempDir::new("crypt_change_data").unwrap();
        let (res, _, out_fname) = encrypt_file(&td, "in_file", "out_file", "Swordfish", "stuff");
        let _ = res.map_err(|e| panic!("error encrypting: {:?}", e));

        let mut fout_stream = OpenOptions::new().read(true).write(true).open(&out_fname).unwrap();
        fout_stream.seek(SeekFrom::End(-2)).unwrap();
        let z: [u8; 2] = [50; 2];
        fout_stream.write(&z).unwrap();
        drop(fout_stream);

        let in_fname = out_fname;
        let out_fname = write_test_file(&td, "out_file.dec", "");
        remove_file(&out_fname).unwrap();

        let mut c = Config::new();
        c.password(PasswordType::Text("Swordfish".to_owned(), scrypt_defaults()));
        c.input_stream(InputStream::File(in_fname.to_owned()));
        c.output_stream(OutputStream::File(out_fname.to_owned()));
        c.decrypt();
        match super::process(&c) {
            Err(EncryptError::CryptoError(_)) => (),
            x => panic!("Unexpected result: {:?}", x),
        }
    }

    #[test]
    fn crypt_overwrite() {
        let td = TempDir::new("crypt_overwrite").unwrap();

        let in_fname = write_test_file(&td, "in_name", "");
        let out_fname = write_test_file(&td, "out_name", "");

        let mut c = Config::new();
        c.input_stream(InputStream::File(in_fname.to_owned()));
        c.output_stream(OutputStream::File(out_fname.to_owned()));
        c.initialization_vector(InitializationVector::GenerateFromRng);
        c.password(PasswordType::Text("Booger".to_owned(), scrypt_defaults()));
        c.encrypt();

        match super::process(&c) {
            Err(EncryptError::OutputFileExists) => (),
            x => panic!("Unexpected result: {:?}", x),
        }

        c.output_stream(OutputStream::File(out_fname.to_owned()));
        c.add_output_option(OutputOption::AllowOverwrite);
        match super::process(&c) {
            Ok(_) => (),
            x => panic!("Unexpected result: {:?}", x),
        }
    }

    #[test]
    fn crypt_no_key_metadata() {
        let td = TempDir::new("crypt_no_key_metadata").unwrap();
        let in_fname = write_test_file(&td, "in_name", "");
        let out_fname = write_test_file(&td, "out_name", "");

        let mut c = Config::new();
        c.input_stream(InputStream::File(in_fname.to_owned()));
        c.output_stream(OutputStream::File(out_fname.to_owned()));
        c.initialization_vector(InitializationVector::GenerateFromRng);
        c.password(PasswordType::Text("Booger".to_owned(), scrypt_defaults()));
        c.add_output_option(OutputOption::AllowOverwrite);
        c.remove_output_option(OutputOption::IncludeKeyMetadata);
        c.encrypt();

        match super::process(&c) {
            Ok(_) => (),
            x => panic!("Unexpected result: {:?}", x),
        }

        let in_fname = out_fname;
        let out_fname = write_test_file(&td, "out_file.dec", "");
        remove_file(&out_fname).unwrap();

        c.decrypt();
        c.input_stream(InputStream::File(in_fname.to_owned()));
        c.output_stream(OutputStream::File(out_fname.to_owned()));
        c.password(PasswordType::Text("Booger".to_owned(), PasswordKeyGenMethod::ReadFromFile));
        match super::process(&c) {
            Err(EncryptError::NoKeyMetadataFound(_)) => (),
            x => panic!("Unexpected result: {:?}", x),
        }
    }
}
