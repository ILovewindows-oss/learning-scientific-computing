use std::iter::repeat;

extern crate crypto;
use self::crypto::{symmetriccipher, buffer, aes, blockmodes};
use self::crypto::buffer::{ReadBuffer, WriteBuffer, BufferResult};
use self::crypto::sha2::Sha256;
use self::crypto::hmac::Hmac;
use self::crypto::mac::Mac;

enum HelperState {
    Encrypting(Box<crypto::symmetriccipher::Encryptor>),
    Decrypting(Box<crypto::symmetriccipher::Decryptor>),
    Done,
}

#[derive(Debug, Clone, Copy)]
pub enum CryptoError {
    AlreadyEncrypting,
    AlreadyDecrypting,
    AlreadyDone,
    SymCipher(symmetriccipher::SymmetricCipherError),
}
impl From<symmetriccipher::SymmetricCipherError> for CryptoError {
    fn from(e: symmetriccipher::SymmetricCipherError) -> Self {
        CryptoError::SymCipher(e)
    }
}

pub struct CryptoHelper {
    state: HelperState,
    pub hmac: Hmac<Sha256>,
}

pub fn hmac_to_vec(hmac: &mut Hmac<Sha256>) -> Vec<u8> {
    let mut hmac_raw: Vec<u8> = repeat(0).take(hmac.output_bytes()).collect();
    hmac.raw_result(&mut hmac_raw);
    hmac_raw
}

impl CryptoHelper {
    pub fn new(key: &[u8], iv: &[u8], encrypting: bool) -> Self {
        let state = {
            if encrypting {
                HelperState::Encrypting(aes::cbc_encryptor(aes::KeySize::KeySize256,
                                                           key,
                                                           iv,
                                                           blockmodes::PkcsPadding))
            } else {
                HelperState::Decrypting(aes::cbc_decryptor(aes::KeySize::KeySize256,
                                                           key,
                                                           iv,
                                                           blockmodes::PkcsPadding))
            }
        };
        CryptoHelper {
            state: state,
            hmac: Hmac::new(Sha256::new(), &key),
        }
    }

    pub fn encrypt(&mut self, data: &[u8], is_all_data: bool) -> Result<Vec<u8>, CryptoError> {
        let final_result = {
            let encryptor = match self.state {
                HelperState::Encrypting(ref mut enc) => enc,
                HelperState::Decrypting(_) => return Err(CryptoError::AlreadyDecrypting),
                HelperState::Done => return Err(CryptoError::AlreadyDone),
            };

            let mut final_result = Vec::<u8>::new();
            let mut read_buffer = buffer::RefReadBuffer::new(data);
            let mut buffer = [0; 4096];
            let mut write_buffer = buffer::RefWriteBuffer::new(&mut buffer);

            loop {
                let result = try!(encryptor.encrypt(&mut read_buffer,
                                                    &mut write_buffer,
                                                    is_all_data));

                final_result.extend(write_buffer.take_read_buffer()
                                                .take_remaining()
                                                .iter()
                                                .cloned());

                match result {
                    BufferResult::BufferUnderflow => break,
                    BufferResult::BufferOverflow => {}
                }
            }

            self.hmac.input(&final_result);
            final_result
        };

        if is_all_data {
            self.state = HelperState::Done;
        }

        Ok(final_result)
    }

    pub fn decrypt(&mut self,
                   encrypted_data: &[u8],
                   is_all_data: bool)
                   -> Result<Vec<u8>, CryptoError> {
        let final_result = {
            let decryptor = match self.state {
                HelperState::Encrypting(_) => return Err(CryptoError::AlreadyEncrypting),
                HelperState::Decrypting(ref mut dec) => dec,
                HelperState::Done => return Err(CryptoError::AlreadyDone),
            };

            let mut final_result = Vec::<u8>::new();
            let mut read_buffer = buffer::RefReadBuffer::new(encrypted_data);
            let mut buffer = [0; 4096];
            let mut write_buffer = buffer::RefWriteBuffer::new(&mut buffer);

            loop {
                let result = try!(decryptor.decrypt(&mut read_buffer,
                                                    &mut write_buffer,
                                                    is_all_data));

                final_result.extend(write_buffer.take_read_buffer()
                                                .take_remaining()
                                                .iter()
                                                .cloned());
                match result {
                    BufferResult::BufferUnderflow => break,
                    BufferResult::BufferOverflow => {}
                }
            }

            self.hmac.input(encrypted_data);
            final_result
        };

        if is_all_data {
            self.state = HelperState::Done;
        }

        Ok(final_result)
    }
}

#[cfg(test)]
mod tests {
    use config::{PwKeyArray, IvArray, PW_KEY_SIZE, IV_SIZE};
    use super::CryptoError;

    #[test]
    fn crypto_util_state() {
        let iv: IvArray = [0; IV_SIZE];
        let key: PwKeyArray = [0; PW_KEY_SIZE];

        {
            let data = [47; 100];
            let mut crypto = super::CryptoHelper::new(&key, &iv, true);
            let _ = crypto.encrypt(&data, false).map_err(|e| panic!("Unexpected error: {:?}", e));
            match crypto.decrypt(&data, true) {
                Err(CryptoError::AlreadyEncrypting) => (),
                e => panic!("Unexpected error: {:?}", e),
            }
            let _ = crypto.encrypt(&data, true).map_err(|e| panic!("Unexpected error: {:?}", e));
            match crypto.encrypt(&data, true) {
                Err(CryptoError::AlreadyDone) => (),
                e => panic!("Unexpected error: {:?}", e),
            }
        }

        {
            let data = {
                let data = [47; 100];
                let mut crypto = super::CryptoHelper::new(&key, &iv, true);
                crypto.encrypt(&data, true)
                      .map_err(|e| panic!("Unexpected error: {:?}", e))
                      .unwrap()
            };
            let mut crypto = super::CryptoHelper::new(&key, &iv, false);
            let _ = crypto.decrypt(&data, false).map_err(|e| panic!("Unexpected error: {:?}", e));
            match crypto.encrypt(&data, true) {
                Err(CryptoError::AlreadyDecrypting) => (),
                e => panic!("Unexpected error: {:?}", e),
            }
            let _ = crypto.decrypt(&data, true).map_err(|e| panic!("Unexpected error: {:?}", e));
            match crypto.decrypt(&data, true) {
                Err(CryptoError::AlreadyDone) => (),
                e => panic!("Unexpected error: {:?}", e),
            }
        }
    }
}
