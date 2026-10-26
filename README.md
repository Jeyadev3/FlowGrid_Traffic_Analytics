# FlowGrid — Dynamic Traffic Congestion Analytics Using Fenwick Tree

> **Data Structures & Algorithms (DSA) Second-Year CSE Case Study Project**  
> **Evaluation Mode:** Automatic Benchmark Demonstration (Explicitly Non-Menu-Driven) & Live Web Integration  
> **Engine:** 1-Based Fenwick Tree (Binary Indexed Tree / BIT) Core implemented in C++17

---

## 1. Project Overview & Team Contributions

**FlowGrid** is a dynamic traffic congestion analytics system designed to monitor urban vehicular corridors in real time. In metropolitan transportation grids, road segments experience rapid fluctuations in traffic density due to signals, lane closures, accidents, and rush-hour surges.

Traffic management centers require two fundamental operations:
1. **Dynamic Point Updates ($O(\log n)$):** Ingest real-time vehicle counts from road sensors as conditions change.
2. **Corridor Range Queries ($O(\log n)$):** Query cumulative vehicle volume over any sub-corridor $[L \dots R]$ and detect whether density exceeds safety thresholds (`NORMAL` vs `POTENTIALLY CONGESTED`).

### Team Work Division
- **Member 1 (Traffic Data Management & Tree Initialization):**
  - Formulated 1-based indexing data representation for 8 corridor segments.
  - Implemented `initializeData()` and linear-time $O(n)$ Fenwick Tree construction (`buildFenwick()`) via forward propagation.
- **Member 2 (Core Bitwise & Tree Operations):**
  - Implemented bitwise `lowbit(x) = x & (-x)`.
  - Implemented dynamic point updates (`update(idx, delta)`) and absolute value setting (`setCount(idx, newCount)`).
  - Implemented prefix sum accumulation (`prefixSum(idx)`).
- **Member 3 (Range Queries & Congestion Detection):**
  - Implemented range queries via principle of inclusion-exclusion: `rangeSum(L, R) = prefixSum(R) - prefixSum(L - 1)`.
  - Implemented threshold classification (`detectCongestion()`).
  - Authored automated non-menu-driven benchmark demonstration covering Steps 1 to 8.
- **Member 4 (Dashboard Improvements, Backend Integration & Testing):**
  - Designed zero-dependency Python HTTP server (`server.py`) bridging browser requests to the compiled C++ executable.
  - Added CLI JSON interface to `src/main.cpp` for live queries and updates while 100% preserving default automated benchmark demo.
  - Enhanced dashboard UI with interactive segment selection, real-time range tags, ancestor path visualization, and backend health indicators.
  - Enforced consistent congestion logic (`< 55` $\implies$ `NORMAL`, `$\ge 55$` $\implies$ `POTENTIALLY CONGESTED`).
  - Authored comprehensive 32-point automated test suite (`tests/test_flowgrid.py`).

---

## 2. System Architecture & Communication Flow

```
+-------------------------------------------------------------------------+
|                       FlowGrid Web Dashboard (UI)                       |
|   - 8-Segment Interactive Grid      - Range Query & Congestion Pill     |
|   - Point Update Controls           - BIT Array & Hierarchy Inspector   |
+-------------------------------------------------------------------------+
                                    |
                    HTTP REST APIs  |  JSON Requests / Responses
              (GET /api/status, GET /api/state, POST /api/query, etc.)
                                    v
+-------------------------------------------------------------------------+
|                  Python 3 Lightweight HTTP Server                       |
|                   (server.py — Python Standard Library)                 |
|   - Serves static assets from app/                                      |
|   - Maintains server corridor state                                     |
|   - Safely invokes compiled C++ executable via subprocess               |
+-------------------------------------------------------------------------+
                                    |
                    CLI Subprocess  |  Arguments: --query, --update, etc.
                    Standard I/O    |  Output: Structured JSON
                                    v
+-------------------------------------------------------------------------+
|                  Compiled C++ Fenwick Tree Engine                       |
|                   (bin/traffic_analytics.exe)                           |
|   - O(1) lowbit(x) = x & (-x)                                           |
|   - O(n) buildFenwick() forward propagation                             |
|   - O(log n) update() and setCount()                                    |
|   - O(log n) prefixSum() and rangeSum()                                 |
|   - O(1) detectCongestion() (< 55 vs >= 55)                             |
+-------------------------------------------------------------------------+
```

---

## 3. Theoretical Background: The Fenwick Tree (BIT)

A **Fenwick Tree** (also known as a **Binary Indexed Tree** or **BIT**), proposed by Peter Fenwick in 1994, is an array-based data structure that efficiently computes prefix sums and supports point modifications in $O(\log n)$ time while using strictly $O(n)$ space.

