# FlowGrid — Dynamic Traffic Congestion Analytics Using Fenwick Tree

> **Data Structures & Algorithms (DSA) Second-Year CSE Case Study Project**  
> **Evaluation Mode:** Automatic Benchmark Demonstration (Explicitly Non-Menu-Driven)  
> **Engine:** 1-Based Fenwick Tree (Binary Indexed Tree / BIT)

---

## 1. Project Overview

**FlowGrid** is a dynamic traffic congestion analytics system designed to monitor urban vehicular corridors in real time. In metropolitan transportation grids, road segments experience rapid fluctuations in traffic density due to signals, lane closures, accidents, and rush-hour surges.

Traffic management centers require two fundamental operations:
1. **Dynamic Point Updates ($O(\log n)$):** Ingest real-time vehicle counts from road sensors as conditions change.
2. **Corridor Range Queries ($O(\log n)$):** Query cumulative vehicle volume over any sub-corridor $[L \dots R]$ and detect whether density exceeds safety thresholds (`NORMAL` vs `POTENTIALLY CONGESTED`).

This repository contains two implementations:
- **Part 1 (C++ Core):** A high-performance, non-menu-driven C++ demonstration program (`src/main.cpp`) executing an automated verification benchmark with boundary safety validation.
- **Part 2 (Web Dashboard):** A client-side visual dashboard (`app/index.html`, `app/style.css`, `app/script.js`) with interactive controls, dynamic road segment cards, Fenwick Tree hierarchy inspection, and an activity audit log.

---

## 2. Theoretical Background: The Fenwick Tree (BIT)

A **Fenwick Tree** (also known as a **Binary Indexed Tree** or **BIT**), proposed by Peter Fenwick in 1994, is an array-based data structure that efficiently computes prefix sums and supports point modifications in $O(\log n)$ time while using strictly $O(n)$ space.

### The `lowbit()` Operator
The structure of a Fenwick Tree relies on the binary representation of indices. The function `lowbit(x)` isolates the lowest set bit (the least significant 1-bit) in the binary representation of $x$:

$$\text{lowbit}(x) = x \ \& \ (-x)$$

Using two's complement arithmetic, $-x = (\sim x) + 1$. Bitwise ANDing $x$ with $-x$ zeroes out all higher bits and preserves only the lowest 1-bit.

### 1-Based Responsibility Intervals
In a 1-based Fenwick Tree of size $n = 8$, each node $\text{bit}[i]$ stores the sum of elements over the contiguous interval:

$$[i - \text{lowbit}(i) + 1 \dots i]$$

The length of this interval is exactly $\text{lowbit}(i)$.

| Index $i$ | Binary ($i$) | $\text{lowbit}(i)$ | Responsibility Interval | Elements Included | Tree Role |
| :---: | :---: | :---: | :---: | :---: | :--- |
| **1** | `0001` | 1 | $[1 \dots 1]$ | $\text{traffic}[1]$ | Leaf (odd index) |
| **2** | `0010` | 2 | $[1 \dots 2]$ | $\text{traffic}[1] + \text{traffic}[2]$ | Sub-root |
| **3** | `0011` | 1 | $[3 \dots 3]$ | $\text{traffic}[3]$ | Leaf (odd index) |
| **4** | `0100` | 4 | $[1 \dots 4]$ | $\text{traffic}[1 \dots 4]$ | Branch Root |
| **5** | `0101` | 1 | $[5 \dots 5]$ | $\text{traffic}[5]$ | Leaf (odd index) |
| **6** | `0110` | 2 | $[5 \dots 6]$ | $\text{traffic}[5] + \text{traffic}[6]$ | Sub-root |
| **7** | `0111` | 1 | $[7 \dots 7]$ | $\text{traffic}[7]$ | Leaf (odd index) |
| **8** | `1000` | 8 | $[1 \dots 8]$ | $\text{traffic}[1 \dots 8]$ | Global Corridor Root |

---

## 3. Algorithmic Operations & Complexities

### Comparative Complexity Analysis

