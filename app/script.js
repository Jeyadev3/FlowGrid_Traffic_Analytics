/**
 * ============================================================================
 * FlowGrid — Traffic Intelligence Dashboard Engine
 * 1-Based Fenwick Tree (Binary Indexed Tree) Client-Side Implementation
 * ============================================================================
 */

class FenwickTreeEngine {
  constructor(size = 8) {
    this.n = size;
    // 1-based indexing: index 0 unused
    this.trafficCounts = new Array(this.n + 1).fill(0);
    this.bit = new Array(this.n + 1).fill(0);
    this.segmentNames = [
      "",
      "North Arterial",
      "Metro Bypass",
      "Central Expressway",
      "Harbor Bridge",
      "Tech Corridor",
      "Airport Link",
      "Outer Ring Road",
      "South Boulevard"
    ];
  }

  /**
   * Isolates the lowest set bit (least significant 1-bit).
   * Formula: x & (-x)
   */
  lowbit(x) {
    return x & (-x);
  }

  /**
   * Initializes original traffic counts array.
   */
  initializeData(data) {
    this.n = data.length;
    this.trafficCounts = new Array(this.n + 1).fill(0);
    this.bit = new Array(this.n + 1).fill(0);

    for (let i = 1; i <= this.n; i++) {
      this.trafficCounts[i] = Math.max(0, data[i - 1]);
    }
  }

  /**
   * O(n) construction of the Fenwick Tree.
   */
  buildFenwick() {
    this.bit.fill(0);
    for (let i = 1; i <= this.n; i++) {
      this.bit[i] += this.trafficCounts[i];
      const parent = i + this.lowbit(i);
      if (parent <= this.n) {
        this.bit[parent] += this.bit[i];
      }
    }
  }

  /**
   * Point update by delta: traverses up the tree.
   * Path: i -> i + lowbit(i)
   * Time Complexity: O(log n)
   */
  update(idx, delta) {
    if (idx < 1 || idx > this.n) {
      return { success: false, path: [] };
    }
    const path = [];
    for (let i = idx; i <= this.n; i += this.lowbit(i)) {
      this.bit[i] += delta;
      path.push(i);
    }
    return { success: true, path };
  }

  /**
   * Set absolute traffic count for segment idx.
   * Computes delta = newCount - trafficCounts[idx] and updates.
   */
  setCount(idx, newCount) {
    if (idx < 1 || idx > this.n || newCount < 0) {
      return { success: false, delta: 0, path: [] };
    }
    const oldCount = this.trafficCounts[idx];
    const delta = newCount - oldCount;
    this.trafficCounts[idx] = newCount;
    const res = this.update(idx, delta);
    return { success: res.success, delta, oldCount, newCount, path: res.path };
  }

  /**
   * Computes prefix sum of traffic counts from segment 1 to idx.
   * Path: i -> i - lowbit(i)
   * Time Complexity: O(log n)
   */
  prefixSum(idx) {
    if (idx < 1) return { sum: 0, path: [], terms: [] };
    if (idx > this.n) idx = this.n;

    let sum = 0;
    const path = [];
    const terms = [];

    for (let i = idx; i > 0; i -= this.lowbit(i)) {
      sum += this.bit[i];
      path.push(i);
      terms.push({ index: i, val: this.bit[i] });
    }
    return { sum, path, terms };
  }

  /**
   * Computes range sum of traffic counts for segments [left, right].
   * Formula: prefixSum(right) - prefixSum(left - 1)
   * Time Complexity: O(log n)
   */
  rangeSum(left, right) {
    if (left < 1 || right > this.n || left > right) {
      return { error: true, message: `Invalid range [${left}..${right}]. Must satisfy 1 <= L <= R <= ${this.n}.` };
    }

    const rightRes = this.prefixSum(right);
    const leftRes = this.prefixSum(left - 1);
    const sum = rightRes.sum - leftRes.sum;

    return {
      error: false,
      left,
      right,
      sum,
      rightPrefix: rightRes.sum,
      rightPath: rightRes.path,
      leftPrefix: leftRes.sum,
      leftPath: leftRes.path
    };
  }

  /**
   * Evaluates congestion based on threshold.
   */
  detectCongestion(sum, threshold) {
    return sum > threshold ? "POTENTIALLY CONGESTED" : "NORMAL";
  }
}

// ============================================================================
// UI Controller & Event Management
// ============================================================================

const INITIAL_COUNTS = [12, 7, 15, 9, 20, 5, 11, 8];
let engine = new FenwickTreeEngine(8);

