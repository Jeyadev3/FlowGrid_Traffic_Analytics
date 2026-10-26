#!/usr/bin/env python3
"""
FlowGrid — Dynamic Traffic Analytics Automated Test Suite (Member 4)
Course: Data Structures & Algorithms (2nd Year CSE)

Verifies:
 1. Initial Fenwick Tree construction & O(n) build
 2. Prefix-sum queries across all indices (1..8)
 3. Range-sum queries (baseline, single segment, full corridor)
 4. Point updates & ancestor traversal paths (i += lowbit(i))
 5. Range queries after updates
 6. Congestion classification below, at, and above the threshold (< 55 vs >= 55)
 7. Invalid ranges, indices, and negative traffic counts
 8. Repeated updates ensuring cumulative BIT integrity
 9. Frontend / Backend communication (server.py + C++ binary)
10. The exact benchmark evaluation scenario (49 NORMAL -> 63 POTENTIALLY CONGESTED)
11. Standalone C++ automated demonstration run (argc == 1)
"""

import sys
import os
import json
import io
import subprocess
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
import server

EXE_PATH = server.CPP_EXE

passed_count = 0
failed_count = 0


def record_result(test_name, passed, detail=""):
    global passed_count, failed_count
    if passed:
        passed_count += 1
        print(f"  [PASS] {test_name}" + (f" -> {detail}" if detail else ""))
    else:
        failed_count += 1
        print(f"  [FAIL] {test_name}" + (f" -> {detail}" if detail else ""))


def run_cpp(args):
    cmd = [str(EXE_PATH)] + [str(a) for a in args]
    proc = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return proc.returncode, proc.stdout.strip(), proc.stderr.strip()


