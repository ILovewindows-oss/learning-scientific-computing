# rust-pwdcrypt

A simple file encryption program in Rust.

To build the executable simply run `cargo build --release`.

## Usage

```
usage: pwdcrypt -[e|d] <filepath> <passphrase>
```

Where `-e` is used to encrypt and `-d` to decrypt files.

## Important

The original author of `encryptfile` deleted the project repository, so for ensure this example keeps working on the long term the sources of that crate are commited in here. The idea is to provide an integration straight into the sample executable or replace that wrapper by some maintained code.