let currentRangeL = 3;
let currentRangeR = 6;
let currentThreshold = 55;
let recentlyUpdatedSeg = null;

// DOM Elements
const kpiTotalTraffic = document.getElementById("kpi-total-traffic");
const kpiCorridorVolume = document.getElementById("kpi-corridor-volume");
const kpiCorridorStatus = document.getElementById("kpi-corridor-status");
const kpiThresholdRef = document.getElementById("kpi-threshold-ref");
const segmentGrid = document.getElementById("segment-grid");
const bitTableBody = document.getElementById("bit-table-body");
const treeHierarchyView = document.getElementById("tree-hierarchy-view");
const activityLog = document.getElementById("activity-log");
const queryBreakdown = document.getElementById("query-breakdown");
const queryStatusBadge = document.getElementById("query-status-badge");

// Form controls
const updateSegmentSelect = document.getElementById("update-segment");
const updateCountInput = document.getElementById("update-count");
const btnApplyUpdate = document.getElementById("btn-apply-update");
const rangeLeftInput = document.getElementById("range-left");
const rangeRightInput = document.getElementById("range-right");
const rangeThresholdInput = document.getElementById("range-threshold");
const btnEvalRange = document.getElementById("btn-eval-range");
const btnReset = document.getElementById("btn-reset");
const btnRunDemo = document.getElementById("btn-run-demo");
const btnClearLog = document.getElementById("btn-clear-log");

// Preset Chips
const chipDemoStep5 = document.getElementById("chip-demo-step5");
const chipDemoSeg3 = document.getElementById("chip-demo-seg3");
const chipClearSeg1 = document.getElementById("chip-clear-seg1");

/**
 * Format timestamp for audit logs
 */
function getTimestamp() {
  const now = new Date();
  return now.toTimeString().split(" ")[0] + "." + String(now.getMilliseconds()).padStart(3, "0");
}

/**
 * Append entry to execution audit log
 */
function logActivity(tag, message, type = "init") {
  const entry = document.createElement("div");
  entry.className = "log-entry";
  entry.innerHTML = `
    <span class="log-time">[${getTimestamp()}]</span>
    <span class="log-tag tag-${type}">${tag}</span>
    <span class="log-msg">${message}</span>
  `;
  activityLog.insertBefore(entry, activityLog.firstChild);
}

/**
 * Render road segment cards
 */
function renderSegments() {
  segmentGrid.innerHTML = "";
  const maxCount = Math.max(...engine.trafficCounts.slice(1), 40);

  for (let i = 1; i <= engine.n; i++) {
    const count = engine.trafficCounts[i];
    const isInQuery = i >= currentRangeL && i <= currentRangeR;
    const isRecentlyUpdated = recentlyUpdatedSeg === i;
    const pct = Math.min(100, Math.round((count / maxCount) * 100));

    const card = document.createElement("div");
    card.className = `segment-card ${isInQuery ? "in-query" : ""} ${isRecentlyUpdated ? "recently-updated" : ""}`;
    card.innerHTML = `
      <div class="seg-header">
        <span class="seg-tag">SEG 0${i}</span>
        <span class="seg-name">${engine.segmentNames[i]}</span>
      </div>
      <div class="seg-count-row">
        <span class="seg-count">${count}</span>
        <span class="seg-unit">veh</span>
      </div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill ${count >= 30 ? "high" : ""}" style="width: ${pct}%"></div>
      </div>
    `;
    segmentGrid.appendChild(card);
  }
}

/**
 * Render Fenwick Tree BIT Table & Hierarchical Breakdown
 */
