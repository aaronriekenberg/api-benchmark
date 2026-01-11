# million-hello-challenge

Benchmarking 1 million HTTP HelloWorld requests to rust/go/kotlin/node/python APIs in GitHub Actions.

# Latest results:
* [latest.md](https://github.com/aaronriekenberg/million-hello-challenge/blob/main/results/latest.md)

# Server APIs:
* [rust-api](https://github.com/aaronriekenberg/million-hello-challenge/tree/main/rust-api) using [axum](https://github.com/tokio-rs/axum)
* [go-api](https://github.com/aaronriekenberg/million-hello-challenge/tree/main/go-api) using builtin `net/http`
* [kotlin-api](https://github.com/aaronriekenberg/million-hello-challenge/tree/main/kotlin-api) using [http4k](https://www.http4k.org) with [Helidon](https://helidon.io) server using virutal threads, Java 25.
* [node-api](https://github.com/aaronriekenberg/million-hello-challenge/tree/main/node-api) using builtin `node:http` server.
* [python-api](https://github.com/aaronriekenberg/million-hello-challenge/tree/main/python-api) using [tornado](https://www.tornadoweb.org/en/stable/) server, using [pre-forking](https://www.tornadoweb.org/en/stable/process.html#tornado.process.fork_processes) to use all available CPUs.

# Benchmark tests:
* Use [oha](https://crates.io/crates/oha) to make 1 million HTTP requests
* Using HTTP 1.1 with varying number of connections.
* At API server measure response times (p50, p99, p99.9), memory usage, cpu usage, threads created, processes created.
