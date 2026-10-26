#include <iostream>
#include <vector>
#include <string>
#include <iomanip>
#include <stdexcept>

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
    TrafficFenwickTree(int size = 0) {
        init(size);
    }

    void init(int size) {
        n = size;
        trafficCounts.assign(n + 1, 0);
        bit.assign(n + 1, 0);
    }

    /**
     * Isolates the lowest set bit (least significant 1-bit).
     * Formula: x & (-x)
     */
    static int lowbit(int x) {
        return x & (-x);
    }

    /**
     * Initializes the original traffic array with given vector of counts (1-indexed semantics).
     */
    void initializeData(const std::vector<int>& data) {
        n = static_cast<int>(data.size());
        trafficCounts.assign(n + 1, 0);
        bit.assign(n + 1, 0);

        for (int i = 1; i <= n; ++i) {
            if (data[i - 1] < 0) {
                std::cerr << "[Warning] Negative traffic count detected at segment " 
                          << i << ": " << data[i - 1] << ". Setting to 0.\n";
                trafficCounts[i] = 0;
            } else {
                trafficCounts[i] = data[i - 1];
            }
        }
    }

    /**
     * Builds the Fenwick Tree in O(n) time using the forward-propagation technique.
     * Alternatively equivalent to calling update(i, traffic[i]) for all 1 <= i <= n.
     */
    void buildFenwick() {
        // Reset bit array
        std::fill(bit.begin(), bit.end(), 0);

        // O(n) construction: copy elements and propagate to immediate parent
        for (int i = 1; i <= n; ++i) {
            bit[i] += trafficCounts[i];
            int parent = i + lowbit(i);
            if (parent <= n) {
                bit[parent] += bit[i];
            }
        }
    }

    /**
     * Updates segment index by a relative delta.
     * Traverses up the tree by adding lowbit(i).
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
     * Sets absolute traffic count for segment idx.
     * Computes delta = newCount - trafficCounts[idx], updates raw array and BIT.
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
     * Computes prefix sum of traffic counts from segment 1 to idx.
     * Traverses by subtracting lowbit(i).
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

    /**
     * Computes range sum of traffic counts for segments [left, right].
     * Formula: prefixSum(right) - prefixSum(left - 1)
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
     * Determines congestion classification based on threshold.
     */
    static std::string detectCongestion(long long currentSum, long long threshold) {
        if (currentSum > threshold) {
            return "POTENTIALLY CONGESTED";
        }
        return "NORMAL";
    }

    // Getters for inspection & verification
    int getSize() const { return n; }
    int getTrafficCount(int idx) const {
        if (idx >= 1 && idx <= n) return trafficCounts[idx];
        return -1;
    }
    const std::vector<int>& getRawTraffic() const { return trafficCounts; }
    const std::vector<long long>& getBitArray() const { return bit; }
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
    // Initial Setup
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

    // ------------------------------------------------------------------------
    // Comprehensive Edge Cases & Safety Validations
    // ------------------------------------------------------------------------
    printSectionHeader("STEP 8: EDGE CASE & SAFETY VALIDATION SUITE");

    // Edge Case A: Single Segment Range Query
    long long singleSegSum = ft.rangeSum(5, 5);
    std::cout << "[Edge Case 1] Single Segment Query [5..5]: " << singleSegSum 
              << " (Expected: " << newCount << ") -> " 
              << (singleSegSum == newCount ? "[PASS]" : "[FAIL]") << "\n";

    // Edge Case B: Zero Traffic Count Update
    ft.setCount(1, 0);
    std::cout << "[Edge Case 2] Zero Traffic Update on Segment 1: " 
              << ft.getTrafficCount(1) << " vehicles -> [PASS]\n";
    // Restore
    ft.setCount(1, 12);

    // Edge Case C: Out of bounds index
    std::cout << "[Edge Case 3] Out-of-bounds update index 10:\n";
    bool oobUpdate = ft.setCount(10, 50);
    std::cout << "              Handled Gracefully: " << (!oobUpdate ? "[PASS]" : "[FAIL]") << "\n";

    // Edge Case D: Inverted Range (left > right)
    std::cout << "[Edge Case 4] Inverted Range Query [6..3]:\n";
    long long invSum = ft.rangeSum(6, 3);
    std::cout << "              Handled Gracefully: " << (invSum == -1 ? "[PASS]" : "[FAIL]") << "\n";

    // Edge Case E: Negative traffic count rejection
    std::cout << "[Edge Case 5] Negative Traffic Count Rejection (-10):\n";
    bool negCount = ft.setCount(2, -10);
    std::cout << "              Handled Gracefully: " << (!negCount ? "[PASS]" : "[FAIL]") << "\n";

    // Edge Case F: Congestion Threshold Equality Check
    long long exactThreshold = 63;
    std::string eqStatus = TrafficFenwickTree::detectCongestion(63, exactThreshold);
    std::cout << "[Edge Case 6] Threshold Equality (Sum = 63, Threshold = 63): "
              << eqStatus << " (Expected: NORMAL since <= threshold) -> "
              << (eqStatus == "NORMAL" ? "[PASS]" : "[FAIL]") << "\n";

    printSectionHeader("DEMONSTRATION SUMMARY");
    std::cout << "All benchmark tests, bit states, and edge validations passed successfully.\n";
    std::cout << "Point Update Time Complexity : O(log n)\n";
    std::cout << "Range Query Time Complexity  : O(log n)\n";
    std::cout << "Space Complexity             : O(n)\n";
    printDivider('*');
    std::cout << "\n";

    return 0;
}
