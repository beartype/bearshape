# Measurements after the isolation correction

Matched sequential local runs on macOS arm64 with Python 3.11.15 and 3.14.5,
NumPy 2.4.6 and optree 0.19.1. All variants use the same normally installed
bearshape wheel. Only the upstream wheel changes: published 0.23.1, corrected
scope proposal `e44afa92`, or optimized proposal `7d039bcb`. The pinned release
base is `f85b67d8`; bearshape implementation inputs are commit `dee5bb1`.

The unchanged transaction benchmark uses 20,000 calls and seven raw repeats,
checking each case before timing. Incorrect baseline unions are recorded as
incorrect. First-call times are single setup observations, not statistical
cold-start results. The unchanged runtime benchmark uses 10,000 calls and five
repeats (with fewer calls for diagnostics) and includes small/large arrays, Like
conversions, nested checking, Value, Tree and error diagnostics. Its JSON
records median/min/max; transaction JSON retains every raw repeat.

Each file identifies script and wheel hashes, versions and normally installed
origins. Package files were compared byte-for-byte against their input wheels:
482 released beartype files, 484 proposal files, and 18 bearshape files. New
virtual environments were used, with no tests running during benchmarks. Full
commands and logs remain under `build/union-isolation-revision/` in the main
checkout. Earlier measurements in the adjacent folder are preserved.

Times below are warm microseconds per call.

| Case           | Python |  Released | Correctness | Optimized |
| -------------- | ------ | --------: | ----------: | --------: |
| Native         | 3.11   |     0.096 |       0.099 |     0.099 |
| Native         | 3.14   |     0.101 |       0.098 |     0.141 |
| Root ref       | 3.11   |     0.646 |       0.717 |     0.725 |
| Root ref       | 3.14   |     0.501 |       0.517 |     0.590 |
| Sampled list   | 3.11   |     0.690 |       1.656 |     0.776 |
| Sampled list   | 3.14   |     0.569 |       1.289 |     0.622 |
| Tuple          | 3.11   |     0.685 |       1.600 |     0.171 |
| Tuple          | 3.14   |     0.535 |       1.256 |     0.186 |
| Mapping        | 3.11   |     0.713 |       1.615 |     0.197 |
| Mapping        | 3.14   |     0.583 |       1.306 |     0.234 |
| Nested lists   | 3.11   |     0.727 |       1.665 |     0.229 |
| Nested lists   | 3.14   |     0.605 |       1.354 |     0.287 |
| Strict         | 3.11   |    12.749 |      11.844 |     8.562 |
| Strict         | 3.14   |    13.626 |      12.577 |     9.422 |
| Explicit       | 3.11   |     8.434 |      10.074 |     6.938 |
| Explicit       | 3.14   |     8.412 |      10.484 |     7.400 |
| Union fallback | 3.11   | Incorrect |      15.942 |    13.787 |
| Union fallback | 3.14   | Incorrect |      16.980 |    14.642 |

On 3.11 the remaining root-reference and sampled-list costs are about 0.08–0.09
microseconds beyond released 0.23.1. Warm ordinary composites avoid transaction
ownership work after specialization. The correctness-only candidate pays more
for owner lookup on the general path; the independent optimization removes that
work where state domains are already known or references are proven plain. Cold,
custom-metaclass and stateful paths retain real costs.

The first full 3.14 run measured native checking at 0.141 microseconds in the
optimized environment, versus 0.101 released. That observation is retained.
Because native generated checks do not enter the transaction path, an additional
stability probe ran three rounds with rotated variant order, one million calls
and seven repeats per case, including a bare-call control. Optimized native
medians were 0.094–0.096; released medians were 0.101–0.103. The probe source,
all samples and generated disassembly are in `native-stability-314.json`. The
initial slowdown did not reproduce; these local timings are not a universal
performance guarantee or a CI threshold.

Fresh installed suites pass 1,251 correctness and 1,262 optimized tests on each
endpoint, including all four checker consumers, the original union probe and 41
added isolation cases. Five CPU skips remain absent CuPy and four platform
precision cases. Upstream units pass 473/481 correctness and 484/492 optimized
cases, with 15/7 existing interpreter, optional and known-issue skips. Upstream
pyright analyzes 483 files with no errors or warnings. The 17 new generic cases
and 24 bearshape cases cover independent nested calls, recursion, discovery
order, caught failures, copied contexts, lifetime and lazy public-scope
allocation.

The tested upstream wheel hashes are:

- Released: `4461b4dc57e3fdd6c8a8464b22cf118002eea107c33e9fef651c69068ab3cce3`
- Corrected: `0e19b66f35fd1a49dff124f67d69f273dd2309d1b850d4b6bc59cad6521a9100`
- Optimized: `0580ede1fe87229728b42674d45fb8c32ce09a7e348f962cc2741304ef2f10d8`

The common bearshape wheel SHA256 is
`fe593320362bee43e8f1f91bb3ec10d1b3f85a0ea1039a3b7f7b409302ad8026`. No package
has been published; the proposal wheels still identify as 0.23.1 and must not be
confused with the published wheel. Supported upstream adoption remains a release
prerequisite.
