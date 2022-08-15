use std::io::{Read, Write, Seek};
use std::collections::HashSet;
use std::rc::Rc;

pub const PW_KEY_SIZE: usize = 64;
pub const IV_SIZE: usize = 16;

use std::clone::Clone;

pub type PwKeyArray = [u8; PW_KEY_SIZE];
pub type IvArray = [u8; IV_SIZE];

/// The current encryption mode.  Initially set to Unknown.
#[derive(Clone)]
pub enum Mode {
    Unknown,
    Encrypt,
    Decrypt,
}

pub trait SeekRead: Seek + Read {}
impl<T> SeekRead for T where T: Seek + Read
{}

pub trait SeekWrite: Seek + Write {}
impl<T> SeekWrite for T where T: Seek + Write
{}

#[derive(PartialEq,Eq,Hash)]
/// Output options.
#[derive(Clone)]
pub enum OutputOption {
    /// If the output file exists and this is set, it will be overwritten.  If this is NOT set
    /// and the file exists, encryption/decryption will return an error.
    ///
    /// This setting is disabled by default.
    AllowOverwrite,
    /// Controls whether metadata about the generated key is included (as cleartext)
    /// in the output file.
    /// For example, if scrypt is used, the metadata contains the Log(N),R,and P
    /// parameters vaues that were provided to scrypt to
    /// generate the key.  The metadata does not include the
    /// original password text or salt.
    ///
    /// This provides a margin of safety in case the original parameters are
    /// lost and the file needs to be decrypted; however, it also make it easier for an attacker
    /// to run brute force attacks since he will know what parameters to use.
    /// This setting only affects password types that use the
    /// `PasswordKeyGenMethod` enum.
    ///
    /// This setting enabled by default.
    IncludeKeyMetadata,
}

/// Data input streams.
#[derive(Clone)]
pub enum InputStream {
    Unknown,
    /// Read from the specified file.
    File(String),
}

/// Data output streams.
#[derive(Clone)]
pub enum OutputStream {
    Unknown,
    /// Write to the specified file.
    File(String),
}

/// Output format.
#[derive(Clone)]
pub enum OutputFormat {
    // EncryptedZip,
    /// The default output format.  This can only (currently) be read by this program.
    EncryptFile,
}

/// Controls how random numbers are generated whenever they are needed by this library.
/// Currently this is only required when generating an initialization vector
/// (`InitializationVector::GenerateFromRng`).  Note, when decrypting, you do not need
/// to specify this.
#[derive(Clone)]
pub enum RngMode {
    /// Use the [Os RNG](https://doc.rust-lang.org/rand/rand/os/struct.OsRng.html) only
    Os,
    /// Use a combination of the Os and
    /// [Isaac64](https://doc.rust-lang.org/rand/rand/isaac/struct.Isaac64Rng.html) generators.
    /// Isaac is seeded with the Os RNG,
    /// and the two RNGs are used to generate the resulting IV 50/50.
    OsIssac,
    /// Use a combination of the Os,
    /// [`rand::random`](https://doc.rust-lang.org/rand/rand/fn.random.html), and Isaac.
    /// Isaac is seeded with the Os Rng
    /// and rand.  Os and Isaac are used to generate the resulting IV 50/50.
    OsRandIssac,
    /// Use the specified function to generate random u8 values.  The function should return a
    /// random u8 each time it is called.
    Func(Rc<Box<Fn() -> u8>>),
}


/// Specifies the initialization vector.  Note, when decrypting, you do not need to specify
/// this since the IV is in the file.
#[derive(Clone)]
pub enum InitializationVector {
    Unknown,
    /// Generate the vector randomly.  See `RngMode`.
    GenerateFromRng,
    /// Use the specified function to provide the IV.  It should return a fully populated IV
    /// array.
    Func(Rc<Box<Fn() -> IvArray>>),
}

/// Specifies the encryption method.
#[derive(Clone)]
pub enum EncryptionMethod {
    AesCbc256,
}

