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
| amazon | 2022_Q4 | captions | 381 | 1 | 0.3% | 0 / 1 | 1 | 0 / 5 | machine transcript (Whisper), no speaker labels; 381 units, outside the typical 400-900 |
| amazon | 2023_Q1 | captions | 546 | 38 | 7.0% | 5 / 33 | 8 | 1 / 11 | machine transcript (Whisper), no speaker labels |
| amazon | 2023_Q2 | captions | 364 | 54 | 14.8% | 37 / 17 | 4 | 1 / 7 | machine transcript (Whisper), no speaker labels; call opening not detected: source may start mid-call; 364 units, outside the typical 400-900 |
| amazon | 2023_Q3 | captions | 392 | 73 | 18.6% | 35 / 38 | 13 | 6 / 6 | machine transcript (Whisper), no speaker labels; 392 units, outside the typical 400-900 |
| amazon | 2023_Q4 | captions | 442 | 50 | 11.3% | 28 / 22 | 7 | 1 / 8 | machine transcript (Whisper), no speaker labels |
| amazon | 2024_Q1 | captions | 457 | 56 | 12.3% | 37 / 19 | 12 | 4 / 18 | machine transcript (Whisper), no speaker labels |
| amazon | 2024_Q2 | captions | 409 | 53 | 13.0% | 33 / 20 | 7 | 2 / 10 | machine transcript (Whisper), no speaker labels |
| amazon | 2024_Q3 | captions | 411 | 58 | 14.1% | 32 / 26 | 10 | 11 / 17 | machine transcript (Whisper), no speaker labels |
| amazon | 2024_Q4 | captions | 384 | 82 | 21.4% | 37 / 45 | 15 | 14 / 19 | machine transcript (Whisper), no speaker labels; 384 units, outside the typical 400-900 |
| amazon | 2025_Q1 | captions | 444 | 70 | 15.8% | 35 / 35 | 22 | 2 / 12 | machine transcript (Whisper), no speaker labels |
| amazon | 2025_Q2 | captions | 492 | 80 | 16.3% | 28 / 52 | 36 | 9 / 11 | machine transcript (Whisper), no speaker labels |
| amazon | 2025_Q3 | captions | 451 | 76 | 16.9% | 44 / 32 | 25 | 7 / 10 | machine transcript (Whisper), no speaker labels |
| amazon | 2025_Q4 | captions | 522 | 96 | 18.4% | 52 / 44 | 29 | 6 / 9 | machine transcript (Whisper), no speaker labels |
| amazon | 2026_Q1 | captions | 425 | 100 | 23.5% | 48 / 52 | 20 | 2 / 15 | machine transcript (Whisper), no speaker labels |
| amazon | 2026_Q2 | captions | 427 | 87 | 20.4% | 48 / 39 | 24 | 5 / 20 | machine transcript (Whisper), no speaker labels |
| apple | FY23_Q1 | captions | 111 | 3 | 2.7% | 1 / 2 | 1 | 0 / 0 | YouTube auto-captions, no speaker labels; call opening not detected: source may start mid-call; unpunctuated captions: units are ~30s caption segments, not sentences; 111 units, outside the typical 400-900 |
| apple | FY23_Q2 | captions | 117 | 4 | 3.4% | 0 / 4 | 0 | 0 / 0 | YouTube auto-captions, no speaker labels; 14 pre-call livestream segments dropped; unpunctuated captions: units are ~30s caption segments, not sentences; 117 units, outside the typical 400-900 |
| apple | FY23_Q3 | captions | 469 | 5 | 1.1% | 0 / 5 | 0 | 0 / 0 | YouTube auto-captions, no speaker labels |
| apple | FY23_Q4 | captions | 116 | 5 | 4.3% | 0 / 5 | 0 | 0 / 3 | YouTube auto-captions, no speaker labels; 28 pre-call livestream segments dropped; unpunctuated captions: units are ~30s caption segments, not sentences; 116 units, outside the typical 400-900 |
| apple | FY24_Q1 | captions | 110 | 11 | 10.0% | 3 / 8 | 0 | 0 / 0 | YouTube auto-captions, no speaker labels; unpunctuated captions: units are ~30s caption segments, not sentences; 110 units, outside the typical 400-900 |
| apple | FY24_Q2 | captions | 111 | 14 | 12.6% | 5 / 9 | 0 | 0 / 2 | YouTube auto-captions, no speaker labels; unpunctuated captions: units are ~30s caption segments, not sentences; 111 units, outside the typical 400-900 |
| apple | FY24_Q3 | captions | 113 | 31 | 27.4% | 10 / 21 | 0 | 0 / 2 | YouTube auto-captions, no speaker labels; 121 pre-call livestream segments dropped; unpunctuated captions: units are ~30s caption segments, not sentences; 113 units, outside the typical 400-900 |
| apple | FY24_Q4 | captions | 463 | 34 | 7.3% | 10 / 24 | 1 | 0 / 4 | YouTube auto-captions, no speaker labels |
| apple | FY25_Q1 | captions | 107 | 24 | 22.4% | 8 / 16 | 0 | 0 / 2 | YouTube auto-captions, no speaker labels; unpunctuated captions: units are ~30s caption segments, not sentences; 107 units, outside the typical 400-900 |
| apple | FY25_Q2 | captions | 473 | 31 | 6.6% | 14 / 17 | 5 | 0 / 11 | YouTube auto-captions, no speaker labels |
| apple | FY25_Q3 | captions | 480 | 35 | 7.3% | 13 / 22 | 3 | 0 / 11 | YouTube auto-captions, no speaker labels |
| apple | FY25_Q4 | captions | 531 | 29 | 5.5% | 15 / 14 | 3 | 0 / 6 | YouTube auto-captions, no speaker labels |
| apple | FY26_Q1 | captions | 483 | 28 | 5.8% | 11 / 17 | 2 | 0 / 8 | YouTube auto-captions, no speaker labels |
| apple | FY26_Q2 | captions | 530 | 25 | 4.7% | 16 / 9 | 2 | 0 / 0 | YouTube auto-captions, no speaker labels |
| apple | FY26_Q3 | captions | 510 | 40 | 7.8% | 20 / 20 | 0 | 0 / 3 | YouTube auto-captions, no speaker labels |
| tesla | 2022_Q4 | fool | 517 | 37 | 7.2% | 4 / 33 | 21 | 0 / 1 | - |
| tesla | 2023_Q1 | captions | 121 | 21 | 17.4% | 7 / 14 | 15 | 0 / 3 | YouTube auto-captions, no speaker labels; 8 pre-call livestream segments dropped; unpunctuated captions: units are ~30s caption segments, not sentences; 121 units, outside the typical 400-900 |
| tesla | 2023_Q2 | fool | 590 | 59 | 10.0% | 19 / 40 | 29 | 9 / 6 | - |
| tesla | 2023_Q3 | fool | 529 | 34 | 6.4% | 10 / 24 | 22 | 12 / 3 | - |
| tesla | 2023_Q4 | fool | 589 | 35 | 5.9% | 8 / 27 | 12 | 14 / 10 | - |
| tesla | 2024_Q1 | fool | 640 | 71 | 11.1% | 17 / 54 | 45 | 7 / 16 | - |
| tesla | 2024_Q2 | fool | 542 | 84 | 15.5% | 18 / 66 | 48 | 16 / 19 | - |
| tesla | 2024_Q3 | fool | 603 | 90 | 14.9% | 31 / 59 | 55 | 5 / 10 | - |
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
| amazon | 15 | 6547 | 974 | 14.9% | 499 / 475 | 233 | 71 / 178 |
| apple | 15 | 4724 | 319 | 6.8% | 126 / 193 | 17 | 0 / 52 |
| tesla | 15 | 7751 | 939 | 12.1% | 280 / 659 | 556 | 285 / 106 |
| **all** | **105** | **48555** | **9662** | **19.9%** | 4862 / 4800 | 2536 | 429 / 1823 |