### The `lowbit()` Operator
The structure of a Fenwick Tree relies on the binary representation of indices. The function `lowbit(x)` isolates the lowest set bit (the least significant 1-bit) in the binary representation of $x$:

$$\text{lowbit}(x) = x \ \& \ (-x)$$

Using two's complement arithmetic, $-x = (\sim x) + 1$. Bitwise ANDing $x$ with $-x$ zeroes out all higher bits and preserves only the lowest 1-bit.

### 1-Based Responsibility Intervals
In a 1-based Fenwick Tree of size $n = 8$, each node $\text{bit}[i]$ stores the sum of elements over the contiguous interval:

$$[i - \text{lowbit}(i) + 1 \dots i]$$

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

## 4. Algorithmic Operations & Complexities

### Comparative Complexity Analysis

| Data Structure | Point Update | Prefix Sum | Range Sum $[L \dots R]$ | Auxiliary Space |
| :--- | :---: | :---: | :---: | :---: |
| **Naive Array** | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ |
| **Prefix Sum Array** | $O(n)$ | $O(1)$ | $O(1)$ | $O(n)$ |
| **Segment Tree** | $O(\log n)$ | $O(\log n)$ | $O(\log n)$ | $O(4n)$ |
| **Fenwick Tree (BIT)** | $\mathbf{O(\log n)}$ | $\mathbf{O(\log n)}$ | $\mathbf{O(\log n)}$ | $\mathbf{O(n)}$ |

### Algorithmic Routines

1. **`buildFenwick()` — $O(n)$ Construction:**
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
   Computes $\Delta = \text{newCount} - \text{trafficCounts}[idx]$, updates the raw array $\text{trafficCounts}[idx] = \text{newCount}$, and calls `update(idx, delta)`.

4. **`prefixSum(idx)` — $O(\log n)$ Cumulative Sum:**
   Accumulates $\text{bit}[i]$ and descends the tree via $i \leftarrow i - \text{lowbit}(i)$ until $i = 0$.

5. **`rangeSum(left, right)` — $O(\log n)$ Range Query:**
   $$\text{rangeSum}(L, R) = \text{prefixSum}(R) - \text{prefixSum}(L - 1)$$

6. **`detectCongestion(currentSum, threshold)` — $O(1)$ Threshold Classification:**
   - **`NORMAL`** if $\text{currentSum} < \text{threshold}$.
   - **`POTENTIALLY CONGESTED`** if $\text{currentSum} \ge \text{threshold}$.

---

## 5. Benchmark Demonstration (Exact Case Study Numbers)

### Initial State
- **Segments 1 to 8:** `[12, 7, 15, 9, 20, 5, 11, 8]`
- **Expected Initial BIT:** `[12, 19, 15, 43, 20, 25, 11, 87]`
- **Expected Total Traffic:** $87$ vehicles

### Execution Sequence
1. **Query Corridor $[3 \dots 6]$ with Threshold $55$:**
   $$\text{prefixSum}(6) = \text{bit}[6] + \text{bit}[4] = 25 + 43 = 68$$
   $$\text{prefixSum}(2) = \text{bit}[2] = 19$$
   $$\text{rangeSum}(3, 6) = 68 - 19 = \mathbf{49}$$
   - Since $49 < 55 \implies$ **`NORMAL`** $\checkmark$

2. **Dynamic Update:** Segment 5 updated from $20$ to $34$ ($\Delta = +14$).
   - Traversal path updated: $\text{bit}[5]$, $\text{bit}[6]$, $\text{bit}[8]$.
   - **Expected Updated BIT:** `[12, 19, 15, 43, 34, 39, 11, 101]` $\checkmark$

3. **Re-Query Corridor $[3 \dots 6]$ with Threshold $55$:**
   $$\text{prefixSum}(6) = \text{bit}[6] + \text{bit}[4] = 39 + 43 = 82$$
   $$\text{prefixSum}(2) = \text{bit}[2] = 19$$
   $$\text{rangeSum}(3, 6) = 82 - 19 = \mathbf{63}$$
   - Since $63 \ge 55 \implies$ **`POTENTIALLY CONGESTED`** $\checkmark$

---

## 6. Workspace File Structure

```
FlowGrid_Traffic_Analytics/
├── .gitignore                          # Git exclusions (build binaries, caches)
├── README.md                           # Comprehensive documentation & evaluation guide
├── generate_pptx.py                    # Standalone PowerPoint generator script
├── server.py                           # Lightweight Python HTTP server & C++ bridge (Member 4)
├── app/                                # Interactive Web Application
│   ├── index.html                      # Semantic dashboard markup with live C++ connection status
│   ├── style.css                       # Responsive dark-theme styling, animations & status indicators
│   └── script.js                       # Frontend controller connected to C++ backend via REST API
├── bin/                                # Compiled binaries directory
│   └── traffic_analytics.exe           # Statically compiled C++17 Fenwick Tree executable
├── presentation/                       # Case Study Presentation
│   └── Fenwick_Tree_Case_Study.pptx    # 14-slide professional PowerPoint deck
├── src/                                # C++ Implementation
│   └── main.cpp                        # Standard C++ Fenwick Tree engine, demo & CLI interface
└── tests/                              # Verification Suite
    ├── test_cases.md                   # 32-case test matrix & verified output logs
    └── test_flowgrid.py                # Automated integration test runner (Member 4)
```

