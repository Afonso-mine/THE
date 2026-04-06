use tokio::net::TcpStream;
use tokio::time::{timeout, Duration};
use std::env;

async fn scan_port(host: &str, port: u16) -> Option<u16> {
    let addr = format!("{}:{}", host, port);

    if let Ok(Ok(_)) = timeout(Duration::from_millis(500), TcpStream::connect(&addr)).await {
        return Some(port);
    }
    None
}

#[tokio::main]
async fn main() {
    let args: Vec<String> = env::args().collect();

    if args.len() < 2 {
        eprintln!("Usage: scanner <host>");
        return;
    }

    let host = &args[1];
    let mut tasks = vec![];

    for port in 1..1025 {
        let h = host.clone();
        tasks.push(tokio::spawn(async move {
            scan_port(&h, port).await
        }));
    }

    let mut open_ports = vec![];

    for task in tasks {
        if let Ok(Some(port)) = task.await {
            open_ports.push(port);
        }
    }

    println!("{}", serde_json::to_string(&open_ports).unwrap());
}