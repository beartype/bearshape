# Remaining optimization evidence

PR [#56](https://github.com/beartype/bearshape/pull/56) prepares builtin dtype
names, keeps plain dtype strings cheap without NumPy, and removes a per-call
Like casting closure. PR [#57](https://github.com/beartype/bearshape/pull/57)
prepares shape traversal once per annotation. They are independent changes on
main `28e8858`, following the already merged lazy-scope and Tree optimizations.
The combined validation head is `e5eddd6`; identity.json pins full source IDs,
archive and wheel hashes. Later documentation commits do not change these
runtime wheels. Publication remains blocked on supported upstream integration
and the existing release prerequisites.

## Method

Use the same tools/benchmark_runtime.py revision, normal wheel installations,
NumPy 2.4.6, optree 0.19.1 and typing_extensions 4.16.0 in all four variants.
Compare exact published beartype 0.23.1 and the unchanged local upstream
proposal separately. On each interpreter, run every environment's Python with
`-I`, from outside the checkout, then the benchmark's absolute path and
`--calls 5000 --repeats 9`. Expensive cases use the smaller per-case counts
recorded in JSON. All runs are sequential with local validation idle:
main/dtype/shape/combined on 3.11, reversed on 3.14. Ordinary proposal
comparisons use
`tools/upstream/benchmark_transactions.py --calls 10000 --repeats 9`. Raw
samples, versions and installed origins accompany this report. These are local
observations, not a portable guarantee or CI threshold. Do not compare these
timings with an older benchmark run to infer an additional speedup.

## Matched warm results

Median microseconds per call; Tree input plus return visits all 100 leaves
twice. “Dtype” and “Shape” each change only their named PR; “Combined” includes
both.

| Dependency / Python | Case        | Main    | Dtype   | Shape   | Combined |
| ------------------- | ----------- | ------- | ------- | ------- | -------- |
| released 3.11       | `strict/3`  | 5.514   | 4.005   | 5.507   | 4.200    |
| released 3.11       | `tree/100`  | 310.550 | 166.441 | 310.151 | 159.878  |
| released 3.11       | `value/3`   | 10.077  | 8.664   | 10.145  | 8.472    |
| released 3.11       | `like-cast` | 3.232   | 2.398   | 3.330   | 2.449    |
| released 3.11       | `multiaxis` | 7.297   | 5.703   | 7.280   | 5.618    |
| released 3.11       | `variadic`  | 7.519   | 5.934   | 7.640   | 5.879    |
| proposal 3.11       | `strict/3`  | 5.069   | 3.402   | 4.881   | 3.253    |
| proposal 3.11       | `tree/100`  | 316.684 | 169.452 | 306.442 | 159.303  |
| proposal 3.11       | `value/3`   | 8.542   | 6.862   | 8.357   | 6.642    |
| proposal 3.11       | `like-cast` | 2.992   | 2.179   | 2.945   | 2.379    |
| proposal 3.11       | `multiaxis` | 6.897   | 5.156   | 6.413   | 4.823    |
| proposal 3.11       | `variadic`  | 6.943   | 5.388   | 6.625   | 4.971    |
| released 3.14       | `strict/3`  | 5.220   | 3.774   | 5.157   | 3.624    |
| released 3.14       | `tree/100`  | 315.511 | 174.293 | 303.637 | 159.987  |
| released 3.14       | `value/3`   | 9.411   | 7.753   | 9.269   | 7.655    |
| released 3.14       | `like-cast` | 3.368   | 2.385   | 3.298   | 2.306    |
| released 3.14       | `multiaxis` | 7.286   | 5.568   | 6.841   | 5.288    |
| released 3.14       | `variadic`  | 7.605   | 5.843   | 7.168   | 5.534    |
| proposal 3.14       | `strict/3`  | 4.949   | 3.536   | 4.783   | 3.333    |
| proposal 3.14       | `tree/100`  | 314.614 | 170.283 | 301.280 | 160.959  |
| proposal 3.14       | `value/3`   | 8.645   | 6.921   | 8.587   | 6.914    |
| proposal 3.14       | `like-cast` | 3.245   | 2.241   | 3.106   | 2.201    |
| proposal 3.14       | `multiaxis` | 6.931   | 5.303   | 6.487   | 4.972    |
| proposal 3.14       | `variadic`  | 7.097   | 5.513   | 6.917   | 5.235    |

The final combined measurements improve strict checks by about 24–36% and
100-leaf Trees by about 48–50% against main. The dtype preparation supplies most
of the improvement. Shape preparation adds a smaller, workload-dependent saving
and reuses the same dimension checker and error ordering. Its isolated 3.11
released results are nearly flat, including a 1.6% higher variadic median. The
combined strict 3.11 released median is also higher than dtype-only (4.200
versus 4.005 us), while the other endpoint/dependency comparisons improve.
Retain these outcomes alongside the favorable cases; small differences are
sensitive to run variance. Tree still takes a snapshot per leaf and for each
enclosing check. No validation result, array, arbitrary dtype, call scope, frame
or user class is cached. Known builtin dtype class identities and strings are
the only retained normalization data; identity keys avoid user metaclass
hashing/equality. The original custom/extension dtype protocol remains live,
including metadata changes, endian and structured layout checks.

## Startup and controls

First dtype extraction is measured in 13 fresh subprocesses per variant, after
NumPy and bearshape imports and array creation. The JSON contains the exact
code. This is one-time normalization setup, not full application startup.

| Python | Main   | Dtype  | Shape | Combined |
| ------ | ------ | ------ | ----- | -------- |
| 3.11   | 11.250 | 27.750 | 9.792 | 28.875   |
| 3.14   | 12.167 | 26.250 | 9.750 | 26.875   |

Preparing the dtype table costs tens of microseconds once. Shape validator
construction also grows slightly; the raw `construct_array_validator` case
measures internal uncached construction, not cached public subscripting. Full
decoration, native controls, diagnostics, Value, composite Trees and
million-item conversion remain in the raw results, including unfavorable/noisy
samples. Conversion still scales with input size; Tree still scales with leaves.

A separate custom-array benchmark asserts that NumPy is never imported. It uses
plain dtype strings and the source saved in experiments.json, 20,000 calls per
repeat and nine repeats. Results below are median microseconds.

| Python | Case           | Main  | Dtype | Shape | Combined |
| ------ | -------------- | ----- | ----- | ----- | -------- |
| 3.11   | custom-extract | 0.099 | 0.062 | 0.095 | 0.065    |
| 3.11   | custom-strict  | 4.134 | 4.034 | 4.007 | 3.950    |
| 3.14   | custom-extract | 0.105 | 0.058 | 0.104 | 0.057    |
| 3.14   | custom-strict  | 3.814 | 3.788 | 3.708 | 3.594    |

The first implementation added an avoidable NumPy discovery cost for root-only
string dtypes. The final narrow fast path removes it, while exact string-type
checking preserves string subclasses with their own dtype-name protocol. Custom
metaclass hashing failures found during review were fixed before the final
measurements; two explicit regressions protect that boundary.

## Ordinary beartype costs and the rejected extra cache

The upstream patch series is unchanged. The same combined bearshape wheel is
installed for released/proposal comparisons. Native controls do not invoke
bearshape; root references and one sampled-reference list retain the native
proxy path. Composite references retain the already implemented specialization.
These costs also apply to ordinary beartype users of the proposed upstream
changes, even without bearshape. No universal zero-overhead claim is made.

| Python | Case                         | Released | Proposal |
| ------ | ---------------------------- | -------- | -------- |
| 3.11   | `native`                     | 0.100    | 0.099    |
| 3.11   | `forward-resolved-stateless` | 0.711    | 0.755    |
| 3.11   | `forward-nested-stateless`   | 0.763    | 0.793    |
| 3.11   | `forward-tuple`              | 0.727    | 0.170    |
| 3.11   | `forward-mapping`            | 0.748    | 0.197    |
| 3.11   | `forward-nested-lists`       | 0.771    | 0.221    |
| 3.14   | `native`                     | 0.106    | 0.094    |
| 3.14   | `forward-resolved-stateless` | 0.515    | 0.502    |
| 3.14   | `forward-nested-stateless`   | 0.585    | 0.556    |
| 3.14   | `forward-tuple`              | 0.517    | 0.175    |
| 3.14   | `forward-mapping`            | 0.579    | 0.220    |
| 3.14   | `forward-nested-lists`       | 0.603    | 0.243    |

We also measured a best-case prepopulated weak lookup cache. On 3.11, current
getattr/weak-map/guarded-weak-set lookup medians were 60.5/40.7/56.9 ns; on
3.14, 12.9/41.1/53.7 ns. Raw samples and exact experiment source are retained.
These are isolated lookup costs, not full checker speedups. The cache
alternative is already slower on 3.14 before accounting for initialization,
invalidation, ownership or custom metaclass semantics. Retain the current lookup
and the prior code-factory compatibility decision; no additional upstream patch
is justified by this experiment. Ordinary first-call samples remain single
observations, not statistical cold-start evidence. Incorrect released-union
cases are labelled as failures rather than timed as valid behavior.

## Validation and limits

Each focused PR passes its runtime and four-checker routes. The combined wheel
passes 1,323 normally installed baseline tests and 1,450 proposal tests on both
Python 3.11.15 and 3.14.5. The proposal total includes all 69 bearshape
composition cases and 58 upstream protocol/scope/mixin cases. It also passes the
unchanged union probe. Source coverage is 91.23%; fresh minimal wheel consumers
and all 95 documentation snippets pass. Five local skips cover missing CuPy and
four platform-specific extended-precision cases, not union semantics. Hosted PR
checks add platform/interpreter, compatibility-floor, docs/notebook and archive
lanes. See each PR for the final check status.

The published dependency still lacks full union rollback. This work does not
replace that release prerequisite or supply fresh CUDA evidence. Nothing has
been published or sent upstream. Both PRs remain subject to merge review.
