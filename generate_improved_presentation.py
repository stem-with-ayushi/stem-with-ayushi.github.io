import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml import parse_xml
import os

def build_master_deck():
    prs = Presentation()
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- SLIDE TRANSITION HELPER ---
    def add_transition(slide, t_type="fade", speed="med", direction="l"):
        # Remove any existing transition elements to prevent duplicates
        for child in list(slide._element):
            if child.tag.endswith('transition'):
                slide._element.remove(child)
        if t_type == "fade":
            xml = f'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="{speed}"><p:fade/></p:transition>'
        elif t_type == "push":
            xml = f'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="{speed}"><p:push dir="{direction}"/></p:transition>'
        elif t_type == "wipe":
            xml = f'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="{speed}"><p:wipe dir="{direction}"/></p:transition>'
        elif t_type == "split":
            xml = f'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="{speed}"><p:split orient="horz"/></p:transition>'
        else:
            xml = f'<p:transition xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main" spd="{speed}"><p:fade/></p:transition>'
        slide._element.append(parse_xml(xml))

    # --- COLOR SYSTEM ---
    NAVY = RGBColor(15, 23, 42)        # #0F172A
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(248, 250, 252)  # #F8FAFC
    CARD_BORDER = RGBColor(203, 213, 225) # #CBD5E1
    TEXT_MAIN = RGBColor(15, 23, 42)
    TEXT_MUTED = RGBColor(100, 116, 139) # #64748B
    
    # Tag Colors
    TAG_TEAL = RGBColor(13, 148, 136)   # #0D9488
    TAG_PURPLE = RGBColor(139, 92, 246) # #8B5CF6
    TAG_BLUE = RGBColor(37, 99, 235)    # #2563EB
    TAG_AMBER = RGBColor(245, 158, 11)  # #F59E0B
    TAG_CORAL = RGBColor(239, 68, 68)   # #EF4444
    TAG_GREEN = RGBColor(16, 185, 129)  # #10B981

    def add_footer(slide, text="Unit 1 · Chemical Models & Energy in Reactions · Grade 10 MYP 5 Sciences · OIS SCI 10.ABC-DS.1–6"):
        tx = slide.shapes.add_textbox(Inches(0.6), Inches(7.1), Inches(12.133), Inches(0.3))
        tf = tx.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED

    def add_header(slide, tag_text, tag_color, title_text, subtitle_text=None):
        tag_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.42), Inches(2.4), Inches(0.35))
        tag_box.fill.solid()
        tag_box.fill.fore_color.rgb = tag_color
        tag_box.line.color.rgb = tag_color
        tf = tag_box.text_frame
        p = tf.paragraphs[0]
        p.text = tag_text.upper()
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

        title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.82), Inches(12.133), Inches(0.65))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(21)
        p.font.bold = True
        p.font.color.rgb = NAVY

        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.6), Inches(1.4), Inches(12.133), Inches(0.4))
            tf = sub_box.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = subtitle_text
            p.font.size = Pt(11.5)
            p.font.italic = True
            p.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title, items, header_color=None, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        if header_color:
            hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.5))
            hdr.fill.solid()
            hdr.fill.fore_color.rgb = header_color
            hdr.line.color.rgb = header_color
            tf = hdr.text_frame
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(12)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.LEFT
            content_top = top + Inches(0.58)
            content_height = height - Inches(0.68)
            first = True
        else:
            content_top = top + Inches(0.12)
            content_height = height - Inches(0.24)
            first = False

        tx = slide.shapes.add_textbox(left + Inches(0.2), content_top, width - Inches(0.4), content_height)
        tf = tx.text_frame
        tf.word_wrap = True
        
        if not header_color:
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = NAVY
            p.space_after = Pt(4)

        for item in items:
            p = tf.add_paragraph() if not first else tf.paragraphs[0]
            first = False
            p.text = item
            p.font.size = Pt(10)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(3)

    def add_button(slide, left, top, width, height, icon_text, label_text, url=None, bg_color=TAG_BLUE):
        btn = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        btn.fill.solid()
        btn.fill.fore_color.rgb = bg_color
        btn.line.color.rgb = bg_color
        tf = btn.text_frame
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        run = p.add_run()
        run.text = f"{icon_text}  {label_text}"
        run.font.size = Pt(10.5)
        run.font.bold = True
        run.font.color.rgb = WHITE
        if url:
            run.hyperlink.address = url

    def set_notes(slide, notes_text):
        notes_slide = slide.notes_slide
        tf = notes_slide.notes_text_frame
        tf.text = notes_text

    # ==========================================
    # SLIDE 1: MASTER TITLE (Dark Navy Theme)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    tag_tx = s1.shapes.add_textbox(Inches(1.0), Inches(1.2), Inches(11.0), Inches(0.4))
    p = tag_tx.text_frame.paragraphs[0]
    p.text = "GRADE 10 · IB MYP YEAR 5 INTEGRATED SCIENCES · UNIT 1"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(96, 165, 250)

    t_tx = s1.shapes.add_textbox(Inches(1.0), Inches(1.7), Inches(11.0), Inches(1.6))
    p = t_tx.text_frame.paragraphs[0]
    p.text = "Chemical Models & Energy in Reactions"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE

    sub_tx = s1.shapes.add_textbox(Inches(1.0), Inches(3.3), Inches(11.0), Inches(1.0))
    p = sub_tx.text_frame.paragraphs[0]
    p.text = "Sub-unit 1 · Periodic Table, Electron States & Bond Energy as the Foundation for Biological & Environmental Chemistry"
    p.font.size = Pt(16)
    p.font.color.rgb = RGBColor(251, 191, 36)

    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.5), Inches(8.5), Inches(0.75))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 58, 138)
    pill.line.color.rgb = RGBColor(59, 130, 246)
    p = pill.text_frame.paragraphs[0]
    p.text = "🎯 Summative Assessment Alignment: Criterion B (Inquiring & Designing) & Criterion C (Processing & Evaluating)"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    add_footer(s1)
    set_notes(s1, "TEACHER FACILITATION NOTES (SLIDE 1):\n• Purpose: Welcome students to Sub-Unit 1. Set the intellectual tone for MYP 5 (Grade 10).\n• Key Message: Emphasize that chemistry explains energy transformations in biology (digestion) and environment (acid rain).\n• Timing: 3-5 minutes introductory framing.")

    # ==========================================
    # SLIDE 2: UNIT OVERVIEW
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "UNIT OVERVIEW", TAG_TEAL, "Curriculum Scope & Target Learning Outcomes")
    add_card(s2, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.9), "Target Academic Standards (OIS I.SCI)", [
        "📌 10.ABC-DS.1: Outermost Electron States & Trends",
        "  Construct & revise explanations for acid-base and displacement outcomes based on valence electrons and periodic trends.",
        "",
        "📌 10.ABC-DS.2: Neutralization & Bond Energy Models",
        "  Model how H+ and OH- neutralization breaks/forms bonds, releasing net energy (ΔH = ΣBonds_broken - ΣBonds_formed).",
        "",
        "📌 10.ABC-DS.3: Characteristic Reactions of Acids & Bases",
        "  Predict products of acids with metals, bases, and carbonates, plus bases with ammonium salts (NH3 gas).",
        "",
        "📌 10.ABC-DS.4: Indicators, pH Scale & [H+] Ions",
        "  Compare [H+] concentrations using litmus, phenolphthalein, methyl orange, universal indicator, and digital probes.",
        "",
        "📌 10.ABC-DS.5: Volumetric Titrations & Stoichiometry",
        "  Perform precision titrations using burettes and pipettes; calculate unknown solution concentrations.",
        "",
        "📌 10.ABC-DS.6: Conservation of Mass in Reactions",
        "  Use balanced equations & molar mass to prove mass conservation during acid-carbonate gas evolution."
    ])
    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.8), Inches(4.9), "Inquiry Pedagogy & Assessment", [
        "🧠 Visual Thinking Routines (Harvard Project Zero):",
        "  • See-Think-Wonder: Digestive pH & chemical homeostasis.",
        "  • Claim – Support – Question: Acid reactivity and single displacement.",
        "  • Zoom In: Macroscopic neutralization → atomic valence shells.",
        "  • Red Light, Yellow Light, Green Light: Experimental error analysis.",
        "  • Generate – Sort – Connect – Elaborate: Master concept synthesis.",
        "",
        "🤝 Collaborative Jigsaw Activity:",
        "  • Peer expert groups investigating Group 1, Group 2, and Group 17 displacement kinetics.",
        "",
        "🎯 Final Summative Assessment:",
        "  • Criterion B: Designing an enthalpy of neutralization calorimeter experiment.",
        "  • Criterion C: Processing experimental thermochemical data, identifying deliberate anomalies, calculating ΔH_neut, and evaluating method limitations."
    ])
    add_footer(s2)
    set_notes(s2, "TEACHER FACILITATION NOTES (SLIDE 2):\n• Walk students through the 6 standards. Highlight how these standards progress logically from valence electrons to thermochemical calorimetry.")

    # ==========================================
    # SLIDE 3: MYP FRAMEWORK
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "MYP FRAMEWORK", TAG_PURPLE, "Statement of Inquiry & Guiding Questions")
    soi_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.6), Inches(12.0), Inches(1.1))
    soi_box.fill.solid()
    soi_box.fill.fore_color.rgb = NAVY
    soi_box.line.color.rgb = RGBColor(59, 130, 246)
    p = soi_box.text_frame.paragraphs[0]
    p.text = '“Models of atomic electron configuration and chemical bond energy allow scientists to predict reaction dynamics and engineer solutions for environmental and biological energy transformations.”'
    p.font.size = Pt(13.5)
    p.font.italic = True
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    add_card(s3, Inches(0.6), Inches(2.9), Inches(3.8), Inches(1.6), "KEY CONCEPT", [
        "Change",
        "Chemical reactions represent fundamental reconfigurations of matter and electron transfer."
    ], header_color=TAG_BLUE)

    add_card(s3, Inches(4.7), Inches(2.9), Inches(3.8), Inches(1.6), "RELATED CONCEPTS", [
        "Energy · Models · Evidence",
        "Quantifying enthalpy changes and using sub-microscopic bonding models backed by empirical data."
    ], header_color=TAG_TEAL)

    add_card(s3, Inches(8.8), Inches(2.9), Inches(3.8), Inches(1.6), "GLOBAL CONTEXT", [
        "Scientific & Technical Innovation",
        "How understanding acid-base neutralization drives medicine (antacids) and industrial green chemistry."
    ], header_color=TAG_PURPLE)

    q_data = [
        ("FACTUAL", TAG_CORAL, "Which subatomic particles determine whether an element displaces another or donates a proton?"),
        ("CONCEPTUAL", TAG_AMBER, "How does the breaking and forming of chemical bonds govern whether an acid reaction releases or absorbs thermal energy?"),
        ("DEBATABLE", TAG_PURPLE, "Can simple laboratory models adequately predict and mitigate complex environmental chemical crises like ocean acidification?")
    ]
    for idx, (q_tag, q_col, q_text) in enumerate(q_data):
        top_y = Inches(4.7 + idx * 0.75)
        tag_s = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), top_y, Inches(2.0), Inches(0.6))
        tag_s.fill.solid()
        tag_s.fill.fore_color.rgb = q_col
        tag_s.line.color.rgb = q_col
        p = tag_s.text_frame.paragraphs[0]
        p.text = q_tag
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

        tx_s = s3.shapes.add_textbox(Inches(2.8), top_y, Inches(9.8), Inches(0.6))
        p = tx_s.text_frame.paragraphs[0]
        p.text = q_text
        p.font.size = Pt(11.5)
        p.font.color.rgb = TEXT_MAIN
    add_footer(s3)
    set_notes(s3, "TEACHER FACILITATION NOTES (SLIDE 3):\n• Statement of Inquiry: Ask students to identify how digestive antacids and industrial limestone scrubbers connect to 'Energy, Models, Evidence'.")

    # ==========================================
    # SLIDE 4: INTERACTIVE LABS & SIMULATIONS HUB
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "LEARNING EXPERIENCE", TAG_TEAL, "Interactive Digital Simulations & Video Library", "Click any button during lessons to launch interactive simulations and video models")

    add_card(s4, Inches(0.6), Inches(1.8), Inches(5.8), Inches(3.6), "Interactive Simulations (PhET & Virtual Chem)", [
        "🧪 PhET: Acid-Base Solutions (Standard 10.ABC-DS.4)",
        "  Investigate how strong vs weak acids dissociate. Compare [H3O+] vs [OH-] equilibrium concentrations.",
        "",
        "🔥 PhET: Energy Forms and Changes (Standard 10.ABC-DS.2)",
        "  Track thermal energy transfer into surrounding water during bond restructuring.",
        "",
        "⚖️ ChemCollective: Virtual Acid-Base Titration Lab (Standard 10.ABC-DS.5)",
        "  Standardize unknown HCl using 0.100 M NaOH with phenolphthalein indicator. Practice reading meniscus.",
        "",
        "⚛️ PhET: Reactants, Products & Leftovers (Standard 10.ABC-DS.6)",
        "  Simulate limiting reagents and mass conservation during gas evolution."
    ], header_color=TAG_TEAL)

    add_card(s4, Inches(6.8), Inches(1.8), Inches(5.8), Inches(3.6), "Video Demonstrations & Pre-Lab Briefings", [
        "🎥 Video 1: Single Displacement & The Activity Series (L2)",
        "  Observe electron transfer between zinc/magnesium and copper(II) sulfate solutions under high magnification.",
        "",
        "🎥 Video 2: Characteristic Acid Gas Tests (L3–L4)",
        "  The 'Squeaky Pop' test for H2, Limewater effervescence for CO2, and damp red litmus for NH3 gas.",
        "",
        "🎥 Video 3: Analytical Titration Technique & Error Avoidance (L7)",
        "  Step-by-step masterclass: rinsing burettes, removing air bubbles, detecting faint pink endpoint.",
        "",
        "🎥 Video 4: Coffee-Cup Calorimetry of Neutralization (L11–L12)",
        "  Measuring temperature evolution ΔT to calculate molar enthalpy ΔH_neut."
    ], header_color=TAG_BLUE)

    # Clickable Launch Buttons at bottom of Slide 4
    add_button(s4, Inches(0.6), Inches(5.7), Inches(3.8), Inches(0.9), "🧪 LAUNCH", "PhET: Acid-Base Solutions", "https://phet.colorado.edu/en/simulations/acid-base-solutions", TAG_TEAL)
    add_button(s4, Inches(4.7), Inches(5.7), Inches(3.8), Inches(0.9), "🔥 LAUNCH", "PhET: Energy Forms & Bonds", "https://phet.colorado.edu/en/simulations/energy-forms-and-changes", TAG_CORAL)
    add_button(s4, Inches(8.8), Inches(5.7), Inches(3.8), Inches(0.9), "⚖️ LAUNCH", "ChemCollective Titration", "https://chemcollective.org/activities/vlab/1", TAG_BLUE)
    add_footer(s4)
    set_notes(s4, "TEACHER FACILITATION NOTES (SLIDE 4):\n• Pre-Lab Instructions: All 3 buttons at the bottom are clickable and launch the virtual labs directly in Chrome.\n• Ensure students test PhET Acid-Base Solutions before Lesson 6.")

    # ==========================================
    # SLIDE 5: VTR 1 - SEE, THINK, WONDER (WITH DIGESTIVE DIAGRAM)
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "VISUAL THINKING ROUTINE", TAG_PURPLE, "See – Think – Wonder: Digestive Chemistry & Acid Homeostasis", "Routine: Observe the phenomenon, make inferences, and generate testable questions")

    add_card(s5, Inches(0.6), Inches(1.8), Inches(6.0), Inches(4.2), "Inquiry Prompts & Observations", [
        "👁️ What do you SEE?",
        "• Gastric juice has pH 1.5 – 2.0 (concentrated HCl).",
        "• Pancreatic juice rapidly raises pH to 7.8 – 8.0 in the duodenum.",
        "",
        "💭 What do you THINK is happening?",
        "• Pancreas secretes bicarbonate (NaHCO₃) to neutralize acid:",
        "  HCl(aq) + NaHCO₃(aq) → NaCl(aq) + H₂O(l) + CO₂(g)",
        "• Protects intestinal enzymes (trypsin, lipase) from denaturing.",
        "",
        "❓ What does it make you WONDER?",
        "• How do commercial antacids chemically mimic this system?",
        "• Does neutralizing stomach acid release thermal energy inside us?"
    ], header_color=TAG_BLUE)

    # Insert Digestive System Homeostasis Diagram on Right
    if os.path.exists("visual_digestive_homeostasis.png"):
        s5.shapes.add_picture("visual_digestive_homeostasis.png", Inches(6.8), Inches(1.8), Inches(5.8), Inches(4.2))

    ex_box = s5.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(6.1), Inches(12.0), Inches(0.85))
    ex_box.fill.solid()
    ex_box.fill.fore_color.rgb = RGBColor(240, 253, 244)
    ex_box.line.color.rgb = TAG_GREEN
    p = ex_box.text_frame.paragraphs[0]
    p.text = "Model Scientific Thinking: The stomach secretes HCl to denature proteins and kill pathogens. In the duodenum, sodium bicarbonate (NaHCO₃) neutralizes the acid: HCl + NaHCO₃ → NaCl + H₂O + CO₂. This chemical system maintains precise pH boundaries essential for enzyme kinetics."
    p.font.size = Pt(9.5)
    p.font.color.rgb = RGBColor(22, 101, 52)
    add_footer(s5)
    set_notes(s5, "TEACHER FACILITATION NOTES (SLIDE 5):\n• Protocol: Give students 2 minutes of silent writing for 'SEE'. Cold-call 3 students. Ensure they do NOT explain yet.\n• Move to 'THINK' (3 mins pair talk): push toward ionic equations.\n• Move to 'WONDER': collect questions for Criterion B.")

    # ==========================================
    # SLIDE 6: LESSON 1 - VALENCE ELECTRONS & TRENDS (WITH DIAGRAM)
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "LESSON 1 · STANDARD 10.ABC-DS.1", TAG_BLUE, "Valence Electron States & Periodic Reactivity Trends", "Inquiry: How do outermost electron configurations govern single displacement and acid reactivity?")

    add_card(s6, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.9), "Atomic Models & Electron Transfer Rules", [
        "🔑 Outermost Electrons Rule Reactivity:",
        "• Chemical reactivity is determined by valence electrons (electrons in the highest energy level).",
        "• Atoms react to achieve stable, low-energy noble gas configurations (full octet).",
        "",
        "⚡ Metals (Cation Formers):",
        "• Have 1, 2, or 3 valence electrons.",
        "• React by losing electrons (oxidation): M(s) -> M^n+(aq) + n e-",
        "• Low electronegativity and low first ionization energy.",
        "",
        "⬇️ Down Group 1 & 2: Metallic Reactivity INCREASES",
        "• Atomic radius increases; outer electrons occupy shells further from nucleus.",
        "• Increased electron shielding weakens nuclear electrostatic pull.",
        "• Valence electrons are lost far more easily (e.g. K > Na > Li).",
        "",
        "➡️ Across a Period (Left to Right): Metallic Reactivity DECREASES",
        "• Nuclear charge (protons) increases while shielding remains constant.",
        "• Stronger electrostatic attraction pulls valence electrons closer, binding them tightly."
    ], header_color=TAG_BLUE)

    # Insert Periodic Trends Diagram
    if os.path.exists("diagram_periodic_trends.png"):
        s6.shapes.add_picture("diagram_periodic_trends.png", Inches(6.8), Inches(1.8), Inches(5.8), Inches(3.2))

    # Add Simulation Launch button
    add_button(s6, Inches(6.8), Inches(5.2), Inches(5.8), Inches(0.7), "🧪 INTERACTIVE SIMULATION", "PhET: Build an Atom & Periodic Trends", "https://phet.colorado.edu/en/simulations/build-an-atom", TAG_TEAL)

    # Callout formula
    pf_box = s6.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(6.8), Inches(6.0), Inches(5.8), Inches(0.8))
    pf_box.fill.solid()
    pf_box.fill.fore_color.rgb = RGBColor(254, 243, 199)
    pf_box.line.color.rgb = TAG_AMBER
    p = pf_box.text_frame.paragraphs[0]
    p.text = "Activity Series Rule: Zn(s) + 2HCl(aq) -> ZnCl2(aq) + H2(g) [REACTION]\nCu(s) + HCl(aq) -> NO REACTION (Cu has higher ionization energy than H!)"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(146, 64, 14)
    add_footer(s6)
    set_notes(s6, "TEACHER FACILITATION NOTES (SLIDE 6):\n• Direct Instruction: Point to the embedded diagram showing the two opposing gradient arrows.\n• Ask: 'Why does metallic character increase towards the bottom-left (Fr/Cs) while non-metallic character increases towards the top-right (F)?'\n• Emphasize that ionization energy measures the energy needed to REMOVE an electron.")

    # ==========================================
    # SLIDE 7: JIGSAW ACTIVITY (10.ABC-DS.1)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "COLLABORATIVE LEARNING", TAG_PURPLE, "Jigsaw Activity: The Great Electron & Reactivity Showdown", "Format: 10 mins in Expert Groups -> 15 mins in Home Jigsaw Groups to synthesize")

    add_card(s7, Inches(0.6), Inches(1.8), Inches(2.8), Inches(4.8), "Group 1: Alkali Metals (Gp 1)", [
        "👥 Expert Focus: Li vs Na vs K",
        "",
        "• Electron config: [He]2s1, [Ne]3s1, [Ar]4s1.",
        "• Analyze reaction vigor with water/acid.",
        "• Explain why K reacts explosively while Li reacts steadily using atomic radius and shielding.",
        "• Write ionic half-equations for electron loss: K -> K+ + e-."
    ], header_color=TAG_CORAL)

    add_card(s7, Inches(3.6), Inches(1.8), Inches(2.8), Inches(4.8), "Group 2: Alk. Earth (Gp 2)", [
        "👥 Expert Focus: Mg vs Ca",
        "",
        "• Electron config: 2 valence electrons.",
        "• Compare first + second ionization energies.",
        "• Why does calcium displace H+ from cold water, but magnesium requires warm water or acid?",
        "• Model electron transfer to form M2+ cations."
    ], header_color=TAG_AMBER)

    add_card(s7, Inches(6.6), Inches(1.8), Inches(2.8), Inches(4.8), "Group 3: Halogens (Gp 17)", [
        "👥 Expert Focus: Cl2 vs Br2 vs I2",
        "",
        "• Electron config: 7 valence electrons.",
        "• Why does non-metal reactivity DECREASE down the group? (Opposite of metals!)",
        "• Model halogen displacement:",
        "  Cl2(aq) + 2 KBr(aq) -> 2 KCl(aq) + Br2(aq)",
        "• Which species is reduced?"
    ], header_color=TAG_TEAL)

    add_card(s7, Inches(9.6), Inches(1.8), Inches(2.8), Inches(4.8), "Group 4: Transition Metals", [
        "👥 Expert Focus: Zn vs Fe vs Cu",
        "",
        "• Variable valency and reactivity plateau.",
        "• Investigate displacement of Cu2+ ions by Zinc granules (blue color fades, copper deposits).",
        "• Explain why copper pipes are used for household plumbing instead of iron or zinc."
    ], header_color=TAG_BLUE)
    add_footer(s7)
    set_notes(s7, "TEACHER FACILITATION NOTES (SLIDE 7):\n• Jigsaw Logistics: 10 mins expert study, 15 mins peer teaching. Call on a student from Group 4 to explain Group 1's trend!")

    # ==========================================
    # SLIDE 8: CHECK FOR UNDERSTANDING - HINGE 1 (WITH DIAGRAM)
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "CHECK FOR UNDERSTANDING", TAG_AMBER, "Hinge Question 1: Predicting Single Displacement", "Show me: 1–4 fingers on 3-2-1")

    hq1_box = s8.shapes.add_textbox(Inches(0.6), Inches(1.8), Inches(12.0), Inches(0.7))
    p = hq1_box.text_frame.paragraphs[0]
    p.text = "A strip of solid Nickel (Ni) is placed into Copper(II) sulfate (CuSO₄). Nickel is above copper on the activity series. What is observed and what is the electron transfer?"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = NAVY

    opts_1 = [
        ("1", "No reaction occurs (copper is more electronegative).", False),
        ("2", "Brown Cu solid deposits; Ni loses 2e⁻ to Cu²⁺ ions.", True),
        ("3", "Nickel gains electrons, forming Ni²⁻ anions.", False),
        ("4", "Sulfate ions transfer electrons directly to Nickel.", False)
    ]

    for idx, (num, text, is_correct) in enumerate(opts_1):
        top_y = Inches(2.6 + idx * 0.75)
        opt_s = s8.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), top_y, Inches(6.0), Inches(0.68))
        opt_s.fill.solid()
        if is_correct:
            opt_s.fill.fore_color.rgb = RGBColor(240, 253, 244)
            opt_s.line.color.rgb = TAG_GREEN
            opt_s.line.width = Pt(2.0)
        else:
            opt_s.fill.fore_color.rgb = CARD_BG
            opt_s.line.color.rgb = CARD_BORDER

        circle = s8.shapes.add_shape(MSO_SHAPE.OVAL, Inches(0.75), top_y + Inches(0.12), Inches(0.42), Inches(0.42))
        circle.fill.solid()
        circle.fill.fore_color.rgb = TAG_AMBER
        circle.line.fill.background()
        p = circle.text_frame.paragraphs[0]
        p.text = num
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

        tx = s8.shapes.add_textbox(Inches(1.3), top_y + Inches(0.08), Inches(5.1), Inches(0.5))
        tf = tx.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(10)
        p.font.color.rgb = TEXT_MAIN

    # Insert Electron Leap Diagram on Right
    if os.path.exists("visual_electron_leap.png"):
        s8.shapes.add_picture("visual_electron_leap.png", Inches(6.8), Inches(2.6), Inches(5.8), Inches(3.0))

    ans1_box = s8.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(5.8), Inches(12.0), Inches(1.0))
    ans1_box.fill.solid()
    ans1_box.fill.fore_color.rgb = RGBColor(220, 252, 231)
    ans1_box.line.color.rgb = TAG_GREEN
    p = ans1_box.text_frame.paragraphs[0]
    p.text = "✔ Correct Answer: 2 (Brown copper solid forms; Ni loses 2e⁻ to Cu²⁺)."
    p.font.bold = True
    p.font.size = Pt(11)
    p.font.color.rgb = RGBColor(22, 101, 52)
    p2 = ans1_box.text_frame.add_paragraph()
    p2.text = "Diagnostic Rationale: Nickel has lower ionization energy and oxidizes: Ni(s) → Ni²⁺(aq) + 2e⁻. Dissolved Cu²⁺ ions accept these electrons and reduce: Cu²⁺(aq) + 2e⁻ → Cu(s). Spectator sulfate ions remain unchanged."
    p2.font.size = Pt(9.5)
    p2.font.color.rgb = TEXT_MAIN

    add_footer(s8)
    set_notes(s8, "TEACHER FACILITATION NOTES (SLIDE 8):\n• Hinge Protocol: 30s think time, 3-2-1 show fingers. If >80% show '2', proceed; if not, re-teach oxidation/reduction half-equations.")

    # ==========================================
    # SLIDE 9: LESSON 2 - CHARACTERISTIC ACID REACTIONS (WITH DIAGRAM)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "LESSON 2 · STANDARD 10.ABC-DS.3", TAG_BLUE, "Characteristic Reactions of Acids & Confirmation Gas Tests", "Inquiry: How do acids behave predictably with metals, bases, and carbonates?")

    add_card(s9, Inches(0.6), Inches(1.8), Inches(3.8), Inches(2.3), "1. Acid + Metal", [
        "Acid + Metal -> Salt + H2(g)",
        "2 HCl(aq) + Zn(s) -> ZnCl2(aq) + H2(g)",
        "Ionic: 2H+ + Zn -> Zn2+ + H2"
    ], header_color=TAG_BLUE)

    add_card(s9, Inches(4.7), Inches(1.8), Inches(3.8), Inches(2.3), "2. Acid + Base", [
        "Acid + Base -> Salt + H2O(l)",
        "HCl(aq) + NaOH(aq) -> NaCl(aq) + H2O(l)",
        "Net Ionic: H+(aq) + OH-(aq) -> H2O(l)"
    ], header_color=TAG_TEAL)

    add_card(s9, Inches(8.8), Inches(1.8), Inches(3.8), Inches(2.3), "3. Acid + Carbonate", [
        "Acid + Carbonate -> Salt + H2O + CO2(g)",
        "2 HNO3 + CaCO3 -> Ca(NO3)2 + H2O + CO2",
        "Effervescent gas evolution"
    ], header_color=TAG_PURPLE)

    # Insert Gas Tests Diagram across the bottom
    if os.path.exists("diagram_gas_tests.png"):
        s9.shapes.add_picture("diagram_gas_tests.png", Inches(0.6), Inches(4.25), Inches(12.133), Inches(2.75))

    add_footer(s9)
    set_notes(s9, "TEACHER FACILITATION NOTES (SLIDE 9):\n• Visual Bridge: The bottom diagram visually outlines the 3 required qualitative gas tests (H2 pop test, CO2 limewater cloudiness, NH3 damp red litmus).\n• Have students sketch these 3 gas tests in their practical books.")

    # ==========================================
    # SLIDE 10: LESSON 2 (CONT) - BASES & AMMONIUM SALTS (10.ABC-DS.3)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "LESSON 2 (CONT) · STANDARD 10.ABC-DS.3", TAG_BLUE, "Reactions of Bases with Ammonium Salts", "Inquiry: What happens when an alkali reacts with an ammonium salt?")

    add_card(s10, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.8), "The Base-Ammonium Salt Reaction", [
        "🧪 General Equation:",
        "Base (Alkali) + Ammonium Salt -> Salt + Water + Ammonia Gas (NH3)",
        "",
        "Chemical Mechanism:",
        "• Ammonium ion (NH4+) is a weak conjugate acid.",
        "• Hydroxide ions (OH-) from strong bases strip a proton (H+) from NH4+:",
        "  NH4+(aq) + OH-(aq) -> NH3(g) + H2O(l)",
        "",
        "Key Example:",
        "  NaOH(aq) + NH4Cl(aq) --(heat)--> NaCl(aq) + H2O(l) + NH3(g)",
        "",
        "Agricultural & Environmental Context:",
        "• Why farmers must NEVER mix ammonium nitrate fertilizers with slaked lime (Ca(OH)2)—it releases nitrogen as volatile ammonia gas into the air, wasting expensive fertilizer!"
    ], header_color=TAG_AMBER)

    add_card(s10, Inches(6.8), Inches(1.8), Inches(5.8), Inches(4.8), "Confirmation & Testing for Ammonia (NH3)", [
        "🔬 Gas Confirmation Test:",
        "1. Damp Red Litmus Paper Test:",
        "  • Hold a strip of damp red litmus paper near the mouth of the reaction tube.",
        "  • Result: Turns blue! (Ammonia is the ONLY common alkaline gas).",
        "  • Why must the paper be DAMP? Ammonia gas dissolves in water to produce hydroxide ions:",
        "    NH3(g) + H2O(l) <-> NH4+(aq) + OH-(aq)",
        "",
        "2. Sensory / Odor Observation:",
        "  • Sharp, pungent, choking smell (smelling salts).",
        "",
        "3. Dense White Smoke Test (Extension):",
        "  • Bring a glass rod dipped in concentrated HCl near NH3 gas:",
        "  • NH3(g) + HCl(g) -> NH4Cl(s) (dense white fumes of ammonium chloride)."
    ], header_color=TAG_TEAL)
    add_footer(s10)
    set_notes(s10, "TEACHER FACILITATION NOTES (SLIDE 10):\n• Live Microscale Demo: Heat 0.5g of ammonium chloride with 1 mL of 1M NaOH. Hold damp red litmus over it.\n• Emphasize why dry litmus will fail.")

    # ==========================================
    # SLIDE 11: 4-STATION ROTATING LAB (10.ABC-DS.3)
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "INVESTIGATION", TAG_CORAL, "Inquiry Lab: 4 Rotating Characteristic Reaction Stations", "Protocol: Groups of 3–4 rotate every 8 minutes. Predict -> Test -> Record -> Explain.")

    st_data = [
        ("Station A: Acid + Metal", "Mg ribbon + 1.0 M HCl", "Collect gas with inverted boiling tube; test with burning splint for pop sound.", "2 HCl + Mg -> MgCl2 + H2", TAG_BLUE),
        ("Station B: Acid + Carbonate", "Solid CaCO3 + 1.0 M HNO3", "Deliver effervescing gas via delivery tube into limewater; observe cloudiness.", "2 HNO3 + CaCO3 -> Ca(NO3)2 + H2O + CO2", TAG_TEAL),
        ("Station C: Acid + Base", "Solid CuO + 1.0 M H2SO4 (warm)", "Warm black copper(II) oxide in dilute acid; observe blue copper sulfate solution.", "H2SO4 + CuO -> CuSO4 + H2O", TAG_AMBER),
        ("Station D: Base + Ammonium", "NH4Cl(s) + 1.0 M NaOH (gentle heat)", "Hold damp red litmus paper over mouth; observe rapid shift to blue.", "NaOH + NH4Cl -> NaCl + H2O + NH3", TAG_CORAL)
    ]

    for idx, (st_name, st_mat, st_inst, st_eq, st_col) in enumerate(st_data):
        col = idx % 2
        row = idx // 2
        left = Inches(0.6 + col * 6.1)
        top = Inches(1.8 + row * 2.5)

        add_card(s11, left, top, Inches(5.8), Inches(2.3), st_name, [
            f"🧪 Reagents: {st_mat}",
            f"📋 Action: {st_inst}",
            f"⚗️ Target Equation: {st_eq}"
        ], header_color=st_col)
    add_footer(s11)
    set_notes(s11, "TEACHER FACILITATION NOTES (SLIDE 11):\n• Safety: Goggles mandatory. Ensure water baths for Station C and good ventilation for Station D.")

    # ==========================================
    # SLIDE 12: LESSON 3 - THE pH SCALE (WITH VISUAL GRADIENT)
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "LESSON 3 · STANDARD 10.ABC-DS.4", TAG_BLUE, "The pH Scale, [H⁺] Concentration & Synthetic Indicators", "Inquiry: How do indicators and the logarithmic pH scale measure hydrogen ion concentration?")

    add_card(s12, Inches(0.6), Inches(1.8), Inches(5.8), Inches(2.4), "Logarithmic Nature of pH & Indicators", [
        "• pH = -log₁₀[H⁺]. 1 pH unit shift = TEN-FOLD (10×) change in [H⁺]!",
        "• pH 1 (Gastric juice) has 1,000,000× more H⁺ than neutral pH 7.",
        "• Phenolphthalein: Colorless (pH < 8.2) → Faint Pink (pH 8.2 – 10.0).",
        "• Litmus: Red (pH < 4.5) → Blue (pH > 8.3) | Methyl Orange: Red → Yellow."
    ], header_color=TAG_BLUE)

    # Insert Strong vs Weak Acid Dissociation Particle Diagram on Right
    if os.path.exists("visual_acid_dissociation.png"):
        s12.shapes.add_picture("visual_acid_dissociation.png", Inches(6.8), Inches(1.8), Inches(5.8), Inches(2.4))

    # Insert Visual pH Scale Diagram across bottom
    if os.path.exists("diagram_ph_scale.png"):
        s12.shapes.add_picture("diagram_ph_scale.png", Inches(0.6), Inches(4.35), Inches(12.133), Inches(2.65))

    add_footer(s12)
    set_notes(s12, "TEACHER FACILITATION NOTES (SLIDE 12):\n• Visual Inspection: Point out the real-world benchmarks on the embedded pH diagram (battery acid to drain cleaner).\n• Ask: 'Why is blood pH (7.4) slightly alkaline, and why does a drop to 7.2 cause medical acidosis?'")

    # ==========================================
    # SLIDE 13: LESSON 4 - VOLUMETRIC TITRATIONS (WITH APPARATUS DIAGRAM)
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "LESSON 4 · STANDARD 10.ABC-DS.5", TAG_BLUE, "Volumetric Analysis: Precision Acid-Base Titration Technique", "Inquiry: How do analytical chemists determine the exact concentration of an unknown solution?")

    add_card(s13, Inches(0.6), Inches(1.8), Inches(6.0), Inches(4.9), "Volumetric Glassware & Procedural Rigor", [
        "🔬 Precision Glassware Specifications:",
        "",
        "1. Class A Bulb Pipette (25.0 cm³ ± 0.03):",
        "  • Delivers single fixed volume of unknown acid.",
        "  • Rinse with deionized water, then rinse with the acid solution.",
        "",
        "2. Precision Burette (50.00 cm³ ± 0.05):",
        "  • Delivers standard titrant drop-by-drop.",
        "  • Read bottom of meniscus at eye level (avoid parallax).",
        "  • All initial/final readings recorded to TWO decimal places.",
        "  • Ensure jet tip is filled and free of air bubbles!",
        "",
        "📊 The Concordancy Rule:",
        "  • Rough trial excluded from average.",
        "  • Concordant titres must agree within ± 0.10 cm³.",
        "  • Mean Concordant Titre = Average of concordant trials only."
    ], header_color=TAG_TEAL)

    # Insert Titration Apparatus Diagram on Right
    if os.path.exists("diagram_titration_apparatus.png"):
        s13.shapes.add_picture("diagram_titration_apparatus.png", Inches(7.0), Inches(1.8), Inches(5.7), Inches(3.8))

    # Virtual Lab Button
    add_button(s13, Inches(7.0), Inches(5.8), Inches(5.7), Inches(0.8), "⚖️ VIRTUAL TITRATION LAB", "Launch ChemCollective Analytical Titration", "https://chemcollective.org/activities/vlab/1", TAG_BLUE)

    add_footer(s13)
    set_notes(s13, "TEACHER FACILITATION NOTES (SLIDE 13):\n• Apparatus Diagram: Walk through each labeled part of the titration rig (burette, stopcock, conical flask, white tile).\n• Direct students to click the ChemCollective virtual lab button for interactive pre-lab homework.")

    # ==========================================
    # SLIDE 14: TITRATION STOICHIOMETRY (WITH FLOWCHART INFOGRAPHIC)
    # ==========================================
    s14 = prs.slides.add_slide(blank_layout)
    add_header(s14, "LESSON 4 (CONT) · STANDARD 10.ABC-DS.5", TAG_BLUE, "Mastering Titration Stoichiometry Calculations", "Inquiry: Step-by-step mathematical algorithm to calculate unknown concentration")

    add_card(s14, Inches(0.6), Inches(1.8), Inches(12.0), Inches(2.6), "The 4-Step Analytical Algorithm", [
        "Problem: 25.0 cm³ of unknown HCl is neutralized by exactly 21.40 cm³ of 0.100 mol/dm³ standardized NaOH.",
        "1. Balanced Equation: HCl(aq) + NaOH(aq) → NaCl(aq) + H₂O(l)  [Mole Ratio 1 : 1]",
        "2. Moles of Known (NaOH): n = C × V = 0.100 mol/dm³ × (21.40 ÷ 1000 dm³) = 0.002140 mol.",
        "3. Mole Ratio: 1 : 1 ratio → n(HCl) = n(NaOH) = 0.002140 mol.",
        "4. Concentration of Unknown: C = n ÷ V = 0.002140 mol ÷ (25.0 ÷ 1000 dm³) = 0.0856 mol/dm³."
    ], header_color=TAG_BLUE)

    # Insert Titration 4-Step Pathway Infographic across bottom
    if os.path.exists("visual_titration_pathway.png"):
        s14.shapes.add_picture("visual_titration_pathway.png", Inches(0.6), Inches(4.5), Inches(12.0), Inches(2.5))

    add_footer(s14)
    set_notes(s14, "TEACHER FACILITATION NOTES (SLIDE 14):\n• 4-Step Protocol: Have students copy this as an algorithm into their revision notes. Common error is forgetting to divide volume by 1000.")

    # ==========================================
    # SLIDE 15: CONSERVATION OF MASS (WITH DUAL BALANCE DIAGRAM)
    # ==========================================
    s15 = prs.slides.add_slide(blank_layout)
    add_header(s15, "LESSON 5 · STANDARD 10.ABC-DS.6", TAG_BLUE, "Conservation of Mass & Gas Evolution Stoichiometry", "Inquiry: Why does mass appear to decrease when an acid reacts with a carbonate in an open beaker?")

    add_card(s15, Inches(0.6), Inches(1.8), Inches(6.0), Inches(4.9), "Mathematical Molar Mass Verification", [
        "⚖️ The Law of Conservation of Mass:",
        "Total mass of reactants = Total mass of products.",
        "",
        "Reaction: CaCO₃(s) + 2HCl(aq) → CaCl₂(aq) + H₂O(l) + CO₂(g)↑",
        "",
        "If 5.00 g of pure CaCO₃ reacts completely:",
        "1. Molar Mass: M(CaCO₃) = 100.09 g/mol | M(CO₂) = 44.01 g/mol",
        "2. Moles of CaCO₃: n = 5.00 ÷ 100.09 = 0.04996 mol",
        "3. Mole Ratio 1 : 1 → Moles of CO₂ evolved = 0.04996 mol",
        "4. Expected Mass of Escaped CO₂:",
        "   mass = n × M = 0.04996 mol × 44.01 g/mol = 2.20 g",
        "",
        "🎯 Experimental Verification:",
        "Open beaker reading drops by exactly 2.20 g as CO₂ escapes!"
    ], header_color=TAG_BLUE)

    # Insert Conservation of Mass Dual Balance Diagram on Right
    if os.path.exists("visual_conservation_mass.png"):
        s15.shapes.add_picture("visual_conservation_mass.png", Inches(6.8), Inches(1.8), Inches(5.8), Inches(4.9))

    add_footer(s15)
    set_notes(s15, "TEACHER FACILITATION NOTES (SLIDE 15):\n• Live Demo: Zero a balance with HCl and marble chips in an un-tipped test tube inside. Tip flask to mix, watch mass decrease live as CO2 escapes.")
    set_notes(s15, "TEACHER FACILITATION NOTES (SLIDE 15):\n• Live Demo: Zero a balance with HCl and marble chips in an un-tipped test tube inside. Tip flask to mix, watch mass decrease live as CO2 escapes.")

    # ==========================================
    # SLIDE 16: LESSON 6 - BOND ENERGY (WITH REACTION PROFILE DIAGRAM)
    # ==========================================
    s16 = prs.slides.add_slide(blank_layout)
    add_header(s16, "LESSON 6 · STANDARD 10.ABC-DS.2", TAG_BLUE, "Bond Energy Models & The Thermochemistry of Neutralization", "Inquiry: Why does neutralization always release thermal energy?")

    add_card(s16, Inches(0.6), Inches(1.8), Inches(6.0), Inches(4.9), "Bond Energy Energetics & Constant ΔH", [
        "🔥 The Fundamental Energetic Rule:",
        "1. Breaking chemical bonds REQUIRES energy (Endothermic, ΔH > 0).",
        "2. Forming chemical bonds RELEASES energy (Exothermic, ΔH < 0).",
        "",
        "Net Ionic Neutralization Reaction:",
        "  H+(aq) + OH-(aq) -> H2O(l)    ΔH = -57.1 kJ/mol",
        "",
        "Sub-Microscopic Mechanism:",
        "• H+ and OH- ions collide to form strong covalent O-H bonds.",
        "• More energy is released forming O-H bonds than was absorbed.",
        "• Excess energy transfers as heat to surrounding water molecules (T rises!).",
        "",
        "💡 Why Neutralization Enthalpy is Constant:",
        "• When ANY strong acid neutralizes ANY strong alkali, ΔH ≈ -57.1 kJ/mol.",
        "• Spectator ions (Na+, Cl-, K+, NO3-) do NOT participate in bonding!",
        "• The ONLY real reaction occurring is: H+(aq) + OH-(aq) -> H2O(l)."
    ], header_color=TAG_CORAL)

    # Insert Reaction Energy Profile Diagram on Right
    if os.path.exists("diagram_energy_profile.png"):
        s16.shapes.add_picture("diagram_energy_profile.png", Inches(7.0), Inches(1.8), Inches(5.7), Inches(3.6))

    # Add Simulation Launch button
    add_button(s16, Inches(7.0), Inches(5.6), Inches(5.7), Inches(0.8), "🔥 INTERACTIVE SIMULATION", "PhET: Energy Forms & Bond Changes", "https://phet.colorado.edu/en/simulations/energy-forms-and-changes", TAG_CORAL)

    add_footer(s16)
    set_notes(s16, "TEACHER FACILITATION NOTES (SLIDE 16):\n• Diagram Analysis: Point out the activation energy hump Ea (bond breaking) and the downward arrow showing net exothermic energy release (Delta H = -57.1 kJ/mol).\n• Students can launch the PhET simulation to visualize kinetic energy transfer.")

    # ==========================================
    # SLIDE 17: CRITERION B SUMMATIVE BRIEF
    # ==========================================
    s17 = prs.slides.add_slide(blank_layout)
    add_header(s17, "CRITERION B SUMMATIVE", TAG_BLUE, "Summative Task Brief: Calorimetric Lab Investigation Design", "Assessment: Criterion B (Inquiring & Designing) — Maximum Achievement Level 8")

    add_card(s17, Inches(0.6), Inches(1.8), Inches(12.0), Inches(5.0), "The Investigation Design Challenge", [
        "🎯 Research Scenario:",
        "  You are a chemical engineer tasked with determining the thermochemical efficiency of neutralization. You will independently design a complete scientific investigation to determine the relationship between reactant concentration and thermal energy release in a coffee-cup calorimeter.",
        "",
        "📋 Criterion B Assessment Requirements (What You Must Produce):",
        "  1. Strand i (Problem / Question): Formulate a focused, testable research question with clear quantitative boundaries.",
        "  2. Strand ii (Hypothesis): Formulate a testable hypothesis and explain it with detailed scientific reasoning using bond energies and collision theory.",
        "  3. Strand iii (Variables): Clearly define the Independent Variable (with at least 5 values), Dependent Variable (with instrument resolution), and at least 3 Controlled Variables (with control methods and rationale).",
        "  4. Strand iv (Design & Safety): Design a clear, logical, step-by-step numbered method including:",
        "     • Labeled apparatus diagram (coffee-cup calorimeter, magnetic stirrer, digital thermometer).",
        "     • Comprehensive risk assessment (hazards of acids/bases, thermal burns, emergency protocols).",
        "     • Protocol ensuring sufficient data reliability (minimum 3 repeat trials per condition)."
    ])
    add_footer(s17)
    set_notes(s17, "TEACHER FACILITATION NOTES (SLIDE 17):\n• Criterion B Task Brief: Supervised planning conditions. Differentiation: provide scaffolded planning matrices for Levels 1-4.")

    # ==========================================
    # SLIDE 18: CRITERION B VARIABLES (WITH CALORIMETER DIAGRAM)
    # ==========================================
    s18 = prs.slides.add_slide(blank_layout)
    add_header(s18, "EXPERIMENT DEVELOPMENT", TAG_CORAL, "Criterion B Exemplar: Variables Matrix & Testable Hypothesis")

    add_card(s18, Inches(0.6), Inches(1.8), Inches(6.8), Inches(4.0), "Variables Matrix (MYP 5 Standard)", [
        "1. Independent Variable (IV): [HCl] Concentration",
        "  • 5 values: 0.20, 0.40, 0.60, 0.80, 1.00 mol/dm³ via serial dilution.",
        "",
        "2. Dependent Variable (DV): Temperature Change (ΔT) & Heat (q)",
        "  • ΔT = T_max - T_initial (°C) logged using digital probe (±0.05 °C).",
        "  • Heat evolved: q = m · c · ΔT (where m = 50.0 g, c = 4.18 J/g·°C).",
        "",
        "3. Controlled Variables (CV):",
        "  • Total solution volume: Fixed at 50.0 cm³ using bulb pipettes.",
        "  • Alkali: Fixed 1.00 M NaOH (excess).",
        "  • Calorimeter insulation: Nested double polystyrene cups with lid."
    ], header_color=TAG_BLUE)

    # Insert Calorimeter Cross-Section Diagram on Right
    if os.path.exists("diagram_calorimeter.png"):
        s18.shapes.add_picture("diagram_calorimeter.png", Inches(7.7), Inches(1.8), Inches(5.0), Inches(4.0))

    hyp_b = s18.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(6.0), Inches(12.0), Inches(0.9))
    hyp_b.fill.solid()
    hyp_b.fill.fore_color.rgb = RGBColor(254, 243, 199)
    hyp_b.line.color.rgb = TAG_AMBER
    p = hyp_b.text_frame.paragraphs[0]
    p.text = "Exemplar Hypothesis: “If the concentration of HCl increases from 0.20 to 1.00 mol/dm³, then the temperature change (ΔT) will increase linearly, because more moles of H⁺ and OH⁻ ions react per unit volume to form water, releasing more thermal energy (q). However, the calculated molar enthalpy (ΔH) will remain constant at approx -57 kJ/mol because the net ionic bond-forming process (H⁺ + OH⁻ → H₂O) is fundamentally identical.”"
    p.font.size = Pt(9.5)
    p.font.bold = True
    p.font.color.rgb = RGBColor(146, 64, 14)
    add_footer(s18)
    set_notes(s18, "TEACHER FACILITATION NOTES (SLIDE 18):\n• Highlight how the embedded calorimeter diagram matches the required labeled apparatus diagram for Criterion B Strand iv.")

    # ==========================================
    # SLIDE 19: CRITERION C DATA PROCESSING & ANOMALIES
    # ==========================================
    s19 = prs.slides.add_slide(blank_layout)
    add_header(s19, "CRITERION C FOCUS", TAG_GREEN, "Criterion C Exemplar: Raw Data Table & Anomaly Screening")

    table_shape = s19.shapes.add_table(7, 6, Inches(0.6), Inches(1.8), Inches(12.0), Inches(3.2))
    table = table_shape.table

    hdrs = ["[HCl] / mol dm⁻³ (±0.02)", "T_initial / °C (±0.05)", "Trial 1: ΔT / °C", "Trial 2: ΔT / °C", "Trial 3: ΔT / °C", "Mean ΔT / °C (±0.1)"]
    for col_idx, h in enumerate(hdrs):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.CENTER

    d_rows = [
        ["0.20", "21.50", "1.30", "1.35", "1.25", "1.30"],
        ["0.40", "21.50", "2.65", "2.70", "2.60", "2.65"],
        ["0.60", "21.55", "3.95", "4.00", "3.90", "3.95"],
        ["0.80", "21.50", "5.25", "1.80*", "5.35", "5.30*"],
        ["1.00", "21.60", "6.60", "6.55", "6.65", "6.60"],
    ]

    for row_idx, row in enumerate(d_rows):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = val
            cell.fill.solid()
            if "*" in val:
                cell.fill.fore_color.rgb = RGBColor(254, 226, 226)
            else:
                cell.fill.fore_color.rgb = WHITE
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.alignment = PP_ALIGN.CENTER

    an_box = s19.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.3), Inches(12.0), Inches(1.5))
    an_box.fill.solid()
    an_box.fill.fore_color.rgb = RGBColor(254, 242, 242)
    an_box.line.color.rgb = TAG_CORAL
    p = an_box.text_frame.paragraphs[0]
    p.text = "⚠️ Anomaly Screening & Justification (Criterion C Strand i):"
    p.font.size = Pt(11.5)
    p.font.bold = True
    p.font.color.rgb = TAG_CORAL

    p2 = an_box.text_frame.add_paragraph()
    p2.text = "At 0.80 mol/dm³ HCl, Trial 2 recorded ΔT = 1.80 °C, which severely diverges from Trial 1 (5.25 °C) and Trial 3 (5.35 °C). This outlier was caused by failure to seat the calorimeter lid immediately, allowing warm convection currents to escape before the sensor equilibrated. This value is flagged as anomalous and excluded from the mean: Mean ΔT = (5.25 + 5.35) ÷ 2 = 5.30 °C."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MAIN
    add_footer(s19)
    set_notes(s19, "TEACHER FACILITATION NOTES (SLIDE 19):\n• Anomaly Management: Teach students that outliers must be explicitly flagged and justified, not quietly deleted.")

    # ==========================================
    # SLIDE 20: CRITERION C EVALUATION (VTR: RED/YELLOW/GREEN)
    # ==========================================
    s20 = prs.slides.add_slide(blank_layout)
    add_header(s20, "EXPERIMENT EVALUATION", TAG_PURPLE, "Evaluating Method Validity & Suggesting Improvements (Criterion C iv & v)", "Routine: Red Light, Yellow Light, Green Light for Scientific Error Analysis")

    add_card(s20, Inches(0.6), Inches(1.8), Inches(3.8), Inches(4.8), "🔴 Red Light: Systematic Errors", [
        "Major Flaws in Method Validity:",
        "",
        "1. Heat Loss to Surroundings:",
        "  • The polystyrene cup is not a perfect insulator; heat escaped through the probe hole.",
        "  • Effect: Measured ΔT is systematically lower than true value -> calculated ΔH is less exothermic than -57.1 kJ/mol.",
        "",
        "2. Heat Capacity of Solution:",
        "  • Assumed c = 4.18 J/g·°C and density = 1.00 g/cm³ like pure water. In reality, dissolved ions lower specific heat capacity."
    ], header_color=TAG_CORAL)

    add_card(s20, Inches(4.7), Inches(1.8), Inches(3.8), Inches(4.8), "🟡 Yellow Light: Limitations", [
        "Uncertainties & Experimental Noise:",
        "",
        "1. Probe Thermal Lag:",
        "  • Digital probe had a 4-second response time; peak temperature cooled slightly while probe registered.",
        "",
        "2. Room Temperature Fluctuations:",
        "  • Initial reactant temperatures varied by ± 0.3 °C between trials due to laboratory air conditioning cycles.",
        "",
        "3. Incomplete Mixing:",
        "  • Manual swirling caused uneven temperature distribution inside the cup."
    ], header_color=TAG_AMBER)

    add_card(s20, Inches(8.8), Inches(1.8), Inches(3.8), Inches(4.8), "🟢 Green Light: Specific Improvements", [
        "Realistic & Targeted Refinements:",
        "",
        "1. Extrapolate Cooling Curve:",
        "  • Record temperature every 15s for 3 min before mixing, mix, then record cooling curve for 5 min. Extrapolate back to t = 0 to determine true instantaneous T_max.",
        "",
        "2. Hardware Upgrade:",
        "  • Use a vacuum-jacketed silvered Dewar flask with a sealed magnetic stirrer.",
        "",
        "3. Calibration:",
        "  • Pre-determine the calorimeter heat capacity (C_cal) using electrical heating."
    ], header_color=TAG_GREEN)
    add_footer(s20)
    set_notes(s20, "TEACHER FACILITATION NOTES (SLIDE 20):\n• Criterion C Evaluation: Green light improvements must directly address Red light systematic errors.")

    # ==========================================
    # SLIDE 21: CHECK FOR UNDERSTANDING - HINGE 2
    # ==========================================
    s21 = prs.slides.add_slide(blank_layout)
    add_header(s21, "CHECK FOR UNDERSTANDING", TAG_AMBER, "Hinge Question 2: Energetics of Dilution vs Volume", "Show me: 1–4 fingers on 3-2-1")

    hq2_box = s21.shapes.add_textbox(Inches(0.6), Inches(1.8), Inches(12.0), Inches(0.8))
    p = hq2_box.text_frame.paragraphs[0]
    p.text = "In an experiment, 25 cm³ of 1.0 mol/dm³ HCl is mixed with 25 cm³ of 1.0 mol/dm³ NaOH, producing a temperature rise of 6.5 °C. If the experiment is repeated using 50 cm³ of 1.0 mol/dm³ HCl and 50 cm³ of 1.0 mol/dm³ NaOH, what will the temperature rise be?"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = NAVY

    opts_2 = [
        ("1", "ΔT = 3.25 °C (half, because total solution volume is doubled).", False),
        ("2", "ΔT = 6.5 °C (the same, because twice the heat heats twice the mass).", True),
        ("3", "ΔT = 13.0 °C (double, because twice as many moles reacted).", False),
        ("4", "ΔT = 0.0 °C (heat absorbed by extra water molecules).", False)
    ]

    for idx, (num, text, is_correct) in enumerate(opts_2):
        col = idx % 2
        row = idx // 2
        left = Inches(0.6 + col * 6.1)
        top = Inches(2.7 + row * 1.4)
        
        opt_s = s21.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.8), Inches(1.15))
        opt_s.fill.solid()
        if is_correct:
            opt_s.fill.fore_color.rgb = RGBColor(240, 253, 244)
            opt_s.line.color.rgb = TAG_GREEN
            opt_s.line.width = Pt(2.5)
        else:
            opt_s.fill.fore_color.rgb = CARD_BG
            opt_s.line.color.rgb = CARD_BORDER

        circle = s21.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.2), top + Inches(0.32), Inches(0.5), Inches(0.5))
        circle.fill.solid()
        circle.fill.fore_color.rgb = TAG_AMBER
        circle.line.fill.background()
        p = circle.text_frame.paragraphs[0]
        p.text = num
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

        tx = s21.shapes.add_textbox(left + Inches(0.8), top + Inches(0.15), Inches(4.8), Inches(0.85))
        tf = tx.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(11)
        p.font.color.rgb = TEXT_MAIN

    ans2_box = s21.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(5.7), Inches(12.0), Inches(1.1))
    ans2_box.fill.solid()
    ans2_box.fill.fore_color.rgb = RGBColor(220, 252, 231)
    ans2_box.line.color.rgb = TAG_GREEN
    p = ans2_box.text_frame.paragraphs[0]
    p.text = "✔ Correct Answer: 2 (ΔT = 6.5 °C)."
    p.font.bold = True
    p.font.size = Pt(11.5)
    p.font.color.rgb = RGBColor(22, 101, 52)
    p2 = ans2_box.text_frame.add_paragraph()
    p2.text = "Diagnostic Rationale: Twice as many moles react (2q heat), but twice the mass (100g vs 50g) is heated. Since ΔT = q ÷ (m·c), the factor of 2 cancels out: ΔT remains unchanged."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MAIN

    add_footer(s21)
    set_notes(s21, "TEACHER FACILITATION NOTES (SLIDE 21):\n• Highly diagnostic question: proves whether students understand the formula Delta T = q / (m*c).")

    # ==========================================
    # SLIDE 22: VTR 5 - MASTER CONCEPT MAP
    # ==========================================
    s22 = prs.slides.add_slide(blank_layout)
    add_header(s22, "VISUAL THINKING ROUTINE", TAG_PURPLE, "Generate – Sort – Connect – Elaborate: Master Concept Synthesis", "Routine: Synthesize the 6 unit standards into an integrated conceptual network")

    add_card(s22, Inches(0.6), Inches(1.8), Inches(2.8), Inches(4.8), "1. Generate", [
        "📝 List Key Vocabulary:",
        "",
        "• Valence electrons",
        "• Activity series",
        "• Single displacement",
        "• Neutralization",
        "• pH scale & [H+]",
        "• Volumetric titration",
        "• Concordant titre",
        "• Conservation of mass",
        "• Bond breaking (endo)",
        "• Bond forming (exo)",
        "• Enthalpy change (ΔH)"
    ], header_color=TAG_CORAL)

    add_card(s22, Inches(3.6), Inches(1.8), Inches(2.8), Inches(4.8), "2. Sort", [
        "🗂️ Organize Hierarchically:",
        "",
        "• Core Concept at Centre:",
        "  “Transformation of Energy & Matter in Acid Reactions”",
        "",
        "• Sub-Branches:",
        "  Branch 1: Microscopic Models (Electrons & Periodic Trends)",
        "  Branch 2: Solution Reactions & Stoichiometry",
        "  Branch 3: Thermochemical Energy Changes"
    ], header_color=TAG_AMBER)

    add_card(s22, Inches(6.6), Inches(1.8), Inches(2.8), Inches(4.8), "3. Connect", [
        "🔗 Draw Meaningful Links:",
        "",
        "• Connect Valence Electrons -> Metal Activity in Acid Displacement.",
        "• Connect [H+] Ion Concentration -> Logarithmic pH Scale.",
        "• Connect Titration Equivalence Point -> Net Ionic Neutralization (H⁺ + OH⁻ -> H₂O).",
        "• Connect Bond Making in Water -> Exothermic Enthalpy Release (ΔH < 0)."
    ], header_color=TAG_TEAL)

    add_card(s22, Inches(9.6), Inches(1.8), Inches(2.8), Inches(4.8), "4. Elaborate", [
        "💡 Deepen with Examples:",
        "",
        "• Add chemical equations to each link.",
        "• Annotate where experimental uncertainties arise in lab measurements.",
        "• Connect to the Global Context: How this knowledge allows engineers to neutralize acidic mine drainage using calcium carbonate slurry."
    ], header_color=TAG_BLUE)
    add_footer(s22)
    set_notes(s22, "TEACHER FACILITATION NOTES (SLIDE 22):\n• End-of-unit Butcher Paper synthesis: 15 minutes paired mapping.")

    # ==========================================
    # SLIDE 23: EXIT TICKET & TRAFFIC LIGHTS
    # ==========================================
    s23 = prs.slides.add_slide(blank_layout)
    add_header(s23, "EXIT TICKET", TAG_CORAL, "Metacognitive Self-Assessment: Criteria B & C Mastery", "Colour each standard: Green = Confident & Mastered · Amber = Nearly there · Red = Needs review")

    st_self = [
        ("10.ABC-DS.1", "I can explain displacement and acid-metal reactions using valence electrons, ionization energy, and the activity series."),
        ("10.ABC-DS.2", "I can model neutralization as bond breaking and bond forming, calculating overall reaction enthalpy (ΔH = Σbroken - Σformed)."),
        ("10.ABC-DS.3", "I can write balanced equations and identify confirmatory gas tests for acid reactions with metals, bases, carbonates, and ammonium salts."),
        ("10.ABC-DS.4", "I can compare [H+] concentrations using logarithmic pH scales and select appropriate indicators (phenolphthalein vs methyl orange)."),
        ("10.ABC-DS.5", "I can perform titration calculations using concordant titres (±0.10 cm³) and balanced mole ratios to find unknown concentrations."),
        ("10.ABC-DS.6 / Crit B & C", "I can design a fair test (IV, DV, CVs), screen data for anomalies, calculate mean ΔT, and evaluate systematic calorimeter errors.")
    ]

    for idx, (s_tag, s_desc) in enumerate(st_self):
        top_y = Inches(1.8 + idx * 0.8)

        t_b = s23.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), top_y, Inches(2.6), Inches(0.65))
        t_b.fill.solid()
        t_b.fill.fore_color.rgb = NAVY
        t_b.line.color.rgb = NAVY
        p = t_b.text_frame.paragraphs[0]
        p.text = s_tag
        p.font.size = Pt(10)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

        d_b = s23.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.3), top_y, Inches(7.4), Inches(0.65))
        d_b.fill.solid()
        d_b.fill.fore_color.rgb = CARD_BG
        d_b.line.color.rgb = CARD_BORDER
        p = d_b.text_frame.paragraphs[0]
        p.text = s_desc
        p.font.size = Pt(9.5)
        p.font.color.rgb = TEXT_MAIN

        cols = [RGBColor(239, 68, 68), RGBColor(245, 158, 11), RGBColor(16, 185, 129)]
        for c_i, c in enumerate(cols):
            circ = s23.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.9 + c_i * 0.65), top_y + Inches(0.08), Inches(0.48), Inches(0.48))
            circ.fill.background()
            circ.line.color.rgb = c
            circ.line.width = Pt(2.2)

    add_footer(s23)
    set_notes(s23, "TEACHER FACILITATION NOTES (SLIDE 23):\n• Exit slip: Collect slips to see if small-group intervention is needed on DS.2 or DS.5.")

    # ==========================================
    # SLIDE 24: KEY VOCABULARY GLOSSARY
    # ==========================================
    s24 = prs.slides.add_slide(blank_layout)
    add_header(s24, "KEY VOCABULARY", TAG_TEAL, "Academic Vocabulary & Command Terms Glossary")

    vocab = [
        ("Valence Electrons", "Electrons in the outermost shell that determine bonding, oxidation, and periodic reactivity trends."),
        ("Activity Series", "An empirical ranking of metals in order of decreasing reactivity (ease of oxidation to cations)."),
        ("Neutralization", "The exothermic chemical reaction between an acid and a base to produce water and a dissolved salt."),
        ("Concordant Titres", "Titration volumes delivered within ± 0.10 cm³ of each other, indicating high procedural precision."),
        ("Enthalpy Change (ΔH)", "The net heat energy transferred during a chemical reaction at constant pressure (measured in kJ/mol)."),
        ("Exothermic Reaction", "A reaction where energy released during bond forming exceeds energy absorbed during bond breaking (ΔH < 0)."),
        ("Limiting Reactant", "The substance completely consumed first in a reaction, determining the theoretical yield of products."),
        ("Systematic Error", "A reproducible inaccuracy inherent to experimental apparatus or design (e.g. calorimeter heat loss).")
    ]

    for idx, (v_term, v_def) in enumerate(vocab):
        col = idx % 2
        row = idx // 2
        left = Inches(0.6 + col * 6.1)
        top = Inches(1.8 + row * 1.25)

        card_v = s24.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.8), Inches(1.1))
        card_v.fill.solid()
        card_v.fill.fore_color.rgb = CARD_BG
        card_v.line.color.rgb = CARD_BORDER

        tx = s24.shapes.add_textbox(left + Inches(0.2), top + Inches(0.1), Inches(5.4), Inches(0.9))
        tf = tx.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = v_term
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = NAVY

        p2 = tf.add_paragraph()
        p2.text = v_def
        p2.font.size = Pt(9.5)
        p2.font.color.rgb = TEXT_MAIN

    add_footer(s24)
    set_notes(s24, "TEACHER FACILITATION NOTES (SLIDE 24):\n• Vocabulary Flashcard review before summative assessment.")

    # --- APPLY SLIDE-TO-SLIDE TRANSITIONS TO ALL SLIDES ---
    transition_map = {
        0: ("fade", "med", "l"),       # Title: Smooth cinematic fade
        1: ("push", "fast", "l"),      # Overview: Slide forward
        2: ("push", "fast", "l"),      # SoI: Slide forward
        3: ("fade", "med", "l"),       # Simulations Hub: Fade
        4: ("fade", "med", "l"),       # See-Think-Wonder: Fade
        5: ("push", "fast", "l"),      # Lesson 1 Trends: Advance
        6: ("wipe", "fast", "l"),      # Jigsaw Activity: Wipe
        7: ("split", "med", "l"),      # Hinge 1: Diagnostic Split Reveal
        8: ("push", "fast", "l"),      # Lesson 2 Reactions: Advance
        9: ("push", "fast", "l"),      # Ammonium salts: Advance
        10: ("wipe", "fast", "l"),     # 4-Station Lab: Wipe
        11: ("fade", "med", "l"),      # pH Scale Gradient: Smooth Fade
        12: ("push", "fast", "l"),     # Titrations: Advance
        13: ("push", "fast", "l"),     # Stoichiometry Algorithm: Advance
        14: ("wipe", "fast", "l"),     # Mass Conservation: Wipe
        15: ("fade", "med", "l"),      # Reaction Profile: Smooth Fade
        16: ("push", "fast", "l"),     # Criterion B Brief: Advance
        17: ("push", "fast", "l"),     # Calorimeter Setup: Advance
        18: ("wipe", "fast", "l"),     # Raw Data & Anomalies: Wipe
        19: ("fade", "med", "l"),      # Error Evaluation: Smooth Fade
        20: ("split", "med", "l"),     # Hinge 2: Diagnostic Split Reveal
        21: ("fade", "med", "l"),      # Master Concept Map: Smooth Fade
        22: ("push", "fast", "l"),     # Self-Assessment Traffic Lights: Advance
        23: ("fade", "med", "l")       # Vocabulary Glossary: Smooth Fade
    }
    for idx, s in enumerate(prs.slides):
        t_type, spd, d = transition_map.get(idx, ("fade", "med", "l"))
        add_transition(s, t_type, spd, d)

    output_filename = "MYP5_Chemical_Models_and_Energy_Master.pptx"
    prs.save(output_filename)
    print(f"Master presentation with embedded diagrams and links generated successfully: {output_filename}")

if __name__ == "__main__":
    build_master_deck()
