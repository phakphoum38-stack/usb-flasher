use std::fs::File;
use std::io::{Read, Write};
use std::time::Instant;
use std::env;

const CHUNK: usize = 4 * 1024 * 1024; // 4MB

fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 3 {
        println!("Usage: flash <image> <device>");
        return;
    }

    let image_path = &args[1];
    let device_path = &args[2];

    let mut img = File::open(image_path).expect("Cannot open image");
    let mut dev = File::create(device_path).expect("Cannot open device");

    let total = img.metadata().unwrap().len();
    let mut written: u64 = 0;

    let start = Instant::now();
    let mut buffer = vec![0u8; CHUNK];

    loop {
        let n = img.read(&mut buffer).unwrap();
        if n == 0 {
            break;
        }

        dev.write_all(&buffer[..n]).unwrap();
        written += n as u64;

        let percent = (written as f64 / total as f64) * 100.0;
        let elapsed = start.elapsed().as_secs_f64();
        let speed = (written as f64 / 1024.0 / 1024.0) / elapsed;

        println!("{:.0}%|{:.2}MB/s", percent, speed);
    }

    println!("DONE");
}
