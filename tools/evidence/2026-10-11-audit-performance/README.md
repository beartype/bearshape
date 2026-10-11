# Audit follow-up performance evidence

Compare corrected bearshape source `1e17a96f9969cb4121042cf1bcdd4406182dec94`
with the scope/Tree optimization at `1991deabe05180f54616aa42a36940d40dedc1e5`.
Both retain all six audit correctness fixes. `identity.json` pins both
sdist-derived wheels and the unchanged published/proposal beartype wheels.

Each side is normally installed in a separate fresh venv on the same macOS arm64
host, with CPython 3.11.15 or 3.14.5, NumPy 2.4.6, optree 0.19.1 and
typing_extensions 4.16.0. Run each environment's interpreter from outside the
package source with `-I tools/benchmark_runtime.py`: proposal comparisons use
`--calls 20000 --repeats 9`; published-baseline comparisons use
`--calls 10000 --repeats 7`. Use the same script revision on both sides.
Benchmarks run sequentially without validation jobs; order is before/after on
3.11 and after/before on 3.14. Raw JSON retains every sample and actual per-case
call counts; expensive cases use the script's smaller counts.

All values below are median microseconds per call. Tree input/return cases visit
all leaves; composite Tree measures its input only. Validator construction is an
internal cold-construction measurement, not the cached public subscript path.
Decoration repeatedly creates a new function with an existing annotation.

| Dependency | Python | Case                       | Before  | After   |
| ---------- | ------ | -------------------------- | ------- | ------- |
| Release    | 3.11   | `native/3`                 | 0.094   | 0.093   |
| Release    | 3.11   | `strict/3`                 | 13.430  | 5.591   |
| Release    | 3.11   | `like/3`                   | 6.897   | 2.980   |
| Release    | 3.11   | `value/3`                  | 10.713  | 10.133  |
| Release    | 3.11   | `tree/100`                 | 804.141 | 313.363 |
| Release    | 3.11   | `tree-value/100`           | 889.923 | 394.958 |
| Release    | 3.11   | `tree-composite/100`       | 415.658 | 306.292 |
| Release    | 3.11   | `decorate_array`           | 112.223 | 112.510 |
| Release    | 3.11   | `construct_tree_validator` | 56.451  | 1.370   |
| Release    | 3.14   | `native/3`                 | 0.095   | 0.092   |
| Release    | 3.14   | `strict/3`                 | 13.533  | 5.144   |
| Release    | 3.14   | `like/3`                   | 7.085   | 2.825   |
| Release    | 3.14   | `value/3`                  | 9.389   | 9.451   |
| Release    | 3.14   | `tree/100`                 | 733.520 | 309.102 |
| Release    | 3.14   | `tree-value/100`           | 834.209 | 405.564 |
| Release    | 3.14   | `tree-composite/100`       | 406.239 | 282.342 |
| Release    | 3.14   | `decorate_array`           | 124.872 | 119.103 |
| Release    | 3.14   | `construct_tree_validator` | 63.068  | 1.413   |
| Proposal   | 3.11   | `native/3`                 | 0.079   | 0.084   |
| Proposal   | 3.11   | `strict/3`                 | 8.642   | 4.829   |
| Proposal   | 3.11   | `like/3`                   | 5.975   | 2.678   |
| Proposal   | 3.11   | `value/3`                  | 8.062   | 8.293   |
| Proposal   | 3.11   | `tree/100`                 | 626.475 | 310.339 |
| Proposal   | 3.11   | `tree-value/100`           | 706.763 | 391.792 |
| Proposal   | 3.11   | `tree-composite/100`       | 439.645 | 388.694 |
| Proposal   | 3.11   | `decorate_array`           | 112.953 | 114.098 |
| Proposal   | 3.11   | `construct_tree_validator` | 56.978  | 1.382   |
| Proposal   | 3.14   | `native/3`                 | 0.091   | 0.115   |
| Proposal   | 3.14   | `strict/3`                 | 8.968   | 4.968   |
| Proposal   | 3.14   | `like/3`                   | 6.356   | 2.771   |
| Proposal   | 3.14   | `value/3`                  | 8.396   | 8.566   |
| Proposal   | 3.14   | `tree/100`                 | 643.599 | 312.491 |
| Proposal   | 3.14   | `tree-value/100`           | 740.058 | 405.044 |
| Proposal   | 3.14   | `tree-composite/100`       | 444.329 | 386.472 |
| Proposal   | 3.14   | `decorate_array`           | 120.344 | 119.809 |
| Proposal   | 3.14   | `construct_tree_validator` | 61.549  | 1.413   |

Strict checks improve by about 44–62%; 100-leaf Tree input/return checks improve
by about 50–61% in these runs. Array size does not materially change strict
metadata checking; conversion still scales with input size. Ordinary beartype
controls remain sub-microsecond and vary between runs. This PR does not change
beartype code or claim zero overhead for the separate upstream proposal.
Value-only calls are broadly similar, including approximately 2–3% higher
medians in the proposal comparison. These are local measurements without a CI
timing threshold or a guarantee for other hardware/workloads.

The profile identified argument binding and repeated leaf context discovery.
Regression guards now reject scope binding for annotations without Value and
require at least 202 snapshots for a 100-leaf input/return. Generic leaves
retain the owned public wrapper; mutable shape/dtype metadata and independent
nested calls are exercised. Dtype normalization remains a measurable cost. No
dtype or checked-value cache was added: custom properties must stay fresh, and
the measured scope improvements do not require additional cache ownership rules.
