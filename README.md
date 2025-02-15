# api-benchmark

Benchmarks of 1 million HTTP requests to a REST API runnning in github actions.

# Latest results:
* [latest.md](https://github.com/aaronriekenberg/api-benchmark/blob/main/results/latest.md)

# REST Server APIs:
* [go-api](https://github.com/aaronriekenberg/api-benchmark/tree/main/go-api) using builtin `net/http`
* [rust-api](https://github.com/aaronriekenberg/api-benchmark/tree/main/rust-api) using `axum`
* [kotlin-api](https://github.com/aaronriekenberg/api-benchmark/tree/main/kotlin-api) using `http4k` with Undertow server.

# Benchmark tests:
* Use [oha](https://crates.io/crates/oha) to make 1 million http requests
* Measure response times (p50, p99, p99.9), memory usage, cpu usage, threads created
* Using HTTP 1.1 with varying number of connections.
