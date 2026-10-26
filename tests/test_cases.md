# Test Suite and Execution Report: Dynamic Traffic Analytics Using Fenwick Tree

**Project Title:** Dynamic Traffic Congestion Analytics Using Fenwick Tree  
**Application:** FlowGrid — Traffic Intelligence  
**Course:** Data Structures & Algorithms (2nd Year CSE Case Study)  
**Evaluation Mode:** Automated Benchmark & Full Integration Test Suite  
**Status:** ALL TESTS PASSED (32/32 Tests — 100% Precision)

---

## 1. Test Methodology

The testing protocol verifies both the **C++ Core Engine** (`src/main.cpp`) and the **Python/Browser Integration** (`server.py`, `app/script.js`). All tests operate on a 1-based Fenwick Tree (Binary Indexed Tree) initialized with the benchmark vector:
```
trafficCounts = [12, 7, 15, 9, 20, 5, 11, 8]  (Indices 1 to 8)
```

### Congestion Threshold Specification
- **Volume $<$ Threshold ($55$):** `NORMAL`
- **Volume $\ge$ Threshold ($55$):** `POTENTIALLY CONGESTED`

---

## 2. Test Execution Matrix

| Test ID | Test Category | Target Segment / Range | Input Data | Expected Output | Actual Output | Verdict |
| :--- | :--- | :--- | :--- | :--- | :--- | :---: |
| **TC-01** | Tree Construction | Segments [1..8] | Initial Counts: `[12, 7, 15, 9, 20, 5, 11, 8]` | BIT: `[12, 19, 15, 43, 20, 25, 11, 87]` | BIT: `[12, 19, 15, 43, 20, 25, 11, 87]` | **PASS** |
| **TC-02** | Total Corridor Volume | Segments [1..8] | `prefixSum(8)` | 87 vehicles | 87 vehicles | **PASS** |
| **TC-03** | Prefix Sum Decomposition | Segments [1..8] | Prefix sums $i \in [1..8]$ | `[12, 19, 34, 43, 63, 68, 79, 87]` | `[12, 19, 34, 43, 63, 68, 79, 87]` | **PASS** |
| **TC-04** | Prefix Traversal Path | Segment 6 | `prefixSum(6)` | `bit[6] + bit[4] = 25 + 43 = 68` | Path: `[6, 4]`, Sum: 68 | **PASS** |
| **TC-05** | Range Query Baseline | Segments [3..6] | `rangeSum(3, 6)` | `prefixSum(6) - prefixSum(2) = 68 - 19 = 49` | 49 vehicles | **PASS** |
| **TC-06** | Congestion Detection (Normal) | Segments [3..6] | Volume: 49, Threshold: 55 | `NORMAL` ($49 < 55$) | `NORMAL` | **PASS** |
| **TC-07** | Point Update (Dynamic Surge) | Segment 5 | Update from 20 to 34 ($\Delta = +14$) | Ancestors updated: `bit[5]`, `bit[6]`, `bit[8]` | Nodes 5, 6, 8 updated | **PASS** |
| **TC-08** | Post-Update BIT Array | Segments [1..8] | Array State Inspection | BIT: `[12, 19, 15, 43, 34, 39, 11, 101]` | BIT: `[12, 19, 15, 43, 34, 39, 11, 101]` | **PASS** |
| **TC-09** | Range Query Re-Evaluation | Segments [3..6] | `rangeSum(3, 6)` | `prefixSum(6) - prefixSum(2) = 82 - 19 = 63` | 63 vehicles | **PASS** |
| **TC-10** | Congestion Detection (Congested) | Segments [3..6] | Volume: 63, Threshold: 55 | `POTENTIALLY CONGESTED` ($63 \ge 55$) | `POTENTIALLY CONGESTED` | **PASS** |
| **TC-11** | Edge Case: Single Segment | Segment [5..5] | `rangeSum(5, 5)` | 34 vehicles (`trafficCounts[5]`) | 34 vehicles | **PASS** |
| **TC-12** | Edge Case: Zero Traffic Count | Segment 1 | `setCount(1, 0)` | Traffic count set to 0; BIT updated | 0 vehicles; BIT valid | **PASS** |
| **TC-13** | Edge Case: Out-of-Bounds Index | Segment 10 | `setCount(10, 50)` | Error handled gracefully; false returned | Error caught; no crash | **PASS** |
| **TC-14** | Edge Case: Inverted Range | Range [6..3] | `rangeSum(6, 3)` | Error handled gracefully; -1 returned | Error caught; return -1 | **PASS** |
| **TC-15** | Edge Case: Negative Traffic Count | Segment 2 | `setCount(2, -10)` | Rejected; validation error reported | Error caught; count unchanged | **PASS** |
| **TC-16** | Edge Case: Threshold Equality | Boundary Check | Volume: 55, Threshold: 55 | `POTENTIALLY CONGESTED` (since $\ge$ threshold) | `POTENTIALLY CONGESTED` | **PASS** |
| **TC-17** | Inverted Range Query CLI | Range [6..3] | `--query 6 3 55` | Return error: `Invalid range [6..3]` | Error caught; exit code 1 | **PASS** |
| **TC-18** | Out-of-Bounds Left CLI | Range [0..5] | `--query 0 5 55` | Return error: `Invalid range [0..5]` | Error caught; exit code 1 | **PASS** |
| **TC-19** | Out-of-Bounds Right CLI | Range [2..9] | `--query 2 9 55` | Return error: `Invalid range [2..9]` | Error caught; exit code 1 | **PASS** |
| **TC-20** | Out-of-Bounds Update CLI | Segment 10 | `--update 10 50` | Return error: `Segment index out of bounds` | Error caught; exit code 1 | **PASS** |
| **TC-21** | Negative Update CLI | Segment 2 | `--update 2 -10` | Return error: `Traffic count must be non-negative` | Error caught; exit code 1 | **PASS** |
| **TC-22** | Repeated Updates Consistency | Corridor | 3 successive updates (Seg 1, 8, 3) | Total Traffic = 107 veh | Total Traffic = 107 veh | **PASS** |
| **TC-23** | HTTP Backend Health | Server Bridge | `GET /api/status` | `{"status": "online", "binary_exists": true}` | Online; binary located | **PASS** |
| **TC-24** | HTTP State Route | Server Bridge | `GET /api/state` | Returns initial C++ BIT array ($87$ veh) | Returned $87$ veh | **PASS** |
| **TC-25** | HTTP Query Route Baseline | Server Bridge | `POST /api/query [3..6]` | Volume: 49 veh, `NORMAL` | Volume: 49, `NORMAL` | **PASS** |
| **TC-26** | HTTP Point Update Route | Server Bridge | `POST /api/update [5 -> 34]` | Path `[5, 6, 8]`, delta $+14$ | Path: `[5, 6, 8]`, delta $+14$ | **PASS** |
| **TC-27** | HTTP Query Re-Evaluation | Server Bridge | `POST /api/query [3..6]` | Volume: 63 veh, `POTENTIALLY CONGESTED` | Volume: 63, `POTENTIALLY CONGESTED` | **PASS** |
| **TC-28** | HTTP State Reset Route | Server Bridge | `POST /api/reset` | Resets to benchmark initial state ($87$ veh) | State reset to $87$ veh | **PASS** |
| **TC-29** | Case Study Scenario Part 1 | Corridor [3..6] | Initial evaluation | Volume: 49 veh, Status: `NORMAL` | Volume: 49, `NORMAL` | **PASS** |
| **TC-30** | Case Study Scenario Part 2 | Segment 5 | Update 20 to 34 veh | Array: `[12, 7, 15, 9, 34, 5, 11, 8]` | Matches expected array | **PASS** |
| **TC-31** | Case Study Scenario Part 3 | Corridor [3..6] | Post-update re-query | Volume: 63 veh, Status: `POTENTIALLY CONGESTED` | Volume: 63, `POTENTIALLY CONGESTED` | **PASS** |
| **TC-32** | Standalone Automated Demo | C++ Binary | Execution without arguments | All 8 benchmark steps pass without prompt | 100% Pass | **PASS** |

