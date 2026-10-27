FlowGrid — Dynamic Traffic Congestion Analytics Using Fenwick Tree

«Domain: Data Structures and Algorithms (DSA)
Academic Level: Second-Year Computer Science Engineering
Language: C++17
Backend: Python 3 Standard Library
Data Structure: Fenwick Tree (Binary Indexed Tree / BIT)
Execution Mode: Automated Benchmark Demonstration and Interactive Web Dashboard»

---

1. Project Overview

FlowGrid is a dynamic traffic congestion analytics system that demonstrates how a Fenwick Tree can efficiently maintain and query vehicle counts across a sequence of road segments.

In urban road networks, traffic conditions change continuously due to accidents, lane closures, traffic signals, and rush-hour surges. Efficient traffic analysis requires a system that can update individual vehicle counts and calculate traffic totals across selected corridors without repeatedly scanning the entire dataset.

FlowGrid addresses this problem using a one-based Fenwick Tree implemented in C++17.

The project supports two fundamental operations:

- Dynamic Point Updates: Update the vehicle count of an individual road segment in O(log n) time.
- Range-Sum Queries: Calculate the total traffic across a selected range of segments in O(log n) time.

The calculated traffic total is compared with a configurable threshold to classify the corridor as "NORMAL" or "POTENTIALLY CONGESTED".

The project also integrates the C++ engine with a Python HTTP server and a browser-based dashboard, providing an interactive interface for traffic updates, range queries, and visualization of Fenwick Tree operations.

2. Project Objectives

The primary objectives of FlowGrid are:

1. Implement a Fenwick Tree using one-based array indexing.
2. Construct the tree efficiently in O(n) time.
3. Support dynamic point updates in O(log n) time.
4. Calculate prefix sums and range sums efficiently.
5. Classify traffic totals using a predefined congestion threshold.
6. Demonstrate the algorithm through an automated, non-menu-driven benchmark.
7. Integrate the C++ engine with a Python HTTP server.
8. Provide an interactive browser-based traffic analytics dashboard.
9. Validate the implementation using automated tests and edge-case checks.
10. Demonstrate the practical application of data structures and algorithmic complexity analysis.

3. Team Contributions

Member 1 — Traffic Data Management and Tree Initialization

- Designed the one-based representation of traffic counts across eight road segments.
- Implemented "initializeData()" to initialize the original traffic array.
- Implemented "buildFenwick()" using linear-time forward propagation.
- Verified the initial Fenwick Tree structure and total traffic count.

Member 2 — Core Bitwise Operations and Dynamic Updates

- Implemented "lowbit(x)" using "x & (-x)".
- Implemented "update(idx, delta)" for point updates.
- Implemented "setCount(idx, newCount)" for setting absolute traffic counts.
- Implemented "prefixSum(idx)" for cumulative traffic calculations.
- Maintained consistency between the original traffic array and the Fenwick Tree.

Member 3 — Range Queries and Congestion Detection

- Implemented "rangeSum(left, right)" using prefix-sum subtraction.
- Implemented "detectCongestion()" for threshold-based classification.
- Developed the automated, non-menu-driven benchmark demonstration.
- Verified baseline and post-update range-query results.
- Added demonstrations for invalid ranges, invalid indices, negative counts, zero-count updates, and threshold boundaries.
- Documented the algorithm's correctness and complexity.

Member 4 — Web Integration, Dashboard, and Testing

- Developed a lightweight Python HTTP server using the Python standard library.
- Integrated browser requests with the compiled C++ executable using subprocess calls.
- Added a CLI JSON interface for state inspection, range queries, and other supported operations.
- Developed the interactive web dashboard with segment selection, update controls, range-query displays, and Fenwick Tree visualization.
- Added backend health indicators and API integration.
- Developed a 32-case automated test suite for algorithmic and integration verification.

4. Technology Stack

Component| Technology
Core algorithm| Fenwick Tree / Binary Indexed Tree
Programming language| C++17
C++ compiler| GCC, Clang, or MSVC
Backend server| Python 3
HTTP server implementation| Python standard library
Frontend structure| HTML5
Frontend styling| CSS3
Frontend interaction| JavaScript
Data exchange| JSON over HTTP
Testing| Python automated test runner
Interface| Browser-based dashboard

The backend is designed to use Python's standard library without requiring third-party Python packages.

5. System Architecture

FlowGrid consists of three main layers.

5.1 Presentation Layer

The browser-based dashboard provides:

- An interactive grid of road segments.
- Controls for updating traffic counts.
- Range-query inputs.
- Congestion status indicators.
- Fenwick Tree array inspection.
- Update and prefix-query traversal visualization.
- Backend connection status.

5.2 Backend Layer

The Python HTTP server:

- Serves static frontend files.
- Handles HTTP API requests.
- Maintains the application's corridor state.
- Invokes the compiled C++ executable through subprocess calls.
- Returns structured JSON responses to the browser.

5.3 Processing Layer

The C++ engine performs the core calculations:

- Fenwick Tree construction.
- Point updates.
- Prefix-sum queries.
- Range-sum queries.
- Congestion classification.
- Automated benchmark execution.

Communication Flow

+------------------------------------------+
|          FlowGrid Web Dashboard          |
|                                          |
| Segment Selection | Point Updates        |
| Range Queries     | Congestion Status    |
| BIT Visualization | Backend Status       |
+--------------------+---------------------+
                     |
                     | HTTP Requests / JSON
                     v
+------------------------------------------+
|           Python HTTP Server             |
|                                          |
| Static File Serving | API Routing        |
| State Management    | Subprocess Bridge  |
+--------------------+---------------------+
                     |
                     | CLI Arguments
                     | JSON Output
                     v
+------------------------------------------+
|          C++ Fenwick Tree Engine         |
|                                          |
| Build | Update | Prefix Sum | Range Sum  |
|             Congestion Detection         |
+------------------------------------------+

6. Theoretical Background: Fenwick Tree

A Fenwick Tree, also called a Binary Indexed Tree, is an array-based data structure designed for efficient prefix-sum calculations and point updates.

Unlike a conventional array that requires scanning multiple elements to calculate a range sum, a Fenwick Tree stores partial sums associated with the binary representation of array indices.

6.1 The Lowbit Operation

The fundamental operation is:

static int lowbit(int x) {
    return x & (-x);
}

The expression "x & (-x)" isolates the lowest set bit in the binary representation of "x".

For example:

Index| Binary| Lowbit
1| 0001| 1
2| 0010| 2
3| 0011| 1
4| 0100| 4
5| 0101| 1
6| 0110| 2
7| 0111| 1
8| 1000| 8

The lowbit value determines the range represented by each Fenwick Tree entry.

6.2 Responsibility Intervals

For a one-based Fenwick Tree, the entry "BIT[i]" stores the sum of the elements in the interval:

"[i - lowbit(i) + 1, i]"

For eight road segments:

BIT Index| Lowbit| Responsibility Interval
1| 1| [1, 1]
2| 2| [1, 2]
3| 1| [3, 3]
4| 4| [1, 4]
5| 1| [5, 5]
6| 2| [5, 6]
7| 1| [7, 7]
8| 8| [1, 8]

This structure enables efficient updates and queries without storing explicit tree nodes or pointers.

7. Core Algorithms

7.1 Fenwick Tree Construction

The tree is constructed using forward propagation.

for (int i = 1; i <= n; ++i) {
    bit[i] += trafficCounts[i];

    int parent = i + lowbit(i);

    if (parent <= n) {
        bit[parent] += bit[i];
    }
}

Each entry contributes its partial sum to its next responsible parent.

Time complexity: O(n)

7.2 Point Update

A point update adds a difference to the BIT entries affected by a changed segment.

for (int i = idx; i <= n; i += lowbit(i)) {
    bit[i] += delta;
}

The index moves forward using "i += lowbit(i)" until it exceeds the tree size.

Time complexity: O(log n)

7.3 Absolute Count Update

To set a segment's count to a new value:

delta = newCount - trafficCounts[idx];
trafficCounts[idx] = newCount;
update(idx, delta);

Only the difference is propagated through the tree, avoiding a complete reconstruction.

Time complexity: O(log n)

7.4 Prefix-Sum Query

The prefix-sum operation calculates the total traffic from segment 1 through the requested segment.

long long prefixSum(int idx) const {
    if (idx < 1) return 0;
    if (idx > n) idx = n;

    long long sum = 0;

    for (int i = idx; i > 0; i -= lowbit(i)) {
        sum += bit[i];
    }

    return sum;
}

The index moves backward using "i -= lowbit(i)" until it reaches zero.

Time complexity: O(log n)

7.5 Range-Sum Query

The range sum is calculated using two prefix sums:

"RangeSum(L, R) = PrefixSum(R) - PrefixSum(L - 1)"

This works because subtracting the traffic before segment L removes all elements outside the requested range.

Time complexity: O(log n)

7.6 Congestion Detection

The system compares the calculated traffic total with the configured threshold.

if (currentSum >= threshold) {
    return "POTENTIALLY CONGESTED";
}

return "NORMAL";

Classification rules:

- "NORMAL" when the total is below the threshold.
- "POTENTIALLY CONGESTED" when the total equals or exceeds the threshold.

Time complexity: O(1)

The complete operation, including the range query and classification, takes O(log n) time.

8. Benchmark Demonstration

The project includes an automated benchmark that demonstrates the Fenwick Tree's operations without requiring menu navigation.

