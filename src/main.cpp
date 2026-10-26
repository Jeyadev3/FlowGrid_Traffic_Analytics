#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <stdexcept>
#include <cassert>

/**
 * ============================================================================
 * FlowGrid — Dynamic Traffic Congestion Analytics Using Fenwick Tree (BIT)
 * Case Study Demonstration Program (Standard C++17 / C++20)
 * ============================================================================
 * 
 * Data Structure: One-based Binary Indexed Tree (Fenwick Tree)
 * Key Characteristics:
 *   - Point Update: O(log n)
 *   - Prefix Sum Query: O(log n)
 *   - Range Sum Query: O(log n)
 *   - Space Complexity: O(n)
 *
 * NOTE: This is a non-menu-driven, fully automated demonstration project
 * designed to rigorously verify and benchmark Fenwick Tree traffic operations.
 */

class TrafficFenwickTree {
private:
    int n;                          // Number of road segments
    std::vector<int> trafficCounts; // Original traffic count array (1-indexed, size n + 1)
    std::vector<long long> bit;     // Fenwick tree / Binary Indexed Tree (1-indexed, size n + 1)

public:
    // ========================================================================
    // MEMBER 1: TRAFFIC DATA MANAGEMENT & FENWICK TREE INITIALIZATION
    // ========================================================================

    /**
     * Default constructor: initializes an empty Fenwick Tree structure.
     */
    TrafficFenwickTree(int size = 0) {
        init(size);
    }

    /**
     * Parameterized constructor: validates and initializes traffic counts from
     * a zero-based vector, then builds the Fenwick Tree in O(n) time.
     * 
     * @param data Zero-based vector containing initial vehicular traffic counts.
     */
    explicit TrafficFenwickTree(const std::vector<int>& data) {
        if (initializeData(data)) {
            buildFenwick();
        }
    }

    /**
     * Resets and sizes internal 1-based arrays with index 0 unused.
     * Memory allocation: (n + 1) elements for both trafficCounts and bit.
     */
    void init(int size) {
        n = size;
        trafficCounts.assign(n + 1, 0);
        bit.assign(n + 1, 0LL);
    }

    // Note: lowbit(i) is Member 2's core bitwise operation (Task 1).
    // Reused here by buildFenwick(). Defined below under MEMBER 2.

    /**
     * Member 1: Traffic Data Validation
     * ----------------------------------
     * Validates that the initial traffic dataset satisfies all physical preconditions:
     *   1. Non-empty: Must contain at least one road segment (data.size() > 0).
     *   2. Non-negative: Traffic volume cannot be negative; each element must be >= 0.
     * 
     * @param data Zero-based vector of initial traffic counts.
     * @return true if data is valid; false if empty or negative count detected.
     */
    static bool validateInitialData(const std::vector<int>& data) {
        if (data.empty()) {
            std::cerr << "[Error] Initial traffic data is empty. Dataset must be non-empty.\n";
            return false;
        }
        for (size_t i = 0; i < data.size(); ++i) {
            if (data[i] < 0) {
                std::cerr << "[Error] Invalid traffic count at segment " << (i + 1) 
                          << " (index " << i << "): " << data[i] 
                          << " (Traffic counts must be non-negative).\n";
                return false;
            }
        }
        return true;
    }

    /**
     * Member 1: Traffic Data Initialization
     * --------------------------------------
     * Initializes the original traffic array with a given zero-based vector of counts.
     * Translates zero-based external input data[0..n-1] to internal one-based
     * indexing trafficCounts[1..n], keeping index 0 unused (trafficCounts[0] = 0).
     * 
     * Preconditions validated via validateInitialData():
     *   - data must be non-empty (n >= 1).
     *   - data must contain non-negative traffic counts (data[i] >= 0).
     *
     * Complexity:
     *   - Time Complexity: O(n) linear validation and copy.
     *   - Space Complexity: O(n) array allocation.
     * 
     * @param data Zero-based vector of initial traffic counts: {12, 7, 15, 9, 20, 5, 11, 8}.
     * @return true if successfully validated and loaded; false otherwise.
     */
    bool initializeData(const std::vector<int>& data) {
        if (!validateInitialData(data)) {
            return false;
        }

        n = static_cast<int>(data.size());
        trafficCounts.assign(n + 1, 0);
        bit.assign(n + 1, 0LL);

        // Populate 1-based trafficCounts array; index 0 remains 0 (unused)
        for (int i = 1; i <= n; ++i) {
            trafficCounts[i] = data[i - 1];
        }
        return true;
    }