---

## 3. Mathematical Verification of Core Indices

### Initial BIT Array Calculation ($n = 8$)
- `bit[1]`: interval `[1..1]` $\implies$ `traffic[1]` = **12**
- `bit[2]`: interval `[1..2]` $\implies$ `traffic[1] + traffic[2]` = 12 + 7 = **19**
- `bit[3]`: interval `[3..3]` $\implies$ `traffic[3]` = **15**
- `bit[4]`: interval `[1..4]` $\implies$ `traffic[1..4]` = 12 + 7 + 15 + 9 = **43**
- `bit[5]`: interval `[5..5]` $\implies$ `traffic[5]` = **20**
- `bit[6]`: interval `[5..6]` $\implies$ `traffic[5] + traffic[6]` = 20 + 5 = **25**
- `bit[7]`: interval `[7..7]` $\implies$ `traffic[7]` = **11**
- `bit[8]`: interval `[1..8]` $\implies$ `traffic[1..8]` = 43 + 25 + 11 + 8 = **87**

### Point Update: Segment 5 (20 $\to$ 34, $\Delta = +14$)
- Traversal path: $i \leftarrow i + \text{lowbit}(i)$
  1. $i = 5 \implies \text{lowbit}(5) = 1 \implies \text{bit}[5] = 20 + 14 = \mathbf{34}$
  2. $i = 6 \implies \text{lowbit}(6) = 2 \implies \text{bit}[6] = 25 + 14 = \mathbf{39}$
  3. $i = 8 \implies \text{lowbit}(8) = 8 \implies \text{bit}[8] = 87 + 14 = \mathbf{101}$
  4. $i = 16 > 8 \implies$ Terminate.

