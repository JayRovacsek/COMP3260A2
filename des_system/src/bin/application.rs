use std::env; // for command line arguments
use std::fs::File; // for file opening
use std::io::prelude::*; // for file io
mod des; // The des module, located at ./des/mod.rs
use des::des::decrypt;
use des::des::encrypt;
use des::des::avalanche;
/**
 * application.rs - COMP3260A2
 * The main thread of the des program
 *
 * Authors: Jay Rovacsek, Cody Lewis
 * Since: 14-MAY-2018
 */
fn main() {
    // The main io thread
    let args: Vec<String> = env::args().collect();
    if args.len() >= 3 {
        // can only run with file and operation flags
        let filename = args[1].clone();
        let out_file = args[2].clone();
        let values = parse_file(filename); // get a tuple of the file text and key
        if values.0 == "0" {
            // Encryption methods
            println!(
                "Encrypting using:\nPlaintext P: {}\nKey K: {}",
                values.1, values.2
            );
            let cipher = encrypt(values.1.clone(), values.2.clone());
            println!("Ciphertext C: {}\nNow working on Avalanche...", cipher);
            let result = (cipher, avalanche(values.1.clone(), values.2.clone()));
            println!("Avalanche:\n{}\nFile written to: {}", result.1, out_file);
            write_results(
                out_file,
                values.1,
                values.2,
                result.0,
                values.0.clone(),
                result.1,
            ).expect("Failed to write file");
        } else if values.0 == "1" {
            // Decryption methods
            println!(
                "Decrypting using:\nCiphertext C: {}\nKey K: {}",
                values.1, values.2
            );
            let result = decrypt(values.1.clone(), values.2.clone());
            println!("Plaintext P: {}\nFile written to: {}", result, out_file);
            write_results(
                out_file,
                values.1,
                values.2,
                result,
                values.0.clone(),
                String::new(),
            ).expect("Failed to write file");
        } else {
            println!("The file you input was not in the right format, please refer to the README.txt file at the root of  the project");
        }
    } else {
        println!("Not enough arguments specified, please refer to the README.txt file at the root of the project");
    }
}

pub fn write_results(
    filename: String,
    plaintext: String,
    key: String,
    ciphertext: String,
    mode: String,
    avalanche: String,
) -> std::io::Result<()> {
    let mut f = File::create(filename)?;
    if mode == "0" {
        write!(
            f,
            "ENCRYPTION\nPlaintext P: {}\nKey K: {}\nCiphertext C: {}\nAvalanche:\n{}",
            plaintext, key, ciphertext, avalanche
        )?;
        f.sync_data()?;
    } else {
        write!(
            f,
            "DECRYPTION\nCiphertext C: {}\nKey K: {}\nPlaintext C: {}",
            plaintext, key, ciphertext
        )?;
        f.sync_data()?;
    }
    Ok(())
}
/// Input file parsing method
pub fn parse_file(filename: String) -> (String, String, String) {
    let mut f = File::open(filename).expect("Failed to read file");
    let mut contents = String::new();
    f.read_to_string(&mut contents)
        .expect("Something went wrong when reading the file");
    let (mode, text, key) = {
        let bytes = contents.as_bytes();
        let mut j = 0;
        let mut k = 0;
        let mut l = 0;
        let mut first = true;
        for (i, &item) in bytes.iter().enumerate() {
            if item == b'\n' {
                if first {
                    j = i;
                    first = false;
                } else if k == 0 {
                    k = i;
                } else {
                    l = i;
                    break;
                }
            }
        }
        (
            contents[..j].to_string(),
            contents[j + 1..k].to_string(),
            contents[k + 1..l].to_string(),
        )
    };
    (String::from(mode), String::from(text), String::from(key))
}
