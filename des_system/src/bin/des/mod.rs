/**
 * des/mod.rs - COMP3260A2
 * Module for the des encryption, decryption and avalanche effect
 *
 * Authors: Jay Rovacsek, Cody Lewis
 * Since: 12-MAY-2018
 */
pub mod des {
    extern crate serde;
    extern crate serde_json;

    use std::fs::File;
    use std::path::Path;
    use std::error::Error;
    use self::serde_json::{Map, Value};
    // Struct for all the data to be stored in the Crypto system
    struct Crypto {
        key: String,
        c: String,
        d: String,
        round: isize,
        mode: char,
        subkeys: Vec<String>,
    }
    // Factory method to generate a Crypto struct from a key and mode
    fn build_crypto(key: String, mode: char) -> Crypto {
        let padded_key = pad_key(key.clone()); // shadows the mutable key
        let key_halves = half_text(shuffle(String::from("../boxes/PC-1.json"), padded_key));
        let subkeys = generate_subkeys(key.clone(), key_halves.clone());
        Crypto {
            key: String::from(key.clone()),
            c: String::from(key_halves.0.clone()),
            d: String::from(key_halves.1.clone()),
            round: 0,
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
            for i in 0..(key.len() / 7) {
                let index = i * 7;
                split_keys.push(key[index..index + 7].to_string());
            }
            key.clear(); // reset contents
            for i in 0..split_keys.len() {
                // the parity calculations
                let mut j: isize = 0;
                for bit in split_keys[i].chars() {
                    j += match bit {
                        '0' => 0,
                        '1' => 1,
                        _ => 0,
                    }
                }
                let parity: char = if (j % 2) == 0 { '0' } else { '1' };
                split_keys[i].push(parity); // add parity to key
                key = format!("{}{}", key, split_keys[i]);
            }
            return key.clone();
        }
        key.clone()
    }
    // Generate the sixteen subkeys for each of the rounds
    fn generate_subkeys(key: String, key_halves: (String, String)) -> Vec<String> {
        let shift_order = parse_json(String::from("../boxes/shift.json")).unwrap();
        let mut subkeys = Vec::new();
        let mut c = key_halves.0.clone();
        let mut d = key_halves.1.clone();
        for k in 1..17 {
            let shift = shift_order[&k.to_string()].as_u64().unwrap() as usize;
            let mut c_shift = String::new();
            let mut d_shift = String::new();
            for i in shift..c.len() {
                c_shift.push_str(&c[i..i + 1]);
                d_shift.push_str(&d[i..i + 1]);
            }
            for i in 0..shift {
                c_shift.push_str(&c[i..i + 1]);
                d_shift.push_str(&d[i..i + 1]);
            }
            c = c_shift;
            d = d_shift;
            subkeys.push(shuffle(
                String::from("../boxes/PC-2.json"),
                format!("{}{}", c, d),
            ));
        }
        subkeys
    }
    /// Avalanche analysis method,
    /// Creates a list of key and string permutations and
    /// returns the average number of bits changed at each permutation
    pub fn avalanche(text: String, key: String) -> String {
        let text_perms = permute_text(text.clone());
        let key_perms = permute_text(text.clone());
        let text_result: String =
            avalanche_perm(text.clone(), key.clone(), text_perms, String::from("text"));
        let key_result: String = avalanche_perm(text, key, key_perms, String::from("key"));
        format!("Avalanche:\n{}\n{}", text_result, key_result)
    }
    /// Avalanche permutation method
    /// Iterates over a Vec<String> and returns a String
    /// of resulting average of modified bits over the range of permutations
    pub fn avalanche_perm(
        text: String,
        key: String,
        perms: Vec<String>,
        perm_type: String,
    ) -> String {
        let mode = char::from('e');
        let mut result = String::new();
        let mut diff_list = Vec::new(); // list the difference between texts in avalanche
        for i in 0..4 {
            let mut temp = Vec::new();
            for j in 0..16 {
                temp.push(Vec::<isize>::new());
            }
            diff_list.push(temp);
        }
        let mut perm_num: usize = 1;
        for perm in perms {
            result = if perm_type == "text" {
                format!("{}\nP and P{} under K\n", result, perm_num)
            } else {
                format!("{}\nP under K and K{}\n", result, perm_num)
            };
            result = format!("{}Round  DES0  DES1  DES2  DES3\n", result);
            let mut des = Vec::new();
            let j = if perm_type == "text" { 2 } else { 1 };
            for k in 0..j {
                let mut temp: Vec<Crypto> = Vec::new();
                for i in 0..4 {
                    temp.push(build_crypto(key.clone(), mode.clone()));
                }
                des.push(temp);
            }
            if perm_type == "key" {
                let mut temp: Vec<Crypto> = Vec::new();
                for i in 0..4 {
                    temp.push(build_crypto(perm.clone(), mode.clone()));
                }
                des.push(temp);
            }
            result = format!("{}    0", result);
            let mut perm_left: Vec<String> = Vec::new();
            let mut perm_right: Vec<String> = Vec::new();
            let mut left_text: Vec<String> = Vec::new();
            let mut right_text: Vec<String> = Vec::new();
            for i in 0..4 {
                let p_text = if perm_type == "text" {
                    half_text(perm.clone())
                } else {
                    half_text(text.clone())
                };
                result = format!(
                    "{}   {}",
                    result,
                    text_diff(text.clone(), format!("{}{}", p_text.0, p_text.1))
                );
                perm_left.push(p_text.0);
                perm_right.push(p_text.1);
                let halved_text = half_text(text.clone());
                left_text.push(halved_text.0);
                right_text.push(halved_text.1);
            }
            for i in 0..16 {
                result = format!("{}\n    {}", result, i + 1);
                let round_text = round(
                    &mut des[0][0],
                    (perm_left[0].clone(), perm_right[0].clone()),
                );
                perm_left[0] = round_text.0;
                perm_right[0] = round_text.1;
                let round_text = round(
                    &mut des[1][0],
                    (left_text[0].clone(), right_text[0].clone()),
                );
                left_text[0] = round_text.0;
                right_text[0] = round_text.1;
                let diff = text_diff(
                    format!("{}{}", left_text[0], right_text[0]),
                    format!("{}{}", perm_left[0], perm_right[0]),
                );
                result = format!("{}   {}", result, diff);
                // unroll the loop for the other 3 deses (same operationsish as what is from here
                // up to the for i loop)
            }
        }
        result
    }
    /// Des encryption method
    /// Runs through the sixteen rounds
    /// returns the cipher text and key
    pub fn encrypt(text: String, key: String) -> String {
        let mut sys = build_crypto(key, char::from('e'));
        crypt(&mut sys, text)
    }
    /// Des decryption method
    /// Runs backwards through the sixteen rounds
    /// returns the plaintext and key
    pub fn decrypt(text: String, key: String) -> String {
        let mut sys = build_crypto(key, char::from('d'));
        crypt(&mut sys, text)
    }
    // The method for both the decryption and encryption
    fn crypt(mut sys: &mut Crypto, text: String) -> String {
        let text = shuffle(String::from("../boxes/IP.json"), text);
        let mut text_halves = half_text(text);
        for i in 0..16 {
            text_halves = round(&mut sys, text_halves.clone()); // borrows the Crypto struct
        }
        let text = shuffle(
            String::from("../boxes/IPinverse.json"),
            format!("{}{}", text_halves.1, text_halves.0), // last flip
        );
        text
    }
    // A round of the des cipher
    fn round(sys: &mut Crypto, text: (String, String)) -> (String, String) {
        let e_text = expand(text.1.clone()); // expand right
        let xor_text = if sys.mode == 'e' {
            // xor with key
            xor(sys.subkeys[sys.round as usize].clone(), e_text)
        } else {
            xor(sys.subkeys[(15 - sys.round) as usize].clone(), e_text)
        };
        let sub_text = substitute(xor_text); // substitute
        let p_text = shuffle(String::from("../boxes/P.json"), sub_text); // permute
        let end_right = xor(p_text, text.0); // xor with left
        sys.round += 1;
        (text.1, end_right)
    }
    // Round function for des1
    fn des1_round(sys: &mut Crypto, text: (String, String)) -> (String, String) {
        let e_text = expand(text.1.clone()); // expand right
        let xor_text = if sys.mode == 'e' {
            // xor with key
            xor(sys.subkeys[sys.round as usize].clone(), e_text)
        } else {
            xor(sys.subkeys[(15 - sys.round) as usize].clone(), e_text)
        };
        let sub_text = substitute(xor_text); // substitute
        let end_right = xor(sub_text, text.0); // xor with left
        sys.round += 1;
        (text.1, end_right)
    }
    // round function for des2
    fn des2_round(sys: &mut Crypto, text: (String, String)) -> (String, String) {
        let e_text = expand(text.1.clone()); // expand right
        let xor_text = if sys.mode == 'e' {
            // xor with key
            xor(sys.subkeys[sys.round as usize].clone(), e_text)
        } else {
            xor(sys.subkeys[(15 - sys.round) as usize].clone(), e_text)
        };
        let einverse_text = shuffle(String::from("../boxes/inverseEbox.json"), xor_text);
        let p_text = shuffle(String::from("../boxes/P.json"), einverse_text); // permute
        let end_right = xor(p_text, text.0); // xor with left
        sys.round += 1;
        (text.1, end_right)
    }
    // round function for des3
    fn des3_round(sys: &mut Crypto, text: (String, String)) -> (String, String) {
        let e_text = expand(text.1.clone()); // expand right
        let xor_text = if sys.mode == 'e' {
            // xor with key
            xor(sys.subkeys[sys.round as usize].clone(), e_text)
        } else {
            xor(sys.subkeys[(15 - sys.round) as usize].clone(), e_text)
        };
        let einverse_text = shuffle(String::from("../boxes/inverseEbox.json"), xor_text);
        let end_right = xor(einverse_text, text.0); // xor with left
        sys.round += 1;
        (text.1, end_right)
    }
    // Expand the input text in accordance to the des ebox
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
    // Pass text through s-boxes
    fn substitute(text: String) -> String {
        let n: usize = 6;
        let split_text = {
            let mut result: Vec<String> = Vec::new();
            for i in 0..(text.len() / n) {
                // split the text into it's blocks
                let index = i * n;
                result.push(text[index..index + 6].to_string());
            }
            result
        };
        let mut s_box: Vec<Map<String, Value>> = Vec::new();
        for i in 1..9 {
            // get the s-boxes
            s_box.push(parse_json(format!("../boxes/s{}.json", i)).unwrap());
        }
        let mut out = String::new();
        for i in 0..8 {
            // sub the text pieces into the s-boxes
            let mut add = format!(
                "{:b}",
                s_box[i].get(&split_text[i]).unwrap().as_u64().unwrap()
            );
            while add.len() < 4 {
                add = format!("{}{}", "0", add);
            }
            out = format!("{}{}", out, add);
        }
        out
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
        let json = serde_json::from_reader(file)?;
        // Return to caller
        Ok(json)
    }
    // Shuffle the text based on a json file input
    fn shuffle(filename: String, text: String) -> String {
        let mut result = String::new();
        let shuffle_map = parse_json(filename).unwrap();
        for i in 0..shuffle_map.len() {
            let val = shuffle_map.get(&format!("{}", i)).unwrap();
            result.push_str(
                &text[(val.as_u64().unwrap() as usize) - 1..(val.as_u64().unwrap() as usize)],
            );
        }
        result
    }
}
