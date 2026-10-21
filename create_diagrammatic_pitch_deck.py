import sys
import os
import pptx
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

TEMPLATE_PATH = r"E:\SMS HACKATHON\SatyaSetu\RotatTech_Impact-A-Thon_2026_PPT_Template.pdf_20261018_105445_0000.pptx"
OUTPUT_PATH = r"E:\SMS HACKATHON\SatyaSetu\SatyaSetu_RotaTech_2026_Final_Pitch.pptx"

SCREENSHOT_VERDICT = r"E:\SMS HACKATHON\SatyaSetu\docs\presentation_screenshots\01_verdict_and_credibility.png"
SCREENSHOT_TELEMETRY = r"E:\SMS HACKATHON\SatyaSetu\docs\presentation_screenshots\02_deception_telemetry_gauges.png"
SCREENSHOT_EVIDENCE = r"E:\SMS HACKATHON\SatyaSetu\docs\presentation_screenshots\03_certified_source_evidence_table.png"

# Institutional Modern Slate Palette (High Contrast, Slate, Deep Cyan & Brand Blue)
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

def add_deployed_link_pill(slide, deployed_url, left_in=11.35, top_in=0.35, width_in=4.15, height_in=0.62):
    """
    Adds a prominent clickable live deployed prototype pill in the top header,
    positioned safely between the center title/oval and the right-hand Rotary emblem.
    """
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in)
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = C_EMERALD_BG
    shape.line.color.rgb = C_EMERALD
    shape.line.width = Pt(1.5)

    tf = shape.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = True
    tf.margin_left = Inches(0.12)
    tf.margin_right = Inches(0.12)
    tf.margin_top = Inches(0.04)
    tf.margin_bottom = Inches(0.04)

    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    
    r_icon = p.add_run()
    r_icon.text = "● LIVE: "
    r_icon.font.name = "Arial"
    r_icon.font.size = Pt(11)
    r_icon.font.bold = True
    r_icon.font.color.rgb = C_EMERALD

    r_link = p.add_run()
    clean_disp = deployed_url.replace("https://", "").replace("http://", "")
    r_link.text = clean_disp
    r_link.font.name = "Arial"
    r_link.font.size = Pt(11)
    r_link.font.bold = True
    r_link.font.color.rgb = C_LINK
    r_link.font.underline = True
    r_link.hyperlink.address = deployed_url

def add_container_card(slide, left_in, top_in, width_in, height_in, title="", border_color=C_BORDER, fill_color=C_CARD_BG):
    """
    Creates a base container card with a dedicated top title bar,
    completely eliminating vertical-centering overlap issues.
    """
    card = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE,
        Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in)
    )
    card.fill.solid()
    card.fill.fore_color.rgb = fill_color
    card.line.color.rgb = border_color
    card.line.width = Pt(1.5)

    if title:
        tb = slide.shapes.add_textbox(Inches(left_in + 0.35), Inches(top_in + 0.16), Inches(width_in - 0.7), Inches(0.48))
        tf = tb.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.word_wrap = True
        tf.margin_left = tf.margin_top = tf.margin_right = tf.margin_bottom = 0
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        p.text = title
        p.font.name = "Arial"
        p.font.size = Pt(16.5)
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
    tf.vertical_anchor = MSO_ANCHOR.TOP
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.14)
    tf.margin_bottom = Inches(0.1)

    # Step Badge & Tag
    p_step = tf.paragraphs[0]
    p_step.alignment = PP_ALIGN.LEFT
    r_num = p_step.add_run()
    r_num.text = f"STAGE {step_num}"
    r_num.font.name = "Arial"
    r_num.font.size = Pt(10.5)
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
    p_title.alignment = PP_ALIGN.LEFT
    p_title.space_before = Pt(3)
    p_title.space_after = Pt(3)
    r_title = p_title.add_run()
    r_title.text = step_title
    r_title.font.name = "Arial"
    r_title.font.size = Pt(12.5)
    r_title.font.bold = True
    r_title.font.color.rgb = C_TITLE

    # Description
    p_desc = tf.add_paragraph()
    p_desc.alignment = PP_ALIGN.LEFT
    r_desc = p_desc.add_run()
    r_desc.text = subtext
    r_desc.font.name = "Arial"
    r_desc.font.size = Pt(10.5)
    r_desc.font.color.rgb = C_BODY

