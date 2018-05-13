use std::env;
mod des;

fn main() {
    let args = env::args().collect();
    if args.len() == 3 {
        values = parse_file(args[2]);
        if args[1] == "-e" || args[1] == "--encrypt" { 
                
        }
    } else {
        println!("Not enough arguments specified, please refer to the README.txt file at the root of the project");
    }
}
fn parse_file(filename: String) -> String {
    filename
}
