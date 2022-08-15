// main.rs
//
// Author : Walter Dal'Maz Silva
// Date   : December 21st 2019
//
// File encryption/decryption in Rust.
//
use std::env;
use std::path::Path;
use std::process;
use encryptfile as ef;

// The types of encryption steps.
enum EncType { Encrypt, Decrypt }

/// Prints the usage if called intentionally or resulting from an error.
fn help() {
    println!("usage: pwdcrypt -h");
    println!("usage: pwdcrypt -[e|d] <filepath> <passphrase>");
}

/// Print `help()` or additional messages depending on provided flag.
fn error_args(flag: &str) {
    if flag == "-h" {
        help();
    } else {
        if flag == "-e" || flag == "-d" {
            println!("pwdcrypt: missing arguments for `{}`", flag);
        } else {
            println!("pwdcrypt: unknown flag `{}`", flag);
        }
        help();
    }
}

/// Parse arguments from command line for running the main program.
/// Returns a tuple containing a flag, file name and password.
fn argparse() -> (String, String, String) {
    let args: Vec<String> = env::args().collect();
    let no_args: usize = args.len();

    let flag: &str;
    let file: &str;
    let pass: &str;

    match no_args {
        4 => {
            flag = &args[1];
            file = &args[2];
            pass = &args[3];

            let path = Path::new(file);
            let suffix = path.extension().unwrap().to_str();

            // Only allowed flags are parsed.
            if flag != "-d" && flag != "-e" {
                error_args(flag);
            }

            // I/O file must exist.
            if !path.exists() {
                panic!("pwdcrypt: file not found: {}", file);
            }

            // Only relative paths accepted.
            if !path.is_relative() {
                panic!("pwdcrypt: only relative paths allowed: {}", file);
            }

            // Check extension of encrypted files.
            if flag == "-d" && suffix != Some("crypto") {
                panic!("pwdcrypt: cannot decrypt {:?}", suffix);
            }

            // Minimum password length.
            if pass.len() < 8 {
                panic!("pwdcrypt: pass length < 8, got {}", pass.len());
            }
        }
        _ => {
            if no_args == 2 {
                error_args(&args[1]);
            } else {
                help();
            }
            process::exit(1);
        }
    }

    (flag.to_string(), file.to_string(), pass.to_string())
}

/// Generates the name of an output file.
fn output_name(file: &String, step: EncType) -> String {
    match step {
        EncType::Encrypt => {
            // Add default extension.
            return file.to_owned() + ".crypto";
        }
        EncType::Decrypt => {
            // Remove default extension.
            let stem = Path::new(&file).file_stem().unwrap();
            return stem.to_str().unwrap().to_string();
        }
    }
}

/// Encrypts file using provided password.
fn encrypt(file: String, pass: String) {
    // Make file path as `file`.crypto.
    let outfile = output_name(&file, EncType::Encrypt);

    let mut c = ef::Config::new();
    c.input_stream(ef::InputStream::File(file.to_owned()))
     .output_stream(ef::OutputStream::File(outfile.to_owned()))
     .add_output_option(ef::OutputOption::AllowOverwrite)
     .initialization_vector(ef::InitializationVector::GenerateFromRng)
     .password(ef::PasswordType::Text(pass.to_owned(), ef::scrypt_defaults()))
     .encrypt();

    let _ = ef::process(&c).map_err(
        |e| panic!("pwdcrypt: error encrypting: {:?}", e));
}

/// Decrypts file using provided password.
fn decrypt(file: String, pass: String) {
    // Remove the `.crypto` from suffix.
    let outfile = output_name(&file, EncType::Decrypt);

    let mut c = ef::Config::new();
    c.input_stream(ef::InputStream::File(file.to_owned()))
     .output_stream(ef::OutputStream::File(outfile.to_owned()))
     .add_output_option(ef::OutputOption::AllowOverwrite)
     .password(ef::PasswordType::Text(
         pass.to_owned(), ef::PasswordKeyGenMethod::ReadFromFile))
     .decrypt();

    let _ = ef::process(&c).map_err(
        |e| panic!("pwdcrypt: error decrypting: {:?}", e));
}

fn main() {
    // TODO transform flag to struct!
    let (flag, file, pass) = argparse();
    let flag = &flag[..];

    match flag {
        "-e" => { encrypt(file, pass); }
        "-d" => { decrypt(file, pass); }
        _ => { error_args(flag); }
    }
}