#[derive(Clone)]
/// The Scrypt LogN parameter.
pub struct ScryptLogN(pub u8);
#[derive(Clone)]
/// The Scrypt R parameter.
pub struct ScryptR(pub u32);
#[derive(Clone)]
/// The Scrypt P parameter.
pub struct ScryptP(pub u32);
/// Controls how the encryption key is generated from a text password.
#[derive(Clone)]
pub enum PasswordKeyGenMethod {
    /// Use the scrypt algorithm.
    /// http://www.tarsnap.com/scrypt/scrypt-slides.pdf
    Scrypt(ScryptLogN, ScryptR, ScryptP),
    /// Read the key parameters from the file.  This is valid for
    /// decryption only, and only if `OutputOption::IncludeKeyMetadata`
    /// was used when encrypting the file.
    ReadFromFile,
}
/// Specifies the encryption password.
#[derive(Clone)]
pub enum PasswordType {
    Unknown,
    /// Use the specified text string and PasswordKeyGenMethod.
    /// Leading/trailing whitespace is not trimmed on the string.  Consider specifying
    /// salt via `Config.salt()`.
    Text(String, PasswordKeyGenMethod),
    /// Use the specified function to provide the key.
    Func(Rc<Box<Fn() -> PwKeyArray>>),
}

#[derive(Debug,Clone)]
pub enum ValidateError {
    ModeNotSet,
    InvalidInputStream,
    InvalidOutputStream,
    PasswordTypeIsUnknown,
    PasswordIsEmpty,
    BufferTooSmall,
}

struct DerivedKeyStruct {
    key: PwKeyArray
}

impl Clone for DerivedKeyStruct {
    fn clone(&self) -> Self {
        let ckey = self.key;
        DerivedKeyStruct {
            key: ckey
        }
    }
}

/// The main Configuration type.  This is a Builder object [1].
///
/// A config object can be reused; for instance, you can initially configure it
/// for encryption using `encrypt()`, then switch it to decryption with `decrypt()`.
///
/// [1]: https://aturon.github.io/ownership/builders.html
#[derive(Clone)]
pub struct Config {
    mode: Mode,
    input_stream: InputStream,
    output_stream: OutputStream,
    output_format: OutputFormat,
    output_options: HashSet<OutputOption>,
    rng_mode: RngMode,
    initialization_vector: InitializationVector,
    password: PasswordType,
    salt: String,
    encryption_method: EncryptionMethod,
    buffer_size: usize,
    derived_key: Option<DerivedKeyStruct>
}

/// Returns true if the specfied slice contains all zero values, false otherwise.
pub fn slice_is_zeroed(d: &[u8]) -> bool {
    d.iter().find(|b| **b != 0).is_none()
}

#[cfg(not(test))]
/// Returns a set of default scrypt parameters: LogN 16, R 8, P 1.
/// See http://www.tarsnap.com/scrypt/scrypt-slides.pdf for more details.
pub fn scrypt_defaults() -> PasswordKeyGenMethod {
    // http://stackoverflow.com/questions/11126315/what-are-optimal-scrypt-work-factors
    PasswordKeyGenMethod::Scrypt(ScryptLogN(16), ScryptR(8), ScryptP(1))
}
// todo: fix 'doc' after this is fixed: https://github.com/rust-lang/rfcs/issues/915
#[cfg(any(test,doc))]
pub fn scrypt_defaults() -> PasswordKeyGenMethod {
    // don't melt my laptop
    PasswordKeyGenMethod::Scrypt(ScryptLogN(4), ScryptR(1), ScryptP(1))
}

#[allow(dead_code)]
/// Returns a set of scrypt parameters tuned for file encryption: LogN 20, R 8, P 1
/// See http://www.tarsnap.com/scrypt/scrypt-slides.pdf for more details.
pub fn scrypt_params_encrypt1() -> PasswordKeyGenMethod {
    PasswordKeyGenMethod::Scrypt(ScryptLogN(20), ScryptR(8), ScryptP(1))
}