    /**
     * Member 1: Fenwick Tree Build Logic (O(n) Linear Time)
     * -----------------------------------------------------
     * Constructs the 1-based Binary Indexed Tree in linear O(n) time using
     * the forward-propagation technique, avoiding naive O(n log n) insertion.
     *
     * Algorithmic Explanation:
     * 1. Internal Structure (1-based, index 0 unused):
     *    In a 1-based BIT of size n, index 0 is permanently unused (bit[0] = 0).
     *    Each node bit[i] stores the cumulative traffic sum over the interval:
     *        [i - lowbit(i) + 1 .. i]
     *    The length of this responsibility interval is exactly lowbit(i).
     *
     * 2. Forward Propagation Algorithm:
     *    - Start with bit[0..n] reset to 0.
     *    - For each index i from 1 to n:
     *        a) Add trafficCounts[i] to bit[i].
     *        b) The immediate parent of node i in the Fenwick Tree hierarchy
     *           is: parent = i + lowbit(i).
     *        c) If parent <= n, propagate the accumulated value of bit[i]
     *           directly to bit[parent]: bit[parent] += bit[i].
     *    - Because the loop traverses sequentially from 1 to n, when the iteration
     *      reaches an index, all of its left-child intervals have already been
     *      accumulated into it.
     *    - Total time complexity: exactly n iterations with O(1) operations -> O(n).
     *    - Auxiliary space: O(1) beyond the O(n) tree storage.
     *
     * 3. Trace for Benchmark Dataset {12, 7, 15, 9, 20, 5, 11, 8}:
     *    i=1: bit[1]=12, lowbit=1, parent=2 -> bit[2] += 12  (bit[2]=12)
     *    i=2: bit[2]+=7 (19), lowbit=2, parent=4 -> bit[4] += 19  (bit[4]=19)
     *    i=3: bit[3]=15, lowbit=1, parent=4 -> bit[4] += 15  (bit[4]=34)
     *    i=4: bit[4]+=9 (43), lowbit=4, parent=8 -> bit[8] += 43  (bit[8]=43)
     *    i=5: bit[5]=20, lowbit=1, parent=6 -> bit[6] += 20  (bit[6]=20)
     *    i=6: bit[6]+=5 (25), lowbit=2, parent=8 -> bit[8] += 25  (bit[8]=68)
     *    i=7: bit[7]=11, lowbit=1, parent=8 -> bit[8] += 11  (bit[8]=79)
     *    i=8: bit[8]+=8 (87), lowbit=8, parent=16 > 8 (terminate)
     *
     *    Resulting Fenwick Tree BIT array (excluding index 0):
     *    Index:      1   2   3   4   5   6   7   8
     *    bit[i]:    12  19  15  43  20  25  11  87
     */
    void buildFenwick() {
        if (n <= 0) return;

        // Reset bit array (index 0 remains unused, bit[0] = 0)
        std::fill(bit.begin(), bit.end(), 0LL);

        // O(n) linear forward-propagation construction
        for (int i = 1; i <= n; ++i) {
            bit[i] += trafficCounts[i];
            int parent = i + lowbit(i);
            if (parent <= n) {
                bit[parent] += bit[i];
            }
        }
    }

    // ========================================================================
    // MEMBER 2: FENWICK TREE CORE OPERATIONS (O(log n))
    // ========================================================================

    /**
     * Member 2 (Task 1): lowbit Operator
     * ----------------------------------
     * Isolates the lowest set bit (least significant 1-bit) of an integer index
     * using two's complement bitwise arithmetic: lowbit(i) = i & (-i).
     * 
     * Mathematical Formula:
     *     lowbit(i) = i & (-i)
     * 
     * Binary Representation Mechanics:
     *     In standard two's complement representation, negating an integer i
     *     inverts all bits and adds 1: -i = (~i) + 1.
     *     Bitwise ANDing i with -i zeros out all higher-order bits, preserving
     *     strictly the single lowest 1-bit.
     * 
     * Algorithmic Roles in FlowGrid:
     *   1. Interval Length: Node bit[i] stores the cumulative volume over exactly
     *      lowbit(i) road segments: [i - lowbit(i) + 1 .. i].
     *   2. Point Update Traversal: parent = i + lowbit(i) (ascends tree in O(log n)).
     *   3. Prefix Sum Traversal: prev = i - lowbit(i) (descends tree in O(log n)).
     *   4. Linear Build (Member 1): parent = i + lowbit(i) (reused in buildFenwick).
     * 
     * Complexity:
     *   - Time Complexity: O(1) bitwise operations.
     *   - Space Complexity: O(1).
     * 
     * @param i 1-based index (road segment number).
     * @return Value of the least significant set bit (power of 2).
     */
    static int lowbit(int i) {
        return i & (-i);
    }

