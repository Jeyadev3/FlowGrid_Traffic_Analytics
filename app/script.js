/**
 * ============================================================================
 * FlowGrid — Traffic Intelligence Dashboard Engine
 * 1-Based Fenwick Tree (Binary Indexed Tree)
 * Frontend Controller with Live C++ Backend Integration (Member 4)
 * ============================================================================
 */

// Road segment designations
const SEGMENT_NAMES = [
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

// Initial Benchmark Vector
const INITIAL_COUNTS = [12, 7, 15, 9, 20, 5, 11, 8];

// Fallback client-side Fenwick Tree engine (used only if backend server is offline)
class ClientFenwickFallback {
  constructor(counts) {
    this.n = counts.length;
    this.trafficCounts = [0, ...counts];
    this.bit = new Array(this.n + 1).fill(0);
    this.build();
  }

  lowbit(x) {
    return x & (-x);
  }

  build() {
    this.bit.fill(0);
    for (let i = 1; i <= this.n; i++) {
      this.bit[i] += this.trafficCounts[i];
      const parent = i + this.lowbit(i);
      if (parent <= this.n) {
        this.bit[parent] += this.bit[i];
      }
    }
  }

  prefixSum(idx) {
    if (idx < 1) return { sum: 0, path: [] };
    if (idx > this.n) idx = this.n;
    let sum = 0;
    const path = [];
    for (let i = idx; i > 0; i -= this.lowbit(i)) {
      sum += this.bit[i];
      path.push(i);
    }
    return { sum, path };
  }

  rangeSum(left, right) {
    const rRes = this.prefixSum(right);
    const lRes = this.prefixSum(left - 1);
    return {
      sum: rRes.sum - lRes.sum,
      rightPrefix: rRes.sum,
      rightPath: rRes.path,
      leftPrefix: lRes.sum,
      leftPath: lRes.path
    };
  }

  setCount(idx, newCount) {
    const oldCount = this.trafficCounts[idx];
    const delta = newCount - oldCount;
    this.trafficCounts[idx] = newCount;
    const path = [];
    for (let i = idx; i <= this.n; i += this.lowbit(i)) {
      this.bit[i] += delta;
      path.push(i);
    }
    return { oldCount, newCount, delta, path };
  }
}

// Application State
let appState = {
  counts: [...INITIAL_COUNTS],
  bit: [12, 19, 15, 43, 20, 25, 11, 87],
  totalTraffic: 87,
  left: 3,
  right: 6,
  threshold: 55,
  querySum: 49,
  queryStatus: "NORMAL",
  rightPrefix: 68,
  rightPath: [6, 4],
  leftPrefix: 19,
  leftPath: [2],
  selectedSegment: 5,
  recentlyUpdatedSeg: null,
  highlightPath: [],
  backendConnected: false,
  fallbackEngine: new ClientFenwickFallback(INITIAL_COUNTS)
};

// DOM References
const engineStatus = document.getElementById("engine-status");
const statusPillWrap = document.getElementById("status-pill-wrap");
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
const validationAlert = document.getElementById("validation-alert");

// Form Inputs
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
 * Isolates lowest set bit (1-bit)
 */
function lowbit(x) {
  return x & (-x);
}

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
 * Show validation alert banner
 */
function showAlert(message) {
  validationAlert.textContent = message;
  validationAlert.classList.remove("hidden");
}

/**
 * Clear validation alert banner
 */
function clearAlert() {
  validationAlert.textContent = "";
  validationAlert.classList.add("hidden");
}

/**
 * Congestion classification rule:
 * Sum < threshold -> NORMAL
 * Sum >= threshold -> POTENTIALLY CONGESTED
 */
function detectCongestion(sum, threshold) {
  return sum >= threshold ? "POTENTIALLY CONGESTED" : "NORMAL";
}

// ============================================================================
// Backend Communication (HTTP API to server.py / C++ Fenwick Tree)
// ============================================================================

async function checkBackend() {
  try {
    const res = await fetch("/api/status");
    if (res.ok) {
      const data = await res.json();
      appState.backendConnected = true;
      statusPillWrap.classList.remove("status-offline");
      engineStatus.textContent = "C++ Fenwick Core: Connected";
      return true;
    }
  } catch (e) {
    // Backend offline
  }
  appState.backendConnected = false;
  statusPillWrap.classList.add("status-offline");
  engineStatus.textContent = "C++ Core Offline (Run: python server.py)";
  return false;
}

async function apiFetchState() {
  if (appState.backendConnected) {
    try {
      const res = await fetch("/api/state");
      if (res.ok) {
        const data = await res.json();
        appState.counts = data.counts;
        appState.bit = data.bit;
        appState.totalTraffic = data.totalTraffic;
        return true;
      }
    } catch (e) {
      logActivity("WARN", "Failed to fetch state from backend; using fallback.", "alert");
    }
  }

  // Fallback
  appState.counts = appState.fallbackEngine.trafficCounts.slice(1);
  appState.bit = appState.fallbackEngine.bit.slice(1);
  appState.totalTraffic = appState.fallbackEngine.prefixSum(8).sum;
  return false;
}

async function apiQueryCorridor(left, right, threshold) {
  clearAlert();
  if (appState.backendConnected) {
    try {
      const res = await fetch("/api/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ left, right, threshold })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        appState.left = data.left;
        appState.right = data.right;
        appState.threshold = data.threshold;
        appState.querySum = data.sum;
        appState.queryStatus = data.status;
        appState.rightPrefix = data.rightPrefix;
        appState.rightPath = data.rightPath;
        appState.leftPrefix = data.leftPrefix;
        appState.leftPath = data.leftPath;
        appState.counts = data.counts;
        appState.bit = data.bit;
        appState.totalTraffic = data.totalTraffic;
        return { success: true, data };
      } else {
        showAlert(data.error || "Query failed");
        return { success: false, error: data.error };
      }
    } catch (e) {
      logActivity("ERROR", "Backend query request failed: " + e.message, "error");
    }
  }

  // Fallback
  const q = appState.fallbackEngine.rangeSum(left, right);
  const status = detectCongestion(q.sum, threshold);
  appState.left = left;
  appState.right = right;
  appState.threshold = threshold;
  appState.querySum = q.sum;
  appState.queryStatus = status;
  appState.rightPrefix = q.rightPrefix;
  appState.rightPath = q.rightPath;
  appState.leftPrefix = q.leftPrefix;
  appState.leftPath = q.leftPath;
  appState.totalTraffic = appState.fallbackEngine.prefixSum(8).sum;
  return { success: true };
}

async function apiUpdateSegment(segment, newCount) {
  clearAlert();
  if (appState.backendConnected) {
    try {
      const res = await fetch("/api/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ segment, newCount })
      });
      const data = await res.json();
      if (res.ok && data.success) {
        appState.counts = data.counts;
        appState.bit = data.bit;
        appState.totalTraffic = data.totalTraffic;
        appState.recentlyUpdatedSeg = segment;
        appState.highlightPath = data.path;
        return { success: true, data };
      } else {
        showAlert(data.error || "Update failed");
        return { success: false, error: data.error };
      }
    } catch (e) {
      logActivity("ERROR", "Backend update request failed: " + e.message, "error");
    }
  }

  // Fallback
  const res = appState.fallbackEngine.setCount(segment, newCount);
  appState.counts = appState.fallbackEngine.trafficCounts.slice(1);
  appState.bit = appState.fallbackEngine.bit.slice(1);
  appState.totalTraffic = appState.fallbackEngine.prefixSum(8).sum;
  appState.recentlyUpdatedSeg = segment;
  appState.highlightPath = res.path;
  return { success: true, data: res };
}

