/**
 * des/mod.rs - COMP3260A2
 * Module for the des encryption, decryption and avalanche effect
 *
 * Authors: Jay Rovacsek, Cody Lewis
 * Since: 12-MAY-2018
 */
mod des {
    extern crate serde;
    extern crate serde_json;

    use std::fs::File;
    use std::path::Path;
    use std::error::Error;
    use self::serde_json::{Map, Value};
    // Struct for all the data to be stored in the Crypto system
    struct Crypto {
        og_key: String,
        key: String,
        c: String,
        d: String,
        round: isize,
        mode: char,
        subkeys: Vec<String>,
    }
    // Factory method to generate a Crypto struct from a key and mode
    fn build_crypto(key: String, mode: char) -> Crypto {
        let key = pad_key(key.clone()); // shadows the mutable key
        let key_halves = half_text(key.clone());
        let subkeys = generate_subkeys(key.clone(), key_halves.clone());
        Crypto {
            og_key: String::from(key.clone()),
            key: String::from(key.clone()),
            c: String::from(key_halves.0.clone()),
            d: String::from(key_halves.1.clone()),
            round: 1,
            mode: char::from(mode),
            subkeys: subkeys,
        }
    }
    // Take a String and returns 2 Strings of either half of the String
    fn half_text(s: String) -> (String, String) {
        (s[..s.len() / 2].to_string(), s[s.len() / 2..].to_string())
    }
    // Pad the key with the parity bits (even parity)
    fn pad_key(key: String) -> String {
        if key.len() == 56 {
            let mut key: String = key.clone(); // shadow the key into mutable
            let mut split_keys: Vec<String> = Vec::new(); // have a vector of the 7 bit blocks of the key
            while key.len() != 7 {
                split_keys.push(key.split_off(7));
            }
            split_keys.push(key.clone());
            key.clear(); // reset contents
            for mut split_key in split_keys {
                // the parity calculations
                let mut i: isize = 0;
                for bit in split_key.chars() {
                    i += match bit {
                        '0' => 0,
                        '1' => 1,
                        _ => 0,
                    }
                }
                let parity: char = if (i % 2) == 0 { '0' } else { '1' };
                split_key.push(parity); // add parity to key
                key.push_str(&String::from(split_key));
            }
        }
        key.clone()
    }
    // Generate the sixteen subkeys for each of the rounds
    fn generate_subkeys(key: String, key_halves: (String, String)) -> Vec<String> {
        let shift_order = parse_json(String::from("../boxes/shift.json")).unwrap();
        let mut subkeys = Vec::new();
        let c = key_halves.0.clone();
        let d = key_halves.1.clone();
        for k in 1..16 {
            let shift = shift_order[&k.to_string()].as_u64().unwrap() as usize;
            let mut c_shift = String::new();
            let mut d_shift = String::new();
            for i in shift..c.len() {
                c_shift.push_str(&c[i..i + 1]);
                d_shift.push_str(&d[i..i + 1]);
            }
            for i in shift..c.len() {
                c_shift.push_str(&c[i..i + 1]);
                d_shift.push_str(&d[i..i + 1]);
            }
            let c = c_shift;
            let d = d_shift;
            subkeys.push(shuffle(
                String::from("../boxes/PC-2.json"),
                c.clone() + d.clone().as_str(),
            ));
        }
        subkeys
    }
    /// Des encryption method
    /// Runs throught the sixteen rounds
    /// returns the cipher text and key
    pub fn encrypt(text: String, key: String) -> (String, String) {
        let sys = build_crypto(key, char::from('e'));
        let text = shuffle(String::from("../boxes/IP.json"), text);
        let text_halves = half_text(text);
        for i in 0..15 {
            let text_halves = round(&sys, text_halves.clone()); // borrows the Crypto struct
        }
        let text = shuffle(
            String::from("../boxes/IPinverse.json"),
            text_halves.0.clone() + text_halves.1.clone().as_str(),
        );
        (text, sys.og_key.clone())
    }
    fn round(sys: &Crypto, text: (String, String)) -> (String, String) {
        let e_text = expand(text.1.clone());
        let xor_text = if sys.mode == 'e' {
            xor(sys.subkeys[sys.round as usize].clone(), e_text)
        } else {
            xor(sys.subkeys[(17 - sys.round) as usize].clone(), e_text)
        };
        text.clone()
    }
    fn expand(text: String) -> String {
        shuffle(String::from("../boxes/ebox.json"), text)
    }
    // xor two Strings containing binary text together
    fn xor(this: String, that: String) -> String {
        let mut result: String = String::new();
        let length = this.len(); // there is no case in this program where this and that are different lengths
        for i in 0..length {
            if this[i..i + 1] == that[i..i + 1] {
                result.push('0');
            } else {
                result.push('1');
            }
        }
        result
    }
    // Take a binary text String and return a vector of all of it's permutations
    fn permute_text(text: String) -> Vec<String> {
        let mut result: Vec<String> = Vec::new();
        for i in 0..text.len() {
            let add: String = if text[i..i + 1].to_string() == "1" {
                String::from("0")
            } else {
                String::from("1")
            };
            let mut push: String = text[..i].to_string();
            push.push_str(&add);
            push.push_str(&text[i + 1..].to_string());
            result.push(push);
        }
        result
    }
    // Find the number of differences between the text and the delta_text
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
    // Parse a json file and return a map representing it
    fn parse_json<P: AsRef<Path>>(path: P) -> Result<Map<String, Value>, Box<Error>> {
        // Open the file
        let file = File::open(path).expect("Failed to read a file");
        let u = serde_json::from_reader(file)?;
        // Return to caller
        Ok(u)
    }
    // Shuffle the text based on a json file input
    fn shuffle(filename: String, text: String) -> String {
        let mut result = String::new();
        let shuffle_map = parse_json(filename).unwrap();
        for val in shuffle_map.values() {
            result.push_str(
                &text[(val.as_u64().unwrap() as usize) - 1..(val.as_u64().unwrap() as usize)],
            );
        }
        result
    }
}