    /**
     * Member 2 (Task 2 & 5): Dynamic Point Update (O(log n))
     * ------------------------------------------------------
     * Updates the Fenwick Tree by adding a relative difference (delta) to
     * segment idx and propagating this change to all ancestor nodes that
     * cover idx in their responsibility intervals.
     * 
     * Algorithmic Traversal:
     *   - Start at index i = idx.
     *   - In each iteration, add delta to bit[i]: bit[i] += delta.
     *   - Advance to the immediate parent node in the Fenwick Tree hierarchy
     *     by adding the lowest set bit: i += lowbit(i).
     *   - Terminate when i exceeds the corridor capacity n.
     * 
     * Trace for Benchmark Dataset (n = 8, idx = 5, delta = +14):
     *   Iteration 1: i = 5 (0101_2), lowbit(5) = 1 -> bit[5] += 14 (20 -> 34)
     *                Next i = 5 + 1 = 6 (0110_2)
     *   Iteration 2: i = 6 (0110_2), lowbit(6) = 2 -> bit[6] += 14 (25 -> 39)
     *                Next i = 6 + 2 = 8 (1000_2)
     *   Iteration 3: i = 8 (1000_2), lowbit(8) = 8 -> bit[8] += 14 (87 -> 101)
     *                Next i = 8 + 8 = 16 > 8 (terminates traversal)
     * 
     * Safety & Validation:
     *   - Validates that idx satisfies 1-based bounds: 1 <= idx <= n.
     *   - If idx is out of bounds, logs an error to std::cerr and returns false safely.
     * 
     * Complexity:
     *   - Time Complexity: O(log n) tree traversal (at most floor(log2 n) + 1 additions).
     *   - Space Complexity: O(1) auxiliary space.
     * 
     * @param idx 1-based segment index to update (1 to n).
     * @param delta Difference to add (+surge / -clearance).
     * @return true if update was successful; false if idx is out of bounds.
     */
    bool update(int idx, int delta) {
        if (idx < 1 || idx > n) {
            std::cerr << "[Error] Index out of bounds in update(): " << idx 
                      << " (Valid range: 1 to " << n << ")\n";
            return false;
        }

        for (int i = idx; i <= n; i += lowbit(i)) {
            bit[i] += delta;
        }
        return true;
    }

    /**
     * Member 2 (Task 3, 5 & 6): Absolute Traffic Count Setting (O(log n))
     * -------------------------------------------------------------------
     * Sets the absolute vehicular traffic count for a specific road segment idx.
     * Automatically calculates the relative change (delta) from the segment's
     * existing count, updates the raw traffic count array, and propagates the delta
     * to the Fenwick Tree via update().
     * 
     * Mathematical Formula:
     *     delta = newCount - trafficCounts[idx]
     * 
     * Preconditions & Validations:
     *   1. Index Bounds: 1 <= idx <= n. Out-of-bounds indices are rejected safely.
     *   2. Non-negative Counts: Traffic volume cannot be negative (newCount >= 0).
     *      Negative counts are safely rejected without modifying data.
     * 
     * State Synchronization:
     *   - Maintains 100% synchronization between original traffic array (trafficCounts)
     *     and the Fenwick Tree (bit).
     * 
     * Trace for Benchmark Case (Segment 5 from 20 to 34):
     *   - oldCount = trafficCounts[5] = 20
     *   - newCount = 34
     *   - delta    = 34 - 20 = +14
     *   - trafficCounts[5] becomes 34
     *   - update(5, 14) updates bit[5], bit[6], bit[8]
     * 
     * Complexity:
     *   - Time Complexity: O(log n) due to update() traversal.
     *   - Space Complexity: O(1) auxiliary space.
     * 
     * @param idx 1-based segment index (1 to n).
     * @param newCount New non-negative vehicular count.
     * @return true if successfully validated and updated; false otherwise.
     */
    bool setCount(int idx, int newCount) {
        if (idx < 1 || idx > n) {
            std::cerr << "[Error] Index out of bounds in setCount(): " << idx 
                      << " (Valid range: 1 to " << n << ")\n";
            return false;
        }
        if (newCount < 0) {
            std::cerr << "[Error] Invalid traffic count: " << newCount 
                      << " (Counts must be non-negative).\n";
            return false;
        }

        int delta = newCount - trafficCounts[idx];
        trafficCounts[idx] = newCount;
        return update(idx, delta);
    }

