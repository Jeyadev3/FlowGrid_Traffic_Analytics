import sys
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)

    # Color definitions
    BG_DARK = RGBColor(15, 23, 42)       # Slate 900
    CARD_BG = RGBColor(30, 41, 59)       # Slate 800
    CARD_BORDER = RGBColor(51, 65, 85)   # Slate 700
    TEXT_LIGHT = RGBColor(248, 250, 252) # Slate 50
    TEXT_MUTED = RGBColor(148, 163, 184) # Slate 400
    ACCENT_BLUE = RGBColor(59, 130, 246) # Blue 500
    ACCENT_CYAN = RGBColor(6, 182, 212)  # Cyan 500
    ACCENT_GREEN = RGBColor(16, 185, 129)# Emerald 500
    ACCENT_CORAL = RGBColor(239, 68, 68) # Red 500

    blank_layout = prs.slide_layouts[6]

    def set_slide_background(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = BG_DARK

    def add_header(slide, title_text, category_text="DSA CASE STUDY EVALUATION"):
        # Category tag
        cat_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.4), Inches(11.7), Inches(0.35))
        tf_cat = cat_box.text_frame
        tf_cat.word_wrap = True
        p_cat = tf_cat.paragraphs[0]
        p_cat.text = category_text.upper()
        p_cat.font.size = Pt(10)
        p_cat.font.bold = True
        p_cat.font.color.rgb = ACCENT_CYAN

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.8), Inches(0.7), Inches(11.7), Inches(0.7))
        tf_title = title_box.text_frame
        tf_title.word_wrap = True
        p_title = tf_title.paragraphs[0]
        p_title.text = title_text
        p_title.font.size = Pt(22)
        p_title.font.bold = True
        p_title.font.color.rgb = TEXT_LIGHT

    def add_card(slide, left, top, width, height, title="", border_color=CARD_BORDER):
        shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        shape.fill.solid()
        shape.fill.fore_color.rgb = CARD_BG
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)

        if title:
            tb = slide.shapes.add_textbox(left + Inches(0.2), top + Inches(0.15), width - Inches(0.4), Inches(0.45))
            tf = tb.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = ACCENT_BLUE

        return shape

    # =========================================================================
    # SLIDE 1: TITLE SLIDE
    # =========================================================================
    s1 = prs.slides.add_slide(blank_layout)
    set_slide_background(s1)

    tbox = s1.shapes.add_textbox(Inches(1.0), Inches(1.4), Inches(11.3), Inches(3.0))
    tf1 = tbox.text_frame
    tf1.word_wrap = True

    p0 = tf1.paragraphs[0]
    p0.text = "DATA STRUCTURES & ALGORITHMS CASE STUDY"
    p0.font.size = Pt(13)
    p0.font.bold = True
    p0.font.color.rgb = ACCENT_CYAN

    p1 = tf1.add_paragraph()
    p1.text = "Dynamic Traffic Congestion Analytics\nUsing Fenwick Tree (Binary Indexed Tree)"
    p1.font.size = Pt(32)
    p1.font.bold = True
    p1.font.color.rgb = TEXT_LIGHT

    p2 = tf1.add_paragraph()
    p2.text = "High-Performance Sub-Corridor Range Aggregation & Point Inflow Tracking"
    p2.font.size = Pt(16)
    p2.font.color.rgb = TEXT_MUTED

    # Team Placeholder Card
    card_team = add_card(s1, Inches(1.0), Inches(4.5), Inches(11.3), Inches(2.2), "PROJECT & EVALUATION METADATA")
    tbox_team = s1.shapes.add_textbox(Inches(1.2), Inches(5.1), Inches(10.9), Inches(1.4))
    tf_team = tbox_team.text_frame
    tf_team.word_wrap = True

    p_t1 = tf_team.paragraphs[0]
    p_t1.text = "Student Team: [Student Name(s) / Team Member Placeholders]"
    p_t1.font.size = Pt(13)
    p_t1.font.color.rgb = TEXT_LIGHT
    
    p_t2 = tf_team.add_paragraph()
    p_t2.text = "Academic Profile: 2nd Year B.Tech Computer Science & Engineering | Semester Evaluation"
    p_t2.font.size = Pt(12)
    p_t2.font.color.rgb = TEXT_MUTED

    p_t3 = tf_team.add_paragraph()
    p_t3.text = "Evaluation Faculty: [Faculty / Evaluator Name Placeholder] | Dept. of CSE"
    p_t3.font.size = Pt(12)
    p_t3.font.color.rgb = TEXT_MUTED

    p_t4 = tf_team.add_paragraph()
    p_t4.text = "System Implementation: FlowGrid Traffic Intelligence (C++ Core Engine & Modern Web Dashboard)"
    p_t4.font.size = Pt(12)
    p_t4.font.bold = True
    p_t4.font.color.rgb = ACCENT_GREEN

    # =========================================================================
    # SLIDE 2: PROBLEM STATEMENT
    # =========================================================================
    s2 = prs.slides.add_slide(blank_layout)
    set_slide_background(s2)
    add_header(s2, "Problem Statement: Dynamic Urban Traffic Monitoring")

    add_card(s2, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "The Urban Congestion Challenge")
    tb = s2.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf = tb.text_frame
    tf.word_wrap = True
    points = [
        "Metropolitan road corridors experience high volatility in vehicle density across adjoining segments.",
        "Sensors, toll plazas, and inductive loops continuously emit real-time vehicle flow counts.",
        "Traffic management authorities must constantly monitor aggregate congestion over flexible sub-corridors [L..R].",
        "Threshold violations require immediate detection to trigger adaptive signal timing and diversion warnings."
    ]
    for pt in points:
        p = tf.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(12)

    add_card(s2, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Algorithmic Inefficiency Bottlenecks")
    tb2 = s2.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf2 = tb2.text_frame
    tf2.word_wrap = True
    points2 = [
        "Naive Array Approach: Point updates take O(1), but range queries require O(n) linear scans. Overwhelmed under thousands of queries.",
        "Static Prefix Sum Array: Range queries take O(1), but every single update cascades across the remaining array taking O(n). Inefficient for live streams.",
        "The Dilemma: Real-time intelligent transportation requires a balanced data structure that handles both dynamic updates and range queries sub-linearly.",
        "Critical Requirement: Standardized 1-based indexing with rigorous boundary safety."
    ]
    for pt in points2:
        p = tf2.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_MUTED
        p.space_after = Pt(12)

    # =========================================================================
    # SLIDE 3: OBJECTIVES
    # =========================================================================
    s3 = prs.slides.add_slide(blank_layout)
    set_slide_background(s3)
    add_header(s3, "Project Objectives & Scope")

    cards_obj = [
        ("1. Core DSA Implementation", "Design and verify a one-based Fenwick Tree (BIT) in standard C++ with zero menu-driven dependency, executing automated demonstration benchmarks.", Inches(0.8), Inches(1.6)),
        ("2. Dual-Array Architecture", "Maintain clean architectural separation between raw traffic counts array (trafficCounts[1..n]) and the cumulative BIT array (bit[1..n]).", Inches(6.8), Inches(1.6)),
        ("3. Dynamic Point Updates", "Implement O(log n) point update and setCount operations to dynamically handle traffic surges, bottlenecks, and sensor updates.", Inches(0.8), Inches(4.3)),
        ("4. Real-Time Thresholding", "Provide O(log n) range sum aggregation (rangeSum(L, R)) to classify corridor status as NORMAL or POTENTIALLY CONGESTED against threshold limits.", Inches(6.8), Inches(4.3))
    ]
    for title, desc, left, top in cards_obj:
        add_card(s3, left, top, Inches(5.7), Inches(2.4), title)
        tb_o = s3.shapes.add_textbox(left + Inches(0.2), top + Inches(0.65), Inches(5.3), Inches(1.6))
        tf_o = tb_o.text_frame
        tf_o.word_wrap = True
        p_o = tf_o.paragraphs[0]
        p_o.text = desc
        p_o.font.size = Pt(13)
        p_o.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 4: PROPOSED SOLUTION
    # =========================================================================
    s4 = prs.slides.add_slide(blank_layout)
    set_slide_background(s4)
    add_header(s4, "Proposed Solution: FlowGrid Architecture")

    add_card(s4, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2), "System Pipeline & Operational Workflow")
    tb_s4 = s4.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(11.1), Inches(4.2))
    tf_s4 = tb_s4.text_frame
    tf_s4.word_wrap = True

    steps = [
        ("Layer 1: Sensor Inflow Array", "Original vehicle counts stored in an independent vector trafficCounts[1..n]. Non-negative validation enforced."),
        ("Layer 2: Fenwick Tree (BIT) Engine", "Constructed in O(n) time. Implements bit[i] storing prefix intervals determined by the lowbit(i) = i & (-i) bitwise operator."),
        ("Layer 3: Analytical Query Layer", "Corridor range query [L..R] computed in O(log n) time by evaluating prefixSum(R) - prefixSum(L - 1)."),
        ("Layer 4: Congestion Classifier", "Compares aggregate vehicle volume against dynamic threshold. Emits NORMAL (<= threshold) or POTENTIALLY CONGESTED (> threshold)."),
        ("Layer 5: Presentation & Dashboard", "Standard automated C++ console benchmark paired with a client-side visual dashboard (FlowGrid) for intuitive demonstration.")
    ]
    for name, detail in steps:
        p_name = tf_s4.add_paragraph()
        p_name.text = name + " — " + detail
        p_name.font.size = Pt(13)
        p_name.font.color.rgb = TEXT_LIGHT
        p_name.space_after = Pt(10)

    # =========================================================================
    # SLIDE 5: WHY FENWICK TREE
    # =========================================================================
    s5 = prs.slides.add_slide(blank_layout)
    set_slide_background(s5)
    add_header(s5, "Why Fenwick Tree? Comparative Data Structure Analysis")

    # Comparison Table
    rows, cols = 5, 5
    left = Inches(0.8)
    top = Inches(1.6)
    width = Inches(11.7)
    height = Inches(4.0)

    table_shape = s5.shapes.add_table(rows, cols, left, top, width, height)
    table = table_shape.table

    headers = ["Data Structure", "Point Update", "Prefix Sum", "Range Sum [L..R]", "Auxiliary Space"]
    data = [
        ["Naive Array", "O(1)", "O(n)", "O(n)", "O(1)"],
        ["Prefix Sum Array", "O(n)", "O(1)", "O(1)", "O(n)"],
        ["Segment Tree", "O(log n)", "O(log n)", "O(log n)", "O(4n) (High Overhead)"],
        ["Fenwick Tree (BIT)", "O(log n)", "O(log n)", "O(log n)", "O(n) (Minimal & Cache-Friendly)"]
    ]

    for c, h in enumerate(headers):
        cell = table.cell(0, c)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = CARD_BG
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = ACCENT_CYAN

    for r, row in enumerate(data):
        for c, val in enumerate(row):
            cell = table.cell(r + 1, c)
            cell.text = val
            cell.fill.solid()
            cell.fill.fore_color.rgb = CARD_BG if r < 3 else RGBColor(30, 58, 138)
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(12)
                p.font.bold = (r == 3)
                p.font.color.rgb = ACCENT_GREEN if (r == 3 and c > 0) else TEXT_LIGHT

    # Bottom summary box
    add_card(s5, Inches(0.8), Inches(5.9), Inches(11.7), Inches(1.1), "")
    tb_w = s5.shapes.add_textbox(Inches(1.0), Inches(6.0), Inches(11.3), Inches(0.9))
    tf_w = tb_w.text_frame
    p_w = tf_w.paragraphs[0]
    p_w.text = "Key Takeaway: The Fenwick Tree achieves the optimal Pareto frontier for real-time traffic systems — balancing O(log n) update and query speeds with strictly O(n) space and zero tree-pointer overhead."
    p_w.font.size = Pt(12)
    p_w.font.color.rgb = TEXT_LIGHT

    # =========================================================================
    # SLIDE 6: TREE REPRESENTATION
    # =========================================================================
    s6 = prs.slides.add_slide(blank_layout)
    set_slide_background(s6)
    add_header(s6, "Fenwick Tree Representation & The lowbit() Concept")

    add_card(s6, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "The lowbit(x) Primitive")
    tb_l = s6.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True

    pts_l = [
        "Mathematical Formula: lowbit(x) = x & (-x)",
        "Two's Complement Property: -x = (~x) + 1. Inverting bits and adding 1 isolates the least significant 1-bit.",
        "Interval of Responsibility: Index i stores the sum of elements in the range [i - lowbit(i) + 1 .. i].",
        "Length of Covered Range: Exactly lowbit(i) elements.",
        "Even vs Odd Indices: Odd indices have lowbit(i) = 1 (leaves storing single elements). Powers of 2 cover all preceding segments [1..i]."
    ]
    for pt in pts_l:
        p = tf_l.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    add_card(s6, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "1-Based Indexing Mapping (n = 8)")
    tb_m = s6.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf_m = tb_m.text_frame
    tf_m.word_wrap = True

    mappings = [
        "bit[1] : 0001_2 | lowbit=1 | Interval [1..1] | Covers Seg 1",
        "bit[2] : 0010_2 | lowbit=2 | Interval [1..2] | Covers Segs 1..2",
        "bit[3] : 0011_2 | lowbit=1 | Interval [3..3] | Covers Seg 3",
        "bit[4] : 0100_2 | lowbit=4 | Interval [1..4] | Covers Segs 1..4",
        "bit[5] : 0101_2 | lowbit=1 | Interval [5..5] | Covers Seg 5",
        "bit[6] : 0110_2 | lowbit=2 | Interval [5..6] | Covers Segs 5..6",
        "bit[7] : 0111_2 | lowbit=1 | Interval [7..7] | Covers Seg 7",
        "bit[8] : 1000_2 | lowbit=8 | Interval [1..8] | Covers Segs 1..8"
    ]
    for mp in mappings:
        p = tf_m.add_paragraph()
        p.text = mp
        p.font.size = Pt(11)
        p.font.color.rgb = ACCENT_CYAN
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 7: UPDATE OPERATION
    # =========================================================================
    s7 = prs.slides.add_slide(blank_layout)
    set_slide_background(s7)
    add_header(s7, "Dynamic Point Update Operation: O(log n)")

    add_card(s7, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Algorithm: update(idx, delta)")
    tb_u = s7.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf_u = tb_u.text_frame
    tf_u.word_wrap = True

    pts_u = [
        "Goal: Add delta to segment idx and propagate the change to all responsible BIT intervals.",
        "Loop Mechanism: Start at i = idx; while i <= n, add delta to bit[i] and advance to parent: i += lowbit(i).",
        "Tree Ascent: Adding lowbit(i) flips the lowest set bit and carries upward, visiting strictly the ancestor nodes in the implicit tree.",
        "Time Complexity: At most log2(n) iterations -> O(log n).",
        "setCount(idx, newCount): Computes delta = newCount - trafficCounts[idx], updates the raw array, then invokes update(idx, delta)."
    ]
    for pt in pts_u:
        p = tf_u.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    add_card(s7, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Trace: Updating Segment 5 by delta = +14")
    tb_tr = s7.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf_tr = tb_tr.text_frame
    tf_tr.word_wrap = True

    traces = [
        "1. Start at i = 5 (0101_2):",
        "   lowbit(5) = 1. Add +14 to bit[5] (20 -> 34).",
        "   Next index: 5 + 1 = 6.",
        "2. Step to i = 6 (0110_2):",
        "   lowbit(6) = 2. Add +14 to bit[6] (25 -> 39).",
        "   Next index: 6 + 2 = 8.",
        "3. Step to i = 8 (1000_2):",
        "   lowbit(8) = 8. Add +14 to bit[8] (87 -> 101).",
        "   Next index: 8 + 8 = 16 > 8 (Termination).",
        "Total Node Updates: Only 3 nodes touched (5, 6, 8) out of 8!"
    ]
    for tr in traces:
        p = tf_tr.add_paragraph()
        p.text = tr
        p.font.size = Pt(11)
        p.font.color.rgb = ACCENT_GREEN if "Total" in tr else TEXT_LIGHT
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 8: PREFIX SUM & RANGE SUM
    # =========================================================================
    s8 = prs.slides.add_slide(blank_layout)
    set_slide_background(s8)
    add_header(s8, "Prefix Sum & Range Sum Aggregation: O(log n)")

    add_card(s8, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Prefix Sum: prefixSum(idx)")
    tb_ps = s8.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf_ps = tb_ps.text_frame
    tf_ps.word_wrap = True

    pts_ps = [
        "Goal: Compute total traffic from segment 1 to idx: sum(traffic[1..idx]).",
        "Loop Mechanism: Start at i = idx; while i > 0, accumulate bit[i] into sum, and step to left disjoint interval: i -= lowbit(i).",
        "Binary Decomposition: Each step strips the lowest set bit from i, decomposing the prefix into at most log2(n) pre-calculated canonical sub-intervals.",
        "Time Complexity: O(log n) addition operations."
    ]
    for pt in pts_ps:
        p = tf_ps.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    add_card(s8, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Corridor Range Sum: rangeSum(L, R)")
    tb_rs = s8.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf_rs = tb_rs.text_frame
    tf_rs.word_wrap = True

    pts_rs = [
        "Fundamental Principle: Range sum equals difference between two prefix sums:",
        "rangeSum(L, R) = prefixSum(R) - prefixSum(L - 1)",
        "Example on Corridor [3..6]:",
        "  prefixSum(6) = bit[6] + bit[4] = 25 + 43 = 68",
        "  prefixSum(2) = bit[2] = 19",
        "  rangeSum(3, 6) = 68 - 19 = 49 vehicles.",
        "Safety Validation:",
        "  Verify: 1 <= L <= R <= n; returns error code (-1) if bounds or ordering violated."
    ]
    for pt in pts_rs:
        p = tf_rs.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = ACCENT_CYAN if "rangeSum(" in pt else TEXT_LIGHT
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 9: WORKED EXAMPLE
    # =========================================================================
    s9 = prs.slides.add_slide(blank_layout)
    set_slide_background(s9)
    add_header(s9, "Worked Example: Step-by-Step Numerical Verification")

    add_card(s9, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Phase 1: Initial State & Query 1")
    tb_w1 = s9.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf_w1 = tb_w1.text_frame
    tf_w1.word_wrap = True

    w1_lines = [
        "Initial Counts: [12, 7, 15, 9, 20, 5, 11, 8]",
        "Constructed BIT Array (1 to 8):",
        "  [12, 19, 15, 43, 20, 25, 11, 87]",
        "Total Network Traffic: prefixSum(8) = 87 [VERIFIED]",
        "Corridor Query [3..6] (Threshold = 55):",
        "  prefixSum(6) = bit[6] + bit[4] = 25 + 43 = 68",
        "  prefixSum(2) = bit[2] = 19",
        "  Volume = 68 - 19 = 49 vehicles.",
        "Classification: 49 <= 55 -> NORMAL [VERIFIED]"
    ]
    for ln in w1_lines:
        p = tf_w1.add_paragraph()
        p.text = ln
        p.font.size = Pt(11)
        p.font.color.rgb = ACCENT_GREEN if "VERIFIED" in ln else TEXT_LIGHT
        p.space_after = Pt(4)

    add_card(s9, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Phase 2: Surge Update & Query 2")
    tb_w2 = s9.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf_w2 = tb_w2.text_frame
    tf_w2.word_wrap = True

    w2_lines = [
        "Point Update: Segment 5 updated from 20 to 34",
        "Delta = 34 - 20 = +14",
        "Propagated Indices: bit[5], bit[6], bit[8]",
        "Updated BIT Array (1 to 8):",
        "  [12, 19, 15, 43, 34, 39, 11, 101]",
        "Corridor Re-Query [3..6] (Threshold = 55):",
        "  prefixSum(6) = bit[6] + bit[4] = 39 + 43 = 82",
        "  prefixSum(2) = bit[2] = 19",
        "  Volume = 82 - 19 = 63 vehicles.",
        "Classification: 63 > 55 -> POTENTIALLY CONGESTED [VERIFIED]"
    ]
    for ln in w2_lines:
        p = tf_w2.add_paragraph()
        p.text = ln
        p.font.size = Pt(11)
        p.font.color.rgb = ACCENT_CORAL if "CONGESTED" in ln else TEXT_LIGHT
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 10: WEB DASHBOARD (FLOWGRID)
    # =========================================================================
    s10 = prs.slides.add_slide(blank_layout)
    set_slide_background(s10)
    add_header(s10, "FlowGrid — Modern Traffic Intelligence Dashboard")

    add_card(s10, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2), "Interactive Client-Side Web Application Architecture")
    tb_db = s10.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(11.1), Inches(4.2))
    tf_db = tb_db.text_frame
    tf_db.word_wrap = True

    db_features = [
        ("Zero Backend Dependency", "Engineered with standard HTML5, modern CSS3, and vanilla ES6 JavaScript. Runs instantly in any standard web browser."),
        ("Dynamic KPI Summary Cards", "Live metrics displaying total network volume (prefixSum(8)), active corridor density, and dynamic threshold state."),
        ("Interactive Segment Cards", "Visual road cards for Segments 1 to 8 showing current traffic volume, corridor naming, and vehicle density progress meters."),
        ("Real-Time Fenwick Tree Inspector", "Comprehensive table detailing 1-based index, binary representation, lowbit(i), covered intervals, formulas, and stored values."),
        ("Traversed Node Highlighting", "Visual highlights indicating exactly which BIT tree ancestors are updated during point updates or prefix queries."),
        ("Audited Execution Log", "Chronological audit trail recording all initialization, update, range query, and threshold classification operations.")
    ]
    for title, desc in db_features:
        p = tf_db.add_paragraph()
        p.text = "• " + title + ": " + desc
        p.font.size = Pt(13)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 11: COMPLEXITY ANALYSIS
    # =========================================================================
    s11 = prs.slides.add_slide(blank_layout)
    set_slide_background(s11)
    add_header(s11, "Algorithmic Complexity & Theoretical Proofs")

    add_card(s11, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Time & Space Bounds")
    tb_c1 = s11.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf_c1 = tb_c1.text_frame
    tf_c1.word_wrap = True

    pts_c1 = [
        "Point Update (update / setCount): O(log n)",
        "  - Maximum number of set bits in integer n is floor(log2(n)) + 1.",
        "  - Each step adds lowbit(i), strictly moving to higher powers of 2.",
        "Prefix Sum Query (prefixSum): O(log n)",
        "  - Each step strips the lowest set bit from index i via i -= lowbit(i).",
        "  - Maximum loop iterations <= log2(n).",
        "Range Sum Query (rangeSum): O(log n)",
        "  - Evaluates two prefix sums: 2 * O(log n) = O(log n).",
        "Fenwick Tree Construction: O(n)",
        "  - Linear forward-propagation builds tree in O(n) without n * log n overhead.",
        "Space Complexity: O(n) contiguous array storage."
    ]
    for pt in pts_c1:
        p = tf_c1.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(6)

    add_card(s11, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Practical Hardware & Cache Benefits")
    tb_c2 = s11.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf_c2 = tb_c2.text_frame
    tf_c2.word_wrap = True

    pts_c2 = [
        "Contiguous Memory Locality:",
        "  Unlike pointer-based Segment Trees or AVL trees that incur frequent CPU cache misses, Fenwick Trees live inside a single flat array.",
        "Bitwise Hardware Acceleration:",
        "  The core index transitions i += (i & -i) compile to single-cycle assembly instructions (BLSI, AND, NEG), making it exceptionally fast on modern CPUs.",
        "Minimal Memory Footprint:",
        "  Requires only (n + 1) integer slots compared to 4n for Segment Trees.",
        "Ideal for Embedded Traffic Controllers:",
        "  Low memory requirements allow deployment on roadside IoT microcontrollers."
    ]
    for pt in pts_c2:
        p = tf_c2.add_paragraph()
        p.text = pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED if ":" in pt else TEXT_LIGHT
        p.space_after = Pt(6)

    # =========================================================================
    # SLIDE 12: TESTING & VALIDATION
    # =========================================================================
    s12 = prs.slides.add_slide(blank_layout)
    set_slide_background(s12)
    add_header(s12, "Empirical Testing & Rigorous Verification")

    add_card(s12, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2), "Test Matrix & Actual Execution Results")
    tb_t = s12.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(11.1), Inches(4.2))
    tf_t = tb_t.text_frame
    tf_t.word_wrap = True

    tests = [
        ("Test Case 1 (O(n) Build & Initial BIT)", "Initial traffic array [12, 7, 15, 9, 20, 5, 11, 8] -> BIT: [12, 19, 15, 43, 20, 25, 11, 87]. Prefix total = 87.", "PASSED [100% Match]"),
        ("Test Case 2 (Baseline Range Query [3..6])", "Query sum returned exactly 49. Evaluated against threshold 55 -> Classified as NORMAL.", "PASSED [100% Match]"),
        ("Test Case 3 (Dynamic Point Update Seg 5)", "Segment 5 updated from 20 to 34 (delta +14). BIT: [12, 19, 15, 43, 34, 39, 11, 101].", "PASSED [100% Match]"),
        ("Test Case 4 (Congestion Re-Query [3..6])", "Corridor volume evaluated to 63 (> 55) -> Classified as POTENTIALLY CONGESTED.", "PASSED [100% Match]"),
        ("Test Case 5 (Edge Case: Single Segment)", "rangeSum(5, 5) evaluated to 34, matching updated point count exactly.", "PASSED [100% Match]"),
        ("Test Case 6 (Zero Traffic & Inverted Bounds)", "setCount(1, 0) updated successfully. Inverted range [6..3] and out-of-bounds indices rejected gracefully.", "PASSED [100% Match]"),
        ("Test Case 7 (Threshold Boundary Equality)", "When volume equals threshold (63 == 63), classified as NORMAL (condition: volume > threshold).", "PASSED [100% Match]")
    ]
    for tc, desc, status in tests:
        p = tf_t.add_paragraph()
        p.text = "• " + tc + ": " + desc + " -> " + status
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(4)

    # =========================================================================
    # SLIDE 13: LIMITATIONS & FUTURE IMPROVEMENTS
    # =========================================================================
    s13 = prs.slides.add_slide(blank_layout)
    set_slide_background(s13)
    add_header(s13, "Limitations & Future Roadmap")

    add_card(s13, Inches(0.8), Inches(1.6), Inches(5.6), Inches(5.2), "Current System Limitations")
    tb_lim = s13.shapes.add_textbox(Inches(1.0), Inches(2.2), Inches(5.2), Inches(4.4))
    tf_lim = tb_lim.text_frame
    tf_lim.word_wrap = True

    pts_lim = [
        "Linear Grid Topology: Current 1D Fenwick Tree assumes linear sequential road corridors. Real-world metropolitan networks feature complex graph topologies and intersections.",
        "Static Segment Count: Fixed n array size. Inserting or deleting road segments dynamically requires array reallocation.",
        "Single-Dimension Metric: Monitors aggregate vehicle count only, without factoring speed, vehicle classification (trucks vs cars), or weather conditions.",
        "Point Update / Range Query Asymmetry: While point updates are fast, range updates (adding delta to an entire range) require dual-tree difference encoding."
    ]
    for pt in pts_lim:
        p = tf_lim.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_LIGHT
        p.space_after = Pt(8)

    add_card(s13, Inches(6.8), Inches(1.6), Inches(5.7), Inches(5.2), "Future Engineering Roadmap")
    tb_fut = s13.shapes.add_textbox(Inches(7.0), Inches(2.2), Inches(5.3), Inches(4.4))
    tf_fut = tb_fut.text_frame
    tf_fut.word_wrap = True

    pts_fut = [
        "2D Fenwick Tree Extension: Extend data structure to a 2D BIT for spatial grid monitoring (intersections and multi-lane urban grids) in O(log^2 n) time.",
        "Dual-Tree Range Update Support: Incorporate two BITs to support O(log n) range updates and O(log n) range queries simultaneously.",
        "Machine Learning Inflow Forecasting: Integrate lightweight predictive models to anticipate congestion thresholds 15 minutes before physical gridlock occurs.",
        "WebSocket Real-Time Sensor Telemetry: Connect edge IoT sensors via live WebSockets directly into the FlowGrid analytics dashboard."
    ]
    for pt in pts_fut:
        p = tf_fut.add_paragraph()
        p.text = "• " + pt
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MUTED if "Extension" in pt else TEXT_LIGHT
        p.space_after = Pt(8)

    # =========================================================================
    # SLIDE 14: CONCLUSION
    # =========================================================================
    s14 = prs.slides.add_slide(blank_layout)
    set_slide_background(s14)
    add_header(s14, "Conclusion & Evaluation Summary")

    add_card(s14, Inches(0.8), Inches(1.6), Inches(11.7), Inches(5.2), "Key Takeaways & Evaluation Readiness")
    tb_end = s14.shapes.add_textbox(Inches(1.1), Inches(2.3), Inches(11.1), Inches(4.2))
    tf_end = tb_end.text_frame
    tf_end.word_wrap = True

    conclusions = [
        "Non-Menu-Driven Automated Execution: Both the C++ core and Web dashboard execute robust, automated verification sequences with zero fragile menu prompts.",
        "Rigorous Algorithmic Precision: All expected values (Initial BIT [12, 19, 15, 43, 20, 25, 11, 87], rangeSum = 49 NORMAL, Updated BIT [12, 19, 15, 43, 34, 39, 11, 101], rangeSum = 63 POTENTIALLY CONGESTED) verified to 100% precision.",
        "Dual-Implementation Fidelity: Independent C++ and JavaScript implementations provide both high-performance compiled logic and intuitive visual interaction.",
        "Production-Grade Edge Handling: Complete validation against out-of-bounds queries, negative vehicle numbers, inverted ranges, and exact threshold equality.",
        "Evaluation Ready: Code, documentation, test suite, and presentation are fully prepared for academic viva examination."
    ]
    for c in conclusions:
        p = tf_end.add_paragraph()
        p.text = "✓ " + c
        p.font.size = Pt(13)
        p.font.bold = True
        p.font.color.rgb = ACCENT_GREEN
        p.space_after = Pt(12)

    # Save presentation
    output_path = os.path.join("presentation", "Fenwick_Tree_Case_Study.pptx")
    prs.save(output_path)
    print(f"Presentation successfully created at: {output_path}")

if __name__ == "__main__":
    create_deck()
