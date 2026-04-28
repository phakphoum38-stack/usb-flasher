use std::fs::File;
use std::io::{Read, Write, BufWriter};
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 3 {
        println!("Usage: rust-flash <img> <device>");
        return;
    }

    let img_path = &args[1];
    let dev_path = &args[2];

    let mut img = File::open(img_path).expect("open image");
    let dev_file = File::options().write(true).open(dev_path).expect("open device");

    let mut dev = BufWriter::with_capacity(16 * 1024 * 1024, dev_file);

    let total = img.metadata().unwrap().len();
    let mut written: u64 = 0;

    let mut buf = vec![0u8; 8 * 1024 * 1024];

    loop {
        let n = img.read(&mut buf).unwrap();
        if n == 0 {
            break;
        }

        dev.write_all(&buf[..n]).unwrap();
        written += n as u64;

        let percent = (written as f64 / total as f64) * 100.0;

        println!("{:.0}%|0", percent);
    }

    dev.flush().unwrap();
}
