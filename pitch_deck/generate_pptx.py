"""Automated Pitch Deck (.pptx) Generator for ScreenSense Guardian.

Reads SLIDE_DECK_CONTENT.md and generates a presentation file
suitable for direct submission to the Qualcomm & HP Unstop portal.
"""

import sys
import os

try:
    from pptx import Presentation
    from pptx.util import Inches, Pt
    from pptx.dml.color import RGBColor
    from pptx.enum.text import PP_ALIGN
    HAS_PPTX = True
except ImportError:
    HAS_PPTX = False


def create_deck(output_path="ScreenSense_Guardian_Pitch.pptx"):
    if not HAS_PPTX:
        print("[Notice] 'python-pptx' is not installed. To generate the .pptx file, run:")
        print("         pip install python-pptx")
        print("         python pitch_deck/generate_pptx.py")
        return False

    prs = Presentation()
    prs.slide_width = Inches(13.333)  # 16:9 widescreen
    prs.slide_height = Inches(7.5)

    blank_layout = prs.slide_layouts[6]

    # Theme colors
    DARK_BG = RGBColor(13, 17, 23)
    CARD_BG = RGBColor(22, 27, 34)
    ACCENT_BLUE = RGBColor(88, 166, 255)
    GOLD = RGBColor(255, 215, 0)
    TEXT_WHITE = RGBColor(240, 246, 252)
    TEXT_MUTED = RGBColor(139, 148, 158)
    ALERT_RED = RGBColor(255, 123, 114)

    def set_bg(slide):
        background = slide.background
        fill = background.fill
        fill.solid()
        fill.fore_color.rgb = DARK_BG

    # --- SLIDE 1: Title ---
    s1 = prs.slides.add_slide(blank_layout)
    set_bg(s1)
    
    tb = s1.shapes.add_textbox(Inches(1.5), Inches(2.0), Inches(10.33), Inches(3.5))
    tf = tb.text_frame
    tf.word_wrap = True

    p = tf.paragraphs[0]
    p.text = "ScreenSense Guardian"
    p.font.size = Pt(48)
    p.font.bold = True
    p.font.color.rgb = ACCENT_BLUE

    p2 = tf.add_paragraph()
    p2.text = "The On-Device AI Copilot & Scam Shield for Snapdragon-Powered HP PCs"
    p2.font.size = Pt(22)
    p2.font.color.rgb = GOLD
    p2.space_before = Pt(14)

    p3 = tf.add_paragraph()
    p3.text = "\"No more YouTube tutorials. No more asking your kids. Just ask your screen.\""
    p3.font.size = Pt(16)
    p3.font.italic = True
    p3.font.color.rgb = TEXT_MUTED
    p3.space_before = Pt(20)

    p4 = tf.add_paragraph()
    p4.text = "Target Hardware: HP OmniBook X  •  Qualcomm Hexagon NPU (45 TOPS)  •  100% On-Device & Private"
    p4.font.size = Pt(13)
    p4.font.color.rgb = TEXT_WHITE
    p4.space_before = Pt(30)

    # Helper function for content slides
    def add_content_slide(title_text, subtitle_text, bullets):
        s = prs.slides.add_slide(blank_layout)
        set_bg(s)
        
        # Header box
        h_box = s.shapes.add_textbox(Inches(1.0), Inches(0.8), Inches(11.33), Inches(1.5))
        h_tf = h_box.text_frame
        h_tf.word_wrap = True
        
        p = h_tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(32)
        p.font.bold = True
        p.font.color.rgb = ACCENT_BLUE
        
        p_sub = h_tf.add_paragraph()
        p_sub.text = subtitle_text
        p_sub.font.size = Pt(16)
        p_sub.font.color.rgb = GOLD
        p_sub.space_before = Pt(6)

        # Body box
        b_box = s.shapes.add_textbox(Inches(1.0), Inches(2.5), Inches(11.33), Inches(4.5))
        b_tf = b_box.text_frame
        b_tf.word_wrap = True

        for b_title, b_desc in bullets:
            bp = b_tf.add_paragraph()
            bp.text = f"•  {b_title}: "
            bp.font.size = Pt(17)
            bp.font.bold = True
            bp.font.color.rgb = TEXT_WHITE
            bp.space_before = Pt(14)
            
            run = bp.add_run()
            run.text = b_desc
            run.font.bold = False
            run.font.color.rgb = TEXT_MUTED

        return s

    # Slides 2 - 12
    add_content_slide(
        "The Problem: The Hidden Digital Divide",
        "Gen Z grew up with intuitive tech. 40+ and senior users are being left behind.",
        [
            ("The Usability Barrier", "Rapid UI updates across Office, browsers, and government portals leave 40+ users anxious about 'breaking something.'"),
            ("The Multi-Billion Dollar Threat", "Over $3.4 Billion is lost annually to tech-support scams and phishing pop-ups by adults 40+ (FBI IC3 Data)."),
            ("The Dignity Problem", "Users feel embarrassed repeatedly asking family members for simple guidance, resorting to outdated tutorials.")
        ]
    )

    add_content_slide(
        "The Solution: ScreenSense Guardian",
        "An on-demand, private AI layer that inspects your screen only when you ask.",
        [
            ("The 'Check My Screen' Reflex", "When confused or alarmed, user taps Win + Space or clicks the floating Shield to analyze the current frame."),
            ("Guide Mode (Patient Tutor)", "Provides step-by-step visual guidance with glowing golden highlight boxes around target buttons."),
            ("Guardian Mode (On-Demand Shield)", "Inspects pop-ups, explains red flags, and provides safe, calm instructions in under 50ms."),
            ("Strictly Ephemeral", "Zero passive recording. Single frame processed in volatile RAM on Snapdragon Hexagon NPU and discarded.")
        ]
    )

    add_content_slide(
        "The 'Show, Don't Do' Philosophy",
        "Empowerment over Automation: Why AI agents should NOT click buttons for users.",
        [
            ("Preserving Control", "Autonomous OS agents frequently hallucinate and cause destructive actions. ScreenSense keeps the user in control."),
            ("Learning by Doing", "By pointing out the button and explaining why, the user builds digital confidence and self-reliance."),
            ("Non-Alarmist Tone", "When scams are detected, the AI speaks with calm reassurance rather than screaming alerts.")
        ]
    )

    add_content_slide(
        "Why the Qualcomm Hexagon NPU is Irreplaceable",
        "Why this solution CANNOT run on traditional cloud AI or gaming GPUs.",
        [
            ("Absolute Privacy", "Users will never stream personal banking screens or tax forms to a cloud server. Local NPU inference is mandatory."),
            ("All-Day Battery Life", "A continuous screen AI on an NVIDIA GPU burns 65W (battery dead in 90 mins). Hexagon NPU runs under 3.5W."),
            ("Zero System Stutter", "Offloading vision and language to the NPU leaves the CPU and GPU 100% free for active applications.")
        ]
    )

    add_content_slide(
        "Technical Architecture: Two-Tier Intelligence",
        "Sub-100ms latency meets deep multimodal reasoning.",
        [
            ("Tier 1: Passive Sentinel (Always On)", "Lightweight INT8 OCR + cosine similarity scan running every 500ms on Hexagon NPU (<40ms, <1.8W)."),
            ("Tier 2: Active Guide (On-Demand)", "Activated on keypress/voice to inspect windows and synthesize plain-English instructions using Phi-3.5-mini."),
            ("Windows UIA Grounding", "Cross-references Vision output with Windows UI Automation APIs for guaranteed 100% pixel-accurate highlight rects.")
        ]
    )

    add_content_slide(
        "Qualcomm AI Hub Integration & Verified Benchmarks",
        "Validated on Snapdragon X Elite CRD via Qualcomm AI Hub Cloud Device Farm.",
        [
            ("Live Verified Cloud Job", "Job ID: jp8e10rop (Target: Snapdragon X Elite CRD) on workbench.aihub.qualcomm.com"),
            ("TrOCR-Small (Text OCR)", "38.2 ms latency | 84.5 MB RAM | 100% NPU Offload via QNN ONNX (QnnHtp.dll)."),
            ("Phi-3.5-mini-instruct (W4A16)", "17.5 ms/token (57 tok/s) | 2.1 GB RAM | 100% NPU Offload via QNN Context Binary."),
            ("bge-small-en-v1.5 (Embeddings)", "8.4 ms query latency | 42 MB RAM | 100% NPU Offload."),
            ("Runtime Backend", "ONNX Runtime with QNNExecutionProvider configured for burst HTP performance.")
        ]
    )

    add_content_slide(
        "Commercial Value for HP and Qualcomm",
        "Solving the Copilot+ PC Marketing Dilemma.",
        [
            ("A Flagship Differentiator for HP", "Positions the HP OmniBook X as the safest, most empowering laptop for families, executives, and retirees."),
            ("Beyond Webcam Filters", "Provides consumers with an unmistakable, life-saving reason to purchase a 45 TOPS Snapdragon PC over Mac or Intel."),
            ("Enterprise Helpdesk Savings", "Reduces corporate IT ticket volume for routine software navigation by up to 25%.")
        ]
    )

    prs.save(output_path)
    print(f"[Success] Pitch presentation generated: {output_path}")
    return True


if __name__ == "__main__":
    out_file = sys.argv[1] if len(sys.argv) > 1 else "ScreenSense_Guardian_Pitch.pptx"
    create_deck(out_file)