---

## 7. Compilation & Execution Instructions

### A. Prerequisites
- **C++ Compiler:** Any standard C++ compiler supporting C++17 (`g++`, `clang++`, or MSVC `cl.exe`).
- **Python:** Python 3.8+ (standard library only; no `pip` packages required).
- **Web Browser:** Any modern web browser (Chrome, Edge, Firefox, Safari).

---

### B. Compiling the C++ Fenwick Tree Engine

From the project root (`FlowGrid_Traffic_Analytics/`), run:

```powershell
# Using g++ (MinGW / GCC) with static linking to eliminate external DLL dependencies:
g++ -std=c++17 -Wall -Wextra -O2 -static -static-libgcc -static-libstdc++ src/main.cpp -o bin/traffic_analytics.exe
```

---

### C. Running the Standalone C++ Automated Benchmark

The C++ program runs the complete automated demonstration when invoked without arguments:

```powershell
.\bin\traffic_analytics.exe
```

CLI modes for scripted queries:
```powershell
# Query range [3..6] with threshold 55:
.\bin\traffic_analytics.exe --query 3 6 55 12 7 15 9 20 5 11 8

# Update segment 5 to count 34:
.\bin\traffic_analytics.exe --update 5 34 12 7 15 9 20 5 11 8

# Query current BIT state:
.\bin\traffic_analytics.exe --state 12 7 15 9 20 5 11 8
```

---

### D. Starting the FlowGrid Backend Server & Dashboard

To launch the integrated application:

```powershell
python server.py
```

Then open your browser to:
```
http://127.0.0.1:8000/
```

#### What happens:
1. `server.py` starts on port 8000 and serves the dashboard from `app/`.
2. The browser automatically connects to the backend and displays `C++ Fenwick Core: Connected`.
3. Clicking **"Run Benchmark Demo"**, **"Apply Update"**, or **"Evaluate"** triggers genuine calls to the compiled C++ `traffic_analytics.exe` binary.
4. Clicking any road segment card in the corridor grid interactively selects that segment for point updates.

---

### E. Running the Automated Test Suite

To run all 32 automated verification and integration tests:

```powershell
python tests/test_flowgrid.py
```

All 32 test cases verify:
- Initial linear-time construction.
- Prefix sums across all 8 indices.
- Corridor range sums ($[3 \dots 6]$, $[5 \dots 5]$, $[1 \dots 8]$).
- Point updates and ancestor paths.
- Re-query after updates.
- Congestion boundary conditions ($< 55$ vs $\ge 55$).
- Out-of-bounds indices, inverted ranges, and negative counts.
- Repeated updates ensuring cumulative state integrity.
- Full HTTP API endpoints (`/api/status`, `/api/state`, `/api/query`, `/api/update`, `/api/reset`).
- Exact case study numbers ($49 \to 63$).
- Automated standalone demonstration execution.

---

## 8. Limitations & Future Roadmap

1. **1D Linear Corridors:**
   - *Current:* Operates on a linear sequence of road segments $[1 \dots n]$.
   - *Future:* Extend to a 2D Fenwick Tree to monitor $M \times N$ road intersections in $O(\log^2 n)$ time.
2. **Fixed Segment Capacity:**
   - *Current:* Fixed array size $n = 8$. Dynamic addition of new segments requires dynamic vector resizing.
3. **Range Updates:**
   - *Current:* Optimized for point updates + range queries.
   - *Future:* Implement dual-tree difference encoding ($D[i]$ and $D[i] \times i$) to support both range updates and range queries in $O(\log n)$.
4. **Predictive Analytics:**
   - *Future:* Couple the BIT cumulative volume tracking with an ARIMA or LSTM time-series model to forecast congestion 15 minutes before thresholds are breached.

---

## 9. Academic Integrity & Note for Faculty

- **Preservation of Existing Work:** Members 1, 2, and 3's core data structure implementations and non-menu benchmark demonstration are 100% preserved.
- **Genuine C++ Integration:** Member 4 connected the web dashboard directly to the compiled C++ executable via a lightweight Python server. The browser does not simulate the Fenwick Tree; all numbers, traversal paths, and congestion classifications are computed by C++ in real time.
- **Consistent Boundary Classification:** Threshold comparison is strictly unified across C++, the server, and the dashboard ($< 55 \implies$ `NORMAL`, $\ge 55 \implies$ `POTENTIALLY CONGESTED`).
