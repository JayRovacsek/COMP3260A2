README.txt - COMP3260 A2
Authors: Cody Lewis, Jay Rovacsek
This program must be run from inside the directory 'des_system/' (not in any of it's branches either) to work!
It is written in rustlang, so you will require rustup and cargo, please ensure they are updated with the command `rustup update`
It may be run with the command: `cargo run <infile> <outfile>` (optionally with the `--release` flag for faster run time)
such that:
<infile> = the input file with format: first line '0' or '1' for encryption/decryption, 
           then the second line is the [cipher|plaintext]text as a binary string ('0's or '1's) of length 64
           and the third line is the key as a binary string of length 56
<outfile> = the file you want the output to be written to (the program will create the file if it does not already exist)
          

Below is the tree of program (before compilation):

des_system/
├── Cargo.toml
├── README.txt
└── src
    ├── bin
    │   ├── application.rs
    │   └── des
    │       └── mod.rs
    └── boxes
        ├── ebox.json
        ├── inverseEbox.json
        ├── IPinverse.json
        ├── IP.json
        ├── PC-1.json
        ├── PC-2.json
        ├── P.json
        ├── s1.json
        ├── s2.json
        ├── s3.json
        ├── s4.json
        ├── s5.json
        ├── s6.json
        ├── s7.json
        ├── s8.json
        └── shift.json

4 directories, 20 files

The code for the interface of the program is contained in application.rs, and the code for the DES crypto-system
is contained in mod.rs.
The .json files specify the boxes of the des system + one for the bit shift pattern.