async function apiReset() {
  clearAlert();
  if (appState.backendConnected) {
    try {
      const res = await fetch("/api/reset", { method: "POST" });
      if (res.ok) {
        const data = await res.json();
        appState.counts = data.counts;
        appState.bit = data.bit;
        appState.totalTraffic = data.totalTraffic;
        return true;
      }
    } catch (e) {}
  }
  appState.fallbackEngine = new ClientFenwickFallback(INITIAL_COUNTS);
  appState.counts = [...INITIAL_COUNTS];
  appState.bit = [12, 19, 15, 43, 20, 25, 11, 87];
  appState.totalTraffic = 87;
  return false;
}

// ============================================================================
// UI Rendering
// ============================================================================

/**
 * Render all 8 road segment visual cards
 */
function renderSegments() {
  segmentGrid.innerHTML = "";
  const maxCount = Math.max(...appState.counts, 40);

  for (let i = 1; i <= 8; i++) {
    const count = appState.counts[i - 1];
    const isInQuery = i >= appState.left && i <= appState.right;
    const isRecentlyUpdated = appState.recentlyUpdatedSeg === i;
    const isSelected = appState.selectedSegment === i;
    const pct = Math.min(100, Math.round((count / maxCount) * 100));

    let rangeTag = "";
    if (i === appState.left && i === appState.right) {
      rangeTag = `<span class="seg-badge-range">[L=R=${i}]</span>`;
    } else if (i === appState.left) {
      rangeTag = `<span class="seg-badge-range">[L=${i}]</span>`;
    } else if (i === appState.right) {
      rangeTag = `<span class="seg-badge-range">[R=${i}]</span>`;
    } else if (isInQuery) {
      rangeTag = `<span class="seg-badge-range">In Range</span>`;
    }

    const card = document.createElement("div");
    card.className = `segment-card ${isInQuery ? "in-query" : ""} ${isRecentlyUpdated ? "recently-updated" : ""} ${isSelected ? "selected" : ""}`;
    card.dataset.segment = i;
    card.innerHTML = `
      <div class="seg-header">
        <span class="seg-tag">SEG 0${i}</span>
        ${rangeTag}
      </div>
      <div class="seg-name">${SEGMENT_NAMES[i]}</div>
      <div class="seg-count-row">
        <span class="seg-count">${count}</span>
        <span class="seg-unit">veh</span>
      </div>
      <div class="progress-bar-bg">
        <div class="progress-bar-fill ${count >= 30 ? "high" : ""}" style="width: ${pct}%"></div>
      </div>
    `;

    // Interactive card selection
    card.addEventListener("click", () => {
      selectSegment(i);
    });

    segmentGrid.appendChild(card);
  }
}

