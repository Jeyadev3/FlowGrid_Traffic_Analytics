# Test Suite and Execution Report: Dynamic Traffic Analytics Using Fenwick Tree

**Project Title:** Dynamic Traffic Congestion Analytics Using Fenwick Tree  
**Application:** FlowGrid — Traffic Intelligence  
**Course:** Data Structures & Algorithms (2nd Year CSE)  
**Evaluation Mode:** Automated Benchmark (Non-Menu-Driven)  
**Status:** ALL TESTS PASSED (100% Precision)

---

## 1. Test Methodology

The testing protocol verifies both the **C++ Core Engine** (`src/main.cpp`) and the **JavaScript Web Dashboard** (`app/script.js`). All tests operate on a 1-based Fenwick Tree (Binary Indexed Tree) initialized with the benchmark vector:
```
trafficCounts = [12, 7, 15, 9, 20, 5, 11, 8]  (Indices 1 to 8)
```

---

## 2. Test Execution Matrix

| Test ID | Test Category | Target Segment / Range | Input Data | Expected Output | Actual Output | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Tree Construction | Segments [1..8] | Initial Counts: `[12, 7, 15, 9, 20, 5, 11, 8]` | BIT: `[12, 19, 15, 43, 20, 25, 11, 87]` | BIT: `[12, 19, 15, 43, 20, 25, 11, 87]` | **PASS** |
| **TC-02** | Total Prefix Sum | Segments [1..8] | `prefixSum(8)` | 87 vehicles | 87 vehicles | **PASS** |
| **TC-03** | Prefix Sum Decomposition | Segments [1..6] | `prefixSum(6)` | `bit[6] + bit[4] = 25 + 43 = 68` | 68 vehicles | **PASS** |
| **TC-04** | Prefix Sum Boundary | Segments [1..2] | `prefixSum(2)` | `bit[2] = 19` | 19 vehicles | **PASS** |
| **TC-05** | Range Query Baseline | Segments [3..6] | `rangeSum(3, 6)` | `prefixSum(6) - prefixSum(2) = 68 - 19 = 49` | 49 vehicles | **PASS** |
| **TC-06** | Congestion Detection (Normal) | Segments [3..6] | Volume: 49, Threshold: 55 | `NORMAL` (49 &le; 55) | `NORMAL` | **PASS** |
| **TC-07** | Point Update (Dynamic Surge) | Segment 5 | Update from 20 to 34 (delta = +14) | Ancestors updated: `bit[5]`, `bit[6]`, `bit[8]` | Nodes 5, 6, 8 updated | **PASS** |
| **TC-08** | Post-Update BIT Array | Segments [1..8] | Array State Inspection | BIT: `[12, 19, 15, 43, 34, 39, 11, 101]` | BIT: `[12, 19, 15, 43, 34, 39, 11, 101]` | **PASS** |
| **TC-09** | Range Query Re-Evaluation | Segments [3..6] | `rangeSum(3, 6)` | `prefixSum(6) - prefixSum(2) = 82 - 19 = 63` | 63 vehicles | **PASS** |
| **TC-10** | Congestion Detection (Congested) | Segments [3..6] | Volume: 63, Threshold: 55 | `POTENTIALLY CONGESTED` (63 > 55) | `POTENTIALLY CONGESTED` | **PASS** |
| **TC-11** | Edge Case: Single Segment | Segment [5..5] | `rangeSum(5, 5)` | 34 vehicles (`trafficCounts[5]`) | 34 vehicles | **PASS** |
| **TC-12** | Edge Case: Zero Traffic Count | Segment 1 | `setCount(1, 0)` | Traffic count set to 0; BIT updated | 0 vehicles; BIT valid | **PASS** |
| **TC-13** | Edge Case: Out-of-Bounds Index | Segment 10 | `setCount(10, 50)` | Error handled gracefully; false returned | Error caught; no crash | **PASS** |
| **TC-14** | Edge Case: Inverted Range | Range [6..3] | `rangeSum(6, 3)` | Error handled gracefully; -1 returned | Error caught; return -1 | **PASS** |
| **TC-15** | Edge Case: Negative Traffic Count | Segment 2 | `setCount(2, -10)` | Rejected; validation error reported | Error caught; count unchanged | **PASS** |
| **TC-16** | Edge Case: Threshold Equality | Segment [3..6] | Volume: 63, Threshold: 63 | `NORMAL` (Condition: `volume > threshold`) | `NORMAL` | **PASS** |

---

## 3. Mathematical Verification of Core Indices

### Initial BIT Array Calculation (n = 8)
- `bit[1]`: interval `[1..1]` &rarr; `traffic[1]` = **12**
- `bit[2]`: interval `[1..2]` &rarr; `traffic[1] + traffic[2]` = 12 + 7 = **19**
- `bit[3]`: interval `[3..3]` &rarr; `traffic[3]` = **15**
- `bit[4]`: interval `[1..4]` &rarr; `traffic[1..4]` = 12 + 7 + 15 + 9 = **43**
- `bit[5]`: interval `[5..5]` &rarr; `traffic[5]` = **20**
- `bit[6]`: interval `[5..6]` &rarr; `traffic[5] + traffic[6]` = 20 + 5 = **25**
- `bit[7]`: interval `[7..7]` &rarr; `traffic[7]` = **11**
- `bit[8]`: interval `[1..8]` &rarr; `traffic[1..8]` = 43 + 25 + 11 + 8 = **87**

