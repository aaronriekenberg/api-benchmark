# Results
`Mon Jun 23 11:33:32 UTC 2025`
## Hardware Info
| CPU Model | Num CPUs | Memory |
| --------- | -------- | ------ |
| AMD EPYC 7763 64-Core Processor | 4 | 16G |

## Benchmarks of 1 Million Requests
| Test Name | Conns | Success Rate | Test Seconds | Requests per Second | P50 Millis | P99 Millis | P99.9 Millis | API Memory MB | API CPU Time | API Threads |
| --------- | ----- | ------------ | ------------ | ------------------- | ---------- | ---------- | ------------ | ------------- | ------------ | ----------- |
| go | 200 | % |  |  |  |  |  | 8.6 | 00:00:00 | 6 |
| go | 400 | % |  |  |  |  |  | 8.4 | 00:00:00 | 6 |
| go | 800 | % |  |  |  |  |  | 8.5 | 00:00:00 | 6 |
| rust | 200 | % |  |  |  |  |  | 3.5 | 00:00:00 | 5 |
| rust | 400 | % |  |  |  |  |  | 3.4 | 00:00:00 | 5 |
| rust | 800 | % |  |  |  |  |  | 3.4 | 00:00:00 | 5 |
| kotlin | 200 | % |  |  |  |  |  | 79.1 | 00:00:00 | 27 |
| kotlin | 400 | % |  |  |  |  |  | 79.3 | 00:00:00 | 27 |
| kotlin | 800 | % |  |  |  |  |  | 79.0 | 00:00:00 | 27 |
