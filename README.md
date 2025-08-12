# api-benchmark

Benchmarks of 1 million HTTP requests to a REST API runnning in github actions.

# Latest results:
* [latest.md](https://github.com/aaronriekenberg/api-benchmark/blob/main/results/latest.md)

# REST Server APIs:
* [rust-api](https://github.com/aaronriekenberg/api-benchmark/tree/main/rust-api) using [axum](https://github.com/tokio-rs/axum)
* [go-api](https://github.com/aaronriekenberg/api-benchmark/tree/main/go-api) using builtin `net/http`
* [kotlin-api](https://github.com/aaronriekenberg/api-benchmark/tree/main/kotlin-api) using [http4k](https://www.http4k.org) with Undertow server.
* [node-api](https://github.com/aaronriekenberg/api-benchmark/tree/main/node-api) using builtin `node:http` server.
* [python-api](https://github.com/aaronriekenberg/api-benchmark/tree/main/python-api) using [tornado](https://www.tornadoweb.org/en/stable/) server

# Benchmark tests:
* Use [oha](https://crates.io/crates/oha) to make 1 million HTTP requests
* Using HTTP 1.1 with varying number of connections.
* At API measure response times (p50, p99, p99.9), memory usage, cpu usage, threads created
