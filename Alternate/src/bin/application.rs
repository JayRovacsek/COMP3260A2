use std::env;
use std::fs::File;
use std::io::prelude::*;
mod des;
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
    if args.len() == 3 {
        let filename = args[2].clone();
        let values = parse_file(filename);
        if args[1] == "-e" || args[1] == "--encrypt" {
            // Encryption methods
        } else if args[1] == "-d" || args[1] == "--decrypt" {
            // Decryption methods
        }
    } else {
        println!("Not enough arguments specified, please refer to the README.txt file at the root of the project");
    }
}
/// Input file parsing method
pub fn parse_file(filename: String) -> (String, String) {
    let mut f = File::open(filename).expect("Failed to read file");
    let mut contents = String::new();
    f.read_to_string(&mut contents)
        .expect("Something went wrong when reading the file");
    let (text, key) = {
        let bytes = contents.as_bytes();
        for (i, &item) in bytes.iter().enumerate() {
            if item == b'\n' {
                return (contents[..i].to_string(), contents[i + 1..].to_string());
            }
        }
        (&contents[..], &contents[..]) // this should never happen, throw exception instead
    };
    (String::from(text), String::from(key))
}