/**
 * Select a segment interactively
 */
function selectSegment(segIdx) {
  appState.selectedSegment = segIdx;
  updateSegmentSelect.value = String(segIdx);
  updateCountInput.value = appState.counts[segIdx - 1];
  updateCountInput.focus();
  renderSegments();
  logActivity("SELECT", `Selected Segment 0${segIdx} (${SEGMENT_NAMES[segIdx]}). Current vehicle count = ${appState.counts[segIdx - 1]} veh.`, "init");
}

/**
 * Render Fenwick Tree BIT Table & Hierarchy
 */
function renderBitTable() {
  bitTableBody.innerHTML = "";

  const intervalLabels = ["", "[1..1]", "[1..2]", "[3..3]", "[1..4]", "[5..5]", "[5..6]", "[7..7]", "[1..8]"];
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

  for (let i = 1; i <= 8; i++) {
    const isHighlighted = appState.highlightPath.includes(i);
    const row = document.createElement("tr");
    if (isHighlighted) row.className = "highlight-node";

    const binStr = i.toString(2).padStart(4, "0");
    const lowbitVal = lowbit(i);
    const lowbitBin = lowbitVal.toString(2).padStart(4, "0");
    const val = appState.bit[i - 1];

    row.innerHTML = `
      <td><code>bit[${i}]</code></td>
      <td><code>${binStr}<sub>2</sub></code></td>
      <td><code>${lowbitVal} (${lowbitBin}<sub>2</sub>)</code></td>
      <td><code>${intervalLabels[i]}</code></td>
      <td>${formulas[i]}</td>
      <td><span class="val-badge">${val}</span></td>
      <td>${roles[i]}</td>
    `;
    bitTableBody.appendChild(row);
  }

  // Hierarchy View
  const b = appState.bit;
  treeHierarchyView.innerHTML = `
    <div class="hierarchy-level">
      <span class="level-title">Global Root (2^3):</span>
      <div class="node-chip-container">
        <span class="node-chip ${appState.highlightPath.includes(8) ? "highlight-node" : ""}">
          Node <strong>bit[8]</strong> = ${b[7]} (Interval [1..8])
        </span>
      </div>
    </div>
    <div class="hierarchy-level">
      <span class="level-title">Branch Roots (2^2):</span>
      <div class="node-chip-container">
        <span class="node-chip ${appState.highlightPath.includes(4) ? "highlight-node" : ""}">
          Node <strong>bit[4]</strong> = ${b[3]} (Interval [1..4])
        </span>
      </div>
    </div>
    <div class="hierarchy-level">
      <span class="level-title">Sub-roots (2^1):</span>
      <div class="node-chip-container">
        <span class="node-chip ${appState.highlightPath.includes(2) ? "highlight-node" : ""}">
          Node <strong>bit[2]</strong> = ${b[1]} (Interval [1..2])
        </span>
        <span class="node-chip ${appState.highlightPath.includes(6) ? "highlight-node" : ""}">
          Node <strong>bit[6]</strong> = ${b[5]} (Interval [5..6])
        </span>
      </div>
    </div>
    <div class="hierarchy-level">
      <span class="level-title">Leaves (2^0):</span>
      <div class="node-chip-container">
        <span class="node-chip ${appState.highlightPath.includes(1) ? "highlight-node" : ""}">bit[1]=${b[0]}</span>
        <span class="node-chip ${appState.highlightPath.includes(3) ? "highlight-node" : ""}">bit[3]=${b[2]}</span>
        <span class="node-chip ${appState.highlightPath.includes(5) ? "highlight-node" : ""}">bit[5]=${b[4]}</span>
        <span class="node-chip ${appState.highlightPath.includes(7) ? "highlight-node" : ""}">bit[7]=${b[6]}</span>
      </div>
    </div>
  `;
}