    /**
     * Member 2 (Task 4 & 5): Prefix Sum Query (O(log n))
     * --------------------------------------------------
     * Computes the cumulative vehicular traffic volume across road segments
     * from segment 1 up to segment idx in O(log n) time.
     * 
     * Mathematical Formula:
     *     prefixSum(idx) = sum_{k=1}^{idx} trafficCounts[k]
     * 
     * Algorithmic Traversal:
     *   - Start at index i = idx.
     *   - In each iteration, add bit[i] to the cumulative sum: sum += bit[i].
     *   - Move to the preceding disjoint interval in the Fenwick Tree by
     *     subtracting the lowest set bit: i -= lowbit(i).
     *   - Terminate when i reaches 0 (all intervals accumulated).
     * 
     * Mathematical Trace for Benchmark Dataset (n = 8):
     *   prefixSum(6) [Before Update: bit = {12, 19, 15, 43, 20, 25, 11, 87}]:
     *     Iteration 1: i = 6 (0110_2), sum += bit[6] (25) = 25
     *                  Next i = 6 - lowbit(6) = 6 - 2 = 4 (0100_2)
     *     Iteration 2: i = 4 (0100_2), sum += bit[4] (43) = 25 + 43 = 68
     *                  Next i = 4 - lowbit(4) = 4 - 4 = 0 (terminate)
     *     Result = 68 vehicles.
     * 
     *   prefixSum(6) [After Segment 5 Updated to 34: bit = {12, 19, 15, 43, 34, 39, 11, 101}]:
     *     Iteration 1: i = 6, sum += bit[6] (39) = 39
     *                  Next i = 6 - 2 = 4
     *     Iteration 2: i = 4, sum += bit[4] (43) = 39 + 43 = 82
     *                  Next i = 4 - 4 = 0 (terminate)
     *     Result = 82 vehicles.
     * 
     * Boundary Safety:
     *   - If idx < 1, returns 0 (sum over empty corridor [1 .. 0] is 0).
     *   - If idx > n, clamps idx to n (sums entire monitored corridor [1 .. n]).
     * 
     * Complexity:
     *   - Time Complexity: O(log n) tree traversal (at most floor(log2 n) + 1 additions).
     *   - Space Complexity: O(1) auxiliary space.
     * 
     * @param idx Upper 1-based segment index of the prefix range [1 .. idx].
     * @return Cumulative traffic count as a 64-bit integer (long long).
     */
    long long prefixSum(int idx) const {
        if (idx < 1) return 0;
        if (idx > n) idx = n;

        long long sum = 0;
        for (int i = idx; i > 0; i -= lowbit(i)) {
            sum += bit[i];
        }
        return sum;
    }

    // ========================================================================
    // MEMBER 3: RANGE QUERIES & CONGESTION DETECTION (O(log n))
    // ========================================================================

    /**
     * Member 3 (Task 1 & 5): Corridor Range Sum Query (O(log n))
     * ----------------------------------------------------------
     * Computes cumulative vehicular traffic volume across road segments
     * within the closed interval [left, right] in O(log n) time.
     * 
     * Mathematical Formula (Principle of Inclusion-Exclusion):
     *     rangeSum(L, R) = prefixSum(R) - prefixSum(L - 1)
     * 
     * Derivation:
     *     sum_{k=L}^{R} trafficCounts[k] = sum_{k=1}^{R} trafficCounts[k] - sum_{k=1}^{L-1} trafficCounts[k]
     * 
     * Mathematical Trace for Benchmark Dataset (n = 8):
     *   1. Baseline Query [3 .. 6] before update:
     *      - prefixSum(6) = bit[6] + bit[4] = 25 + 43 = 68
     *      - prefixSum(2) = bit[2] = 19
     *      - rangeSum(3, 6) = 68 - 19 = 49 vehicles.
     *   2. Re-Query [3 .. 6] after Segment 5 update (20 -> 34, delta = +14):
     *      - prefixSum(6) = bit[6] + bit[4] = 39 + 43 = 82
     *      - prefixSum(2) = bit[2] = 19
     *      - rangeSum(3, 6) = 82 - 19 = 63 vehicles.
     * 
     * Preconditions & Validations (Task 5):
     *   1. Lower Bound: left >= 1 (road segments are 1-based; left < 1 is rejected).
     *   2. Upper Bound: right <= n (corridor length is n; right > n is rejected).
     *   3. Ordered Range: left <= right (inverted ranges left > right are rejected).
     *   - If any condition is violated, logs an error to std::cerr and safely returns -1.
     * 
     * Complexity:
     *   - Time Complexity: O(log n) — performs exactly two prefixSum() calls, each O(log n).
     *   - Space Complexity: O(1) auxiliary space.
     * 
     * @param left 1-based start segment index (L, left >= 1).
     * @param right 1-based end segment index (R, right <= n).
     * @return Cumulative traffic volume as 64-bit integer (long long), or -1 if range is invalid.
     */
    long long rangeSum(int left, int right) const {
        if (left < 1 || right > n || left > right) {
            std::cerr << "[Error] Invalid range query [" << left << ", " << right 
                      << "] for array size " << n << ".\n";
            return -1;
        }
        return prefixSum(right) - prefixSum(left - 1);
    }