8.1 Initial Traffic Data

The eight road segments contain the following vehicle counts:

[12, 7, 15, 9, 20, 5, 11, 8]

The expected initial BIT is:

[12, 19, 15, 43, 20, 25, 11, 87]

The total traffic across all eight segments is 87 vehicles.

8.2 Baseline Query

Selected range: segments 3 through 6.

Threshold: 55 vehicles.

Prefix sum at segment 6:

BIT[6] + BIT[4]
= 25 + 43
= 68

Prefix sum at segment 2:

BIT[2] = 19

Range sum:

RangeSum(3, 6) = 68 - 19 = 49

Since 49 is less than 55, the status is:

"NORMAL"

8.3 Dynamic Update

Segment 5 changes from 20 vehicles to 34 vehicles.

Delta = 34 - 20 = +14

The update visits BIT indices 5, 6, and 8.

The updated BIT becomes:

[12, 19, 15, 43, 34, 39, 11, 101]

The total traffic across all eight segments increases from 87 to 101.

8.4 Re-Query After the Update

Prefix sum at segment 6:

BIT[6] + BIT[4]
= 39 + 43
= 82

Prefix sum at segment 2:

BIT[2] = 19

Updated range sum:

RangeSum(3, 6) = 82 - 19 = 63

Since 63 is greater than or equal to 55, the status becomes:

"POTENTIALLY CONGESTED"

8.5 Results Summary

Metric| Before Update| After Update
Segment 5 Count| 20| 34
PrefixSum(6)| 68| 82
PrefixSum(2)| 19| 19
RangeSum(3, 6)| 49| 63
Threshold| 55| 55
Classification| NORMAL| POTENTIALLY CONGESTED

The benchmark demonstrates how a local change in traffic can alter the total for a selected corridor without rebuilding the entire Fenwick Tree.

9. Comparative Complexity Analysis

Data Structure| Point Update| Prefix Sum| Range Sum| Storage
Conventional Array| O(1)| O(n)| O(n)| O(n)
Static Prefix-Sum Array| O(n)| O(1)| O(1)| O(n)
Segment Tree| O(log n)| O(log n)| O(log n)| O(n)
Fenwick Tree| O(log n)| O(log n)| O(log n)| O(n)

A Fenwick Tree provides a practical balance between implementation simplicity, storage efficiency, and operation performance for dynamic range-sum queries.

The construction method used in FlowGrid takes O(n) time, while the update and query operations take O(log n) time.

10. Project File Structure

The following structure describes the proposed project organization:

FlowGrid_Traffic_Analytics/
├── .gitignore
├── README.md
├── generate_pptx.py
├── server.py
├── app/
│   ├── index.html
│   ├── style.css
│   └── script.js
├── bin/
│   └── traffic_analytics.exe
├── presentation/
│   └── Fenwick_Tree_Case_Study.pptx
├── src/
│   └── main.cpp
├── docs/
│   └── member-3-range-queries.md
└── tests/
    ├── test_cases.md
    └── test_flowgrid.py

This structure separates the C++ algorithm, browser interface, Python backend, documentation, generated presentation, and automated tests.

Compiled binaries may be excluded from version control depending on the repository's build and release strategy.

11. Compilation and Execution

11.1 Prerequisites

- A C++17-compatible compiler such as GCC, Clang, or MSVC.
- Python 3.8 or later.
- A modern web browser.

11.2 Compile the C++ Engine

From the project root, create the "bin" directory if it does not exist.

Using GCC or MinGW on Windows:

mkdir bin
g++ -std=c++17 -Wall -Wextra -O2 -static -static-libgcc -static-libstdc++ src/main.cpp -o bin/traffic_analytics.exe

If the "bin" directory already exists, the directory-creation step can be skipped.

11.3 Run the Automated Benchmark

.\bin\traffic_analytics.exe

The executable runs the default automated benchmark when no arguments are provided.

The explicit demo mode is also supported:

.\bin\traffic_analytics.exe --demo

11.4 Query a Traffic Range

.\bin\traffic_analytics.exe --query 3 6 55 12 7 15 9 20 5 11 8

This command queries segments 3 through 6 with a threshold of 55 and the specified initial traffic counts.

11.5 Inspect the Initial State

.\bin\traffic_analytics.exe --state 12 7 15 9 20 5 11 8

This command requests the initial traffic state and Fenwick Tree representation.

Note: CLI modes must be implemented in the compiled C++ source for these commands to work. The standalone benchmark and CLI interfaces should be validated against the actual repository version.

11.6 Start the Web Application

Run:

python server.py

Then open:

http://127.0.0.1:8000/

The Python server serves the frontend and handles supported API requests that invoke the C++ executable.

The compiled executable must be present at the path expected by the server.

12. Web Dashboard and API Integration