### Point Update: Segment 5 (20 &rarr; 34, delta = +14)
- Traversal path: $i \leftarrow i + \text{lowbit}(i)$
  1. $i = 5 \implies \text{lowbit}(5) = 1 \implies \text{bit}[5] = 20 + 14 = \mathbf{34}$
  2. $i = 6 \implies \text{lowbit}(6) = 2 \implies \text{bit}[6] = 25 + 14 = \mathbf{39}$
  3. $i = 8 \implies \text{lowbit}(8) = 8 \implies \text{bit}[8] = 87 + 14 = \mathbf{101}$
  4. $i = 16 > 8 \implies$ Terminate.

### Range Sum [3..6] After Update
- $\text{prefixSum}(6) = \text{bit}[6] + \text{bit}[4] = 39 + 43 = 82$
- $\text{prefixSum}(2) = \text{bit}[2] = 19$
- $\text{rangeSum}(3, 6) = 82 - 19 = \mathbf{63}$
- Threshold = 55: Since $63 > 55$, status is **POTENTIALLY CONGESTED**.

---

## 4. Actual Program Output Log

Below is the verbatim terminal output produced by executing `bin/traffic_analytics.exe`:

```text
******************************************************************************
  FLOWGRID — DYNAMIC TRAFFIC CONGESTION ANALYTICS
  Data Structures & Algorithms Case Study Evaluation
  Fenwick Tree (Binary Indexed Tree) Automatic Demonstration
******************************************************************************

==============================================================================
  STEP 1: INITIAL DATA SETUP & FENWICK TREE CONSTRUCTION
==============================================================================
Initial Traffic Counts (Segments 1 to 8):
Segments [1..8]     : [12, 7, 15, 9, 20, 5, 11, 8]

Fenwick Tree constructed successfully in O(n) time.
Computed BIT Array  : [12, 19, 15, 43, 20, 25, 11, 87]
Expected BIT Array  : [12, 19, 15, 43, 20, 25, 11, 87]
Total Traffic (Segments 1 to 8): 87 (Expected: 87) -> [PASS]
Initial BIT Array Verification: [PASS] Exact Match

==============================================================================
  STEP 2, 3 & 4: RANGE QUERY & CONGESTION DETECTION (BASELINE)
==============================================================================
Corridor Query Range     : Segments [3 .. 6]
Configured Threshold     : 55 vehicles
Calculation Detail       : prefixSum(6) - prefixSum(2)
                         : 68 - 19 = 49
Query Result             : Traffic Volume = 49
Congestion Status        : NORMAL
Benchmark Check          : [PASS] Expected 49 and NORMAL

==============================================================================
  STEP 5: DYNAMIC POINT UPDATE (ACCIDENT / SURGE ON SEGMENT 5)
==============================================================================
Target Segment           : 5
Prior Vehicle Count      : 20
Updated Vehicle Count    : 34
Computed Delta           : 14

Updated Traffic Counts Array:
Segments [1..8]     : [12, 7, 15, 9, 34, 5, 11, 8]

Updated Fenwick Tree BIT Array:
Computed BIT Array  : [12, 19, 15, 43, 34, 39, 11, 101]
Expected BIT Array  : [12, 19, 15, 43, 34, 39, 11, 101]
Updated BIT Array Verification: [PASS] Exact Match

==============================================================================
  STEP 6 & 7: RE-EVALUATION OF RANGE QUERY [3..6]
==============================================================================
Calculation Detail       : prefixSum(6) - prefixSum(2)
                         : 82 - 19 = 63
Query Result             : Traffic Volume = 63
Congestion Status        : POTENTIALLY CONGESTED
Benchmark Check          : [PASS] Expected 63 and POTENTIALLY CONGESTED

==============================================================================
  STEP 8: EDGE CASE & SAFETY VALIDATION SUITE
==============================================================================
[Edge Case 1] Single Segment Query [5..5]: 34 (Expected: 34) -> [PASS]
[Edge Case 2] Zero Traffic Update on Segment 1: 0 vehicles -> [PASS]
[Edge Case 3] Out-of-bounds update index 10:
[Error] Index out of bounds in setCount(): 10 (Valid range: 1 to 8)
              Handled Gracefully: [PASS]
[Edge Case 4] Inverted Range Query [6..3]:
[Error] Invalid range query [6, 3] for array size 8.
              Handled Gracefully: [PASS]
[Edge Case 5] Negative Traffic Count Rejection (-10):
[Error] Invalid traffic count: -10 (Counts must be non-negative).
              Handled Gracefully: [PASS]
[Edge Case 6] Threshold Equality (Sum = 63, Threshold = 63): NORMAL (Expected: NORMAL since <= threshold) -> [PASS]

==============================================================================
  DEMONSTRATION SUMMARY
==============================================================================
All benchmark tests, bit states, and edge validations passed successfully.
Point Update Time Complexity : O(log n)
Range Query Time Complexity  : O(log n)
Space Complexity             : O(n)
******************************************************************************
```

---

## 5. Conclusion

Both the C++ command-line demonstration program and the JavaScript client application achieve 100% numerical and logical parity across all test vectors, boundary checks, and edge cases.