impl Config {
    /// Constructs a new Config with default settings.  At a minimum, you must set input
    /// streams and a password method, and configure it for encryption or decryption.
    pub fn new() -> Self {
        let mut def_opts = HashSet::new();
        def_opts.insert(OutputOption::IncludeKeyMetadata);

        Config {
            mode: Mode::Unknown,
            input_stream: InputStream::Unknown,
            output_stream: OutputStream::Unknown,
            output_format: OutputFormat::EncryptFile,
            output_options: def_opts,
            rng_mode: RngMode::OsIssac,
            initialization_vector: InitializationVector::GenerateFromRng,
            password: PasswordType::Unknown,
            salt: "DefaultSalt".to_owned(),
            encryption_method: EncryptionMethod::AesCbc256,
            buffer_size: 65536,
            derived_key: None
        }
    }

    /// Enable decryption mode.
    pub fn decrypt(&mut self) -> &mut Self {
        self.mode = Mode::Decrypt;
        self
    }
    /// Enable encryption mode.
    pub fn encrypt(&mut self) -> &mut Self {
        self.mode = Mode::Encrypt;
        self
    }
    /// Set the input stream.
    pub fn input_stream(&mut self, is: InputStream) -> &mut Self {
        self.input_stream = is;
        self
    }
    /// Set the output stream.
    pub fn output_stream(&mut self, os: OutputStream) -> &mut Self {
        self.output_stream = os;
        self
    }
    /// Set output options.
    pub fn output_options(&mut self, opts: HashSet<OutputOption>) -> &mut Self {
        self.output_options = opts;
        self
    }
    /// Add an output option.
    pub fn add_output_option(&mut self, opt: OutputOption) -> &mut Self {
        self.output_options.insert(opt);
        self
    }
    /// Remove an output option.
    pub fn remove_output_option(&mut self, opt: OutputOption) -> &mut Self {
        self.output_options.remove(&opt);
        self
    }
    /// Set the random number mode.  See the `RngMode` enum for information
    /// on how this is used.
    pub fn rng_mode(&mut self, rng_mode: RngMode) -> &mut Self {
        self.rng_mode = rng_mode;
        self
    }
    /// Set the method of determining the initialization vector.
    pub fn initialization_vector(&mut self,
                                 initialization_vector: InitializationVector)
                                 -> &mut Self {
        self.initialization_vector = initialization_vector;
        self
    }
    /// Set the password method.  Also clears the derived key.
    pub fn password(&mut self, password: PasswordType) -> &mut Self {
        self.password = password;
        self.derived_key = None;
        self
    }
    /// Set the salt.  Only used in password methods that require it; if not set,
    /// defaults to "DefaultSalt".
    pub fn salt(&mut self, salt: &str) -> &mut Self {
        self.salt = salt.to_owned();
        self
    }
    /// Set the encryption method.
    pub fn encryption_method(&mut self, encryption_method: EncryptionMethod) -> &mut Self {
        self.encryption_method = encryption_method;
        self
    }
    /// Set the buffer size used for encryption and decryption.  Default is 65536 bytes.
    pub fn buffer_size(&mut self, buffer_size: usize) -> &mut Self {
        self.buffer_size = buffer_size;
        self
    }
    /// Derive the encryption key.  The key is returned and is also
    /// cached on this object (accessible via `get_derived_key()`).  See that function
    /// for details on how long this cached version persists.
    ///
    /// It is not necessary to call this if you are just calling `process()` on a file.
    /// But it is useful if you want to use the key to decrypt many files, or if you
    /// want to use the key for other purposes (such as calculating HMACs).
    pub fn derive_key(&mut self) -> Result<PwKeyArray, super::EncryptError>{
        super::get_pw_key(self)
            .map(|key| {
                self.derived_key = Some(DerivedKeyStruct {
                    key: key
                });
                key
            })
    }

    /// Validate the encryption object; it is not necessary to call this manually since the
    /// configuration will be validated when it is used.
    pub fn validate(&self) -> Result<(), ValidateError> {
        if let Mode::Unknown = self.mode {
            return Err(ValidateError::ModeNotSet);
        }
        if let InputStream::Unknown = self.input_stream {
            return Err(ValidateError::InvalidInputStream);
        }
        if let OutputStream::Unknown = self.output_stream {
            return Err(ValidateError::InvalidOutputStream);
        }
        match self.password {
            PasswordType::Unknown => return Err(ValidateError::PasswordTypeIsUnknown),
            PasswordType::Text(ref s, _) if s.is_empty() => {
                return Err(ValidateError::PasswordIsEmpty)
            }

            PasswordType::Func(_) |
            PasswordType::Text(_, _) => (),
        }
        if self.buffer_size < 4096 {
            return Err(ValidateError::BufferTooSmall);
        }

        Ok(())
    }