    /**
     * Member 3 (Task 2, 3, 4 & 6): Congestion Detection & Threshold Classification (O(1))
     * -----------------------------------------------------------------------------------
     * Evaluates traffic congestion status based on cumulative vehicular volume and threshold.
     * 
     * Classification Logic (Task 3 & 4):
     *   - NORMAL: queried traffic is strictly below configured threshold (currentSum < threshold).
     *   - POTENTIALLY CONGESTED: queried traffic is greater than or equal to threshold (currentSum >= threshold).
     * 
     * Input Validation (Task 6):
     *   - Thresholds must be non-negative (threshold >= 0).
     *   - Traffic volume sum must be non-negative (currentSum >= 0).
     *   - Returns "INVALID" and logs an error to std::cerr if invalid input detected.
     * 
     * Complexity:
     *   - Time Complexity: O(1) comparison.
     *   - Space Complexity: O(1).
     * 
     * @param currentSum Cumulative vehicular volume.
     * @param threshold Configured congestion threshold.
     * @return "NORMAL", "POTENTIALLY CONGESTED", or "INVALID".
     */
    static std::string detectCongestion(long long currentSum, long long threshold) {
        if (threshold < 0) {
            std::cerr << "[Error] Invalid threshold: " << threshold 
                      << " (Threshold must be non-negative).\n";
            return "INVALID";
        }
        if (currentSum < 0) {
            std::cerr << "[Error] Invalid traffic volume sum: " << currentSum 
                      << " (Traffic volume cannot be negative).\n";
            return "INVALID";
        }
        if (currentSum >= threshold) {
            return "POTENTIALLY CONGESTED";
        }
        return "NORMAL";
    }

    /**
     * Member 3 (Task 2, 5 & 6): Corridor Range Congestion Detection (O(log n))
     * ------------------------------------------------------------------------
     * Computes the cumulative vehicular traffic volume across segments [left, right]
     * using the existing rangeSum() operation and classifies congestion against
     * the configured threshold.
     * 
     * Preconditions & Validations:
     *   - Range validated via rangeSum(left, right): 1 <= left <= right <= n.
     *   - Threshold validated: threshold >= 0.
     *   - Returns "INVALID" safely if range query or threshold validation fails.
     * 
     * Complexity:
     *   - Time Complexity: O(log n) tree traversal via rangeSum().
     *   - Space Complexity: O(1) auxiliary space.
     * 
     * @param left 1-based start segment index (L).
     * @param right 1-based end segment index (R).
     * @param threshold Configured congestion threshold.
     * @return "NORMAL", "POTENTIALLY CONGESTED", or "INVALID".
     */
    std::string detectCongestion(int left, int right, long long threshold) const {
        if (threshold < 0) {
            std::cerr << "[Error] Invalid threshold: " << threshold 
                      << " (Threshold must be non-negative).\n";
            return "INVALID";
        }
        long long volume = rangeSum(left, right);
        if (volume < 0) {
            return "INVALID";
        }
        return detectCongestion(volume, threshold);
    }

    // ========================================================================
    // INSPECTION & GETTERS (MEMBER 1 DATA INSPECTION)
    // ========================================================================
    int getSize() const { return n; }
    int getTrafficCount(int idx) const {
        if (idx >= 1 && idx <= n) return trafficCounts[idx];
        return -1;
    }
    const std::vector<int>& getRawTraffic() const { return trafficCounts; }
    const std::vector<long long>& getBitArray() const { return bit; }

    /**
     * Member 1: Returns Fenwick Tree values strictly excluding unused index 0.
     * Expected values for initial dataset: {12, 19, 15, 43, 20, 25, 11, 87}.
     */
    std::vector<long long> getFenwickTreeValues() const {
        if (bit.size() <= 1) return {};
        return std::vector<long long>(bit.begin() + 1, bit.end());
    }
};

// ============================================================================
// Helper Formatting and Verification Functions
// ============================================================================

void printDivider(char ch = '-', int len = 78) {
    std::cout << std::string(len, ch) << "\n";
}

void printSectionHeader(const std::string& title) {
    std::cout << "\n";
    printDivider('=');
    std::cout << "  " << title << "\n";
    printDivider('=');
}

void printArray(const std::string& label, const std::vector<int>& arr) {
    std::cout << std::left << std::setw(20) << label << ": [";
    for (size_t i = 1; i < arr.size(); ++i) {
        std::cout << arr[i] << (i + 1 < arr.size() ? ", " : "");
    }
    std::cout << "]\n";
}

void printBitArray(const std::string& label, const std::vector<long long>& arr) {
    std::cout << std::left << std::setw(20) << label << ": [";
    for (size_t i = 1; i < arr.size(); ++i) {
        std::cout << arr[i] << (i + 1 < arr.size() ? ", " : "");
    }
    std::cout << "]\n";
}

bool verifyBit(const std::vector<long long>& actual, const std::vector<long long>& expected) {
    if (actual.size() != expected.size()) return false;
    // Verify that index 0 is strictly unused (0)
    if (!actual.empty() && actual[0] != 0) return false;
    for (size_t i = 1; i < expected.size(); ++i) {
        if (actual[i] != expected[i]) return false;
    }
    return true;
}

