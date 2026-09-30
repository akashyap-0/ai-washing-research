# Earnings calls: AI-sentence extraction index

One row per transcript. "Total" counts every sentence the parser kept after noise removal (for unpunctuated caption files, caption segments). "AI" counts sentences in the main AI sections (Prepared remarks + Q&A), excluding the Borderline sections. Method and validation: FILTER_METHOD.md.

| Company | Period | Format | Total | AI | % AI | AI in prepared / Q&A | ⚑ uncertain | Borderline auto / infra | Flags |
|---|---|---|---:|---:|---:|---|---:|---|---|
| meta | 2022_Q4 | meta | 509 | 34 | 6.7% | 12 / 22 | 2 | 2 / 15 | - |
| meta | 2023_Q1 | meta | 487 | 64 | 13.1% | 32 / 32 | 8 | 1 / 17 | - |
| meta | 2023_Q2 | meta | 497 | 75 | 15.1% | 29 / 46 | 11 | 0 / 16 | - |
| meta | 2023_Q3 | meta | 471 | 77 | 16.3% | 39 / 38 | 5 | 1 / 23 | - |
| meta | 2023_Q4 | meta | 467 | 83 | 17.8% | 49 / 34 | 4 | 5 / 18 | - |
| meta | 2024_Q1 | meta | 447 | 119 | 26.6% | 57 / 62 | 21 | 4 / 11 | - |
| meta | 2024_Q2 | meta | 468 | 111 | 23.7% | 53 / 58 | 13 | 2 / 26 | - |
| meta | 2024_Q3 | meta | 443 | 85 | 19.2% | 37 / 48 | 9 | 0 / 28 | - |
| meta | 2024_Q4 | meta | 463 | 94 | 20.3% | 37 / 57 | 8 | 1 / 31 | - |
| meta | 2025_Q1 | meta | 455 | 122 | 26.8% | 63 / 59 | 19 | 1 / 28 | - |
| meta | 2025_Q2 | meta | 451 | 112 | 24.8% | 61 / 51 | 19 | 0 / 33 | - |
| meta | 2025_Q3 | meta | 446 | 101 | 22.6% | 54 / 47 | 25 | 9 / 31 | - |
| meta | 2025_Q4 | meta | 477 | 112 | 23.5% | 63 / 49 | 42 | 0 / 24 | - |
| meta | 2026_Q1 | meta | 480 | 135 | 28.1% | 62 / 73 | 54 | 0 / 23 | - |
| meta | 2026_Q2 | meta | 509 | 143 | 28.1% | 82 / 61 | 65 | 0 / 34 | - |
| microsoft | FY23_Q2 | msft | 485 | 49 | 10.1% | 28 / 21 | 5 | 2 / 7 | - |
| microsoft | FY23_Q3 | msft | 464 | 79 | 17.0% | 47 / 32 | 3 | 0 / 11 | - |
| microsoft | FY23_Q4 | msft | 516 | 101 | 19.6% | 47 / 54 | 0 | 2 / 20 | - |
| microsoft | FY24_Q1 | msft | 476 | 90 | 18.9% | 58 / 32 | 3 | 1 / 9 | - |
| microsoft | FY24_Q2 | msft | 522 | 123 | 23.6% | 70 / 53 | 12 | 0 / 15 | - |
| microsoft | FY24_Q3 | msft | 502 | 118 | 23.5% | 71 / 47 | 6 | 1 / 12 | - |
| microsoft | FY24_Q4 | msft | 507 | 94 | 18.5% | 67 / 27 | 2 | 0 / 21 | - |
| microsoft | FY25_Q1 | msft | 524 | 140 | 26.7% | 80 / 60 | 17 | 1 / 18 | - |
| microsoft | FY25_Q2 | msft | 501 | 142 | 28.3% | 78 / 64 | 22 | 0 / 17 | - |
| microsoft | FY25_Q3 | msft | 485 | 116 | 23.9% | 79 / 37 | 22 | 0 / 33 | - |
| microsoft | FY25_Q4 | msft | 454 | 106 | 23.3% | 71 / 35 | 23 | 0 / 34 | - |
| microsoft | FY26_Q1 | msft | 508 | 125 | 24.6% | 87 / 38 | 25 | 0 / 20 | - |
| microsoft | FY26_Q2 | msft | 483 | 137 | 28.4% | 104 / 33 | 45 | 0 / 28 | - |
| microsoft | FY26_Q3 | msft | 506 | 138 | 27.3% | 94 / 44 | 43 | 0 / 28 | - |
| microsoft | FY26_Q4 | msft | 519 | 138 | 26.6% | 97 / 41 | 55 | 1 / 33 | - |
| nvidia | FY23_Q4 | fool | 482 | 126 | 26.1% | 44 / 82 | 36 | 0 / 42 | - |
| nvidia | FY24_Q1 | fool | 518 | 144 | 27.8% | 50 / 94 | 42 | 0 / 73 | - |
| nvidia | FY24_Q2 | fool | 470 | 138 | 29.4% | 58 / 80 | 35 | 1 / 56 | - |
| nvidia | FY24_Q3 | fool | 541 | 193 | 35.7% | 65 / 128 | 40 | 0 / 36 | - |
| nvidia | FY24_Q4 | captions | 511 | 143 | 28.0% | 74 / 69 | 27 | 2 / 44 | YouTube auto-captions, no speaker labels |
| nvidia | FY25_Q1 | fool | 484 | 166 | 34.3% | 95 / 71 | 74 | 0 / 42 | - |
| nvidia | FY25_Q2 | fool | 544 | 195 | 35.8% | 69 / 126 | 90 | 2 / 48 | - |
| nvidia | FY25_Q3 | fool | 507 | 189 | 37.3% | 65 / 124 | 82 | 2 / 26 | - |
| nvidia | FY25_Q4 | fool | 505 | 187 | 37.0% | 66 / 121 | 75 | 5 / 26 | - |
| nvidia | FY26_Q1 | factset | 470 | 203 | 43.2% | 120 / 83 | 71 | 2 / 22 | - |
| nvidia | FY26_Q2 | factset | 466 | 181 | 38.8% | 77 / 104 | 84 | 6 / 36 | - |
| nvidia | FY26_Q3 | factset | 498 | 170 | 34.1% | 91 / 79 | 62 | 1 / 26 | - |
| nvidia | FY26_Q4 | factset | 509 | 172 | 33.8% | 65 / 107 | 80 | 1 / 37 | - |
| nvidia | FY27_Q1 | factset | 525 | 173 | 33.0% | 55 / 118 | 66 | 3 / 34 | - |
| nvidia | FY27_Q2 | factset | 479 | 139 | 29.0% | 62 / 77 | 57 | 0 / 37 | - |
| alphabet | 2022_Q4 | alphabet | 468 | 76 | 16.2% | 52 / 24 | 5 | 1 / 11 | - |
| alphabet | 2023_Q1 | alphabet | 516 | 79 | 15.3% | 48 / 31 | 5 | 1 / 11 | - |
| alphabet | 2023_Q2 | alphabet | 509 | 95 | 18.7% | 56 / 39 | 1 | 3 / 11 | - |
| alphabet | 2023_Q3 | alphabet | 453 | 83 | 18.3% | 53 / 30 | 4 | 1 / 11 | - |
| alphabet | 2023_Q4 | alphabet | 496 | 96 | 19.4% | 63 / 33 | 2 | 3 / 10 | - |
| alphabet | 2024_Q1 | alphabet | 488 | 87 | 17.8% | 65 / 22 | 4 | 1 / 24 | - |
| alphabet | 2024_Q2 | alphabet | 496 | 109 | 22.0% | 72 / 37 | 20 | 1 / 11 | - |
| alphabet | 2024_Q3 | alphabet | 558 | 129 | 23.1% | 84 / 45 | 23 | 0 / 13 | - |
| alphabet | 2024_Q4 | alphabet | 527 | 127 | 24.1% | 71 / 56 | 23 | 0 / 19 | - |
| alphabet | 2025_Q1 | alphabet | 488 | 107 | 21.9% | 63 / 44 | 13 | 1 / 18 | - |
| alphabet | 2025_Q2 | alphabet | 508 | 126 | 24.8% | 81 / 45 | 16 | 0 / 21 | - |
| alphabet | 2025_Q3 | alphabet | 453 | 141 | 31.1% | 81 / 60 | 26 | 0 / 17 | - |
| alphabet | 2025_Q4 | alphabet | 515 | 158 | 30.7% | 102 / 56 | 23 | 1 / 25 | - |
| alphabet | 2026_Q1 | alphabet | 504 | 161 | 31.9% | 100 / 61 | 20 | 1 / 21 | - |
| alphabet | 2026_Q2 | alphabet | 523 | 174 | 33.3% | 102 / 72 | 36 | 0 / 15 | - |
| amazon | 2022_Q4 | captions | 380 | 1 | 0.3% | 0 / 1 | 1 | 0 / 5 | machine transcript (Whisper), no speaker labels; 380 units, outside the typical 400-900 |
| amazon | 2023_Q1 | captions | 545 | 38 | 7.0% | 5 / 33 | 8 | 1 / 11 | machine transcript (Whisper), no speaker labels |
| amazon | 2023_Q2 | captions | 363 | 54 | 14.9% | 37 / 17 | 4 | 1 / 7 | machine transcript (Whisper), no speaker labels; call opening not detected: source may start mid-call; 363 units, outside the typical 400-900 |
| amazon | 2023_Q3 | captions | 391 | 73 | 18.7% | 35 / 38 | 13 | 6 / 6 | machine transcript (Whisper), no speaker labels; 391 units, outside the typical 400-900 |
| amazon | 2023_Q4 | captions | 441 | 50 | 11.3% | 28 / 22 | 7 | 1 / 8 | machine transcript (Whisper), no speaker labels |
| amazon | 2024_Q1 | captions | 456 | 56 | 12.3% | 37 / 19 | 12 | 4 / 18 | machine transcript (Whisper), no speaker labels |
| amazon | 2024_Q2 | captions | 408 | 53 | 13.0% | 33 / 20 | 7 | 2 / 10 | machine transcript (Whisper), no speaker labels |
| amazon | 2024_Q3 | captions | 410 | 58 | 14.1% | 32 / 26 | 10 | 11 / 17 | machine transcript (Whisper), no speaker labels |
| apple | FY23_Q1 | captions | 110 | 8 | 7.3% | 3 / 5 | 6 | 0 / 0 | YouTube auto-captions, no speaker labels; call opening not detected: source may start mid-call; unpunctuated captions: units are ~30s caption segments, not sentences; 110 units, outside the typical 400-900 |
| apple | FY23_Q2 | captions | 116 | 6 | 5.2% | 0 / 6 | 2 | 0 / 0 | YouTube auto-captions, no speaker labels; 14 pre-call livestream segments dropped; unpunctuated captions: units are ~30s caption segments, not sentences; 116 units, outside the typical 400-900 |
| apple | FY23_Q3 | captions | 469 | 5 | 1.1% | 0 / 5 | 0 | 0 / 0 | YouTube auto-captions, no speaker labels |
| apple | FY23_Q4 | captions | 115 | 7 | 6.1% | 0 / 7 | 2 | 0 / 3 | YouTube auto-captions, no speaker labels; 28 pre-call livestream segments dropped; unpunctuated captions: units are ~30s caption segments, not sentences; 115 units, outside the typical 400-900 |
| apple | FY24_Q1 | captions | 109 | 18 | 16.5% | 7 / 11 | 7 | 0 / 0 | YouTube auto-captions, no speaker labels; unpunctuated captions: units are ~30s caption segments, not sentences; 109 units, outside the typical 400-900 |
| apple | FY24_Q2 | captions | 110 | 17 | 15.5% | 6 / 11 | 3 | 0 / 2 | YouTube auto-captions, no speaker labels; unpunctuated captions: units are ~30s caption segments, not sentences; 110 units, outside the typical 400-900 |
| apple | FY24_Q3 | captions | 112 | 33 | 29.5% | 11 / 22 | 2 | 0 / 2 | YouTube auto-captions, no speaker labels; 121 pre-call livestream segments dropped; unpunctuated captions: units are ~30s caption segments, not sentences; 112 units, outside the typical 400-900 |
| apple | FY24_Q4 | captions | 463 | 37 | 8.0% | 12 / 25 | 4 | 0 / 4 | YouTube auto-captions, no speaker labels |
| apple | FY25_Q1 | captions | 106 | 29 | 27.4% | 11 / 18 | 5 | 0 / 2 | YouTube auto-captions, no speaker labels; unpunctuated captions: units are ~30s caption segments, not sentences; 106 units, outside the typical 400-900 |
| apple | FY25_Q2 | captions | 473 | 35 | 7.4% | 17 / 18 | 9 | 0 / 11 | YouTube auto-captions, no speaker labels |
| apple | FY25_Q3 | captions | 480 | 39 | 8.1% | 15 / 24 | 7 | 0 / 11 | YouTube auto-captions, no speaker labels |
| apple | FY25_Q4 | captions | 531 | 36 | 6.8% | 17 / 19 | 10 | 0 / 6 | YouTube auto-captions, no speaker labels |
| apple | FY26_Q1 | captions | 483 | 33 | 6.8% | 12 / 21 | 7 | 0 / 7 | YouTube auto-captions, no speaker labels |
| apple | FY26_Q2 | captions | 530 | 30 | 5.7% | 17 / 13 | 7 | 0 / 0 | YouTube auto-captions, no speaker labels |
| apple | FY26_Q3 | captions | 510 | 43 | 8.4% | 23 / 20 | 3 | 0 / 2 | YouTube auto-captions, no speaker labels |
| tesla | 2022_Q4 | fool | 509 | 37 | 7.3% | 4 / 33 | 21 | 0 / 1 | - |
| tesla | 2023_Q1 | captions | 120 | 21 | 17.5% | 7 / 14 | 15 | 0 / 3 | YouTube auto-captions, no speaker labels; 8 pre-call livestream segments dropped; unpunctuated captions: units are ~30s caption segments, not sentences; 120 units, outside the typical 400-900 |
| tesla | 2023_Q2 | fool | 578 | 59 | 10.2% | 19 / 40 | 29 | 9 / 6 | - |
| tesla | 2023_Q3 | fool | 479 | 26 | 5.4% | 2 / 24 | 19 | 12 / 2 | - |
| tesla | 2023_Q4 | fool | 577 | 35 | 6.1% | 16 / 19 | 12 | 14 / 10 | - |
| tesla | 2024_Q1 | fool | 629 | 71 | 11.3% | 49 / 22 | 45 | 7 / 16 | - |
| tesla | 2024_Q2 | fool | 541 | 84 | 15.5% | 18 / 66 | 48 | 16 / 19 | - |
| tesla | 2024_Q3 | fool | 596 | 90 | 15.1% | 31 / 59 | 55 | 5 / 10 | - |
| tesla | 2024_Q4 | fool | 590 | 75 | 12.7% | 27 / 48 | 52 | 39 / 5 | - |
| tesla | 2025_Q1 | captions | 697 | 56 | 8.0% | 18 / 38 | 44 | 19 / 2 | YouTube auto-captions, no speaker labels; 9 pre-call livestream segments dropped |
| tesla | 2025_Q2 | captions | 466 | 71 | 15.2% | 33 / 38 | 42 | 26 / 3 | YouTube auto-captions, no speaker labels; 6 pre-call livestream segments dropped |
| tesla | 2025_Q3 | captions | 497 | 89 | 17.9% | 22 / 67 | 36 | 45 / 2 | YouTube auto-captions, no speaker labels; 12 pre-call livestream segments dropped |
| tesla | 2025_Q4 | captions | 455 | 71 | 15.6% | 19 / 52 | 46 | 30 / 8 | YouTube auto-captions, no speaker labels; 5 pre-call livestream segments dropped |
| tesla | 2026_Q1 | captions | 424 | 78 | 18.4% | 18 / 60 | 49 | 20 / 3 | YouTube auto-captions, no speaker labels |
| tesla | 2026_Q2 | captions | 491 | 68 | 13.8% | 29 / 39 | 40 | 43 / 15 | YouTube auto-captions, no speaker labels |

## Totals

| Company | Files | Total | AI | % AI | AI in prepared / Q&A | ⚑ uncertain | Borderline auto / infra |
|---|---:|---:|---:|---:|---|---:|---|
| meta | 15 | 7070 | 1467 | 20.7% | 730 / 737 | 305 | 26 / 358 |
| microsoft | 15 | 7452 | 1696 | 22.8% | 1078 / 618 | 283 | 8 / 306 |
| nvidia | 15 | 7509 | 2519 | 33.5% | 1056 / 1463 | 921 | 25 / 585 |
| alphabet | 15 | 7502 | 1748 | 23.3% | 1093 / 655 | 221 | 14 / 238 |
| amazon | 8 | 3394 | 383 | 11.3% | 207 / 176 | 62 | 26 / 82 |
| apple | 15 | 4717 | 376 | 8.0% | 151 / 225 | 74 | 0 / 50 |
| tesla | 15 | 7649 | 931 | 12.2% | 312 / 619 | 553 | 285 / 105 |
| **all** | **98** | **45293** | **9120** | **20.1%** | 4627 / 4493 | 2419 | 384 / 1724 |