| Data Structure | Point Update | Prefix Sum | Range Sum $[L \dots R]$ | Auxiliary Space |
| :--- | :---: | :---: | :---: | :---: |
| **Naive Array** | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ |
| **Prefix Sum Array** | $O(n)$ | $O(1)$ | $O(1)$ | $O(n)$ |
| **Segment Tree** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(4n)$ |
| **Fenwick Tree (BIT)** | $\mathbf{O(\log n)}$ | $\mathbf{O(\log n)}$ | $\mathbf{O(\log n)}$ | $\mathbf{O(n)}$ |

### Algorithmic Routines

1. **`buildFenwick()` — $O(n)$ Construction:**
   Instead of calling `update()` $n$ times ($O(n \log n)$), the tree is built in linear $O(n)$ time by pushing the value of each node $\text{bit}[i]$ forward to its direct parent $i + \text{lowbit}(i)$:
   ```cpp
   for (int i = 1; i <= n; ++i) {
       bit[i] += trafficCounts[i];
       int parent = i + lowbit(i);
       if (parent <= n) {
           bit[parent] += bit[i];
       }
   }
   ```

2. **`update(idx, delta)` — $O(\log n)$ Point Update:**
   Adds `delta` to $\text{bit}[i]$ and ascends the tree via $i \leftarrow i + \text{lowbit}(i)$ until $i > n$.

3. **`setCount(idx, newCount)` — $O(\log n)$ Absolute Setting:**
   Computes $\Delta = \text{newCount} - \text{trafficCounts}[idx]$, updates the raw array $\text{trafficCounts}[idx] = \text{newCount}$, and executes `update(idx, delta)`.

4. **`prefixSum(idx)` — $O(\log n)$ Cumulative Sum:**
   Accumulates $\text{bit}[i]$ and descends the tree via $i \leftarrow i - \text{lowbit}(i)$ until $i = 0$.

5. **`rangeSum(left, right)` — $O(\log n)$ Range Query:**
   Uses the principle of inclusion-exclusion:
   $$\text{rangeSum}(L, R) = \text{prefixSum}(R) - \text{prefixSum}(L - 1)$$

6. **`detectCongestion(currentSum, threshold)` — $O(1)$ Threshold Classification:**
   Returns `"POTENTIALLY CONGESTED"` if $\text{currentSum} > \text{threshold}$, otherwise `"NORMAL"`.

---

## 4. Benchmark Demonstration (Exact Case Study Numbers)

### Initial State
- **Segments 1 to 8:** `[12, 7, 15, 9, 20, 5, 11, 8]`
- **Expected Initial BIT:** `[12, 19, 15, 43, 20, 25, 11, 87]`
- **Expected Total Traffic:** $87$ vehicles

### Execution Sequence
1. **Query Corridor $[3 \dots 6]$ with Threshold $55$:**
   $$\text{prefixSum}(6) = \text{bit}[6] + \text{bit}[4] = 25 + 43 = 68$$
   $$\text{prefixSum}(2) = \text{bit}[2] = 19$$
   $$\text{rangeSum}(3, 6) = 68 - 19 = \mathbf{49}$$
   - Since $49 \le 55 \implies$ **`NORMAL`** $\checkmark$

2. **Dynamic Update:** Segment 5 updated from $20$ to $34$ ($\Delta = +14$).
   - Traversal path updated: $\text{bit}[5]$, $\text{bit}[6]$, $\text{bit}[8]$.
   - **Expected Updated BIT:** `[12, 19, 15, 43, 34, 39, 11, 101]` $\checkmark$

3. **Re-Query Corridor $[3 \dots 6]$ with Threshold $55$:**
   $$\text{prefixSum}(6) = \text{bit}[6] + \text{bit}[4] = 39 + 43 = 82$$
   $$\text{prefixSum}(2) = \text{bit}[2] = 19$$
   $$\text{rangeSum}(3, 6) = 82 - 19 = \mathbf{63}$$
   - Since $63 > 55 \implies$ **`POTENTIALLY CONGESTED`** $\checkmark$

---

## 5. Workspace File Structure