def add_arrow_connector(slide, left_in, top_in, width_in=0.35, height_in=0.3):
    """Draws a clean directional connector arrow."""
    tx = slide.shapes.add_textbox(Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in))
    p = tx.text_frame.paragraphs[0]
    p.text = "➔"
    p.font.name = "Arial"
    p.font.size = Pt(18)
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
    box.line.width = Pt(1.2)

    tf = box.text_frame
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = True
    tf.margin_left = Inches(0.15)
    tf.margin_right = Inches(0.15)
    tf.margin_top = Inches(0.08)
    tf.margin_bottom = Inches(0.08)

    p_val = tf.paragraphs[0]
    p_val.alignment = PP_ALIGN.CENTER
    r_val = p_val.add_run()
    r_val.text = metric_val
    r_val.font.name = "Arial"
    r_val.font.size = Pt(21)
    r_val.font.bold = True
    r_val.font.color.rgb = color

    p_lbl = tf.add_paragraph()
    p_lbl.alignment = PP_ALIGN.CENTER
    r_lbl = p_lbl.add_run()
    r_lbl.text = label_text
    r_lbl.font.name = "Arial"
    r_lbl.font.size = Pt(9.5)
    r_lbl.font.bold = True
    r_lbl.font.color.rgb = C_MUTED

def add_resource_link_footer(slide, links, left_in=1.0, top_in=9.65, width_in=18.0, height_in=0.58):
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
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.word_wrap = True
    tf.margin_left = Inches(0.25)
    tf.margin_right = Inches(0.25)
    tf.margin_top = Inches(0.06)
    tf.margin_bottom = Inches(0.06)

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

def add_screenshot_frame(slide, img_path, left_in, top_in, width_in, height_in, caption_text=""):
    """Inserts a verified system screenshot within an institutional bordered frame and caption."""
    frame = slide.shapes.add_shape(
        MSO_SHAPE.RECTANGLE,
        Inches(left_in), Inches(top_in), Inches(width_in), Inches(height_in)
    )
    frame.fill.solid()
    frame.fill.fore_color.rgb = RGBColor(248, 250, 252)
    frame.line.color.rgb = C_BORDER
    frame.line.width = Pt(1.0)

    pad = 0.05
    caption_h = 0.35 if caption_text else 0.0
    img_h = height_in - caption_h - (pad * 2)
    img_w = width_in - (pad * 2)
    
    if os.path.exists(img_path):
        slide.shapes.add_picture(
            img_path,
            Inches(left_in + pad), Inches(top_in + pad),
            Inches(img_w), Inches(img_h)
        )

    if caption_text:
        tb = slide.shapes.add_textbox(
            Inches(left_in), Inches(top_in + height_in - caption_h),
            Inches(width_in), Inches(caption_h)
        )
        tf = tb.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.word_wrap = True
        tf.margin_left = Inches(0.1)
        tf.margin_right = Inches(0.1)
        tf.margin_top = Inches(0.02)
        tf.margin_bottom = Inches(0.02)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        r = p.add_run()
        r.text = f"📸 {caption_text}"
        r.font.name = "Arial"
        r.font.size = Pt(9.5)
        r.font.bold = True
        r.font.color.rgb = C_MUTED

