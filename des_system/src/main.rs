extern crate serde;
#[macro_use]
extern crate serde_derive;
extern crate serde_json;

use std::error::Error;
use std::fs::File;
use std::path::Path;

#[derive(Serialize, Deserialize, Debug)]
struct Json {
    key: i8
}

fn parse_json<P: AsRef<Path>>(path: P) -> Result<Json, Box<Error>> {
    // Open the file in read-only mode.
    let file = File::open(path)?;

    // Read the JSON contents of the file
    let k = serde_json::from_reader(file)?;

    // Return the `User`.
    Ok(k)
}

fn main() {

    let k = parse_json("P.json").unwrap();
    println!("{:#?}", k);
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