/**
 * Update summary KPI cards and formula breakdown
 */
function renderKPIsAndBreakdown() {
  const isCongested = appState.queryStatus === "POTENTIALLY CONGESTED";

  kpiTotalTraffic.textContent = appState.totalTraffic;
  kpiCorridorVolume.textContent = appState.querySum;
  kpiThresholdRef.textContent = appState.threshold;

  kpiCorridorStatus.className = `status-pill ${isCongested ? "status-congested" : "status-normal"}`;
  kpiCorridorStatus.textContent = appState.queryStatus;

  const rightPathStr = appState.rightPath && appState.rightPath.length > 0
    ? appState.rightPath.map(i => `bit[${i}]`).join(" + ")
    : "0";
  const leftPathStr = appState.leftPath && appState.leftPath.length > 0
    ? appState.leftPath.map(i => `bit[${i}]`).join(" + ")
    : "0";

  const comparisonSym = isCongested ? "&ge;" : "&lt;";

  queryBreakdown.innerHTML = `
    <div class="breakdown-formula">
      <span class="formula-label">C++ Algorithm Execution:</span>
      <code>
        rangeSum(${appState.left}, ${appState.right}) = prefixSum(${appState.right}) [${rightPathStr || "0"}=${appState.rightPrefix}] 
        &minus; prefixSum(${appState.left - 1}) [${leftPathStr}=${appState.leftPrefix}] 
        = <strong>${appState.querySum} veh</strong>
      </code>
    </div>
    <div class="breakdown-verdict">
      <span>Congestion Status:</span>
      <span class="status-pill ${isCongested ? "status-congested" : "status-normal"}">
        ${appState.queryStatus} (${appState.querySum} ${comparisonSym} ${appState.threshold})
      </span>
    </div>
  `;
}

/**
 * Full UI refresh
 */
function refreshUI() {
  renderSegments();
  renderBitTable();
  renderKPIsAndBreakdown();
}

// ============================================================================
// Actions & Handlers
// ============================================================================

async function handleEvaluateRange() {
  const left = parseInt(rangeLeftInput.value, 10);
  const right = parseInt(rangeRightInput.value, 10);
  const threshold = parseInt(rangeThresholdInput.value, 10);

  if (isNaN(left) || isNaN(right) || left < 1 || right > 8 || left > right) {
    showAlert(`Invalid range [${left}..${right}]. Must satisfy 1 <= Start [L] <= End [R] <= 8.`);
    logActivity("ERROR", `Invalid Range [${left}..${right}] rejected.`, "error");
    return;
  }

  if (isNaN(threshold) || threshold < 1) {
    showAlert("Threshold must be a positive integer.");
    return;
  }

  const res = await apiQueryCorridor(left, right, threshold);
  if (res.success) {
    refreshUI();
    const tag = appState.queryStatus === "POTENTIALLY CONGESTED" ? "alert" : "query";
    logActivity(
      "QUERY",
      `Evaluated corridor [${left}..${right}] via C++: Volume = ${appState.querySum} veh, Threshold = ${threshold}. Status = ${appState.queryStatus}.`,
      tag
    );
  }
}