The web interface provides an interactive way to explore the traffic data and observe the Fenwick Tree in operation.

The project overview identifies the following API endpoints:

Endpoint| Intended Purpose
"GET /api/status"| Check backend availability
"GET /api/state"| Retrieve traffic and tree state
"POST /api/query"| Execute a range query
"POST /api/update"| Update a segment's count
"POST /api/reset"| Reset the corridor state

The exact HTTP methods, request payloads, response formats, and reset behavior should be confirmed against "server.py" and the frontend implementation.

The intended integration flow is:

1. The user interacts with the browser dashboard.
2. JavaScript sends a request to the Python HTTP server.
3. The server validates and processes the request.
4. The server invokes the compiled C++ executable when required.
5. The C++ engine calculates the result and returns structured output.
6. The server returns the response to the browser.
7. The dashboard updates its displayed state.

This architecture allows the browser interface to use the C++ Fenwick Tree implementation instead of independently simulating the core algorithm.

13. Automated Testing and Verification

The project overview specifies a Python test suite containing 32 test cases.

The described verification areas include:

- Initial Fenwick Tree construction.
- Prefix sums across the eight segment indices.
- Range queries such as [3, 6], [5, 5], and [1, 8].
- Point updates and traversal paths.
- Re-querying after an update.
- Congestion threshold boundary conditions.
- Invalid indices and inverted ranges.
- Negative-count rejection.
- Repeated updates and state consistency.
- HTTP API integration.
- Expected benchmark results of 49 and 63.
- Standalone automated benchmark execution.

Run the suite from the project root:

python tests/test_flowgrid.py

A passing test run should be confirmed from the actual command output rather than assumed.

The benchmark should also verify the computed BIT against the expected BIT and check each expected range total and congestion status.

14. Limitations

14.1 One-Dimensional Corridor Model

The current model represents road segments as a linear sequence. It does not directly model a two-dimensional urban road network.

14.2 Fixed Segment Capacity

The demonstration uses eight road segments. Adding segments requires suitable resizing or reconstruction logic.

14.3 Sum-Based Queries

The implemented Fenwick Tree supports prefix and range sums. It is not designed in its current form for range minimum or maximum queries.

14.4 Fixed Threshold Classification

The congestion classification uses a predefined threshold. It does not account for speed, road capacity, vehicle type, weather, or time-dependent traffic patterns.

14.5 Simulation-Based Data

The sample traffic counts are illustrative. The project does not independently collect real-world sensor data or control traffic signals.

14.6 Predictive Capabilities

The current system calculates traffic totals and classifies congestion. It does not forecast future congestion using a predictive model.

15. Future Enhancements

Potential improvements include:

1. Two-Dimensional Fenwick Tree: Extend the system to represent traffic counts across a grid of intersections.
2. Range Updates: Implement a suitable multi-tree Fenwick Tree approach to support range modifications and range queries.
3. Live Sensor Integration: Ingest traffic counts from real or simulated sensor streams.
4. Historical Traffic Analysis: Store measurements over time to analyze daily and weekly traffic patterns.
5. Predictive Analytics: Integrate time-series forecasting methods, such as ARIMA or LSTM, to estimate future traffic conditions.
6. Configurable Thresholds: Allow thresholds to vary by corridor, time, or estimated road capacity.
7. Expanded Automated Tests: Add randomized tests that compare Fenwick Tree answers against direct array calculations.
8. Deployment Improvements: Add structured logging, clearer API error handling, and deployment configuration.

16. Academic and Technical Notes

FlowGrid is an educational DSA case study demonstrating the application of a Fenwick Tree to dynamic range-sum queries.

The architecture separates algorithmic processing from the web interface. The C++ implementation handles the core tree operations, while the Python server and frontend provide an integration layer for interactive use.

For consistency, the congestion rule should be documented uniformly:

- Total below threshold: "NORMAL".
- Total greater than or equal to threshold: "POTENTIALLY CONGESTED".

The implementation, report, and tests should use the same boundary condition.

The final repository should also distinguish implemented and tested functionality from planned enhancements.

17. Conclusion

FlowGrid demonstrates how a Fenwick Tree can be applied to dynamic traffic congestion analytics. Its array-based structure supports efficient point updates, prefix sums, and range-sum queries while maintaining O(n) storage complexity.

The benchmark demonstrates a corridor total changing from 49 to 63 vehicles after the count of segment 5 increases from 20 to 34. Under the configured threshold of 55, the corridor changes from "NORMAL" to "POTENTIALLY CONGESTED".

By combining a C++17 algorithmic engine with a Python HTTP server and an interactive browser dashboard, the project illustrates how fundamental data structures can be integrated into a larger software application.

FlowGrid provides a foundation for further work in real-time data processing, traffic monitoring, and & status indicators
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
