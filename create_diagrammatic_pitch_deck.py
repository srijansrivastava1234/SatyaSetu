import sys
import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

TEMPLATE_PATH = r"E:\SMS HACKATHON\SatyaSetu\RotatTech_Impact-A-Thon_2026_PPT_Template.pdf_20261018_105445_0000.pptx"
OUTPUT_PATH = r"E:\SMS HACKATHON\SatyaSetu\SatyaSetu_RotaTech_2026_Final_Pitch.pptx"

# Modern Institutional Palette (High Contrast, Professional Slate & Brand Blue)
C_CARD_BG = RGBColor(255, 255, 255)         # Crisp White
C_CARD_BG_ALT = RGBColor(248, 250, 252)     # Slate 50
C_BORDER = RGBColor(203, 213, 225)          # Slate 300
C_BORDER_ACCENT = RGBColor(14, 116, 144)    # Deep Cyan 700
C_TITLE = RGBColor(15, 23, 42)              # Slate 900
C_BODY = RGBColor(51, 65, 85)               # Slate 700
C_MUTED = RGBColor(100, 116, 139)           # Slate 500
C_BRAND = RGBColor(37, 99, 235)             # Brand Blue
C_BRAND_DARK = RGBColor(29, 78, 216)        # Darker Blue
C_EMERALD = RGBColor(16, 185, 129)          # Emerald Verified
C_EMERALD_BG = RGBColor(236, 253, 245)      # Light Emerald
C_CRIMSON = RGBColor(220, 38, 38)           # Crimson Debunked
C_AMBER = RGBColor(217, 119, 6)             # Amber Warning
C_LINK = RGBColor(2, 132, 199)              # Sky Blue Link

def remove_element(shape):
    sp = shape._element
    sp.getparent().remove(sp)

def add_header_badge(slide, text="Team SatyaSetu"):
    """Adds the team name in the top badge box."""
    box = slide.shapes.add_textbox(Inches(8.5), Inches(0.35), Inches(3.0), Inches(0.8))
    tf = box.text_frame
    p = tf.paragraphs[0]
    p.text = text
    p.font.name = "Arial"
    p.font.size = Pt(18)
    p.font.bold = True
    p.font.color.rgb = C_TITLE
    p.alignment = PP_ALIGN.CENTER

def add_deployed_link_pill(slide, deployed_url, left_in=12.2, top_in=0.35, width_in=6.6, height_in=0.65):
    """Adds a prominent clickable live deployed prototype pill in the top header."""
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = C_EMERALD_BG
    shape.line.color.rgb = C_EMERALD
    shape.line.width = Pt(1.5)

    tf = shape.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.2)
    tf.margin_right = Inches(0.2)
    tf.margin_top = Inches(0.08)
    tf.margin_bottom = Inches(0.08)

    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    
    r_icon = p.add_run()
    r_icon.text = "● LIVE SYSTEM: "
    r_icon.font.name = "Arial"
    r_icon.font.size = Pt(12)
    r_icon.font.bold = True
    r_icon.font.color.rgb = C_EMERALD

    r_link = p.add_run()
    clean_disp = deployed_url.replace("https://", "").replace("http://", "")
    r_link.text = clean_disp
    r_link.font.name = "Arial"
    r_link.font.size = Pt(12)
    r_link.font.bold = True
    r_link.font.color.rgb = C_LINK
    r_link.font.underline = True
    r_link.hyperlink.address = deployed_url

def add_container_card(slide, left_in, top_in, width_in, height_in, title="", border_color=C_BORDER, fill_color=C_CARD_BG):
    """Creates a base container card."""
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)

    if title:
        tf = card.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.35)
        tf.margin_right = Inches(0.35)
        tf.margin_top = Inches(0.25)
        p = tf.paragraphs[0]
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(18)
        p.font.bold = True
        p.font.color.rgb = C_TITLE

    return card