async function handlePointUpdate(segment, newCount) {
  if (isNaN(segment) || segment < 1 || segment > 8) {
    showAlert(`Segment index must be between 1 and 8 (received ${segment}).`);
    logActivity("ERROR", `Segment index ${segment} out of bounds.`, "error");
    return;
  }

  if (isNaN(newCount) || newCount < 0) {
    showAlert("Traffic count must be a non-negative integer.");
    logActivity("ERROR", `Negative traffic count ${newCount} rejected.`, "error");
    return;
  }

  const res = await apiUpdateSegment(segment, newCount);
  if (res.success) {
    // Re-evaluate range after update
    await apiQueryCorridor(appState.left, appState.right, appState.threshold);
    refreshUI();

    const d = res.data;
    const deltaStr = d.delta >= 0 ? `+${d.delta}` : `${d.delta}`;
    const pathStr = d.path ? d.path.map(i => `bit[${i}]`).join(" &rarr; ") : "";

    logActivity(
      "UPDATE",
      `Segment ${segment} (${SEGMENT_NAMES[segment]}) updated: ${d.oldCount} &rarr; ${newCount} (delta: ${deltaStr}). C++ BIT ancestors updated: [${pathStr}].`,
      "update"
    );
  }
}

async function handleReset() {
  await apiReset();
  appState.left = 3;
  appState.right = 6;
  appState.threshold = 55;
  appState.selectedSegment = 5;
  appState.recentlyUpdatedSeg = null;
  appState.highlightPath = [];

  rangeLeftInput.value = 3;
  rangeRightInput.value = 6;
  rangeThresholdInput.value = 55;
  updateSegmentSelect.value = "5";
  updateCountInput.value = String(appState.counts[4]);

  await apiQueryCorridor(3, 6, 55);
  refreshUI();
  logActivity("INIT", `Dashboard reset to benchmark initial counts [${INITIAL_COUNTS.join(", ")}].`, "init");
}

/**
 * Automated Demonstration Runner (Evaluates the exact benchmark case study sequence)
 */
async function runDemoSequence() {
  logActivity("DEMO", "Starting automated DSA Case Study benchmark sequence...", "init");
  await handleReset();
  await new Promise(r => setTimeout(r, 900));

  // Step 1: Baseline query [3..6] with threshold 55
  logActivity("DEMO", "Step 1: Baseline Range Query [3..6] with Threshold 55", "query");
  rangeLeftInput.value = 3;
  rangeRightInput.value = 6;
  rangeThresholdInput.value = 55;
  await handleEvaluateRange();
  await new Promise(r => setTimeout(r, 1400));

  // Step 2: Dynamic Point Update on Segment 5 (20 -> 34)
  logActivity("DEMO", "Step 2: Simulating traffic surge on Segment 5: 20 -> 34 vehicles", "update");
  updateSegmentSelect.value = "5";
  updateCountInput.value = "34";
  selectSegment(5);
  await handlePointUpdate(5, 34);
  await new Promise(r => setTimeout(r, 1200));

  // Step 3: Re-evaluate Corridor [3..6]
  logActivity("DEMO", "Step 3: Corridor [3..6] re-evaluated via C++ -> Exceeds Threshold (63 >= 55: POTENTIALLY CONGESTED)", "alert");
}

// ============================================================================
// Event Listeners
// ============================================================================

btnApplyUpdate.addEventListener("click", () => {
  const seg = parseInt(updateSegmentSelect.value, 10);
  const count = parseInt(updateCountInput.value, 10);
  handlePointUpdate(seg, count);
});

btnEvalRange.addEventListener("click", () => {
  handleEvaluateRange();
});

btnReset.addEventListener("click", () => {
  handleReset();
});

btnRunDemo.addEventListener("click", () => {
  runDemoSequence();
});

btnClearLog.addEventListener("click", () => {
  activityLog.innerHTML = "";
  logActivity("SYSTEM", "Activity audit log cleared.", "init");
});

chipDemoStep5.addEventListener("click", () => {
  selectSegment(5);
  updateCountInput.value = "34";
  handlePointUpdate(5, 34);
});

chipDemoSeg3.addEventListener("click", () => {
  selectSegment(3);
  updateCountInput.value = "30";
  handlePointUpdate(3, 30);
});

chipClearSeg1.addEventListener("click", () => {
  selectSegment(1);
  updateCountInput.value = "0";
  handlePointUpdate(1, 0);
});

updateSegmentSelect.addEventListener("change", (e) => {
  const seg = parseInt(e.target.value, 10);
  selectSegment(seg);
});

// App Initialization
window.addEventListener("DOMContentLoaded", async () => {
  await checkBackend();
  await handleReset();
});