// ============================================================================
// Automated Demonstration
// ============================================================================

int main() {
    std::cout << "\n";
    printDivider('*');
    std::cout << "  FLOWGRID — DYNAMIC TRAFFIC CONGESTION ANALYTICS\n";
    std::cout << "  Data Structures & Algorithms Case Study Evaluation\n";
    std::cout << "  Fenwick Tree (Binary Indexed Tree) Automatic Demonstration\n";
    printDivider('*');

    // ------------------------------------------------------------------------
    // Member 1: Initial Data Setup (Zero-based vector {12, 7, 15, 9, 20, 5, 11, 8})
    // ------------------------------------------------------------------------
    TrafficFenwickTree ft;
    const std::vector<int> initialCounts = {12, 7, 15, 9, 20, 5, 11, 8};
    const std::vector<long long> expectedInitialBit = {0, 12, 19, 15, 43, 20, 25, 11, 87};
    const std::vector<long long> expectedUpdatedBit = {0, 12, 19, 15, 43, 34, 39, 11, 101};

    printSectionHeader("STEP 1: INITIAL DATA SETUP & FENWICK TREE CONSTRUCTION");
    ft.initializeData(initialCounts);
    std::cout << "Initial Traffic Counts (Segments 1 to 8):\n";
    printArray("Segments [1..8]", ft.getRawTraffic());

    ft.buildFenwick();
    std::cout << "\nFenwick Tree constructed successfully in O(n) time.\n";
    printBitArray("Computed BIT Array", ft.getBitArray());
    printBitArray("Expected BIT Array", expectedInitialBit);

    long long totalInitialTraffic = ft.prefixSum(8);
    std::cout << "Total Traffic (Segments 1 to 8): " << totalInitialTraffic 
              << " (Expected: 87) -> " << (totalInitialTraffic == 87 ? "[PASS]" : "[FAIL]") << "\n";

    bool initialBitMatch = verifyBit(ft.getBitArray(), expectedInitialBit);
    std::cout << "Initial BIT Array Verification: " 
              << (initialBitMatch ? "[PASS] Exact Match" : "[FAIL] Mismatch Detected") << "\n";

    // ------------------------------------------------------------------------
    // Baseline Query: Segments 3 to 6
    // ------------------------------------------------------------------------
    printSectionHeader("STEP 2, 3 & 4: RANGE QUERY & CONGESTION DETECTION (BASELINE)");
    int qLeft = 3;
    int qRight = 6;
    long long threshold = 55;

    std::cout << "Corridor Query Range     : Segments [" << qLeft << " .. " << qRight << "]\n";
    std::cout << "Configured Threshold     : " << threshold << " vehicles\n";

    long long sumQ1 = ft.rangeSum(qLeft, qRight);
    std::string statusQ1 = TrafficFenwickTree::detectCongestion(sumQ1, threshold);

    std::cout << "Calculation Detail       : prefixSum(" << qRight << ") - prefixSum(" << qLeft - 1 << ")\n";
    std::cout << "                         : " << ft.prefixSum(qRight) << " - " << ft.prefixSum(qLeft - 1) 
              << " = " << sumQ1 << "\n";
    std::cout << "Query Result             : Traffic Volume = " << sumQ1 << "\n";
    std::cout << "Congestion Status        : " << statusQ1 << "\n";

    bool passQ1 = (sumQ1 == 49 && statusQ1 == "NORMAL");
    std::cout << "Benchmark Check          : " 
              << (passQ1 ? "[PASS] Expected 49 and NORMAL" : "[FAIL] Output deviated") << "\n";
    assert(ft.prefixSum(6) == 68); // Member 2: prefixSum(6) before update must equal 68
    assert(ft.prefixSum(2) == 19); // Member 2: prefixSum(2) before update must equal 19
    assert(sumQ1 == 49);           // Member 3: rangeSum(3, 6) = 68 - 19 = 49
    assert(statusQ1 == "NORMAL");  // Member 3: 49 < 55 -> NORMAL
    assert(ft.detectCongestion(qLeft, qRight, threshold) == "NORMAL"); // Member 3: range congestion detection

    // ------------------------------------------------------------------------
    // Dynamic Point Update: Segment 5 from 20 to 34
    // ------------------------------------------------------------------------
    printSectionHeader("STEP 5: DYNAMIC POINT UPDATE (ACCIDENT / SURGE ON SEGMENT 5)");
    int updateSeg = 5;
    int oldCount = ft.getTrafficCount(updateSeg);
    int newCount = 34;

    std::cout << "Target Segment           : " << updateSeg << "\n";
    std::cout << "Prior Vehicle Count      : " << oldCount << "\n";
    std::cout << "Updated Vehicle Count    : " << newCount << "\n";
    std::cout << "Computed Delta           : " << (newCount - oldCount) << "\n";

    ft.setCount(updateSeg, newCount);

    std::cout << "\nUpdated Traffic Counts Array:\n";
    printArray("Segments [1..8]", ft.getRawTraffic());

    std::cout << "\nUpdated Fenwick Tree BIT Array:\n";
    printBitArray("Computed BIT Array", ft.getBitArray());
    printBitArray("Expected BIT Array", expectedUpdatedBit);

    bool updatedBitMatch = verifyBit(ft.getBitArray(), expectedUpdatedBit);
    std::cout << "Updated BIT Array Verification: " 
              << (updatedBitMatch ? "[PASS] Exact Match" : "[FAIL] Mismatch Detected") << "\n";
    assert(ft.prefixSum(6) == 82); // Member 2: prefixSum(6) after update must equal 82

    // ------------------------------------------------------------------------
    // Re-Query: Segments 3 to 6
    // ------------------------------------------------------------------------
    printSectionHeader("STEP 6 & 7: RE-EVALUATION OF RANGE QUERY [3..6]");
    long long sumQ2 = ft.rangeSum(qLeft, qRight);
    std::string statusQ2 = TrafficFenwickTree::detectCongestion(sumQ2, threshold);

    std::cout << "Calculation Detail       : prefixSum(" << qRight << ") - prefixSum(" << qLeft - 1 << ")\n";
    std::cout << "                         : " << ft.prefixSum(qRight) << " - " << ft.prefixSum(qLeft - 1) 
              << " = " << sumQ2 << "\n";
    std::cout << "Query Result             : Traffic Volume = " << sumQ2 << "\n";
    std::cout << "Congestion Status        : " << statusQ2 << "\n";

    bool passQ2 = (sumQ2 == 63 && statusQ2 == "POTENTIALLY CONGESTED");
    std::cout << "Benchmark Check          : " 
              << (passQ2 ? "[PASS] Expected 63 and POTENTIALLY CONGESTED" : "[FAIL] Output deviated") << "\n";
    assert(ft.prefixSum(6) == 82); // Member 2: prefixSum(6) after update must equal 82
    assert(ft.prefixSum(2) == 19); // Member 2: prefixSum(2) after update must equal 19
    assert(sumQ2 == 63);           // Member 3: rangeSum(3, 6) = 82 - 19 = 63
    assert(statusQ2 == "POTENTIALLY CONGESTED"); // Member 3: 63 >= 55 -> POTENTIALLY CONGESTED
    assert(ft.detectCongestion(qLeft, qRight, threshold) == "POTENTIALLY CONGESTED");

    // ------------------------------------------------------------------------
    // Comprehensive Edge Cases & Safety Validations
    // ------------------------------------------------------------------------
    printSectionHeader("STEP 8: EDGE CASE & SAFETY VALIDATION SUITE");

    // Edge Case 1: Single Segment Range Query [5..5]
    long long singleSegSum = ft.rangeSum(5, 5);
    std::cout << "[Edge Case 1] Single Segment Query [5..5]: " << singleSegSum 
              << " (Expected: " << newCount << ") -> " 
              << (singleSegSum == newCount ? "[PASS]" : "[FAIL]") << "\n";
    assert(singleSegSum == newCount);

    // Edge Case 2: Zero Traffic Count Update
    ft.setCount(1, 0);
    std::cout << "[Edge Case 2] Zero Traffic Update on Segment 1: " 
              << ft.getTrafficCount(1) << " vehicles -> [PASS]\n";
    assert(ft.getTrafficCount(1) == 0);
    // Restore
    ft.setCount(1, 12);
    assert(ft.getTrafficCount(1) == 12);

    // Edge Case 3: Out of bounds index
    std::cout << "[Edge Case 3] Out-of-bounds update index 10:\n";
    bool oobUpdate = ft.setCount(10, 50);
    std::cout << "              Handled Gracefully: " << (!oobUpdate ? "[PASS]" : "[FAIL]") << "\n";
    assert(!oobUpdate);

    // Edge Case 4: Inverted Range (left > right) [6..3]
    std::cout << "[Edge Case 4] Inverted Range Query [6..3]:\n";
    long long invSum = ft.rangeSum(6, 3);
    std::cout << "              Handled Gracefully: " << (invSum == -1 ? "[PASS]" : "[FAIL]") << "\n";
    assert(invSum == -1);

    // Edge Case 5: Negative traffic count rejection
    std::cout << "[Edge Case 5] Negative Traffic Count Rejection (-10):\n";
    bool negCount = ft.setCount(2, -10);
    std::cout << "              Handled Gracefully: " << (!negCount ? "[PASS]" : "[FAIL]") << "\n";
    assert(!negCount);

    // Edge Case 6: Congestion Threshold Equality Check (Sum = 63, Threshold = 63)
    long long exactThreshold = 63;
    std::string eqStatus = TrafficFenwickTree::detectCongestion(63, exactThreshold);
    std::cout << "[Edge Case 6] Threshold Equality (Sum = 63, Threshold = 63): "
              << eqStatus << " (Expected: POTENTIALLY CONGESTED since >= threshold) -> "
              << (eqStatus == "POTENTIALLY CONGESTED" ? "[PASS]" : "[FAIL]") << "\n";
    assert(eqStatus == "POTENTIALLY CONGESTED");

    // Edge Case 7: Full Corridor Range Query [1..8]
    long long fullRangeSum = ft.rangeSum(1, 8);
    std::cout << "[Edge Case 7] Full Corridor Range Query [1..8]: " << fullRangeSum 
              << " (Expected: 101) -> " 
              << (fullRangeSum == 101 ? "[PASS]" : "[FAIL]") << "\n";
    assert(fullRangeSum == 101);

    // Edge Case 8: Invalid Range Query L < 1 [0..3]
    std::cout << "[Edge Case 8] Invalid Range Query L < 1 [0..3]:\n";
    long long lowerOobSum = ft.rangeSum(0, 3);
    std::cout << "              Handled Gracefully: " << (lowerOobSum == -1 ? "[PASS]" : "[FAIL]") << "\n";
    assert(lowerOobSum == -1);

    // Edge Case 9: Invalid Range Query R > n [5..9]
    std::cout << "[Edge Case 9] Invalid Range Query R > n [5..9]:\n";
    long long upperOobSum = ft.rangeSum(5, 9);
    std::cout << "              Handled Gracefully: " << (upperOobSum == -1 ? "[PASS]" : "[FAIL]") << "\n";
    assert(upperOobSum == -1);

    // Edge Case 10: Congestion Below Threshold (Sum = 63, Threshold = 70)
    std::string normalStatus = TrafficFenwickTree::detectCongestion(63, 70);
    std::cout << "[Edge Case 10] Congestion Below Threshold (Sum = 63, Threshold = 70): "
              << normalStatus << " (Expected: NORMAL since < threshold) -> "
              << (normalStatus == "NORMAL" ? "[PASS]" : "[FAIL]") << "\n";
    assert(normalStatus == "NORMAL");

    // Edge Case 11: Negative Threshold Rejection
    std::cout << "[Edge Case 11] Negative Threshold Rejection (Threshold = -5):\n";
    std::string negThreshStatus = TrafficFenwickTree::detectCongestion(63, -5);
    std::cout << "               Handled Gracefully: " << (negThreshStatus == "INVALID" ? "[PASS]" : "[FAIL]") << "\n";
    assert(negThreshStatus == "INVALID");

    // Edge Case 12: Range Congestion Query with Invalid Range [6..3]
    std::cout << "[Edge Case 12] Range Congestion Query with Invalid Range [6..3]:\n";
    std::string invalidRangeCongestion = ft.detectCongestion(6, 3, 55);
    std::cout << "               Handled Gracefully: " << (invalidRangeCongestion == "INVALID" ? "[PASS]" : "[FAIL]") << "\n";
    assert(invalidRangeCongestion == "INVALID");

    // Member 2 Core Operations Invariant Verification
    assert(TrafficFenwickTree::lowbit(1) == 1);
    assert(TrafficFenwickTree::lowbit(2) == 2);
    assert(TrafficFenwickTree::lowbit(3) == 1);
    assert(TrafficFenwickTree::lowbit(4) == 4);
    assert(TrafficFenwickTree::lowbit(5) == 1);
    assert(TrafficFenwickTree::lowbit(6) == 2);
    assert(TrafficFenwickTree::lowbit(7) == 1);
    assert(TrafficFenwickTree::lowbit(8) == 8);
    assert(ft.prefixSum(0) == 0);
    assert(ft.prefixSum(-5) == 0);
    assert(ft.prefixSum(100) == ft.prefixSum(8));

    // Member 3 Range Sum Invariant Verification
    for (int i = 1; i <= 8; ++i) {
        assert(ft.rangeSum(i, i) == ft.getTrafficCount(i));
    }
    for (int k = 1; k <= 8; ++k) {
        assert(ft.rangeSum(1, k) == ft.prefixSum(k));
    }

    printSectionHeader("DEMONSTRATION SUMMARY");
    std::cout << "All benchmark tests, bit states, and edge validations passed successfully.\n";
    std::cout << "Point Update Time Complexity : O(log n)\n";
    std::cout << "Range Query Time Complexity  : O(log n)\n";
    std::cout << "Space Complexity             : O(n)\n";
    printDivider('*');
    std::cout << "\n";

    return 0;
}