def add_diagram_step_box(slide, left_in, top_in, width_in, height_in, step_num, step_title, subtext, tag="", is_highlight=False):
    """Renders a single process step block with a step number badge."""
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(238, 242, 255) if is_highlight else C_CARD_BG
    box.line.color.rgb = C_BRAND if is_highlight else C_BORDER
    box.line.width = Pt(1.8 if is_highlight else 1.2)

    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.18)
    tf.margin_right = Inches(0.18)
    tf.margin_top = Inches(0.15)
    tf.margin_bottom = Inches(0.15)

    # Step Badge & Tag
    p_step = tf.paragraphs[0]
    r_num = p_step.add_run()
    r_num.text = f"STEP {step_num}"
    r_num.font.name = "Arial"
    r_num.font.size = Pt(11)
    r_num.font.bold = True
    r_num.font.color.rgb = C_BRAND if is_highlight else C_MUTED
    
    if tag:
        r_tag = p_step.add_run()
        r_tag.text = f"  [{tag}]"
        r_tag.font.name = "Arial"
        r_tag.font.size = Pt(10)
        r_tag.font.bold = True
        r_tag.font.color.rgb = C_EMERALD if "ms" in tag or "IFCN" in tag else C_AMBER

    # Step Title
    p_title = tf.add_paragraph()
    p_title.space_before = Pt(4)
    p_title.space_after = Pt(4)
    r_title = p_title.add_run()
    r_title.text = step_title
    r_title.font.name = "Arial"
    r_title.font.size = Pt(14)
    r_title.font.bold = True
    r_title.font.color.rgb = C_TITLE

    # Description
    p_desc = tf.add_paragraph()
    r_desc = p_desc.add_run()
    r_desc.text = subtext
    r_desc.font.name = "Arial"
    r_desc.font.size = Pt(11.5)
    r_desc.font.color.rgb = C_BODY

def add_arrow_connector(slide, left_in, top_in, width_in=0.4, height_in=0.3):
    """Draws a clean directional connector arrow."""
    tx = slide.shapes.add_textbox(Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
    p = tx.text_frame.paragraphs[0]
    p.text = "➔"
    p.font.name = "Arial"
    p.font.size = Pt(20)
    p.font.bold = True
    p.font.color.rgb = C_BRAND
    p.alignment = PP_ALIGN.CENTER

def add_metric_callout(slide, left_in, top_in, width_in, height_in, metric_val, label_text, color=C_BRAND):
    """Renders a prominent stat/metric callout box."""
    box = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in)
    )
    box.fill.solid()
    box.fill.fore_color.rgb = C_CARD_BG_ALT
    box.line.color.rgb = C_BORDER
    box.line.width = Pt(1.0)

    tf = box.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.12)
    tf.margin_bottom = Inches(0.1)

    p_val = tf.paragraphs[0]
    p_val.alignment = PP_ALIGN.CENTER
    r_val = p_val.add_run()
    r_val.text = metric_val
    r_val.font.name = "Arial"
    r_val.font.size = Pt(22)
    r_val.font.bold = True
    r_val.font.color.rgb = color

    p_lbl = tf.add_paragraph()
    p_lbl.alignment = PP_ALIGN.CENTER
    r_lbl = p_lbl.add_run()
    r_lbl.text = label_text
    r_lbl.font.name = "Arial"
    r_lbl.font.size = Pt(11)
    r_lbl.font.bold = True
    r_lbl.font.color.rgb = C_MUTED

def add_resource_link_footer(slide, links, left_in=1.2, top_in=9.65, width_in=17.6, height_in=0.6):
    """Draws a clean verifiable resource bar with clickable links at the bottom of a slide."""
    bar = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in)
    )
    bar.fill.solid()
    bar.fill.fore_color.rgb = RGBColor(241, 245, 249)
    bar.line.color.rgb = C_BORDER
    bar.line.width = Pt(1.0)

    tf = bar.text_frame
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.08)
    tf.margin_bottom = Inches(0.08)

    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.LEFT

    r_hdr = p.add_run()
    r_hdr.text = "VERIFIABLE RESOURCES & AUDIT TRAILS:  "
    r_hdr.font.name = "Arial"
    r_hdr.font.size = Pt(10.5)
    r_hdr.font.bold = True
    r_hdr.font.color.rgb = C_TITLE

    for idx, (label, url) in enumerate(links):
        if idx > 0:
            r_sep = p.add_run()
            r_sep.text = "   |   "
            r_sep.font.name = "Arial"
            r_sep.font.size = Pt(10)
            r_sep.font.color.rgb = C_MUTED

        r_lnk = p.add_run()
        r_lnk.text = f"🔗 {label}"
        r_lnk.font.name = "Arial"
        r_lnk.font.size = Pt(10.5)
        r_lnk.font.bold = True
        r_lnk.font.color.rgb = C_LINK
        r_lnk.font.underline = True
        r_lnk.hyperlink.address = url

