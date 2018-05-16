extern crate serde;
#[macro_use]
extern crate serde_derive;
extern crate serde_json;

use std::fs::File;
use std::path::Path;
use std::error::Error;
use serde_json::Value;
use serde_json::Map;

fn parse_json<P: AsRef<Path>>(path: P) -> Result<Map<String, Value>, Box<Error>> {
    // Open the file in read-only mode.
    let file = File::open(path).expect("failed to read file");
    let u = serde_json::from_reader(file)?;
    // Return the `User`.
    Ok(u)
}

fn main() {
    let k = parse_json("../P.json").unwrap();
    for (_key, value) in k.iter() {
        println!("{}", value);
    }
    // let mut file = File::open("../ebox.json").expect("Unable to read file");
    // let mut contents = String::new();
    // file.read_to_string(contents).expect("Cannot read file");
    // println!("Contents:\n\n{}", contents);
    // parse_json(contents);
}

// fn parse_json(json_str: String){

//     let res = serde_json::from_String(json_str);

//     if res.is_ok() {
//         let j: Json = res.unwrap();
//         println!("Json key: {}",j.key);
//         // for val in j.iter(){
//         //     println!("Json key: {}",j.key);
//         // }
//     } else {
//         println!("Error parsing JSON file");
//     }
// }