```
FlowGrid_Traffic_Analytics/
├── .gitignore                          # Git exclusions (build binaries, caches)
├── README.md                           # Comprehensive documentation & evaluation guide
├── generate_pptx.py                    # Standalone PowerPoint generator script
├── app/                                # Part 2: Interactive Web Application
│   ├── index.html                      # Modern semantic dashboard markup
│   ├── style.css                       # Responsive dark glassmorphism styling
│   └── script.js                       # 1-based JavaScript Fenwick Tree engine
├── bin/                                # Compiled binaries directory
│   └── traffic_analytics.exe           # Compiled C++ demonstration executable
├── presentation/                       # Part 4: Case Study Presentation
│   └── Fenwick_Tree_Case_Study.pptx    # 14-slide professional PowerPoint deck
├── src/                                # Part 1: C++ Implementation
│   └── main.cpp                        # Standard C++ Fenwick Tree engine & demo
└── tests/                              # Part 3: Verification Suite
    └── test_cases.md                   # Complete test matrix & verified output logs
```

---

## 6. Compilation & Execution Instructions

### A. C++ Core Demonstration Program

#### Prerequisites
- Any standard C++ compiler supporting C++17 or C++20 (`g++`, `clang++`, or MSVC `cl.exe`).

#### Compilation Command
Open PowerShell or your preferred terminal in the project root:

```powershell
# Using g++ (MinGW / MSYS2 / Linux GCC)
g++ -std=c++17 -Wall -Wextra -O2 src/main.cpp -o bin/traffic_analytics.exe
```

#### Execution Command
```powershell
.\bin\traffic_analytics.exe
```

> **Note:** The program runs an automatic, non-menu-driven benchmark demonstration that outputs every calculation step, verifies initial and updated BIT arrays, tests threshold classifications, and executes edge-case validations.

---

### B. FlowGrid Web Dashboard

#### Prerequisites
- Any modern web browser (Google Chrome, Microsoft Edge, Mozilla Firefox, Safari).
- **No backend or server required** — runs purely client-side.

#### Opening the Dashboard
Simply double-click `app/index.html` or run in PowerShell:

```powershell
Start-Process "app/index.html"
```

#### Dashboard Features:
- **Run Benchmark Demo Button:** Runs an animated 3-step sequence recreating the case study.
- **Dynamic Segment Cards:** Visual cards displaying real-time traffic volume and density meters.
- **Point Update Panel:** Enter segment index ($1 \dots 8$) and vehicle count, then see tree ancestors highlight in real time.
- **Range Query Panel:** Adjust start segment $[L]$, end segment $[R]$, and threshold to evaluate live corridor congestion.
- **BIT Structural Inspector:** Table detailing binary representations, $\text{lowbit}(i)$, and interval coverage.
- **Audit Log:** Timestamped log tracking every engine operation.

---

### C. PowerPoint Presentation

The editable PowerPoint presentation is pre-generated at:
```
presentation/Fenwick_Tree_Case_Study.pptx
```
It contains 14 structured slides covering the problem statement, objectives, tree representation, mathematical walkthroughs, complexity analysis, test matrix, and limitations.

To regenerate or modify slides programmatically:
```powershell
python generate_pptx.py
```

---

## 7. Limitations & Future Roadmap

1. **1D Linear Corridors:**
   - *Current:* Operates on a linear sequence of road segments $[1 \dots n]$.
   - *Future:* Extend to a 2D Fenwick Tree to monitor $M \times N$ road intersections and spatial urban grids in $O(\log^2 n)$ time.
2. **Fixed Segment Capacity:**
   - *Current:* Fixed array size $n = 8$. Dynamic addition of new segments requires dynamic resizing.
3. **Range Updates:**
   - *Current:* Optimized for point updates + range queries.
   - *Future:* Implement dual-tree difference encoding ($D[i]$ and $D[i] \times i$) to support both range updates and range queries in $O(\log n)$.
4. **Predictive Analytics:**
   - *Future:* Couple the BIT cumulative volume tracking with an ARIMA or LSTM time-series model to forecast congestion 15 minutes before thresholds are breached.

---

## 8. Academic Integrity & Note for Faculty

- **Zero Menu-Driven Code:** Per faculty guidelines, the C++ implementation runs an end-to-end automated verification suite without interactive menus or fragile input prompts.
- **Separation of Implementations:** The C++ program (`src/main.cpp`) and the JavaScript dashboard (`app/script.js`) are standalone implementations. Both enforce 1-based indexing and match the exact mathematical specifications.
- **Clean Academic Attribution:** Team member and faculty placeholders are provided on Slide 1 of the PowerPoint deck for student customization.