def build_presentation(deployed_url="https://satyasetu.onrender.com"):
    prs = pptx.Presentation(TEMPLATE_PATH)
    print(f"[DeckBuilder] Loaded template: {prs.slide_width/914400:.1f}\" x {prs.slide_height/914400:.1f}\"")
    print(f"[DeckBuilder] Embedding Deployed System Link: {deployed_url}")

    # =========================================================================
    # SLIDE 1: TITLE PAGE & EXECUTIVE ARCHITECTURE
    # =========================================================================
    s1 = prs.slides[0]
    for s in list(s1.shapes):
        if s.name in ["TextBox 12", "TextBox 14", "TextBox 15"]:
            remove_element(s)

    add_deployed_link_pill(s1, deployed_url, left_in=12.2, top_in=0.35, width_in=6.6, height_in=0.65)

    # Left Container: Problem Statement & Competition Identity
    add_container_card(s1, 1.2, 2.7, 8.6, 6.7, "Problem Statement & Solution Identity")
    left_items = [
        ("Problem Statement ID", "202611 (TrustAI: Tackling Digital Misinformation)"),
        ("Theme & Focus", "AI Integrity, Cyber Safety & Grassroots Truth Verification"),
        ("System Name", "SatyaSetu (सत्यसेतु) — Digital Truth Bridge"),
        ("Target Users", "500M+ First-time mobile citizens & WhatsApp group admins"),
        ("Core Architecture", "Zero-Hallucination 3-Tier Multi-Source Verification Engine"),
        ("Operational Status", "Production Ready with Live API & Web UI Interface")
    ]
    # Add text inside left container
    tb_l = s1.shapes.add_textbox(Inches(1.5), Inches(3.4), Inches(8.0), Inches(5.8))
    tf_l = tb_l.text_frame
    tf_l.word_wrap = True
    for idx, (head, val) in enumerate(left_items):
        p = tf_l.paragraphs[0] if idx == 0 else tf_l.add_paragraph()
        p.space_after = Pt(8)
        r_h = p.add_run()
        r_h.text = f"• {head}: "
        r_h.font.bold = True
        r_h.font.size = Pt(13)
        r_h.font.color.rgb = C_BORDER_ACCENT
        r_v = p.add_run()
        r_v.text = val
        r_v.font.size = Pt(12.5)
        r_v.font.color.rgb = C_BODY

    # Right Container: Team Execution Roster (5 Roles)
    add_container_card(s1, 10.2, 2.7, 8.6, 6.7, "Team Roster & Operational Split")
    team_members = [
        ("Anshika Pandey", "Team Leader & Stage Anchor", "Speaker A (5-Min Narrative), Evaluation Framing, Q&A Anchor"),
        ("Srijan Srivastava", "Full-Stack System Architect", "FastAPI Orchestrator, Async Pipelines, Cloud Deployment"),
        ("Amit Kumar Rajput", "Fact-Checking Architect", "ClaimReview Standards, PIB & Statutory Gazette Verification"),
        ("Akhilesh Sharma", "Frontend & UI Lead", "Speaker B (Live Demo Driver), Responsive UI, Telemetry Meters"),
        ("Suryansh Pandey", "AI Vision & Multimodal Lead", "Adaptive OpenCV OCR, Gemini NLI Prompts, Chrome Extension")
    ]
    tb_r = s1.shapes.add_textbox(Inches(10.5), Inches(3.4), Inches(8.0), Inches(5.8))
    tf_r = tb_r.text_frame
    tf_r.word_wrap = True
    for idx, (name, role, duty) in enumerate(team_members):
        p = tf_r.paragraphs[0] if idx == 0 else tf_r.add_paragraph()
        p.space_after = Pt(8)
        r_n = p.add_run()
        r_n.text = f"👤 {name} "
        r_n.font.bold = True
        r_n.font.size = Pt(13)
        r_n.font.color.rgb = C_TITLE
        r_role = p.add_run()
        r_role.text = f"({role})\n"
        r_role.font.bold = True
        r_role.font.size = Pt(11.5)
        r_role.font.color.rgb = C_BRAND
        r_duty = p.add_run()
        r_duty.text = f"   Scope: {duty}"
        r_duty.font.size = Pt(11)
        r_duty.font.color.rgb = C_MUTED

    add_resource_link_footer(s1, [
        ("GitHub Repository", "https://github.com/srijansrivastava1234/SatyaSetu"),
        ("Live Deployed Application", deployed_url),
        ("IFCN Global Fact-Check Principles", "https://www.ifcncodeofprinciples.poynter.org")
    ])

    # =========================================================================
    # SLIDE 2: PROPOSED SOLUTION & INNOVATION (DIAGRAMMATIC)
    # =========================================================================
    s2 = prs.slides[1]
    for s in list(s2.shapes):
        if s.name in ["TextBox 26", "TextBox 27", "TextBox 28", "TextBox 29", "Group 12", "Group 14", "Group 16", "Group 18", "Group 20"]:
            remove_element(s)
        elif s.name == "TextBox 23":
            s.text_frame.text = ""
            p = s.text_frame.paragraphs[0]
            p.text = "SatyaSetu: Dual-Circuit Solution Architecture"
            p.font.name = "Arial"
            p.font.size = Pt(32)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.alignment = PP_ALIGN.CENTER

    add_header_badge(s2)
    add_deployed_link_pill(s2, deployed_url)

    # Top Half: The Grassroots Misinformation Problem Diagram
    add_container_card(s2, 1.2, 2.7, 17.6, 2.8, "The Grassroots Crisis: Anatomy of a Viral WhatsApp Rumor")
    prob_steps = [
        ("1. Sensational Seed", "Fabricated scheme, fake disaster alert, or banking threat created.", C_CRIMSON),
        ("2. Psychological Urgency", "Weaponized phrasing ('Forward to 10 groups', 'Account blocked').", C_AMBER),
        ("3. Zero Source Anchors", "No official gazette links, no circular numbers, anonymous claims.", C_CRIMSON),
        ("4. Viral Forwarding", "Citizens forward out of panic without reading 1,500-word portals.", C_CRIMSON)
    ]
    for i, (st, desc, col) in enumerate(prob_steps):
        left_pos = 1.6 + (i * 4.0)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(3.4), Inches(3.4), Inches(1.8))
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG_ALT
        box.line.color.rgb = col
        box.line.width = Pt(1.4)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.12)
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = st
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = col
        p2 = tf.add_paragraph()
        p2.space_before = Pt(4)
        r2 = p2.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY
        if i < 3:
            add_arrow_connector(s2, left_pos + 3.48, 4.15, width_in=0.45)

    # Bottom Half: The SatyaSetu Circuit-Breaker Solution
    add_container_card(s2, 1.2, 5.7, 17.6, 3.7, "The SatyaSetu Innovation: 4-Pillar Digital Circuit-Breaker")
    sol_pillars = [
        ("Pillar 1: Multimodal OCR", "Adaptive OpenCV contrast normalization + Tesseract extracts text directly from compressed WhatsApp screenshots."),
        ("Pillar 2: Certified IFCN Desks", "Real-time Google Fact Check Tools API queries fetching certified ClaimReview schemas from AltNews, BOOM, Factly."),
        ("Pillar 3: Deception Telemetry", "Algorithmic quantification of Manufactured Urgency (0-100%), Outrage triggers, and Missing Journalistic Anchors."),
        ("Pillar 4: Respectful Counter-Cards", "1-Click bilingual fact cards in Hindi & English that citizens can copy-paste into group chats to stop rumors peacefully.")
    ]
    for i, (st, desc) in enumerate(sol_pillars):
        left_pos = 1.6 + (i * 4.0)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(6.4), Inches(3.4), Inches(2.7))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(240, 253, 250)
        box.line.color.rgb = C_EMERALD
        box.line.width = Pt(1.5)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.15)
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = st
        r1.font.bold = True
        r1.font.size = Pt(12.5)
        r1.font.color.rgb = C_BORDER_ACCENT
        p2 = tf.add_paragraph()
        p2.space_before = Pt(6)
        r2 = p2.add_run()
        r2.text = desc
        r2.font.size = Pt(11.5)
        r2.font.color.rgb = C_BODY

    add_resource_link_footer(s2, [
        ("IFCN Code of Principles", "https://www.ifcncodeofprinciples.poynter.org"),
        ("Live Deployed Prototype", deployed_url),
        ("Google Fact Check Tools API", "https://toolbox.google.com/factcheck/explorer")
    ])

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH (ARCHITECTURE FLOW)
    # =========================================================================
    s3 = prs.slides[2]
    for s in list(s3.shapes):
        if s.name in ["TextBox 20", "TextBox 21", "Group 12", "Group 14"]:
            remove_element(s)

    add_header_badge(s3)
    add_deployed_link_pill(s3, deployed_url)

    add_container_card(s3, 1.2, 2.7, 17.6, 6.7, "End-to-End Multi-Tier Verification Architecture")

    # 5 Horizontal Sequential Stages across the slide
    stages = [
        ("1", "Multimodal Ingestion", "Raw text, URL, or image upload. OpenCV adaptive thresholding + Tesseract OCR engine.", "OCR Pipeline", False),
        ("2", "L1 Canonical Cache", "SQLite WAL index mapping recurring viral hoaxes (<15ms). Resolves 80% volume with 0 API cost.", "< 15ms Latency", True),
        ("3", "L2 IFCN ClaimReview", "Real-time Google Fact Check Tools API queries to certified desks (AltNews, BOOM, PIB).", "250-450ms", True),
        ("4", "L3 Gazette & Web RAG", "Live Google News RSS + DuckDuckGo scraper restricted to official statutory portals (pib.gov.in, rbi.org.in).", "Live Grounding", True),
        ("5", "NLI Verdict & Telemetry", "Gemini 2.5 Flash Premise-Hypothesis NLI with strict Pydantic schema and deception scoring.", "temp=0.1", False)
    ]

    for i, (num, title, desc, tag, is_hl) in enumerate(stages):
        left_pos = 1.5 + (i * 3.3)
        add_diagram_step_box(s3, left_pos, 3.4, 2.9, 3.4, num, title, desc, tag=tag, is_highlight=is_hl)
        if i < 4:
            add_arrow_connector(s3, left_pos + 2.95, 4.8, width_in=0.32)

    # Architecture Sub-System Highlights (Bottom row inside Slide 3)
    sub_highlights = [
        ("FastAPI Async Core", "Python 3.11 asynchronous non-blocking pipeline running on Uvicorn with HTTPX client connections for sub-second responses."),
        ("Zero-Hallucination Stance", "Strict temperature=0.1 sampling requiring verbatim quotes from retrieved gazettes; defaults to 'UNVERIFIABLE' if evidence is missing."),
        ("Manifest V3 Extension", "Chrome extension service worker capturing on-page text selection with activeTab permissions and local storage.")
    ]
    for i, (title, desc) in enumerate(sub_highlights):
        left_pos = 1.5 + (i * 5.6)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(7.1), Inches(5.2), Inches(2.0))
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG_ALT
        box.line.color.rgb = C_BORDER
        box.line.width = Pt(1.2)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.12)
        p1 = tf.paragraphs[0]
        r1 = p1.add_run()
        r1.text = f"⚙ {title}"
        r1.font.bold = True
        r1.font.size = Pt(13)
        r1.font.color.rgb = C_BRAND
        p2 = tf.add_paragraph()
        p2.space_before = Pt(4)
        r2 = p2.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY

    add_resource_link_footer(s3, [
        ("FastAPI Framework Docs", "https://fastapi.tiangolo.com"),
        ("Google Fact Check API Docs", "https://developers.google.com/fact-check/tools/api"),
        ("Google GenAI SDK (Gemini)", "https://ai.google.dev"),
        ("Live Deployed App", deployed_url)
    ])

    # =========================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY (BENCHMARKS & RISK ENGINEERING)
    # =========================================================================
    s4 = prs.slides[3]
    for s in list(s4.shapes):
        if s.name in ["TextBox 22", "TextBox 23", "Group 12", "Group 14", "Group 16"]:
            remove_element(s)

    add_header_badge(s4)
    add_deployed_link_pill(s4, deployed_url)

    # Left Container: Empirical Accuracy Benchmarks (4 Metric Callouts + Table)
    add_container_card(s4, 1.2, 2.7, 8.6, 6.7, "Empirical Validation & Benchmark Results")
    add_metric_callout(s4, 1.5, 3.4, 3.8, 1.3, "100.0%", "OVERALL ACCURACY (20/20 PASS)", color=C_EMERALD)
    add_metric_callout(s4, 5.7, 3.4, 3.8, 1.3, "0.0%", "FALSE POSITIVE RATE (SAFE)", color=C_EMERALD)
    add_metric_callout(s4, 1.5, 4.9, 3.8, 1.3, "< 15 ms", "L1 CACHED PIPELINE LATENCY", color=C_BRAND)
    add_metric_callout(s4, 5.7, 4.9, 3.8, 1.3, "2.2 s", "COLD WEB RAG MEAN LATENCY", color=C_BRAND)

    tb_bench = s4.shapes.add_textbox(Inches(1.5), Inches(6.4), Inches(8.0), Inches(2.8))
    tf_b = tb_bench.text_frame
    tf_b.word_wrap = True
    bench_bullets = [
        ("Test Suite Scope", "Evaluated on 20 authentic Indian hoaxes, phishing attacks, medical myths, and genuine PIB announcements."),
        ("Zero False Positives", "Official gazette news (ISRO launches, Solar Subsidies, Vande Bharat) accurately verified without false debunk flags."),
        ("Automated CI/CD Test", "Re-runnable via `python test_system.py` with in-process TestClient and live HTTP endpoint.")
    ]
    for idx, (b_title, b_desc) in enumerate(bench_bullets):
        p = tf_b.paragraphs[0] if idx == 0 else tf_b.add_paragraph()
        p.space_after = Pt(6)
        r_h = p.add_run()
        r_h.text = f"• {b_title}: "
        r_h.font.bold = True
        r_h.font.size = Pt(12)
        r_h.font.color.rgb = C_BORDER_ACCENT
        r_d = p.add_run()
        r_d.text = b_desc
        r_d.font.size = Pt(11.5)
        r_d.font.color.rgb = C_BODY

    # Right Container: Risk Engineering & Offline Resilience (4 Strategy Cards)
    add_container_card(s4, 10.2, 2.7, 8.6, 6.7, "Risk Engineering & Operational Feasibility")
    risks = [
        ("Risk 1: Auditorium Wi-Fi Failure", "Zero reliance on venue Wi-Fi: Backend binds to local loopback (127.0.0.1) and runs autonomously via mobile hotspot with pre-cached scenarios."),
        ("Risk 2: External API Rate Limits", "If external search engines are throttled, local regex scam engine and psychological urgency detectors continue on-device without crashing."),
        ("Risk 3: User Privacy & Surveillance", "Zero personal phone numbers, chat histories, or contact books are stored. Operates strictly as a stateless, privacy-preserving utility."),
        ("Risk 4: Cloud Unit Economics", "Cost is $0.00 for 80% cached queries. Novel RAG syntheses consume < 500 tokens (approx ₹0.04/call), easily covered by public interest grants.")
    ]
    tb_risk = s4.shapes.add_textbox(Inches(10.5), Inches(3.4), Inches(8.0), Inches(5.8))
    tf_r = tb_risk.text_frame
    tf_r.word_wrap = True
    for idx, (r_head, r_text) in enumerate(risks):
        p = tf_r.paragraphs[0] if idx == 0 else tf_r.add_paragraph()
        p.space_after = Pt(8)
        r_h = p.add_run()
        r_h.text = f"🛡 {r_head}\n"
        r_h.font.bold = True
        r_h.font.size = Pt(12.5)
        r_h.font.color.rgb = C_BRAND
        r_t = p.add_run()
        r_t.text = f"   {r_text}"
        r_t.font.size = Pt(11.5)
        r_t.font.color.rgb = C_BODY

    add_resource_link_footer(s4, [
        ("Benchmark Dataset (test_dataset.json)", "https://github.com/srijansrivastava1234/SatyaSetu/blob/main/test_dataset.json"),
        ("Live Deployed Verification Endpoint", deployed_url),
        ("FastAPI Automated Test Suite", "https://github.com/srijansrivastava1234/SatyaSetu/blob/main/backend/test_system.py")
    ])

    # =========================================================================
    # SLIDE 5: IMPACT AND BENEFITS (GRASSROOTS SCALE)
    # =========================================================================
    s5 = prs.slides[4]
    for s in list(s5.shapes):
        if s.name in ["TextBox 20", "TextBox 21", "TextBox 22", "Group 12", "Group 14"]:
            remove_element(s)

    add_header_badge(s5)
    add_deployed_link_pill(s5, deployed_url)

    # Left Container: 3 Core Target Beneficiary Personas
    add_container_card(s5, 1.2, 2.7, 8.6, 6.7, "Target Beneficiaries & Grassroots Users")
    personas = [
        ("Grassroots Tier-2/3 & Rural Citizens", "500M+ First-time mobile users in Bharat who navigate exclusively via WhatsApp and cannot parse complex 1,500-word English investigative articles."),
        ("Senior Citizens & Pensioners", "Vulnerable demographic routinely targeted by high-urgency electricity disconnection scams, fake pension links, and PAN-Aadhaar phishing frauds."),
        ("Family & Community WhatsApp Admins", "Group gatekeepers who need objective, respectful, third-party fact cards to counter rumors in family groups without social awkwardness.")
    ]
    tb_p = s5.shapes.add_textbox(Inches(1.5), Inches(3.4), Inches(8.0), Inches(5.8))
    tf_p = tb_p.text_frame
    tf_p.word_wrap = True
    for idx, (p_title, p_desc) in enumerate(personas):
        p = tf_p.paragraphs[0] if idx == 0 else tf_p.add_paragraph()
        p.space_after = Pt(12)
        r_h = p.add_run()
        r_h.text = f"👥 {p_title}\n"
        r_h.font.bold = True
        r_h.font.size = Pt(13)
        r_h.font.color.rgb = C_BORDER_ACCENT
        r_d = p.add_run()
        r_d.text = f"   {p_desc}"
        r_d.font.size = Pt(11.5)
        r_d.font.color.rgb = C_BODY

    # Right Container: Viral Distribution Loop & Measurable Impact
    add_container_card(s5, 10.2, 2.7, 8.6, 6.7, "Organic 1-to-256 Viral Distribution Loop")
    loop_steps = [
        ("Step 1: Detection", "User suspects a forward and checks via SatyaSetu Web UI or Extension."),
        ("Step 2: Verification", "Engine generates a factual, objective counter-card in Hindi and English."),
        ("Step 3: Group Share", "User copies card into a 256-member WhatsApp group with one click."),
        ("Step 4: Network Immunity", "255 other group members are organically educated at zero acquisition cost.")
    ]
    for i, (st, desc) in enumerate(loop_steps):
        top_pos = 3.5 + (i * 1.0)
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.5), Inches(top_pos), Inches(8.0), Inches(0.85))
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG_ALT
        box.line.color.rgb = C_BRAND
        box.line.width = Pt(1.2)
        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.08)
        p = tf.paragraphs[0]
        r1 = p.add_run()
        r1.text = f"▶ {st}: "
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = C_BRAND
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY

    add_metric_callout(s5, 10.5, 7.7, 3.8, 1.4, "500M+", "POTENTIAL RURAL CITIZENS REACHED", color=C_BRAND)
    add_metric_callout(s5, 14.7, 7.7, 3.8, 1.4, "100%", "BILINGUAL COVERAGE (HINDI & ENG)", color=C_EMERALD)

    add_resource_link_footer(s5, [
        ("PIB Fact Check Official Desk", "https://factcheck.pib.gov.in"),
        ("RBI Financial Education Portal", "https://paisaboltahai.rbi.org.in"),
        ("Live Deployed Prototype", deployed_url)
    ])

    # =========================================================================
    # SLIDE 6: RESEARCH AND REFERENCES (STANDARDS & LINKS)
    # =========================================================================
    s6 = prs.slides[5]
    for s in list(s6.shapes):
        if s.name in ["TextBox 18", "TextBox 19", "TextBox 20", "Group 12"]:
            remove_element(s)

    add_header_badge(s6)
    add_deployed_link_pill(s6, deployed_url)

    # 3 Column Structured Table of Authoritative References
    add_container_card(s6, 1.2, 2.7, 17.6, 6.7, "Authoritative References, Standards & Academic Grounding")

    ref_cols = [
        ("Certified Fact-Checking Desks", [
            ("Poynter IFCN Code of Principles", "International standard for non-partisanship & fairness", "https://www.ifcncodeofprinciples.poynter.org"),
            ("Alt News Investigation Archive", "Certified IFCN fact-checking desk covering Indian rumors", "https://www.altnews.in"),
            ("BOOM Live Fact Check", "IFCN certified digital verification covering health & communal hoaxes", "https://www.boomlive.in"),
            ("Factly Media & Research", "Certified IFCN platform specializing in public data verification", "https://factly.in")
        ]),
        ("Official Statutory Gazettes", [
            ("Press Information Bureau (PIB)", "Official nodal agency of the Government of India", "https://factcheck.pib.gov.in"),
            ("Reserve Bank of India (RBI)", "Central bank circulars, repo rates & currency notices", "https://www.rbi.org.in"),
            ("CBSE Examination Board", "Official circulars and date sheets verifying student notices", "https://www.cbse.gov.in"),
            ("UNESCO Official Portal", "Refuting recurring national anthem viral declarations", "https://www.unesco.org")
        ]),
        ("Academic Research & Standards", [
            ("FEVER Benchmark (Thorne et al.)", "Large-scale fact extraction and NLI verification standard", "https://fever.ai"),
            ("Schema.org ClaimReview", "Open data standard for structured fact-checking markups", "https://schema.org/ClaimReview"),
            ("Google Fact Check Tools API", "Google API surfacing ClaimReview schemas globally", "https://developers.google.com/fact-check/tools/api"),
            ("SatyaSetu GitHub Codebase", "Open-source codebase with 100% passing test suites", "https://github.com/srijansrivastava1234/SatyaSetu")
        ])
    ]

    for col_idx, (col_title, items) in enumerate(ref_cols):
        left_pos = 1.5 + (col_idx * 5.7)
        box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(3.4), Inches(5.4), Inches(5.7))
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG_ALT
        box.line.color.rgb = C_BORDER
        box.line.width = Pt(1.2)

        tf = box.text_frame
        tf.word_wrap = True
        tf.margin_left = Inches(0.2)
        tf.margin_right = Inches(0.2)
        tf.margin_top = Inches(0.15)

        p_hdr = tf.paragraphs[0]
        r_h = p_hdr.add_run()
        r_h.text = col_title
        r_h.font.bold = True
        r_h.font.size = Pt(14)
        r_h.font.color.rgb = C_BRAND

        for it_title, it_desc, it_url in items:
            p_item = tf.add_paragraph()
            p_item.space_before = Pt(8)
            r_t = p_item.add_run()
            r_t.text = f"• {it_title}\n"
            r_t.font.bold = True
            r_t.font.size = Pt(11.5)
            r_t.font.color.rgb = C_TITLE

            r_d = p_item.add_run()
            r_d.text = f"  {it_desc}\n"
            r_d.font.size = Pt(10.5)
            r_d.font.color.rgb = C_MUTED

            r_u = p_item.add_run()
            r_u.text = f"  🔗 Link: {it_url.replace('https://', '')[:30]}..."
            r_u.font.size = Pt(10.5)
            r_u.font.bold = True
            r_u.font.color.rgb = C_LINK
            r_u.font.underline = True
            r_u.hyperlink.address = it_url

    add_resource_link_footer(s6, [
        ("SatyaSetu Production Deployment", deployed_url),
        ("GitHub Repository", "https://github.com/srijansrivastava1234/SatyaSetu"),
        ("IFCN Global Code of Principles", "https://www.ifcncodeofprinciples.poynter.org")
    ])

    # =========================================================================
    # DELETE SLIDE 7 (Instruction Slide)
    # =========================================================================
    if len(prs.slides) > 6:
        rId = prs.slides._sldIdLst[6].rId
        prs.part.drop_rel(rId)
        del prs.slides._sldIdLst[6]

    prs.save(OUTPUT_PATH)
    print(f"[DeckBuilder] SUCCESS: Saved diagrammatic deck to {OUTPUT_PATH}")

if __name__ == "__main__":
    url_arg = sys.argv[1] if len(sys.argv) > 1 else "https://satyasetu.onrender.com"
    build_presentation(url_arg)