### Range Sum [3..6] After Update
- $\text{prefixSum}(6) = \text{bit}[6] + \text{bit}[4] = 39 + 43 = 82$
- $\text{prefixSum}(2) = \text{bit}[2] = 19$
- $\text{rangeSum}(3, 6) = 82 - 19 = \mathbf{63}$
- Threshold = 55: Since $63 \ge 55$, status is **POTENTIALLY CONGESTED**.

---

## 4. Actual Program Output Log (`bin/traffic_analytics.exe`)

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
[Edge Case 6] Threshold Boundary (Threshold = 55):
              Sum = 55: POTENTIALLY CONGESTED (Expected: POTENTIALLY CONGESTED since >= threshold)
              Sum = 54: NORMAL (Expected: NORMAL since < threshold) -> [PASS]

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

## 5. Automated Integration Test Log (`python tests/test_flowgrid.py`)

```text
============================================================================
  FLOWGRID — COMPREHENSIVE AUTOMATED TEST SUITE (MEMBER 4)
  C++ Fenwick Tree Engine + Python Server Integration
============================================================================
  Target Binary: C:\Users\Harish\OneDrive\Desktop\FlowGrid_Traffic_Analytics\FlowGrid_Traffic_Analytics\bin\traffic_analytics.exe

--- Test Group 1: Initial Fenwick Tree Construction ---
  [PASS] TC-01: BIT Array Matches Expected Forward-Propagated Values -> BIT: [12, 19, 15, 43, 20, 25, 11, 87]
  [PASS] TC-02: Total Corridor Volume Initial State -> Total = 87 veh

--- Test Group 2: Prefix Sum Decomposition ---
  [PASS] TC-03: Prefix Sums [1..1] through [1..8] -> Matches [12, 19, 34, 43, 63, 68, 79, 87]
  [PASS] TC-04: Prefix Sum 6 Traversal Path -> rightPath = [6, 4] (sum=68)

--- Test Group 3: Range Sum Queries ---
  [PASS] TC-05: Baseline Range Sum [3..6] -> Volume = 49 veh
  [PASS] TC-06: Single Segment Range Sum [5..5]
  [PASS] TC-07: Full Corridor Range Sum [1..8]

--- Test Group 4: Point Updates & Traversal Paths ---
  [PASS] TC-08: Traversal Path for Update(5, +14) -> Path = [5, 6, 8]
  [PASS] TC-09: Updated Raw Traffic Array -> Counts = [12, 7, 15, 9, 34, 5, 11, 8]
  [PASS] TC-10: Updated Fenwick Tree (BIT Array) -> BIT = [12, 19, 15, 43, 34, 39, 11, 101]

--- Test Group 5: Range Queries After Updates ---
  [PASS] TC-11: Re-Query Range [3..6] Post-Update -> Volume = 63 veh
  [PASS] TC-12: Single Segment [5..5] Post-Update

--- Test Group 6: Congestion Classification (< 55 vs >= 55) ---
  [PASS] TC-13: Below Threshold (Sum 49 < Threshold 55) -> Status = NORMAL
  [PASS] TC-14: At Threshold Boundary (Sum 55 == Threshold 55) -> Status = POTENTIALLY CONGESTED
  [PASS] TC-15: Just Below Boundary (Sum 54 < Threshold 55) -> Status = NORMAL
  [PASS] TC-16: Above Threshold (Sum 63 > Threshold 55) -> Status = POTENTIALLY CONGESTED

--- Test Group 7: Boundary & Safety Validations ---
  [PASS] TC-17: Inverted Range Query [6..3] Rejected
  [PASS] TC-18: Out-of-Bounds Range Left [0..5] Rejected
  [PASS] TC-19: Out-of-Bounds Range Right [2..9] Rejected
  [PASS] TC-20: Out-of-Bounds Segment Update [Idx 10] Rejected
  [PASS] TC-21: Negative Traffic Count [-10] Rejected

--- Test Group 8: Repeated Dynamic Updates ---
  [PASS] TC-22: Cumulative State After 3 Repeated Updates -> Total Traffic = 107 veh

--- Test Group 9: Python Server & C++ HTTP Integration ---
  [PASS] TC-23: HTTP GET /api/status Reports C++ Engine Online
  [PASS] TC-24: HTTP GET /api/state Returns Initial C++ BIT State
  [PASS] TC-25: HTTP POST /api/query Computes Range [3..6] -> 49 veh, NORMAL
  [PASS] TC-26: HTTP POST /api/update Modifies Segment 5 to 34 veh
  [PASS] TC-27: HTTP POST /api/query Re-Evaluation -> 63 veh, POTENTIALLY CONGESTED
  [PASS] TC-28: HTTP POST /api/reset Restores Benchmark State (87 veh)

--- Test Group 10: Case Study Exact Demonstration Scenario ---
  [PASS] TC-29: Initial Query [3..6]: Sum = 49, Status = NORMAL
  [PASS] TC-30: Dynamic Update: Segment 5 -> 34 veh, Delta = +14
  [PASS] TC-31: Re-Query Corridor [3..6]: Sum = 63, Status = POTENTIALLY CONGESTED

--- Test Group 11: C++ Standalone Automated Demonstration (argc == 1) ---
  [PASS] TC-32: Standalone C++ Automated Benchmark Suite Execution -> Preserved 100% of Members 1-3 demo

============================================================================
  TEST EXECUTION SUMMARY: 32 PASSED, 0 FAILED
============================================================================
```

---

## 6. Parity & Parallels Summary

Both the C++ command-line demonstration program and the Python-backed dashboard achieve 100% numerical and logical parity across all test vectors, boundary checks, and edge cases.