def run_tests():
    print("=" * 76)
    print("  FLOWGRID — COMPREHENSIVE AUTOMATED TEST SUITE (MEMBER 4)")
    print("  C++ Fenwick Tree Engine + Python Server Integration")
    print("=" * 76)
    print(f"  Target Binary: {EXE_PATH}\n")

    # -------------------------------------------------------------------------
    # Test 1: Initial Construction
    # -------------------------------------------------------------------------
    print("--- Test Group 1: Initial Fenwick Tree Construction ---")
    ret, out, _ = run_cpp(["--state", 12, 7, 15, 9, 20, 5, 11, 8])
    data = json.loads(out)
    expected_bit = [12, 19, 15, 43, 20, 25, 11, 87]
    bit_matches = (data.get("bit") == expected_bit)
    traffic_matches = (data.get("totalTraffic") == 87)
    record_result("TC-01: BIT Array Matches Expected Forward-Propagated Values", bit_matches, f"BIT: {data.get('bit')}")
    record_result("TC-02: Total Corridor Volume Initial State", traffic_matches, f"Total = {data.get('totalTraffic')} veh")

    # -------------------------------------------------------------------------
    # Test 2: Prefix-sum queries across all indices
    # -------------------------------------------------------------------------
    print("\n--- Test Group 2: Prefix Sum Decomposition ---")
    prefix_expected = [12, 19, 34, 43, 63, 68, 79, 87]
    all_prefix_pass = True
    for i in range(1, 9):
        ret, out, _ = run_cpp(["--query", 1, i, 1000, 12, 7, 15, 9, 20, 5, 11, 8])
        q_data = json.loads(out)
        if q_data.get("sum") != prefix_expected[i - 1]:
            all_prefix_pass = False
    record_result("TC-03: Prefix Sums [1..1] through [1..8]", all_prefix_pass, f"Matches {prefix_expected}")

    # Specific check for prefixSum(6) decomposition: bit[6] + bit[4] = 25 + 43 = 68
    ret, out, _ = run_cpp(["--query", 1, 6, 1000, 12, 7, 15, 9, 20, 5, 11, 8])
    q6 = json.loads(out)
    p6_pass = (q6.get("sum") == 68 and q6.get("rightPath") == [6, 4])
    record_result("TC-04: Prefix Sum 6 Traversal Path", p6_pass, f"rightPath = {q6.get('rightPath')} (sum=68)")

    # -------------------------------------------------------------------------
    # Test 3: Range-sum queries
    # -------------------------------------------------------------------------
    print("\n--- Test Group 3: Range Sum Queries ---")
    ret, out, _ = run_cpp(["--query", 3, 6, 55, 12, 7, 15, 9, 20, 5, 11, 8])
    q_base = json.loads(out)
    record_result("TC-05: Baseline Range Sum [3..6]", q_base.get("sum") == 49, f"Volume = {q_base.get('sum')} veh")
    record_result("TC-06: Single Segment Range Sum [5..5]", json.loads(run_cpp(["--query", 5, 5, 55, 12, 7, 15, 9, 20, 5, 11, 8])[1]).get("sum") == 20)
    record_result("TC-07: Full Corridor Range Sum [1..8]", json.loads(run_cpp(["--query", 1, 8, 100, 12, 7, 15, 9, 20, 5, 11, 8])[1]).get("sum") == 87)

    # -------------------------------------------------------------------------
    # Test 4: Point updates
    # -------------------------------------------------------------------------
    print("\n--- Test Group 4: Point Updates & Traversal Paths ---")
    ret, out, _ = run_cpp(["--update", 5, 34, 12, 7, 15, 9, 20, 5, 11, 8])
    up_data = json.loads(out)
    expected_updated_bit = [12, 19, 15, 43, 34, 39, 11, 101]
    expected_updated_counts = [12, 7, 15, 9, 34, 5, 11, 8]
    record_result("TC-08: Traversal Path for Update(5, +14)", up_data.get("path") == [5, 6, 8], f"Path = {up_data.get('path')}")
    record_result("TC-09: Updated Raw Traffic Array", up_data.get("counts") == expected_updated_counts, f"Counts = {up_data.get('counts')}")
    record_result("TC-10: Updated Fenwick Tree (BIT Array)", up_data.get("bit") == expected_updated_bit, f"BIT = {up_data.get('bit')}")

    # -------------------------------------------------------------------------
    # Test 5: Range queries after updates
    # -------------------------------------------------------------------------
    print("\n--- Test Group 5: Range Queries After Updates ---")
    ret, out, _ = run_cpp(["--query", 3, 6, 55, 12, 7, 15, 9, 34, 5, 11, 8])
    q_post = json.loads(out)
    record_result("TC-11: Re-Query Range [3..6] Post-Update", q_post.get("sum") == 63, f"Volume = {q_post.get('sum')} veh")
    record_result("TC-12: Single Segment [5..5] Post-Update", json.loads(run_cpp(["--query", 5, 5, 55, 12, 7, 15, 9, 34, 5, 11, 8])[1]).get("sum") == 34)

    # -------------------------------------------------------------------------
    # Test 6: Congestion classification below, at, and above the threshold
    # -------------------------------------------------------------------------
    print("\n--- Test Group 6: Congestion Classification (< 55 vs >= 55) ---")
    # Below threshold: Sum = 49, Threshold = 55 -> NORMAL
    s_below = json.loads(run_cpp(["--query", 3, 6, 55, 12, 7, 15, 9, 20, 5, 11, 8])[1]).get("status")
    record_result("TC-13: Below Threshold (Sum 49 < Threshold 55)", s_below == "NORMAL", f"Status = {s_below}")

    # At threshold: Sum = 55, Threshold = 55 -> POTENTIALLY CONGESTED
    # Let's create an exact sum 55 corridor: [1..4] = 12 + 7 + 15 + 9 = 43. With segment 4 = 21 -> sum = 55
    s_at = json.loads(run_cpp(["--query", 1, 4, 55, 12, 7, 15, 21, 20, 5, 11, 8])[1]).get("status")
    record_result("TC-14: At Threshold Boundary (Sum 55 == Threshold 55)", s_at == "POTENTIALLY CONGESTED", f"Status = {s_at}")

    # Below boundary: Sum = 54, Threshold = 55 -> NORMAL
    s_boundary_below = json.loads(run_cpp(["--query", 1, 4, 55, 12, 7, 15, 20, 20, 5, 11, 8])[1]).get("status")
    record_result("TC-15: Just Below Boundary (Sum 54 < Threshold 55)", s_boundary_below == "NORMAL", f"Status = {s_boundary_below}")

    # Above threshold: Sum = 63, Threshold = 55 -> POTENTIALLY CONGESTED
    s_above = json.loads(run_cpp(["--query", 3, 6, 55, 12, 7, 15, 9, 34, 5, 11, 8])[1]).get("status")
    record_result("TC-16: Above Threshold (Sum 63 > Threshold 55)", s_above == "POTENTIALLY CONGESTED", f"Status = {s_above}")

    # -------------------------------------------------------------------------
    # Test 7: Invalid ranges and indices
    # -------------------------------------------------------------------------
    print("\n--- Test Group 7: Boundary & Safety Validations ---")
    ret_inv, out_inv, _ = run_cpp(["--query", 6, 3, 55, 12, 7, 15, 9, 20, 5, 11, 8])
    record_result("TC-17: Inverted Range Query [6..3] Rejected", json.loads(out_inv).get("success") is False)

    ret_oob, out_oob, _ = run_cpp(["--query", 0, 5, 55, 12, 7, 15, 9, 20, 5, 11, 8])
    record_result("TC-18: Out-of-Bounds Range Left [0..5] Rejected", json.loads(out_oob).get("success") is False)

    ret_oob_r, out_oob_r, _ = run_cpp(["--query", 2, 9, 55, 12, 7, 15, 9, 20, 5, 11, 8])
    record_result("TC-19: Out-of-Bounds Range Right [2..9] Rejected", json.loads(out_oob_r).get("success") is False)

    ret_oob_seg, out_oob_seg, _ = run_cpp(["--update", 10, 50, 12, 7, 15, 9, 20, 5, 11, 8])
    record_result("TC-20: Out-of-Bounds Segment Update [Idx 10] Rejected", json.loads(out_oob_seg).get("success") is False)

    ret_neg, out_neg, _ = run_cpp(["--update", 2, -10, 12, 7, 15, 9, 20, 5, 11, 8])
    record_result("TC-21: Negative Traffic Count [-10] Rejected", json.loads(out_neg).get("success") is False)

    # -------------------------------------------------------------------------
    # Test 8: Repeated updates
    # -------------------------------------------------------------------------
    print("\n--- Test Group 8: Repeated Dynamic Updates ---")
    # Start: [12, 7, 15, 9, 20, 5, 11, 8]
    # Update 1: Seg 1 -> 0
    _, out_u1, _ = run_cpp(["--update", 1, 0, 12, 7, 15, 9, 20, 5, 11, 8])
    c1 = json.loads(out_u1)["counts"]
    # Update 2: Seg 8 -> 25
    _, out_u2, _ = run_cpp(["--update", 8, 25] + c1)
    c2 = json.loads(out_u2)["counts"]
    # Update 3: Seg 3 -> 30
    _, out_u3, _ = run_cpp(["--update", 3, 30] + c2)
    c3 = json.loads(out_u3)["counts"]
    # Check total traffic: 0 + 7 + 30 + 9 + 20 + 5 + 11 + 25 = 107
    _, out_st, _ = run_cpp(["--state"] + c3)
    st = json.loads(out_st)
    record_result("TC-22: Cumulative State After 3 Repeated Updates", st.get("totalTraffic") == 107 and c3 == [0, 7, 30, 9, 20, 5, 11, 25], f"Total Traffic = {st.get('totalTraffic')} veh")

    # -------------------------------------------------------------------------
    # Test 9: Frontend / Backend HTTP API communication
    # -------------------------------------------------------------------------
    print("\n--- Test Group 9: Python Server & C++ HTTP Integration ---")

    class MockSocket:
        def __init__(self, request_bytes):
            self.rfile = io.BytesIO(request_bytes)
            self.wfile = io.BytesIO()

        def makefile(self, mode, *args, **kwargs):
            return self.rfile if "r" in mode else self.wfile

        def sendall(self, data):
            self.wfile.write(data)

    class DummyServer:
        pass

    # Reset server state first
    server.current_traffic = list(server.INITIAL_COUNTS)

    # 9a: GET /api/status
    req_status = b"GET /api/status HTTP/1.1\r\nHost: localhost\r\n\r\n"
    s1 = MockSocket(req_status)
    h1 = server.FlowGridRequestHandler(s1, ("127.0.0.1", 1000), DummyServer())
    raw1 = s1.wfile.getvalue().decode()
    json1 = json.loads(raw1.split("\r\n\r\n", 1)[1])
    record_result("TC-23: HTTP GET /api/status Reports C++ Engine Online", json1.get("status") == "online" and json1.get("binary_exists") is True)

    # 9b: GET /api/state
    req_state = b"GET /api/state HTTP/1.1\r\nHost: localhost\r\n\r\n"
    s2 = MockSocket(req_state)
    h2 = server.FlowGridRequestHandler(s2, ("127.0.0.1", 1000), DummyServer())
    raw2 = s2.wfile.getvalue().decode()
    json2 = json.loads(raw2.split("\r\n\r\n", 1)[1])
    record_result("TC-24: HTTP GET /api/state Returns Initial C++ BIT State", json2.get("totalTraffic") == 87)

    # 9c: POST /api/query
    body_q = json.dumps({"left": 3, "right": 6, "threshold": 55}).encode()
    req_q = b"POST /api/query HTTP/1.1\r\nHost: localhost\r\nContent-Length: " + str(len(body_q)).encode() + b"\r\n\r\n" + body_q
    s3 = MockSocket(req_q)
    h3 = server.FlowGridRequestHandler(s3, ("127.0.0.1", 1000), DummyServer())
    raw3 = s3.wfile.getvalue().decode()
    json3 = json.loads(raw3.split("\r\n\r\n", 1)[1])
    record_result("TC-25: HTTP POST /api/query Computes Range [3..6] -> 49 veh, NORMAL", json3.get("sum") == 49 and json3.get("status") == "NORMAL")

    # 9d: POST /api/update
    body_u = json.dumps({"segment": 5, "newCount": 34}).encode()
    req_u = b"POST /api/update HTTP/1.1\r\nHost: localhost\r\nContent-Length: " + str(len(body_u)).encode() + b"\r\n\r\n" + body_u
    s4 = MockSocket(req_u)
    h4 = server.FlowGridRequestHandler(s4, ("127.0.0.1", 1000), DummyServer())
    raw4 = s4.wfile.getvalue().decode()
    json4 = json.loads(raw4.split("\r\n\r\n", 1)[1])
    record_result("TC-26: HTTP POST /api/update Modifies Segment 5 to 34 veh", json4.get("segment") == 5 and json4.get("newCount") == 34 and json4.get("path") == [5, 6, 8])

    # 9e: POST /api/query after update
    s5 = MockSocket(req_q)
    h5 = server.FlowGridRequestHandler(s5, ("127.0.0.1", 1000), DummyServer())
    raw5 = s5.wfile.getvalue().decode()
    json5 = json.loads(raw5.split("\r\n\r\n", 1)[1])
    record_result("TC-27: HTTP POST /api/query Re-Evaluation -> 63 veh, POTENTIALLY CONGESTED", json5.get("sum") == 63 and json5.get("status") == "POTENTIALLY CONGESTED")

    # 9f: POST /api/reset
    req_r = b"POST /api/reset HTTP/1.1\r\nHost: localhost\r\nContent-Length: 0\r\n\r\n"
    s6 = MockSocket(req_r)
    h6 = server.FlowGridRequestHandler(s6, ("127.0.0.1", 1000), DummyServer())
    raw6 = s6.wfile.getvalue().decode()
    json6 = json.loads(raw6.split("\r\n\r\n", 1)[1])
    record_result("TC-28: HTTP POST /api/reset Restores Benchmark State (87 veh)", json6.get("totalTraffic") == 87)

    # -------------------------------------------------------------------------
    # Test 10: Case Study End-to-End Evaluation Scenario
    # -------------------------------------------------------------------------
    print("\n--- Test Group 10: Case Study Exact Demonstration Scenario ---")
    # Step A: Initial query [3..6]
    _, out_s1, _ = run_cpp(["--query", 3, 6, 55, 12, 7, 15, 9, 20, 5, 11, 8])
    d_s1 = json.loads(out_s1)
    scenario_part1 = (d_s1.get("sum") == 49 and d_s1.get("status") == "NORMAL")
    record_result("TC-29: Initial Query [3..6]: Sum = 49, Status = NORMAL", scenario_part1)

    # Step B: Point Update Segment 5: 20 -> 34
    _, out_s2, _ = run_cpp(["--update", 5, 34, 12, 7, 15, 9, 20, 5, 11, 8])
    d_s2 = json.loads(out_s2)
    scenario_part2 = (d_s2.get("counts") == [12, 7, 15, 9, 34, 5, 11, 8] and d_s2.get("delta") == 14)
    record_result("TC-30: Dynamic Update: Segment 5 -> 34 veh, Delta = +14", scenario_part2)

    # Step C: Re-Query [3..6]
    _, out_s3, _ = run_cpp(["--query", 3, 6, 55] + d_s2.get("counts"))
    d_s3 = json.loads(out_s3)
    scenario_part3 = (d_s3.get("sum") == 63 and d_s3.get("status") == "POTENTIALLY CONGESTED")
    record_result("TC-31: Re-Query Corridor [3..6]: Sum = 63, Status = POTENTIALLY CONGESTED", scenario_part3)

    # -------------------------------------------------------------------------
    # Test 11: Standalone Non-Menu-Driven Automated Demonstration
    # -------------------------------------------------------------------------
    print("\n--- Test Group 11: C++ Standalone Automated Demonstration (argc == 1) ---")
    proc_demo = subprocess.run([str(EXE_PATH)], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    demo_out = proc_demo.stdout
    demo_ok = (
        proc_demo.returncode == 0
        and "STEP 1: INITIAL DATA SETUP & FENWICK TREE CONSTRUCTION" in demo_out
        and "STEP 5: DYNAMIC POINT UPDATE" in demo_out
        and "STEP 6 & 7: RE-EVALUATION OF RANGE QUERY [3..6]" in demo_out
        and "[Edge Case 6] Threshold Boundary" in demo_out
        and "All benchmark tests, bit states, and edge validations passed successfully." in demo_out
    )
    record_result("TC-32: Standalone C++ Automated Benchmark Suite Execution", demo_ok, "Preserved 100% of Members 1-3 demo")

    # -------------------------------------------------------------------------
    # Summary
    # -------------------------------------------------------------------------
    print("\n" + "=" * 76)
    print(f"  TEST EXECUTION SUMMARY: {passed_count} PASSED, {failed_count} FAILED")
    print("=" * 76)

    if failed_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    run_tests()
