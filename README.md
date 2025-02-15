# api-benchmark

Benchmarks of 1 million HTTP requests to a REST API runnning in github actions.

# Latest results:
* [latest.csv](https://github.com/aaronriekenberg/api-benchmark/blob/main/results/latest.csv)

# REST Server APIs:
* go using builtin `net.http`
* rust using `axum`
* kotlin using `http4k` with Undertow server.

# Benchmark tests:
* Use [oha](https://crates.io/crates/oha) to make 1 million http requests
* Measure response times (p50, p99, p99.9), memory usage, cpu usage, threads created
* Using HTTP 1.1 with varying number of connections.
