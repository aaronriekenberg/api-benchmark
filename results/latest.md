# Results
`Fri Aug 1 10:22:43 UTC 2025`
## Hardware Info
| CPU Model | Num CPUs | Memory |
| --------- | -------- | ------ |
| AMD EPYC 7763 64-Core Processor | 4 | 16G |

## Benchmarks of 1 Million Requests
| Test Name | Conns | Success Rate | Test Seconds | Requests per Second | P50 Millis | P99 Millis | P99.9 Millis | API Memory MB | API CPU Time | API Threads |
| --------- | ----- | ------------ | ------------ | ------------------- | ---------- | ---------- | ------------ | ------------- | ------------ | ----------- |
| node | 200 | 100.0% | 34.8 | 28712.5 | 5.9507 | 10.6720 | 10.9505 | 111.9 | 00:00:35 | 7 |
| node | 400 | 100.0% | 34.3 | 29100.6 | 11.7791 | 19.0539 | 24.6587 | 144.6 | 00:00:34 | 7 |
| node | 800 | 100.0% | 36.3 | 27562.8 | 24.9940 | 40.3027 | 45.0448 | 152.5 | 00:00:36 | 7 |
| go | 200 | 100.0% | 11.6 | 85647.0 | 1.8359 | 7.3650 | 10.0971 | 17.7 | 00:00:27 | 11 |
| go | 400 | 100.0% | 11.2 | 88842.5 | 3.7677 | 13.7430 | 19.3729 | 24.2 | 00:00:26 | 13 |
| go | 800 | 100.0% | 11.5 | 86420.4 | 8.2504 | 25.9968 | 38.5915 | 37.6 | 00:00:27 | 12 |
| rust | 200 | 100.0% | 8.8 | 112967.2 | 1.6425 | 4.5388 | 6.1629 | 8.4 | 00:00:17 | 5 |
| rust | 400 | 100.0% | 8.5 | 116469.4 | 3.2465 | 7.0095 | 9.4650 | 13.0 | 00:00:17 | 5 |
| rust | 800 | 100.0% | 8.7 | 114182.8 | 6.8671 | 11.1989 | 15.7918 | 22.1 | 00:00:17 | 5 |
| kotlin | 200 | 100.0% | 19.6 | 51060.8 | 3.2352 | 14.6124 | 33.7420 | 297.8 | 00:01:00 | 147 |
| kotlin | 400 | 100.0% | 19.1 | 52616.6 | 6.3797 | 27.3341 | 67.5972 | 399.8 | 00:00:57 | 155 |
| kotlin | 800 | 100.0% | 20.2 | 49522.9 | 13.5302 | 62.1069 | 177.9502 | 495.1 | 00:01:00 | 155 |