function renderBitTable(highlightPath = []) {
  bitTableBody.innerHTML = "";

  const intervalLabels = [
    "",
    "[1..1]",
    "[1..2]",
    "[3..3]",
    "[1..4]",
    "[5..5]",
    "[5..6]",
    "[7..7]",
    "[1..8]"
  ];

  const formulas = [
    "",
    "A[1]",
    "A[1] + A[2]",
    "A[3]",
    "A[1] + A[2] + A[3] + A[4]",
    "A[5]",
    "A[5] + A[6]",
    "A[7]",
    "A[1] + ... + A[8]"
  ];

  const roles = [
    "",
    "Leaf (Odd index, len 1)",
    "Sub-root (len 2)",
    "Leaf (Odd index, len 1)",
    "Major Branch Root (len 4)",
    "Leaf (Odd index, len 1)",
    "Sub-root (len 2)",
    "Leaf (Odd index, len 1)",
    "Global Corridor Root (len 8)"
  ];

  for (let i = 1; i <= engine.n; i++) {
    const isHighlighted = highlightPath.includes(i);
    const row = document.createElement("tr");
    if (isHighlighted) row.className = "highlight-node";

    const binStr = i.toString(2).padStart(4, "0");
    const lowbitVal = engine.lowbit(i);
    const lowbitBin = lowbitVal.toString(2).padStart(4, "0");

    row.innerHTML = `
      <td><code>bit[${i}]</code></td>
      <td><code>${binStr}<sub>2</sub></code></td>
      <td><code>${lowbitVal} (${lowbitBin}<sub>2</sub>)</code></td>
      <td><code>${intervalLabels[i]}</code></td>
      <td>${formulas[i]}</td>
      <td><span class="val-badge">${engine.bit[i]}</span></td>
      <td>${roles[i]}</td>
    `;
    bitTableBody.appendChild(row);
  }

  // Hierarchy view
  treeHierarchyView.innerHTML = `
    <div class="hierarchy-level">
      <span class="level-title">Global Root (2^3):</span>
      <div class="node-chip-container">
        <span class="node-chip">Node <strong>bit[8]</strong> = ${engine.bit[8]} (Interval [1..8])</span>
      </div>
    </div>
    <div class="hierarchy-level">
      <span class="level-title">Branch Roots (2^2):</span>
      <div class="node-chip-container">
        <span class="node-chip">Node <strong>bit[4]</strong> = ${engine.bit[4]} (Interval [1..4])</span>
      </div>
    </div>
    <div class="hierarchy-level">
      <span class="level-title">Sub-roots (2^1):</span>
      <div class="node-chip-container">
        <span class="node-chip">Node <strong>bit[2]</strong> = ${engine.bit[2]} (Interval [1..2])</span>
        <span class="node-chip">Node <strong>bit[6]</strong> = ${engine.bit[6]} (Interval [5..6])</span>
      </div>
    </div>
    <div class="hierarchy-level">
      <span class="level-title">Leaves (2^0):</span>
      <div class="node-chip-container">
        <span class="node-chip">bit[1]=${engine.bit[1]}</span>
        <span class="node-chip">bit[3]=${engine.bit[3]}</span>
        <span class="node-chip">bit[5]=${engine.bit[5]}</span>
        <span class="node-chip">bit[7]=${engine.bit[7]}</span>
      </div>
    </div>
  `;
}

/**
 * Re-evaluate range query and update summary cards
 */
function evaluateCorridor(highlightUpdatePath = []) {
  const left = parseInt(rangeLeftInput.value, 10);
  const right = parseInt(rangeRightInput.value, 10);
  const threshold = parseInt(rangeThresholdInput.value, 10);

  currentRangeL = left;
  currentRangeR = right;
  currentThreshold = threshold;

  kpiThresholdRef.textContent = threshold;

  // Validation
  if (isNaN(left) || isNaN(right) || left < 1 || right > engine.n || left > right) {
    logActivity("ERROR", `Invalid Range [${left}..${right}]. Bound conditions violated.`, "error");
    queryBreakdown.innerHTML = `<span style="color:#f87171;">Error: Invalid query range [${left}..${right}]. Please select valid 1 <= L <= R <= 8.</span>`;
    return;
  }

  const queryRes = engine.rangeSum(left, right);
  const status = engine.detectCongestion(queryRes.sum, threshold);
  const isCongested = status === "POTENTIALLY CONGESTED";

  // Total traffic
  const totalNet = engine.prefixSum(engine.n).sum;
  kpiTotalTraffic.textContent = totalNet;
  kpiCorridorVolume.textContent = queryRes.sum;

  // Update Status Pill
  kpiCorridorStatus.className = `status-pill ${isCongested ? "status-congested" : "status-normal"}`;
  kpiCorridorStatus.textContent = status;

  // Breakdown formatting
  const rightPathStr = queryRes.rightPath.map(i => `bit[${i}]`).join(" + ");
  const leftPathStr = queryRes.leftPath.length > 0 ? queryRes.leftPath.map(i => `bit[${i}]`).join(" + ") : "0";

  queryBreakdown.innerHTML = `
    <div class="breakdown-formula">
      <span class="formula-label">Algorithm Execution:</span>
      <code>
        rangeSum(${left}, ${right}) = prefixSum(${right}) [${rightPathStr || "0"}=${queryRes.rightPrefix}] 
        &minus; prefixSum(${left - 1}) [${leftPathStr}=${queryRes.leftPrefix}] 
        = <strong>${queryRes.sum} veh</strong>
      </code>
    </div>
    <div class="breakdown-verdict">
      <span>Verdict:</span>
      <span class="status-pill ${isCongested ? "status-congested" : "status-normal"}">${status} (${queryRes.sum} ${isCongested ? ">" : "&le;"} ${threshold})</span>
    </div>
  `;

  renderSegments();
  renderBitTable(highlightUpdatePath);

  logActivity(
    "QUERY",
    `Evaluated corridor [${left}..${right}]: Volume = ${queryRes.sum} veh, Status = ${status}`,
    isCongested ? "alert" : "query"
  );
}