    pub fn get_mode(&self) -> &Mode {
        return &self.mode;
    }
    pub fn get_input_stream(&self) -> &InputStream {
        return &self.input_stream;
    }
    pub fn get_output_stream(&self) -> &OutputStream {
        return &self.output_stream;
    }
    pub fn get_output_format(&self) -> &OutputFormat {
        return &self.output_format;
    }
    pub fn get_output_options(&self) -> &HashSet<OutputOption> {
        return &self.output_options;
    }
    pub fn get_rng_mode(&self) -> &RngMode {
        return &self.rng_mode;
    }
    pub fn get_initialization_vector(&self) -> &InitializationVector {
        return &self.initialization_vector;
    }
    pub fn get_password(&self) -> &PasswordType {
        return &self.password;
    }
    pub fn get_salt(&self) -> &str {
        return &self.salt;
    }
    pub fn get_encryption_method(&self) -> &EncryptionMethod {
        return &self.encryption_method;
    }
    pub fn get_buffer_size(&self) -> usize {
        return self.buffer_size;
    }
    /// If `derive_key()` has been called, returns the derived encryption key.  Otherwise returns
    /// None.  Each time `password()` is called, the derived key will be reset to None.
    pub fn get_derived_key(&self) -> Option<PwKeyArray> {
        match &self.derived_key {
            &None => None,
            &Some(ref ks) => {
                Some(ks.clone().key)
            }
        }
    }
}

#[test]
fn validate() {
    macro_rules! check {
        ( $c:expr, $case:path ) => {
            match $c.validate() {
                Err( $case ) => (),
                x => panic!("Unexpected validate error: {:?}", x)
            }
        }
    }
    macro_rules! check_ok {
        ( $c:expr ) => {
            match $c.validate() {
                Ok(_) => (),
                x => panic!("Unexpected validate error: {:?}", x)
            }
        }
    }

    let mut c = Config::new();

    check!(c, ValidateError::ModeNotSet);
    c.decrypt();
    check!(c, ValidateError::InvalidInputStream);
    c.input_stream(InputStream::File("/foo".to_owned()));
    check!(c, ValidateError::InvalidOutputStream);
    c.output_stream(OutputStream::File("/foo.out".to_owned()));
    check!(c, ValidateError::PasswordTypeIsUnknown);

    c.password(PasswordType::Text("".to_owned(), scrypt_defaults()));
    check!(c, ValidateError::PasswordIsEmpty);
    c.password(PasswordType::Text("    ".to_owned(), scrypt_defaults()));
    check_ok!(c);

    let mut pd: [u8; PW_KEY_SIZE] = [0; PW_KEY_SIZE];
    pd[0] = 1;
    c.password(PasswordType::Func(Rc::new(Box::new(move || pd))));
    check_ok!(c);

    c.buffer_size(0);
    check!(c, ValidateError::BufferTooSmall);
    c.buffer_size(4096);
    check_ok!(c);
}

#[test]
fn derived_key() {
    fn are_eq(a:&[u8], b:&[u8]) -> bool {
        a == b
    }

    let mut c = Config::new();
    c.password(PasswordType::Text("Foo".to_owned(), scrypt_defaults()));
    assert!(c.get_derived_key().is_none());
    let key = c.derive_key().map_err(|e| panic!("Unexpected error: {:?}", e)).unwrap();
    let keyx = c.get_derived_key().unwrap();
    assert!(are_eq(&key,&keyx));

    c.password(PasswordType::Text("Bar".to_owned(), scrypt_defaults()));
    assert!(c.get_derived_key().is_none());
    let key2 = c.derive_key().map_err(|e| panic!("Unexpected error: {:?}", e)).unwrap();
    let key2x = c.get_derived_key().unwrap();
    assert!(are_eq(&key2,&key2x));
    assert!(!are_eq(&key,&key2));
}
