/**
 * des/mod.rs - COMP3260A2
 * Module for the des encryption, decryption and avalanche effect
 *
 * Authors: Jay Rovacsek, Cody Lewis
 * Since: 12-MAY-2018
 */
mod des {
    struct Crypto {
        og_key: String,
        key: String,
        c: String,
        d: String,
        round: isize,
        mode: char,
        subkeys: Vec<String>,
    }
    fn build_crypto(key: String, mode: char) -> Crypto {
        let key = pad_key(key); // shadows the mutable key
        let key_halves = half_text(key);
        Crypto {
            og_key: String::from(key),
            key: String::from(key),
            c: String::from(key_halves.0),
            d: String::from(key_halves.1),
            round: 1,
            mode: char::from(mode),
            // generate subkeys
        }
    }
    pub fn half_text(s: String) -> (String, String) {
        (s[..s.len() / 2].to_string(), s[s.len() / 2..].to_string())
    }
    fn pad_key(key: String) -> String {
        if key.len() == 56 {
            let mut key: String = key;
            let mut split_keys: Vec<String> = Vec::new();
            while key.len() != 7 {
                split_keys.push(key.split_off(7));
            }
            split_keys.push(key);
            key.clear(); // reset contents
            for split_key in split_keys {
                let mut i: isize = 0;
                for bit in split_key.chars() {
                    i += match bit {
                        '0' => 0,
                        '1' => 1,
                        _ => 0,
                    }
                }
                let parity: char = if (i % 2) == 0 { '0' } else { '1' };
                split_key.push(parity);
                key.push_str(&String::from(split_key));
            }
        }
        key
    }
    pub fn encrypt(text: String, key: String) {
        let sys = build_crypto(key, char::from('e'));
    }

    fn permute_text(text: String) -> Vec<String> {
        let mut result: Vec<String> = Vec::new();
        for i in 0..text.len() {
            let add: String = String::new();
            let add: String = if text[i..i + 1].to_string() == "1" {
                String::from("0")
            } else {
                String::from("1")
            };
            let push: String = text[..i].to_string();
            push.push_str(&add);
            push.push_str(&text[i + 1..].to_string());
            result.push(push);
        }
        result
    }
    fn text_diff(text: String, delta_text: String) -> isize {
        let mut result: isize = 0;
        let length = if text.len() <= delta_text.len() {
            text.len()
        } else {
            delta_text.len()
        };
        for i in 0..length {
            if text[i..i + 1] != delta_text[i..i + 1] {
                result += 1
            }
        }
        result
    }
}