/**
 * Handle Point Update
 */
function handleUpdate(segment, newCount) {
  if (segment < 1 || segment > engine.n) {
    logActivity("ERROR", `Segment index ${segment} out of bounds (1..${engine.n})`, "error");
    return;
  }
  if (newCount < 0) {
    logActivity("ERROR", `Negative traffic count ${newCount} rejected`, "error");
    return;
  }

  const res = engine.setCount(segment, newCount);
  if (res.success) {
    recentlyUpdatedSeg = segment;
    logActivity(
      "UPDATE",
      `Segment ${segment} (${engine.segmentNames[segment]}) updated: ${res.oldCount} &rarr; ${newCount} (delta: ${res.delta >= 0 ? "+" + res.delta : res.delta}). Ancestor path updated: [${res.path.join(" &rarr; ")}]`,
      "update"
    );
    evaluateCorridor(res.path);
  }
}

/**
 * Reset dashboard to initial benchmark state
 */
function resetBenchmark() {
  engine.initializeData(INITIAL_COUNTS);
  engine.buildFenwick();

  currentRangeL = 3;
  currentRangeR = 6;
  currentThreshold = 55;
  recentlyUpdatedSeg = null;

  rangeLeftInput.value = 3;
  rangeRightInput.value = 6;
  rangeThresholdInput.value = 55;
  updateSegmentSelect.value = "5";
  updateCountInput.value = "34";

  logActivity("INIT", `Dashboard reset to benchmark initial counts [${INITIAL_COUNTS.join(", ")}]`, "init");
  evaluateCorridor();
}

/**
 * Automated Demonstration Runner
 */
async function runDemoSequence() {
  logActivity("DEMO", "Starting automated DSA Case Study benchmark sequence...", "init");
  resetBenchmark();
  await new Promise(r => setTimeout(r, 900));

  logActivity("DEMO", "Step 1: Baseline Query on Corridor [3..6] with Threshold 55", "query");
  rangeLeftInput.value = 3;
  rangeRightInput.value = 6;
  rangeThresholdInput.value = 55;
  evaluateCorridor();

  await new Promise(r => setTimeout(r, 1400));
  logActivity("DEMO", "Step 2: Simulating traffic surge/accident on Segment 5 (20 -> 34 veh)", "update");
  updateSegmentSelect.value = "5";
  updateCountInput.value = "34";
  handleUpdate(5, 34);

  await new Promise(r => setTimeout(r, 1200));
  logActivity("DEMO", "Step 3: Corridor [3..6] re-evaluated -> Congestion threshold exceeded (63 > 55)", "alert");
}

// ============================================================================
// Event Listeners
// ============================================================================

btnApplyUpdate.addEventListener("click", () => {
  const seg = parseInt(updateSegmentSelect.value, 10);
  const count = parseInt(updateCountInput.value, 10);
  handleUpdate(seg, count);
});

btnEvalRange.addEventListener("click", () => {
  evaluateCorridor();
});

btnReset.addEventListener("click", () => {
  resetBenchmark();
});

btnRunDemo.addEventListener("click", () => {
  runDemoSequence();
});

btnClearLog.addEventListener("click", () => {
  activityLog.innerHTML = "";
  logActivity("SYSTEM", "Activity audit log cleared", "init");
});

chipDemoStep5.addEventListener("click", () => {
  updateSegmentSelect.value = "5";
  updateCountInput.value = "34";
  handleUpdate(5, 34);
});

chipDemoSeg3.addEventListener("click", () => {
  updateSegmentSelect.value = "3";
  updateCountInput.value = "30";
  handleUpdate(3, 30);
});

chipClearSeg1.addEventListener("click", () => {
  updateSegmentSelect.value = "1";
  updateCountInput.value = "0";
  handleUpdate(1, 0);
});

// Initialize on page load
window.addEventListener("DOMContentLoaded", () => {
  resetBenchmark();
});
