import collections.abc
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE

def create_myp5_presentation():
    prs = Presentation()
    # 16:9 Widescreen
    prs.slide_width = Inches(13.333)
    prs.slide_height = Inches(7.5)
    blank_layout = prs.slide_layouts[6]

    # --- COLOR PALETTE ---
    NAVY = RGBColor(15, 23, 42)       # #0F172A
    SLATE = RGBColor(30, 41, 59)      # #1E293B
    WHITE = RGBColor(255, 255, 255)
    CARD_BG = RGBColor(248, 250, 252) # #F8FAFC
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

    def add_footer(slide, text="Unit 1 · Chemical Models & Energy in Reactions · Grade 10 MYP 5 Sciences"):
        tx = slide.shapes.add_textbox(Inches(0.6), Inches(7.1), Inches(12.133), Inches(0.3))
        tf = tx.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(9)
        p.font.color.rgb = TEXT_MUTED

    def add_header(slide, tag_text, tag_color, title_text, subtitle_text=None):
        # Category Tag (Pill)
        tag_box = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(0.5), Inches(2.2), Inches(0.35))
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

        # Title
        title_box = slide.shapes.add_textbox(Inches(0.6), Inches(0.95), Inches(12.133), Inches(0.6))
        tf = title_box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = title_text
        p.font.size = Pt(22)
        p.font.bold = True
        p.font.color.rgb = NAVY

        # Subtitle
        if subtitle_text:
            sub_box = slide.shapes.add_textbox(Inches(0.6), Inches(1.5), Inches(12.133), Inches(0.4))
            tf = sub_box.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.text = subtitle_text
            p.font.size = Pt(12)
            p.font.italic = True
            p.font.color.rgb = TEXT_MUTED

    def add_card(slide, left, top, width, height, title, items, header_color=None, bg_color=CARD_BG, border_color=CARD_BORDER):
        card = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
        card.fill.solid()
        card.fill.fore_color.rgb = bg_color
        card.line.color.rgb = border_color
        card.line.width = Pt(1.5)

        # Header block if header_color provided
        if header_color:
            hdr = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, left, top, width, Inches(0.55))
            hdr.fill.solid()
            hdr.fill.fore_color.rgb = header_color
            hdr.line.color.rgb = header_color
            tf = hdr.text_frame
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(13)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.LEFT
            content_top = top + Inches(0.65)
            content_height = height - Inches(0.75)
        else:
            content_top = top + Inches(0.15)
            content_height = height - Inches(0.3)

        tx = slide.shapes.add_textbox(left + Inches(0.2), content_top, width - Inches(0.4), content_height)
        tf = tx.text_frame
        tf.word_wrap = True
        
        if not header_color:
            p = tf.paragraphs[0]
            p.text = title
            p.font.size = Pt(14)
            p.font.bold = True
            p.font.color.rgb = NAVY
            first = False
        else:
            first = True

        for item in items:
            p = tf.add_paragraph() if not first else tf.paragraphs[0]
            first = False
            p.text = item
            p.font.size = Pt(11)
            p.font.color.rgb = TEXT_MAIN
            p.space_after = Pt(6)

    # ==========================================
    # SLIDE 1: TITLE SLIDE (Dark Navy)
    # ==========================================
    s1 = prs.slides.add_slide(blank_layout)
    bg1 = s1.shapes.add_shape(MSO_SHAPE.RECTANGLE, 0, 0, prs.slide_width, prs.slide_height)
    bg1.fill.solid()
    bg1.fill.fore_color.rgb = NAVY
    bg1.line.fill.background()

    # Meta tag
    tag_tx = s1.shapes.add_textbox(Inches(1.0), Inches(1.5), Inches(11.0), Inches(0.5))
    p = tag_tx.text_frame.paragraphs[0]
    p.text = "GRADE 10 · IB MYP YEAR 5 INTEGRATED SCIENCES · UNIT 1"
    p.font.size = Pt(13)
    p.font.bold = True
    p.font.color.rgb = RGBColor(96, 165, 250)

    # Title
    t_tx = s1.shapes.add_textbox(Inches(1.0), Inches(2.1), Inches(11.0), Inches(1.5))
    p = t_tx.text_frame.paragraphs[0]
    p.text = "Chemical Models & Energy in Reactions"
    p.font.size = Pt(36)
    p.font.bold = True
    p.font.color.rgb = WHITE

    # Subtitle
    sub_tx = s1.shapes.add_textbox(Inches(1.0), Inches(3.7), Inches(11.0), Inches(1.0))
    p = sub_tx.text_frame.paragraphs[0]
    p.text = "Sub-unit 1 · Periodic trends, bond energy, acid-base stoichiometry & neutralization thermochemistry"
    p.font.size = Pt(17)
    p.font.color.rgb = RGBColor(251, 191, 36)

    # Summative Pill
    pill = s1.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(1.0), Inches(4.8), Inches(7.5), Inches(0.8))
    pill.fill.solid()
    pill.fill.fore_color.rgb = RGBColor(30, 58, 138)
    pill.line.color.rgb = RGBColor(59, 130, 246)
    p = pill.text_frame.paragraphs[0]
    p.text = "🎯 Summative Assessment Focus: Criterion B (Inquiring & Designing) & Criterion C (Processing & Evaluating)"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    add_footer(s1, "Unit 1 · Chemical Models & Energy in Reactions · Grade 10 MYP 5 Sciences · OIS I.SCI 10.ABC-DS.1–6")

    # ==========================================
    # SLIDE 2: UNIT OVERVIEW
    # ==========================================
    s2 = prs.slides.add_slide(blank_layout)
    add_header(s2, "UNIT OVERVIEW", TAG_TEAL, "What This Sub-Unit Is About")
    
    add_card(s2, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.8), "Course & Standards Scope", [
        "📚 Subject & Phase: MYP Year 5 Integrated Sciences (Chemistry Focus), Grade 10.",
        "🔬 Sub-unit 1: Chemical Models & Energy in Reactions.",
        "⏱️ Duration: 15 Lessons leading into the Criteria B & C Summative Lab.",
        "📌 Key Standards:",
        "  • 10.ABC-DS.1: Outermost electron states & periodic trends in displacement.",
        "  • 10.ABC-DS.2: Bond breaking/forming & total bond energy in neutralization.",
        "  • 10.ABC-DS.3: Characteristic acid reactions (metals, bases, carbonates, ammonium salts).",
        "  • 10.ABC-DS.4: Indicators, pH scale, and [H+] ion concentration.",
        "  • 10.ABC-DS.5: Acid-base titrations, volumetric glassware & stoichiometry.",
        "  • 10.ABC-DS.6: Conservation of mass & molar stoichiometry (gas evolution)."
    ])

    add_card(s2, Inches(6.8), Inches(1.8), Inches(5.8), Inches(4.8), "Assessment & Inquiry Pedagogy", [
        "🎯 Summative Assessment:",
        "  • Criterion B: Inquiring & designing a rigorous enthalpy/stoichiometry lab.",
        "  • Criterion C: Processing experimental raw data, error propagation, and evaluation.",
        "",
        "🧠 How We Learn (Harvard Project Zero):",
        "  • Thinking routines to make scientific reasoning visible (Zoom In, Claim-Support-Question, Red/Yellow/Green Light).",
        "  • Dual representation: Macroscopic lab observations paired with sub-microscopic electron & particle models.",
        "",
        "💡 Summative Challenge:",
        "  • Design and evaluate a calorimetry investigation to determine the molar enthalpy of neutralization (ΔH_neut) or mass conservation in gas evolution."
    ])
    add_footer(s2)

    # ==========================================
    # SLIDE 3: MYP FRAMEWORK (SoI & Questions)
    # ==========================================
    s3 = prs.slides.add_slide(blank_layout)
    add_header(s3, "MYP FRAMEWORK", TAG_PURPLE, "Statement of Inquiry & Inquiry Questions")

    # SoI Callout Box
    soi_box = s3.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(1.6), Inches(12.0), Inches(1.1))
    soi_box.fill.solid()
    soi_box.fill.fore_color.rgb = NAVY
    soi_box.line.color.rgb = RGBColor(59, 130, 246)
    p = soi_box.text_frame.paragraphs[0]
    p.text = '“Models of atomic electron configuration and chemical bond energy allow scientists to predict reaction dynamics and engineer solutions for environmental and biological energy transformations.”'
    p.font.size = Pt(14)
    p.font.italic = True
    p.font.bold = True
    p.font.color.rgb = WHITE
    p.alignment = PP_ALIGN.CENTER

    # Concepts 3 columns
    add_card(s3, Inches(0.6), Inches(2.9), Inches(3.8), Inches(1.6), "KEY CONCEPT", [
        "Change",
        "Transformation of matter, electron exchange, and chemical bond restructuring."
    ], header_color=TAG_BLUE)

    add_card(s3, Inches(4.7), Inches(2.9), Inches(3.8), Inches(1.6), "RELATED CONCEPTS", [
        "Energy · Models · Evidence",
        "Quantifying bond enthalpies and using sub-microscopic particle models as proof."
    ], header_color=TAG_TEAL)

    add_card(s3, Inches(8.8), Inches(2.9), Inches(3.8), Inches(1.6), "GLOBAL CONTEXT", [
        "Scientific & Technical Innovation",
        "How understanding neutralization and acid kinetics drives green industrial processes."
    ], header_color=TAG_PURPLE)

    # Questions Rows
    q1 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(4.7), Inches(2.0), Inches(0.6))
    q1.fill.solid()
    q1.fill.fore_color.rgb = TAG_CORAL
    q1.text_frame.paragraphs[0].text = "FACTUAL"
    q1.text_frame.paragraphs[0].font.bold = True
    q1.text_frame.paragraphs[0].font.color.rgb = WHITE
    q1.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    t1 = s3.shapes.add_textbox(Inches(2.8), Inches(4.7), Inches(9.8), Inches(0.6))
    t1.text_frame.paragraphs[0].text = "How does outermost valence electron configuration govern single displacement and acid-base reactivity?"
    t1.text_frame.paragraphs[0].font.size = Pt(12)

    q2 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(5.4), Inches(2.0), Inches(0.6))
    q2.fill.solid()
    q2.fill.fore_color.rgb = TAG_AMBER
    q2.text_frame.paragraphs[0].text = "CONCEPTUAL"
    q2.text_frame.paragraphs[0].font.bold = True
    q2.text_frame.paragraphs[0].font.color.rgb = WHITE
    q2.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    t2 = s3.shapes.add_textbox(Inches(2.8), Inches(5.4), Inches(9.8), Inches(0.6))
    t2.text_frame.paragraphs[0].text = "Why is the net ionic enthalpy of strong acid - strong alkali neutralization essentially constant regardless of acid identity?"
    t2.text_frame.paragraphs[0].font.size = Pt(12)

    q3 = s3.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(6.1), Inches(2.0), Inches(0.6))
    q3.fill.solid()
    q3.fill.fore_color.rgb = TAG_PURPLE
    q3.text_frame.paragraphs[0].text = "DEBATABLE"
    q3.text_frame.paragraphs[0].font.bold = True
    q3.text_frame.paragraphs[0].font.color.rgb = WHITE
    q3.text_frame.paragraphs[0].alignment = PP_ALIGN.CENTER

    t3 = s3.shapes.add_textbox(Inches(2.8), Inches(6.1), Inches(9.8), Inches(0.6))
    t3.text_frame.paragraphs[0].text = "Are laboratory chemical models sufficient to predict real-world environmental acid neutralization?"
    t3.text_frame.paragraphs[0].font.size = Pt(12)
    add_footer(s3)

    # ==========================================
    # SLIDE 4: 15-LESSON INQUIRY JOURNEY (ROADMAP)
    # ==========================================
    s4 = prs.slides.add_slide(blank_layout)
    add_header(s4, "ROADMAP", TAG_BLUE, "Our 15-Lesson Inquiry & Assessment Pathway")

    add_card(s4, Inches(0.6), Inches(1.8), Inches(3.8), Inches(4.8), "Phase 1: Foundations (L1–L5)", [
        "⚡ L1: Valence Electrons & Periodic Trends (10.ABC-DS.1)",
        "  Explaining reactivity via ionization energy & electronegativity.",
        "",
        "⚡ L2: Displacement Reactions & Redox (10.ABC-DS.1)",
        "  Activity series of metals; writing half-equations.",
        "",
        "⚡ L3: Reactions of Acids (10.ABC-DS.3)",
        "  Acids with metals, bases, and carbonates; gas tests.",
        "",
        "⚡ L4: Reactions of Bases & Ammonium Salts (10.ABC-DS.3)",
        "  Base characteristics, precipitation, and ammonia gas release.",
        "",
        "⚡ L5: Formative Check 1 & Synthesis",
        "  Consolidating ionic equations and gas evolution mechanics."
    ], header_color=TAG_BLUE)

    add_card(s4, Inches(4.7), Inches(1.8), Inches(3.8), Inches(4.8), "Phase 2: Quantifying Systems (L6–L10)", [
        "🧪 L6: pH Scale & [H+] Concentration (10.ABC-DS.4)",
        "  Logarithmic scale, strong vs weak acids, indicator ranges.",
        "",
        "🧪 L7: Volumetric Titrations (10.ABC-DS.5)",
        "  Precision glassware (pipette, burette), titre concordancy.",
        "",
        "🧪 L8: Titration Stoichiometry (10.ABC-DS.5)",
        "  Calculating unknown molarities; concentration calculations.",
        "",
        "🧪 L9: Conservation of Mass & Gas Evolution (10.ABC-DS.6)",
        "  Open vs closed systems, mass loss of CO2, molar volume.",
        "",
        "🧪 L10: Formative Lab (Criterion B/C Trial)",
        "  Mock investigation: variable manipulation and uncertainty."
    ], header_color=TAG_TEAL)

    add_card(s4, Inches(8.8), Inches(1.8), Inches(3.8), Inches(4.8), "Phase 3: Thermochemistry & Summative (L11–L15)", [
        "🔥 L11: Bond Energy & Enthalpy (10.ABC-DS.2)",
        "  Bond breaking (endo) vs bond forming (exo); energy profiles.",
        "",
        "🔥 L12: Calorimetry of Neutralization (10.ABC-DS.2)",
        "  q = mcΔT, polystyrene cup calorimeter, calculating ΔH_neut.",
        "",
        "🎯 L13: Summative Assessment – Criterion B",
        "  Independent experimental design: variables, hypothesis & protocol.",
        "",
        "🎯 L14: Summative Assessment – Criterion C Lab",
        "  Execution, data collection (3 trials), anomaly screening.",
        "",
        "🎯 L15: Summative Assessment – Processing & Evaluation",
        "  Graphing, uncertainty analysis, validity discussion & improvements."
    ], header_color=TAG_CORAL)
    add_footer(s4)

    # ==========================================
    # SLIDE 5: VISUAL THINKING ROUTINES
    # ==========================================
    s5 = prs.slides.add_slide(blank_layout)
    add_header(s5, "VISUAL THINKING ROUTINE", TAG_PURPLE, "Harvard Project Zero Routines We Will Use", "Routines from Harvard Project Zero that make scientific thinking visible")

    routines = [
        ("Zoom In", "LOOK · ZOOM · REVISE", "Examine macroscopic acid reaction, zoom into atomic lattice, then valence electron exchange. (Lesson 1)", TAG_BLUE),
        ("Claim – Support – Question", "CLAIM · EVIDENCE · REASONING", "Test claims about acid strength vs concentration using pH evidence. (Lesson 6)", TAG_TEAL),
        ("Generate – Sort – Connect", "CONCEPT MAPPING", "Map acid reactions, products, energy changes, and ionic models into a unified web. (Lesson 5 & 10)", TAG_PURPLE),
        ("Same & Different", "COMPARE · CONTRAST · ABSTRACT", "Compare neutralization enthalpy across strong acids (HCl vs HNO3 vs H2SO4). (Lesson 12)", TAG_AMBER),
        ("Red Light, Yellow Light, Green Light", "EVALUATE · UNCERTAINTIES", "Identify systematic heat losses (Red), assumptions (Yellow), and improvements (Green). (Lesson 15)", TAG_CORAL),
        ("Explanation Game", "NAME IT · EXPLAIN IT · GIVE REASONS", "Explain why temperature rises during neutralization using bond breaking/forming. (Lesson 11)", TAG_GREEN)
    ]

    for idx, (rt_title, rt_sub, rt_desc, rt_col) in enumerate(routines):
        col = idx % 3
        row = idx // 3
        left = Inches(0.6 + col * 4.1)
        top = Inches(1.8 + row * 2.5)
        add_card(s5, left, top, Inches(3.8), Inches(2.2), rt_title, [
            rt_sub,
            "",
            rt_desc
        ], header_color=rt_col)
    add_footer(s5)

    # ==========================================
    # SLIDE 6: SIMULATIONS & INTERACTIVE LABS
    # ==========================================
    s6 = prs.slides.add_slide(blank_layout)
    add_header(s6, "LEARNING EXPERIENCE", TAG_TEAL, "Simulations, Datasets & Virtual Labs")

    add_card(s6, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.8), "Interactive Simulations (PhET & Virtual Chem)", [
        "🧪 PhET: Acid-Base Solutions (L6)",
        "  Visualize strong vs weak acids, dissociation equilibrium, and [H3O+] vs [OH-].",
        "  🔗 https://phet.colorado.edu/en/simulations/acid-base-solutions",
        "",
        "🧪 PhET: Energy Forms and Changes (L11)",
        "  Track kinetic and thermal energy transfers during exothermic interactions.",
        "  🔗 https://phet.colorado.edu/en/simulations/energy-forms-and-changes",
        "",
        "🧪 ChemCollective: Virtual Acid-Base Titration Lab (L7–L8)",
        "  Practice standardized titrations, reading burette meniscuses, and indicator endpoints.",
        "",
        "🧪 PhET: Reactants, Products and Leftovers (L9)",
        "  Model limiting reactants and mass conservation during gas evolution."
    ], header_color=TAG_TEAL)

    add_card(s6, Inches(6.8), Inches(1.8), Inches(5.8), Inches(4.8), "Video Demonstrations & Pre-Lab Briefings", [
        "🎥 Video: Energetics of Neutralization (L11)",
        "  Calorimetry in a coffee-cup calorimeter: setup, temperature probes, heat capacities.",
        "",
        "🎥 Video: Single Displacement & The Activity Series (L2)",
        "  Real-time electron transfer between zinc/magnesium and copper(II) sulfate.",
        "",
        "🎥 Video: Titration Technique & Avoiding Systematic Error (L7)",
        "  Eliminating air bubbles in burette tips, rinsing glassware, parallax error.",
        "",
        "🎥 Video: Gas Evolution Stoichiometry (L9)",
        "  Measuring mass loss of CO2 when calcium carbonate reacts with excess HCl."
    ], header_color=TAG_BLUE)
    add_footer(s6)

    # ==========================================
    # SLIDE 7: CRITERION B FOCUS (DESIGNING A FAIR TEST)
    # ==========================================
    s7 = prs.slides.add_slide(blank_layout)
    add_header(s7, "CRITERION B FOCUS", TAG_BLUE, "Formulating Variables & Hypotheses (MYP 5 Level)")

    add_card(s7, Inches(0.6), Inches(1.8), Inches(3.8), Inches(4.0), "Independent Variable (IV)", [
        "What you deliberately manipulate:",
        "",
        "• Must state a continuous quantitative range (at least 5 distinct values) or clear qualitative states.",
        "• Example: Concentration of HCl(aq):",
        "  [0.2, 0.4, 0.6, 0.8, 1.0 mol/dm³].",
        "• State exactly HOW it is manipulated (serial dilution using volumetric flasks)."
    ], header_color=TAG_BLUE)

    add_card(s7, Inches(4.7), Inches(1.8), Inches(3.8), Inches(4.0), "Dependent Variable (DV)", [
        "What you quantitatively measure:",
        "",
        "• Must specify the exact physical parameter, instrument, and precision/resolution.",
        "• Example: Temperature change (ΔT = T_max - T_initial):",
        "  Measured using a digital temperature probe (±0.05 °C) logged at 1 Hz.",
        "• Total enthalpy calculated via q = mcΔT."
    ], header_color=TAG_TEAL)

    add_card(s7, Inches(8.8), Inches(1.8), Inches(3.8), Inches(4.0), "Controlled Variables (CV)", [
        "What must be held strictly constant:",
        "",
        "• At least 3 significant controlled variables.",
        "• For EACH variable:",
        "  1. State the variable (e.g. Volume of NaOH).",
        "  2. State HOW it is controlled (volumetric pipette).",
        "  3. Explain WHY uncontrolled variation affects DV validity (dilution changes thermal mass)."
    ], header_color=TAG_PURPLE)

    # Hypothesis strip
    hyp_box = s7.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(6.0), Inches(12.0), Inches(0.9))
    hyp_box.fill.solid()
    hyp_box.fill.fore_color.rgb = RGBColor(254, 243, 199)
    hyp_box.line.color.rgb = TAG_AMBER
    p = hyp_box.text_frame.paragraphs[0]
    p.text = "MYP 5 Hypothesis Standard: “If [change in IV], then [predicted change in DV], because [scientific explanation using bond energies, collision theory, and net ionic neutralization equations].”"
    p.font.size = Pt(11)
    p.font.bold = True
    p.font.color.rgb = RGBColor(146, 64, 14)
    add_footer(s7)

    # ==========================================
    # SLIDE 8: CRITERION B SUMMATIVE PROMPT
    # ==========================================
    s8 = prs.slides.add_slide(blank_layout)
    add_header(s8, "EXPERIMENT DEVELOPMENT", TAG_CORAL, "Criterion B Summative: The Investigation Plan")

    add_card(s8, Inches(0.6), Inches(1.8), Inches(12.0), Inches(5.0), "Summative Investigation: Calorimetric Determination of Neutralization Enthalpy", [
        "🎯 Research Question:",
        "  “How does the concentration of hydrochloric acid (0.2 to 1.0 mol/dm³) affect the maximum temperature change (ΔT) and calculated molar enthalpy of neutralization (ΔH_neut) when reacted with excess 1.0 mol/dm³ sodium hydroxide in a coffee-cup calorimeter?”",
        "",
        "📋 Methodological Requirements for Full Marks (Criterion B Strands i–iv):",
        "  1. Formulate a focused problem/question with scientific justification.",
        "  2. State a testable hypothesis with quantitative predictions and net ionic chemical reasoning (H+(aq) + OH-(aq) → H2O(l)).",
        "  3. Tabulate all variables (IV range, DV resolution, and 4 CVs with control methods and failure impacts).",
        "  4. Design a clear, logical, numbered method including:",
        "     • Apparatus diagram with labeled components (calorimeter, magnetic stirrer, digital probe).",
        "     • Explicit safety, environmental, and ethical risk assessment (corrosive acids, caustic alkali, exothermic splash hazards).",
        "     • Minimum of 3 repeat trials per condition to ensure data reliability."
    ])
    add_footer(s8)

    # ==========================================
    # SLIDE 9: CRITERION C FOCUS (PROCESSING DATA)
    # ==========================================
    s9 = prs.slides.add_slide(blank_layout)
    add_header(s9, "CRITERION C FOCUS", TAG_GREEN, "Criterion C: Data Processing, Uncertainties & Anomaly Screening")

    add_card(s9, Inches(0.6), Inches(1.8), Inches(5.8), Inches(4.8), "Strand i & ii: Processing & Graphing", [
        "📊 Raw Data Presentation:",
        "  • Unambiguous column headers with SI units and equipment uncertainties (e.g., Temperature / °C ± 0.05).",
        "  • Consistent decimal places matching instrument precision.",
        "",
        "🔢 Processing Steps:",
        "  • Identify and justify the exclusion of anomalous trials.",
        "  • Calculate Mean Temperature Change: ΔT_mean = (Trial 1 + Trial 2 + Trial 3) / 3.",
        "  • Heat evolved: q = mcΔT (where m = total mass of solution in g, c = 4.18 J/g·°C).",
        "  • Molar enthalpy: ΔH = -q / n_limiting (kJ/mol).",
        "",
        "📈 Graphing Standards:",
        "  • Independent variable on x-axis, Dependent on y-axis.",
        "  • Correctly scaled axes covering ≥ 50% of grid, error bars where appropriate, linear line of best fit."
    ], header_color=TAG_GREEN)

    add_card(s9, Inches(6.8), Inches(1.8), Inches(5.8), Inches(4.8), "Strand iii, iv & v: Discussing & Evaluating", [
        "🔍 Strand iii: Hypothesis Validity:",
        "  • Compare calculated ΔH_neut against the theoretical literature value (-57.1 kJ/mol).",
        "  • Explicitly calculate Percentage Error: % Error = |(Experimental - Theoretical) / Theoretical| × 100%.",
        "",
        "⚠️ Strand iv: Method Validity (Error Analysis):",
        "  • Distinguish between Systematic Errors (heat loss to surroundings, thermal absorption by plastic cup, heat capacity assumption) and Random Errors (parallax, fluctuating initial room temp).",
        "",
        "🛠️ Strand v: Specific & Realistic Improvements:",
        "  • Do NOT say “be more careful”. Suggest concrete procedural refinements (e.g. use a double-walled vacuum calorimeter, extrapolating cooling curve, automated burettes)."
    ], header_color=TAG_TEAL)
    add_footer(s9)

    # ==========================================
    # SLIDE 10: SAMPLE DATA & ANOMALY ANALYSIS (CRITERION C)
    # ==========================================
    s10 = prs.slides.add_slide(blank_layout)
    add_header(s10, "INVESTIGATION", TAG_CORAL, "Criterion C Exemplar: Raw Data Table & Anomaly Screening")

    # Table
    table_shape = s10.shapes.add_table(7, 6, Inches(0.6), Inches(1.8), Inches(12.0), Inches(3.2))
    table = table_shape.table

    headers = ["[HCl] / mol dm⁻³ (±0.02)", "T_initial / °C (±0.05)", "Trial 1: ΔT / °C", "Trial 2: ΔT / °C", "Trial 3: ΔT / °C", "Mean ΔT / °C (±0.1)"]
    for col_idx, h in enumerate(headers):
        cell = table.cell(0, col_idx)
        cell.text = h
        cell.fill.solid()
        cell.fill.fore_color.rgb = NAVY
        for p in cell.text_frame.paragraphs:
            p.font.size = Pt(11)
            p.font.bold = True
            p.font.color.rgb = WHITE
            p.alignment = PP_ALIGN.CENTER

    data = [
        ["0.20", "21.50", "1.30", "1.35", "1.25", "1.30"],
        ["0.40", "21.50", "2.65", "2.70", "2.60", "2.65"],
        ["0.60", "21.55", "3.95", "4.00", "3.90", "3.95"],
        ["0.80", "21.50", "5.25", "1.80*", "5.35", "5.30*"],
        ["1.00", "21.60", "6.60", "6.55", "6.65", "6.60"],
    ]

    for row_idx, row in enumerate(data):
        for col_idx, val in enumerate(row):
            cell = table.cell(row_idx + 1, col_idx)
            cell.text = val
            cell.fill.solid()
            if "*" in val:
                cell.fill.fore_color.rgb = RGBColor(254, 226, 226) # Highlight anomaly
            else:
                cell.fill.fore_color.rgb = WHITE
            for p in cell.text_frame.paragraphs:
                p.font.size = Pt(11)
                p.alignment = PP_ALIGN.CENTER

    # Anomaly Callout Box
    anom_box = s10.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(0.6), Inches(5.3), Inches(12.0), Inches(1.5))
    anom_box.fill.solid()
    anom_box.fill.fore_color.rgb = RGBColor(254, 242, 242)
    anom_box.line.color.rgb = TAG_CORAL
    p = anom_box.text_frame.paragraphs[0]
    p.text = "⚠️ Anomaly Justification (Criterion C Strand i):"
    p.font.size = Pt(12)
    p.font.bold = True
    p.font.color.rgb = TAG_CORAL

    p2 = anom_box.text_frame.add_paragraph()
    p2.text = "At 0.80 mol/dm³ HCl, Trial 2 recorded ΔT = 1.80 °C, which deviates severely from Trials 1 (5.25 °C) and 3 (5.35 °C). This was likely caused by delayed addition of NaOH or failure to close the calorimeter lid before temperature peaked. The value is identified as an anomaly and excluded from the mean: (5.25 + 5.35) ÷ 2 = 5.30 °C."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MAIN
    add_footer(s10)

    # ==========================================
    # SLIDE 11: EVALUATION (RED LIGHT, YELLOW LIGHT, GREEN LIGHT)
    # ==========================================
    s11 = prs.slides.add_slide(blank_layout)
    add_header(s11, "EXPERIMENT EVALUATION", TAG_PURPLE, "Evaluating the Neutralization Method (Criterion C iv & v)")

    add_card(s11, Inches(0.6), Inches(1.8), Inches(3.8), Inches(4.8), "🔴 Red Light: Major Errors", [
        "Systematic Heat Loss to Air:",
        "• Polystyrene cup has an open probe hole; warm air escaped before peak T recorded.",
        "• Impact: ΔT measured was lower than true value → calculated ΔH was significantly less exothermic than -57.1 kJ/mol.",
        "",
        "Heat Capacity Assumption:",
        "• Assumed solution specific heat capacity c = 4.18 J/g·°C and density = 1.0 g/cm³ like pure water.",
        "• Dissolved NaCl ions actually lower specific heat capacity."
    ], header_color=TAG_CORAL)

    add_card(s11, Inches(4.7), Inches(1.8), Inches(3.8), Inches(4.8), "🟡 Yellow Light: Limitations", [
        "Thermal Inertia of Probe:",
        "• Temperature probe took 4–6 seconds to equilibrate; maximum temperature may have cooled slightly while probe registered.",
        "",
        "Volumetric Inaccuracies:",
        "• Graduated measuring cylinders (±0.5 cm³) were used instead of volumetric pipettes.",
        "• Resulted in ±2.0% volume uncertainty in total reacting solution."
    ], header_color=TAG_AMBER)

    add_card(s11, Inches(8.8), Inches(1.8), Inches(3.8), Inches(4.8), "🟢 Green Light: Improvements", [
        "Cooling Curve Extrapolation:",
        "• Measure temperature every 15s for 3 min before mixing, mix, then record cooling curve for 5 min to extrapolate true T_max at t = 0.",
        "",
        "Calorimeter Refinement:",
        "• Use a nested double-cup calorimeter with vacuum insulation and sealed rubber bung.",
        "",
        "Precision Glassware:",
        "• Use 25.0 cm³ Class A volumetric pipettes (±0.03 cm³) to eliminate volume discrepancies."
    ], header_color=TAG_GREEN)
    add_footer(s11)

    # ==========================================
    # SLIDE 12: HINGE QUESTION (FORMATIVE CHECK)
    # ==========================================
    s12 = prs.slides.add_slide(blank_layout)
    add_header(s12, "CHECK FOR UNDERSTANDING", TAG_AMBER, "Hinge Question: Neutralization Thermochemistry", "Show me: 1–4 fingers on 3-2-1")

    hq_box = s12.shapes.add_textbox(Inches(0.6), Inches(1.8), Inches(12.0), Inches(0.8))
    p = hq_box.text_frame.paragraphs[0]
    p.text = "When 25 cm³ of 1.0 mol/dm³ HCl is neutralized by 25 cm³ of 1.0 mol/dm³ NaOH, ΔT is 6.5 °C. If you instead mix 50 cm³ of 1.0 mol/dm³ HCl with 50 cm³ of 1.0 mol/dm³ NaOH, what will ΔT be?"
    p.font.size = Pt(14)
    p.font.bold = True
    p.font.color.rgb = NAVY

    opts = [
        ("1", "ΔT = 3.25 °C (half, because volume doubled)", False),
        ("2", "ΔT = 6.5 °C (unchanged, because twice the heat heats twice the mass)", True),
        ("3", "ΔT = 13.0 °C (double, because twice the moles reacted)", False),
        ("4", "ΔT = 0 °C (neutral solution absorbs heat)", False)
    ]

    for idx, (num, text, is_correct) in enumerate(opts):
        col = idx % 2
        row = idx // 2
        left = Inches(0.6 + col * 6.1)
        top = Inches(2.8 + row * 1.5)
        
        opt_shape = s12.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, Inches(5.8), Inches(1.2))
        opt_shape.fill.solid()
        if is_correct:
            opt_shape.fill.fore_color.rgb = RGBColor(240, 253, 244)
            opt_shape.line.color.rgb = TAG_GREEN
            opt_shape.line.width = Pt(2.5)
        else:
            opt_shape.fill.fore_color.rgb = CARD_BG
            opt_shape.line.color.rgb = CARD_BORDER

        # Number circle
        num_circle = s12.shapes.add_shape(MSO_SHAPE.OVAL, left + Inches(0.2), top + Inches(0.35), Inches(0.5), Inches(0.5))
        num_circle.fill.solid()
        num_circle.fill.fore_color.rgb = TAG_AMBER
        num_circle.line.fill.background()
        p = num_circle.text_frame.paragraphs[0]
        p.text = num
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

        tx = s12.shapes.add_textbox(left + Inches(0.8), top + Inches(0.2), Inches(4.8), Inches(0.8))
        tf = tx.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.text = text
        p.font.size = Pt(12)
        p.font.color.rgb = TEXT_MAIN

    # Answer explanation strip
    ans_box = s12.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), Inches(5.8), Inches(12.0), Inches(1.0))
    ans_box.fill.solid()
    ans_box.fill.fore_color.rgb = RGBColor(220, 252, 231)
    ans_box.line.color.rgb = TAG_GREEN
    p = ans_box.text_frame.paragraphs[0]
    p.text = "✔ Correct Answer: 2 (ΔT = 6.5 °C)."
    p.font.bold = True
    p.font.size = Pt(12)
    p.font.color.rgb = RGBColor(22, 101, 52)
    p2 = ans_box.text_frame.add_paragraph()
    p2.text = "Scientific Reasoning: Twice as many moles react, releasing 2× the heat energy (q). However, the total solution mass (m) is also doubled (100 g vs 50 g). Since ΔT = q / (m·c), the factor of 2 cancels out, resulting in the exact same temperature rise."
    p2.font.size = Pt(10)
    p2.font.color.rgb = TEXT_MAIN
    add_footer(s12)

    # ==========================================
    # SLIDE 13: EXIT TICKET & RUBRIC SELF-ASSESSMENT
    # ==========================================
    s13 = prs.slides.add_slide(blank_layout)
    add_header(s13, "EXIT TICKET", TAG_CORAL, "Criterion B & C Self-Assessment (Traffic Lights)")

    standards = [
        ("Criterion B (i & ii)", "I have stated a focused research question and formulated a testable hypothesis with net ionic bond energy justification."),
        ("Criterion B (iii & iv)", "I have fully described all variables (5 IV values, DV precision, 3 controlled variables) and a safe, numbered method."),
        ("Criterion C (i & ii)", "I have recorded raw data with correct SI units/uncertainties, removed anomalies, and plotted an appropriately scaled graph."),
        ("Criterion C (iii)", "I have interpreted experimental trends and calculated percentage error against the literature value (-57.1 kJ/mol)."),
        ("Criterion C (iv & v)", "I have critically evaluated systematic vs random errors and suggested specific, realistic procedural improvements.")
    ]

    for idx, (crit_tag, crit_desc) in enumerate(standards):
        top = Inches(1.8 + idx * 0.95)
        
        # Tag box
        t_box = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.6), top, Inches(2.5), Inches(0.75))
        t_box.fill.solid()
        t_box.fill.fore_color.rgb = NAVY
        t_box.line.color.rgb = NAVY
        p = t_box.text_frame.paragraphs[0]
        p.text = crit_tag
        p.font.size = Pt(11)
        p.font.bold = True
        p.font.color.rgb = WHITE
        p.alignment = PP_ALIGN.CENTER

        # Description box
        d_box = s13.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(3.2), top, Inches(7.5), Inches(0.75))
        d_box.fill.solid()
        d_box.fill.fore_color.rgb = CARD_BG
        d_box.line.color.rgb = CARD_BORDER
        p = d_box.text_frame.paragraphs[0]
        p.text = crit_desc
        p.font.size = Pt(10.5)
        p.font.color.rgb = TEXT_MAIN

        # Traffic light circles (Green, Amber, Red)
        colors = [RGBColor(239, 68, 68), RGBColor(245, 158, 11), RGBColor(16, 185, 129)]
        for c_idx, c in enumerate(colors):
            circle = s13.shapes.add_shape(MSO_SHAPE.OVAL, Inches(10.9 + c_idx * 0.65), top + Inches(0.12), Inches(0.5), Inches(0.5))
            circle.fill.background()
            circle.line.color.rgb = c
            circle.line.width = Pt(2.5)

    add_footer(s13)

    # Save presentation
    output_filename = "MYP5_Chemistry_Criterion_B_C_Unit.pptx"
    prs.save(output_filename)
    print(f"Presentation generated successfully: {output_filename}")

if __name__ == "__main__":
    create_myp5_presentation()