def build_presentation(deployed_url="https://satyasetu-wtpy.onrender.com"):
    prs = pptx.Presentation(TEMPLATE_PATH)
    print(f"[DeckBuilder] Loaded template: {prs.slide_width/914400:.1f}\" x {prs.slide_height/914400:.1f}\"")
    print(f"[DeckBuilder] Embedding Deployed System Link: {deployed_url}")

    # =========================================================================
    # SLIDE 1: TITLE PAGE & EXECUTIVE ARCHITECTURE
    # =========================================================================
    s1 = prs.slides[0]
    
    # Clean template placeholders on Slide 1
    for s in list(s1.shapes):
        if s.name in ["TextBox 14", "TextBox 15"]:
            remove_element(s)
        elif s.name == "TextBox 13": # ROTATECH 2026 header
            s.left = Inches(5.0)
            s.top = Inches(0.3)
            s.width = Inches(5.5)
            s.height = Inches(0.8)
            s.text_frame.text = ""
            p = s.text_frame.paragraphs[0]
            p.text = "ROTATECH 2026"
            p.font.name = "Arial"
            p.font.size = Pt(30)
            p.font.bold = True
            p.font.color.rgb = C_BRAND_DARK
        elif s.name == "TextBox 12": # Subtitle
            s.left = Inches(5.0)
            s.top = Inches(1.15)
            s.width = Inches(10.2)
            s.height = Inches(0.9)
            s.text_frame.text = ""
            p = s.text_frame.paragraphs[0]
            p.text = "SatyaSetu (सत्यसेतु) — Digital Truth Verification Engine"
            p.font.name = "Arial"
            p.font.size = Pt(18)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p2 = s.text_frame.add_paragraph()
            p2.space_before = Pt(3)
            r2 = p2.add_run()
            r2.text = "Problem Statement 202611 | Zero-Hallucination Multimodal Fact-Checking Architecture"
            r2.font.name = "Arial"
            r2.font.size = Pt(12)
            r2.font.color.rgb = C_MUTED

    add_deployed_link_pill(s1, deployed_url, left_in=10.8, top_in=0.32, width_in=4.4, height_in=0.62)

    # Left Container: Problem Statement & Solution Identity
    add_container_card(s1, 1.0, 2.35, 8.8, 7.05, "Problem Statement & Solution Identity")
    left_items = [
        ("Problem Statement ID", "202611"),
        ("Problem Statement Title", "TrustAI: Tackling Digital Misinformation"),
        ("Theme & Focus", "AI Integrity, Cyber Safety & Grassroots Trust"),
        ("Core Architecture", "Zero-Hallucination 3-Tier Multi-Source Engine"),
        ("Target Demographic", "500M+ Rural Citizens & WhatsApp Group Admins"),
        ("Key Innovation", "<15ms L1 Cache + Certified IFCN + Gazette RAG"),
        ("Operational Status", "Production Ready with Live API & Web UI Interface")
    ]
    tb_l = s1.shapes.add_textbox(Inches(1.3), Inches(2.95), Inches(8.2), Inches(5.5))
    tf_l = tb_l.text_frame
    tf_l.vertical_anchor = MSO_ANCHOR.TOP
    tf_l.word_wrap = True
    for idx, (head, val) in enumerate(left_items):
        p = tf_l.paragraphs[0] if idx == 0 else tf_l.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(7)
        r_h = p.add_run()
        r_h.text = f"• {head}: "
        r_h.font.bold = True
        r_h.font.size = Pt(13)
        r_h.font.color.rgb = C_BORDER_ACCENT
        r_v = p.add_run()
        r_v.text = val
        r_v.font.size = Pt(12.5)
        r_v.font.color.rgb = C_BODY

    # Institutional Trust Badge inside Left Container
    badge_box = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(8.65), Inches(8.2), Inches(0.55))
    badge_box.fill.solid()
    badge_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
    badge_box.line.color.rgb = C_BRAND
    badge_box.line.width = Pt(1.2)
    tf_badge = badge_box.text_frame
    tf_badge.vertical_anchor = MSO_ANCHOR.MIDDLE
    p_b = tf_badge.paragraphs[0]
    p_b.alignment = PP_ALIGN.CENTER
    r_b = p_b.add_run()
    r_b.text = "🛡 TRUSTAI VERIFICATION SEAL | IFCN PRINCIPLES | ZERO HALLUCINATIONS"
    r_b.font.name = "Arial"
    r_b.font.size = Pt(10)
    r_b.font.bold = True
    r_b.font.color.rgb = C_BRAND_DARK

    # Right Container: Team Execution Roster (5 Roles)
    add_container_card(s1, 10.2, 2.35, 8.8, 7.05, "Team Roster & Operational Split (SatyaSetu)")
    team_members = [
        ("Anshika Pandey", "Team Leader & Stage Presenter (Speaker A)", "5-Min Pitch Narrative, Cognitive Impact Framing, Q&A Anchor"),
        ("Srijan Srivastava", "Full-Stack System Architect", "FastAPI Asynchronous Backend, SQLite WAL L1 Cache, Deployment"),
        ("Amit Kumar Rajput", "Fact-Checking Architect", "ClaimReview Standards, IFCN Audit Principles, Statutory Gazette Verification"),
        ("Akhilesh Sharma", "Frontend & UI Lead (Speaker B)", "Drives Live Screen Demo (1:10–3:10), Responsive Dashboard & Meters"),
        ("Suryansh Pandey", "AI Vision & Multimodal Lead", "Adaptive OpenCV Image Pre-processing, Tesseract OCR, Gemini NLI Prompts")
    ]
    tb_r = s1.shapes.add_textbox(Inches(10.5), Inches(2.95), Inches(8.2), Inches(6.2))
    tf_r = tb_r.text_frame
    tf_r.vertical_anchor = MSO_ANCHOR.TOP
    tf_r.word_wrap = True
    for idx, (name, role, duty) in enumerate(team_members):
        p = tf_r.paragraphs[0] if idx == 0 else tf_r.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(7)
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
    # SLIDE 2: PROPOSED SOLUTION & INNOVATION (DUAL-CIRCUIT ARCHITECTURE)
    # =========================================================================
    s2 = prs.slides[1]
    for s in list(s2.shapes):
        if s.name in ["TextBox 28", "TextBox 29", "Group 12", "Group 14", "Group 16", "Group 18", "Group 20"]:
            remove_element(s)
        elif s.name == "TextBox 23": # Slide title
            s.left = Inches(4.5)
            s.top = Inches(1.4)
            s.width = Inches(11.0)
            s.height = Inches(0.7)
            s.text_frame.text = ""
            p = s.text_frame.paragraphs[0]
            p.text = "SatyaSetu: Dual-Circuit Solution Architecture"
            p.font.name = "Arial"
            p.font.size = Pt(22)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.alignment = PP_ALIGN.CENTER
        elif s.name == "TextBox 26": # Team name in oval
            s.text_frame.text = ""
            s.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = s.text_frame.paragraphs[0]
            p.text = "Team SatyaSetu"
            p.font.name = "Arial"
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.alignment = PP_ALIGN.CENTER
        elif s.name == "TextBox 27":
            remove_element(s)

    add_deployed_link_pill(s2, deployed_url, left_in=11.35, top_in=0.35, width_in=4.15, height_in=0.62)

    # Top Half: The Grassroots Misinformation Problem Diagram
    add_container_card(s2, 1.0, 2.35, 18.0, 2.45, "The Grassroots Crisis: Anatomy of a Viral WhatsApp Rumor")
    prob_steps = [
        ("1. Sensational Seed", "Fabricated scheme, fake disaster alert, or banking threat created.", C_CRIMSON),
        ("2. Psychological Urgency", "Weaponized phrasing ('Forward to 10 groups', 'Account blocked').", C_AMBER),
        ("3. Zero Source Anchors", "No official gazette links, no circular numbers, anonymous claims.", C_CRIMSON),
        ("4. Viral Forwarding", "Citizens forward out of panic without reading 1,500-word portals.", C_CRIMSON)
    ]
    for i, (st, desc, col) in enumerate(prob_steps):
        left_pos = 1.3 + (i * 4.2)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(2.95), Inches(3.8), Inches(1.65))
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG_ALT
        box.line.color.rgb = col
        box.line.width = Pt(1.4)
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.word_wrap = True
        tf.margin_left = Inches(0.15)
        tf.margin_right = Inches(0.15)
        tf.margin_top = Inches(0.14)
        p1 = tf.paragraphs[0]
        p1.alignment = PP_ALIGN.LEFT
        r1 = p1.add_run()
        r1.text = st
        r1.font.bold = True
        r1.font.size = Pt(12)
        r1.font.color.rgb = col
        p2 = tf.add_paragraph()
        p2.alignment = PP_ALIGN.LEFT
        p2.space_before = Pt(4)
        r2 = p2.add_run()
        r2.text = desc
        r2.font.size = Pt(11)
        r2.font.color.rgb = C_BODY
        if i < 3:
            add_arrow_connector(s2, left_pos + 3.85, 3.65, width_in=0.35)

    # Bottom Half: Left Container (4 Pillars) + Right Container (Live Screenshot)
    add_container_card(s2, 1.0, 4.95, 9.8, 4.55, "The SatyaSetu Innovation: 4-Pillar Digital Circuit-Breaker")
    sol_pillars = [
        ("Pillar 1: Multimodal OCR & Vision", "Adaptive OpenCV edge detection + Otsu binarization extracts text from compressed WhatsApp forwards.", C_BORDER_ACCENT),
        ("Pillar 2: Certified IFCN ClaimReview", "Real-time Google Fact Check Tools API fetching cryptographically verifiable ClaimReview schemas.", C_BRAND),
        ("Pillar 3: Deception Telemetry", "Algorithmic quantification of Urgency (0-100%), Outrage intensity, and Absence of official circulars.", C_AMBER),
        ("Pillar 4: Respectful Counter-Cards", "1-Click bilingual fact cards in Hindi & English that citizens copy-paste into group chats to stop rumors.", C_EMERALD)
    ]
    for i, (st, desc, col) in enumerate(sol_pillars):
        top_pos = 5.55 + (i * 0.94)
        box = s2.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.3), Inches(top_pos), Inches(9.2), Inches(0.85))
        box.fill.solid()
        box.fill.fore_color.rgb = RGBColor(248, 250, 252)
        box.line.color.rgb = col
        box.line.width = Pt(1.3)
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.1)
        p1 = tf.paragraphs[0]
        p1.alignment = PP_ALIGN.LEFT
        r1 = p1.add_run()
        r1.text = f"{st}: "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = col
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_BODY

    # Right Container: Live Operational Telemetry Screenshot
    add_container_card(s2, 11.1, 4.95, 7.9, 4.55, "Operational Telemetry: Real-Time Deception Gauges")
    add_screenshot_frame(
        s2, SCREENSHOT_TELEMETRY,
        left_in=11.35, top_in=5.55, width_in=7.4, height_in=3.75,
        caption_text="Live Telemetry: 78% Urgency | 62% Outrage | 95% Missing Authority Anchors"
    )

    add_resource_link_footer(s2, [
        ("IFCN Code of Principles", "https://www.ifcncodeofprinciples.poynter.org"),
        ("Live Deployed Prototype", deployed_url),
        ("Google Fact Check Tools API", "https://toolbox.google.com/factcheck/explorer")
    ])

    # =========================================================================
    # SLIDE 3: TECHNICAL APPROACH (ARCHITECTURE FLOW & EVIDENCE TABLE)
    # =========================================================================
    s3 = prs.slides[2]
    for s in list(s3.shapes):
        if s.name in ["TextBox 20", "Group 12", "Group 14"]:
            remove_element(s)
        elif s.name == "TextBox 17": # Title
            s.left = Inches(4.5)
            s.top = Inches(1.4)
            s.width = Inches(11.0)
            s.height = Inches(0.7)
            s.text_frame.text = ""
            p = s.text_frame.paragraphs[0]
            p.text = "TECHNICAL APPROACH & PIPELINE"
            p.font.name = "Arial"
            p.font.size = Pt(22)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.alignment = PP_ALIGN.CENTER
        elif s.name == "TextBox 21": # Team name in oval
            s.text_frame.text = ""
            s.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = s.text_frame.paragraphs[0]
            p.text = "Team SatyaSetu"
            p.font.name = "Arial"
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.alignment = PP_ALIGN.CENTER

    add_deployed_link_pill(s3, deployed_url, left_in=11.35, top_in=0.35, width_in=4.15, height_in=0.62)

    # Top Half: 5 Sequential Stages
    add_container_card(s3, 1.0, 2.35, 18.0, 3.25, "End-to-End Multi-Tier Verification Architecture (Strict Latency Budgets)")
    stages = [
        ("1", "Multimodal Ingestion", "Raw text, URL, or image forward. OpenCV adaptive thresholding + Tesseract OCR engine.", "OCR Pipeline", False),
        ("2", "L1 Canonical Cache", "SQLite WAL index mapping recurring viral hoaxes (<15ms). Resolves 80% volume with 0 API cost.", "< 15ms Latency", True),
        ("3", "L2 IFCN ClaimReview", "Real-time Google Fact Check Tools API queries fetching verified ClaimReview JSON schemas.", "250-450ms", True),
        ("4", "L3 Gazette & Web RAG", "Live Google News RSS + DuckDuckGo scraper restricted to official portals (pib.gov.in, rbi.org.in).", "Live Grounding", True),
        ("5", "NLI Verdict & Telemetry", "Gemini 2.5 Flash Premise-Hypothesis NLI with strict Pydantic schema and deception scoring.", "temp=0.1", False)
    ]
    for i, (num, title, desc, tag, is_hl) in enumerate(stages):
        left_pos = 1.25 + (i * 3.45)
        add_diagram_step_box(s3, left_pos, 2.95, 3.15, 2.45, num, title, desc, tag=tag, is_highlight=is_hl)
        if i < 4:
            add_arrow_connector(s3, left_pos + 3.2, 4.0, width_in=0.25)

    # Bottom Half: Left (Sub-systems) + Right (Evidence Screenshot)
    add_container_card(s3, 1.0, 5.75, 9.6, 3.75, "Architectural Highlights & Integrity Guarantees")
    sub_highlights = [
        ("FastAPI Asynchronous Core", "Python 3.11 non-blocking pipeline running on Uvicorn with HTTPX client pooling for sub-second parallel retrieval."),
        ("Zero-Hallucination Stance Policy", "Strict temp=0.1 sampling requiring verbatim quotes from retrieved gazette evidence; defaults to 'UNVERIFIABLE' if missing."),
        ("Manifest V3 Chrome Extension", "Chrome extension service worker capturing on-page text selection with activeTab permissions and local storage.")
    ]
    for i, (title, desc) in enumerate(sub_highlights):
        top_pos = 6.35 + (i * 0.98)
        box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.25), Inches(top_pos), Inches(9.1), Inches(0.88))
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG_ALT
        box.line.color.rgb = C_BORDER
        box.line.width = Pt(1.2)
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.1)
        p1 = tf.paragraphs[0]
        p1.alignment = PP_ALIGN.LEFT
        r1 = p1.add_run()
        r1.text = f"⚙ {title}: "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = C_BRAND
        r2 = p1.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_BODY

    # Right Container: Certified Evidence Table Screenshot
    add_container_card(s3, 10.9, 5.75, 8.1, 3.75, "Live Certified Source Evidence Engine")
    add_screenshot_frame(
        s3, SCREENSHOT_EVIDENCE,
        left_in=11.15, top_in=6.35, width_in=7.6, height_in=3.0,
        caption_text="Dual-Action Links: Direct Fact-Check Investigation + Live News Fallback"
    )

    add_resource_link_footer(s3, [
        ("FastAPI Framework Docs", "https://fastapi.tiangolo.com"),
        ("Google Fact Check API Docs", "https://developers.google.com/fact-check/tools/api"),
        ("Google GenAI SDK (Gemini)", "https://ai.google.dev"),
        ("Live Deployed App", deployed_url)
    ])

    # =========================================================================
    # SLIDE 4: FEASIBILITY AND VIABILITY (BENCHMARKS & RISK DEFENSE)
    # =========================================================================
    s4 = prs.slides[3]
    for s in list(s4.shapes):
        if s.name in ["TextBox 22", "Group 12", "Group 14", "Group 16"]:
            remove_element(s)
        elif s.name == "TextBox 19": # Title
            s.left = Inches(4.5)
            s.top = Inches(1.4)
            s.width = Inches(11.0)
            s.height = Inches(0.7)
            s.text_frame.text = ""
            p = s.text_frame.paragraphs[0]
            p.text = "FEASIBILITY AND VIABILITY (BENCHMARKS & RISKS)"
            p.font.name = "Arial"
            p.font.size = Pt(21)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.alignment = PP_ALIGN.CENTER
        elif s.name == "TextBox 23": # Team name in oval
            s.text_frame.text = ""
            s.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = s.text_frame.paragraphs[0]
            p.text = "Team SatyaSetu"
            p.font.name = "Arial"
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.alignment = PP_ALIGN.CENTER

    add_deployed_link_pill(s4, deployed_url, left_in=11.35, top_in=0.35, width_in=4.15, height_in=0.62)

    # Left Container: Benchmarks + Live Verdict Screenshot
    add_container_card(s4, 1.0, 2.35, 9.4, 7.05, "Empirical Validation & Real-Time Verdict Audit")
    add_metric_callout(s4, 1.25, 2.95, 4.3, 1.2, "100.0%", "OVERALL ACCURACY (20/20 PASS)", color=C_EMERALD)
    add_metric_callout(s4, 5.85, 2.95, 4.3, 1.2, "0.0%", "FALSE POSITIVE RATE (SAFE)", color=C_EMERALD)
    add_metric_callout(s4, 1.25, 4.25, 4.3, 1.15, "< 15 ms", "L1 CACHED PIPELINE LATENCY", color=C_BRAND)
    add_metric_callout(s4, 5.85, 4.25, 4.3, 1.15, "2.2 s", "COLD WEB RAG MEAN LATENCY", color=C_BRAND)

    # Screenshot 1: Verdict and Credibility Meter
    add_screenshot_frame(
        s4, SCREENSHOT_VERDICT,
        left_in=1.25, top_in=5.55, width_in=8.9, height_in=3.65,
        caption_text="Live Verification: Categorical Verdict (FALSE) | Credibility 0/100 | <15ms Cached"
    )

    # Right Container: Risk Engineering & 4 Real-World Defense Vectors
    add_container_card(s4, 10.7, 2.35, 8.3, 7.05, "Risk Engineering & Operational Feasibility")
    risks = [
        ("Risk 1: Auditorium Wi-Fi Outage", "Zero dependence on venue Wi-Fi: Backend binds to local loopback (127.0.0.1:8000) and operates via an isolated mobile hotspot with pre-cached test cases."),
        ("Risk 2: External API Rate Limits", "Graceful degradation: If external search engines fail, local regex scam heuristics and on-device psychological deception scoring continue operating."),
        ("Risk 3: User Privacy & Surveillance", "Zero-storage architecture: SatyaSetu stores no phone numbers, no personal chat histories, and no contact books. All verification requests are stateless hashes."),
        ("Risk 4: Cloud Unit Economics", "Cost is $0.00 for 80% cached queries. Novel RAG syntheses consume < 500 tokens on Gemini Flash (~₹0.04/call), exceptionally viable via public CSR grants.")
    ]
    for idx, (r_head, r_text) in enumerate(risks):
        top_pos = 2.95 + (idx * 1.55)
        box = s4.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.95), Inches(top_pos), Inches(7.8), Inches(1.42))
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG_ALT
        box.line.color.rgb = C_BORDER
        box.line.width = Pt(1.2)
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.12)
        p1 = tf.paragraphs[0]
        p1.alignment = PP_ALIGN.LEFT
        r_h = p1.add_run()
        r_h.text = f"🛡 {r_head}\n"
        r_h.font.bold = True
        r_h.font.size = Pt(12)
        r_h.font.color.rgb = C_BRAND
        r_t = p1.add_run()
        r_t.text = f"   {r_text}"
        r_t.font.size = Pt(11)
        r_t.font.color.rgb = C_BODY

    add_resource_link_footer(s4, [
        ("Benchmark Dataset (test_dataset.json)", "https://github.com/srijansrivastava1234/SatyaSetu/blob/main/test_dataset.json"),
        ("Live Deployed Verification Endpoint", deployed_url),
        ("FastAPI Automated Test Suite", "https://github.com/srijansrivastava1234/SatyaSetu/blob/main/backend/test_system.py")
    ])

    # =========================================================================
    # SLIDE 5: IMPACT AND BENEFITS (GRASSROOTS SCALE & VIRAL SROI)
    # =========================================================================
    s5 = prs.slides[4]
    for s in list(s5.shapes):
        if s.name in ["TextBox 20", "TextBox 21", "Group 12", "Group 14"]:
            remove_element(s)
        elif s.name == "TextBox 17": # Title
            s.left = Inches(4.5)
            s.top = Inches(1.4)
            s.width = Inches(11.0)
            s.height = Inches(0.7)
            s.text_frame.text = ""
            p = s.text_frame.paragraphs[0]
            p.text = "IMPACT AND BENEFITS (GRASSROOTS SCALE)"
            p.font.name = "Arial"
            p.font.size = Pt(21)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.alignment = PP_ALIGN.CENTER
        elif s.name == "TextBox 22": # Team name in oval
            s.text_frame.text = ""
            s.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = s.text_frame.paragraphs[0]
            p.text = "Team SatyaSetu"
            p.font.name = "Arial"
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.alignment = PP_ALIGN.CENTER

    add_deployed_link_pill(s5, deployed_url, left_in=11.35, top_in=0.35, width_in=4.15, height_in=0.62)

    # Left Container: 3 Core Target Beneficiary Personas
    add_container_card(s5, 1.0, 2.35, 8.8, 7.05, "Target Beneficiaries & Grassroots Personas")
    personas = [
        ("Grassroots Tier-2/3 & Rural Citizens", [
            ("Scale", "500M+ First-time mobile smartphone users across Bharat."),
            ("Vulnerability", "Navigate exclusively via WhatsApp; cannot parse 1,500-word English fact-checks."),
            ("SatyaSetu Impact", "Instant visual truth badge delivered in under 15ms in vernacular Hindi.")
        ]),
        ("Senior Citizens & Pensioners", [
            ("Scale", "120M+ Older adults actively targeted by cyber fraud networks."),
            ("Vulnerability", "High-urgency utility disconnection threats ('Power cut tonight') & fake pension links."),
            ("SatyaSetu Impact", "Authoritative categorical verdict with zero technical jargon.")
        ]),
        ("Family & Community WhatsApp Admins", [
            ("Scale", "Millions of civic gatekeepers managing family and village groups."),
            ("Vulnerability", "Reluctant to challenge elder family members without official proof."),
            ("SatyaSetu Impact", "1-Click respectful counter-cards to neutralize false rumors peacefully.")
        ])
    ]
    for idx, (p_title, p_points) in enumerate(personas):
        top_pos = 3.0 + (idx * 2.05)
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.25), Inches(top_pos), Inches(8.3), Inches(1.85))
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG_ALT
        box.line.color.rgb = C_BORDER
        box.line.width = Pt(1.2)
        
        # Dedicated Header Box inside Persona Card
        hdr_box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.25), Inches(top_pos), Inches(8.3), Inches(0.42))
        hdr_box.fill.solid()
        hdr_box.fill.fore_color.rgb = RGBColor(238, 242, 255)
        hdr_box.line.color.rgb = C_BORDER_ACCENT
        hdr_box.line.width = Pt(1.0)
        tf_h = hdr_box.text_frame
        tf_h.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_h = tf_h.paragraphs[0]
        p_h.alignment = PP_ALIGN.LEFT
        p_h.margin_left = Inches(0.12)
        r_h = p_h.add_run()
        r_h.text = f"👥 {p_title}"
        r_h.font.bold = True
        r_h.font.size = Pt(11.5)
        r_h.font.color.rgb = C_BORDER_ACCENT

        # Points Box
        tb_pts = s5.shapes.add_textbox(Inches(1.4), Inches(top_pos + 0.45), Inches(8.0), Inches(1.35))
        tf_pts = tb_pts.text_frame
        tf_pts.vertical_anchor = MSO_ANCHOR.TOP
        tf_pts.word_wrap = True
        for pt_idx, (k, v) in enumerate(p_points):
            p_pt = tf_pts.paragraphs[0] if pt_idx == 0 else tf_pts.add_paragraph()
            p_pt.alignment = PP_ALIGN.LEFT
            p_pt.space_after = Pt(3)
            r_k = p_pt.add_run()
            r_k.text = f"• {k}: "
            r_k.font.bold = True
            r_k.font.size = Pt(10.5)
            r_k.font.color.rgb = C_TITLE
            r_v = p_pt.add_run()
            r_v.text = v
            r_v.font.size = Pt(10.5)
            r_v.font.color.rgb = C_BODY

    # Right Container: Viral Distribution Loop & Measurable Impact
    add_container_card(s5, 10.2, 2.35, 8.8, 7.05, "Organic 1-to-256 Viral Distribution Loop")
    loop_steps = [
        ("Step 1: Detection", "User suspects a viral forward and checks via SatyaSetu Web UI or Extension."),
        ("Step 2: Verification", "Engine generates a factual, objective counter-card in Hindi and English."),
        ("Step 3: Group Share", "User copies card into a 256-member WhatsApp group with one click."),
        ("Step 4: Network Immunity", "255 other group members are organically educated at zero acquisition cost.")
    ]
    for i, (st, desc) in enumerate(loop_steps):
        top_pos = 3.0 + (i * 0.96)
        box = s5.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(10.5), Inches(top_pos), Inches(8.2), Inches(0.82))
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG_ALT
        box.line.color.rgb = C_BRAND
        box.line.width = Pt(1.2)
        tf = box.text_frame
        tf.vertical_anchor = MSO_ANCHOR.MIDDLE
        tf.word_wrap = True
        tf.margin_left = Inches(0.18)
        tf.margin_right = Inches(0.18)
        tf.margin_top = Inches(0.06)
        tf.margin_bottom = Inches(0.06)
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.LEFT
        r1 = p.add_run()
        r1.text = f"▶ {st}: "
        r1.font.bold = True
        r1.font.size = Pt(11.5)
        r1.font.color.rgb = C_BRAND
        r2 = p.add_run()
        r2.text = desc
        r2.font.size = Pt(10.5)
        r2.font.color.rgb = C_BODY

    add_metric_callout(s5, 10.5, 7.2, 2.5, 1.8, "500M+", "REACHABLE CITIZENS IN BHARAT", color=C_BRAND)
    add_metric_callout(s5, 13.35, 7.2, 2.5, 1.8, "₹0", "FINANCIAL LOSS PER NEUTRALIZED SCAM", color=C_CRIMSON)
    add_metric_callout(s5, 16.2, 7.2, 2.5, 1.8, "100%", "BILINGUAL COVERAGE (HINDI & ENG)", color=C_EMERALD)

    add_resource_link_footer(s5, [
        ("PIB Fact Check Official Desk", "https://factcheck.pib.gov.in"),
        ("RBI Financial Fraud Awareness", "https://paisaboltahai.rbi.org.in"),
        ("Live Deployed Prototype", deployed_url)
    ])

    # =========================================================================
    # SLIDE 6: RESEARCH AND REFERENCES (STANDARDS & AUDIT TRAILS)
    # =========================================================================
    s6 = prs.slides[5]
    for s in list(s6.shapes):
        if s.name in ["TextBox 18", "TextBox 19", "Group 12"]:
            remove_element(s)
        elif s.name == "TextBox 15": # Title
            s.left = Inches(4.5)
            s.top = Inches(1.4)
            s.width = Inches(11.0)
            s.height = Inches(0.7)
            s.text_frame.text = ""
            p = s.text_frame.paragraphs[0]
            p.text = "RESEARCH AND REFERENCES"
            p.font.name = "Arial"
            p.font.size = Pt(21)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.alignment = PP_ALIGN.CENTER
        elif s.name == "TextBox 20": # Team name in oval
            s.text_frame.text = ""
            s.text_frame.vertical_anchor = MSO_ANCHOR.MIDDLE
            p = s.text_frame.paragraphs[0]
            p.text = "Team SatyaSetu"
            p.font.name = "Arial"
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = C_TITLE
            p.alignment = PP_ALIGN.CENTER

    add_deployed_link_pill(s6, deployed_url, left_in=11.35, top_in=0.35, width_in=4.15, height_in=0.62)

    # 3 Column Structured Table of Authoritative References
    add_container_card(s6, 1.0, 2.35, 18.0, 7.05, "Authoritative References, Standards & Academic Grounding")

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
        left_pos = 1.3 + (col_idx * 5.85)
        box = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(3.0), Inches(5.55), Inches(6.1))
        box.fill.solid()
        box.fill.fore_color.rgb = C_CARD_BG_ALT
        box.line.color.rgb = C_BORDER
        box.line.width = Pt(1.2)

        # Dedicated Column Header Bar
        col_hdr = s6.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left_pos), Inches(3.0), Inches(5.55), Inches(0.55))
        col_hdr.fill.solid()
        col_hdr.fill.fore_color.rgb = RGBColor(238, 242, 255)
        col_hdr.line.color.rgb = C_BRAND
        col_hdr.line.width = Pt(1.0)
        tf_ch = col_hdr.text_frame
        tf_ch.vertical_anchor = MSO_ANCHOR.MIDDLE
        p_ch = tf_ch.paragraphs[0]
        p_ch.alignment = PP_ALIGN.CENTER
        r_ch = p_ch.add_run()
        r_ch.text = col_title
        r_ch.font.bold = True
        r_ch.font.size = Pt(12.5)
        r_ch.font.color.rgb = C_BRAND_DARK

        # Column Content Textbox
        tb_col = s6.shapes.add_textbox(Inches(left_pos + 0.2), Inches(3.65), Inches(5.15), Inches(5.35))
        tf = tb_col.text_frame
        tf.vertical_anchor = MSO_ANCHOR.TOP
        tf.word_wrap = True

        for it_idx, (it_title, it_desc, it_url) in enumerate(items):
            p_item = tf.paragraphs[0] if it_idx == 0 else tf.add_paragraph()
            p_item.alignment = PP_ALIGN.LEFT
            if it_idx > 0:
                p_item.space_before = Pt(8)
            r_t = p_item.add_run()
            r_t.text = f"• {it_title}\n"
            r_t.font.bold = True
            r_t.font.size = Pt(11)
            r_t.font.color.rgb = C_TITLE

            r_d = p_item.add_run()
            r_d.text = f"  {it_desc}\n"
            r_d.font.size = Pt(10)
            r_d.font.color.rgb = C_MUTED

            r_u = p_item.add_run()
            r_u.text = f"  🔗 Link: {it_url.replace('https://', '')[:30]}..."
            r_u.font.size = Pt(10)
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
    print(f"[DeckBuilder] SUCCESS: Saved finalized diagrammatic pitch deck to {OUTPUT_PATH}")

if __name__ == "__main__":
    url_arg = sys.argv[1] if len(sys.argv) > 1 else "https://satyasetu-wtpy.onrender.com"
    build_presentation(url_arg)
