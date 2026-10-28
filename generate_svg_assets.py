import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generate_svg_assets():
    plt.rcParams['font.family'] = 'DejaVu Sans'

    # =========================================================================
    # 1. DIGESTIVE SYSTEM HOMEOSTASIS DIAGRAM (Stomach to Duodenum)
    # =========================================================================
    fig, ax = plt.subplots(figsize=(8, 4.5), dpi=250)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # Background card
    bg = patches.FancyBboxPatch((0.3, 0.3), 9.4, 9.4, boxstyle="round,pad=0.2", fc='#F8FAFC', ec='#CBD5E1', lw=1.5)
    ax.add_patch(bg)

    # Title
    ax.text(5, 9.2, 'Digestive Acid-Base Homeostasis System', ha='center', fontweight='bold', fontsize=12, color='#0F172A')

    # Stomach Box
    stomach = patches.FancyBboxPatch((0.8, 4.8), 3.8, 3.8, boxstyle="round,pad=0.15", fc='#FEE2E2', ec='#EF4444', lw=2)
    ax.add_patch(stomach)
    ax.text(2.7, 8.0, '1. Gastric Phase (Stomach)', ha='center', fontweight='bold', fontsize=10.5, color='#991B1B')
    ax.text(2.7, 7.3, 'Secretes: Gastric Juice (HCl)\npH 1.5 – 2.0 (High [H⁺])', ha='center', fontsize=9, fontweight='semibold', color='#B91C1C')
    ax.text(2.7, 5.7, '• Denatures dietary proteins\n• Activates pepsin enzyme\n• Sterilizes ingested pathogens', ha='center', fontsize=8.5, color='#334155')

    # Duodenum Box
    duod = patches.FancyBboxPatch((5.4, 4.8), 3.8, 3.8, boxstyle="round,pad=0.15", fc='#EFF6FF', ec='#3B82F6', lw=2)
    ax.add_patch(duod)
    ax.text(7.3, 8.0, '2. Intestinal Phase (Duodenum)', ha='center', fontweight='bold', fontsize=10.5, color='#1E40AF')
    ax.text(7.3, 7.3, 'Secretes: Pancreatic Juice & Bile\npH 7.8 – 8.0 (Alkaline)', ha='center', fontsize=9, fontweight='semibold', color='#2563EB')
    ax.text(7.3, 5.7, '• Rich in NaHCO₃ (Bicarbonate)\n• Rapidly neutralizes chyme\n• Protects intestinal epithelium', ha='center', fontsize=8.5, color='#334155')

    # Arrow connecting Stomach -> Duodenum
    ax.annotate('', xy=(5.3, 6.7), xytext=(4.7, 6.7), arrowprops=dict(arrowstyle='->', lw=3, color='#0F172A'))
    ax.text(5.0, 7.1, 'Chyme\nTransfer', ha='center', fontsize=7.5, fontweight='bold', color='#475569')

    # Neutralization Equation Banner at bottom
    banner = patches.FancyBboxPatch((0.8, 0.8), 8.4, 3.5, boxstyle="round,pad=0.15", fc='#ECFDF5', ec='#10B981', lw=2)
    ax.add_patch(banner)
    ax.text(5, 3.8, 'The In-Vivo Neutralization Reaction', ha='center', fontweight='bold', fontsize=10.5, color='#065F46')
    ax.text(5, 2.9, 'HCl(aq)  +  NaHCO₃(aq)   →   NaCl(aq)  +  H₂O(l)  +  CO₂(g)', ha='center', fontweight='bold', fontsize=11, color='#047857')
    ax.text(5, 2.1, 'Net Ionic: H⁺(aq)  +  HCO₃⁻(aq)   →   H₂O(l)  +  CO₂(g)', ha='center', fontweight='bold', fontsize=10, color='#0D9488')
    ax.text(5, 1.2, 'Key Insight: Protects intestinal enzymes (trypsin, lipase) which would denature in acid.', ha='center', fontsize=8.5, color='#334155')

    plt.tight_layout()
    plt.savefig('visual_digestive_homeostasis.png', bbox_inches='tight')
    plt.savefig('visual_digestive_homeostasis.svg', bbox_inches='tight')
    plt.close()

    # =========================================================================
    # 2. STRONG VS WEAK ACID DISSOCIATION (Particle Model)
    # =========================================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.5), dpi=250)

    # Strong Acid Panel (HCl)
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    beaker1 = patches.FancyBboxPatch((0.5, 0.5), 9, 9, boxstyle="round,pad=0.2", fc='#FEF2F2', ec='#EF4444', lw=2)
    ax1.add_patch(beaker1)
    ax1.text(5, 8.8, 'Strong Acid (e.g. HCl)', ha='center', fontweight='bold', fontsize=11, color='#991B1B')
    ax1.text(5, 8.0, '100% Complete Dissociation', ha='center', fontweight='bold', fontsize=9.5, color='#DC2626')
    ax1.text(5, 7.3, 'HCl(aq) → H⁺(aq) + Cl⁻(aq)', ha='center', fontweight='bold', fontsize=9, color='#0F172A')

    # Draw dissociated ion pairs
    coords1 = [(2.5, 5.5), (7.0, 5.8), (3.0, 3.2), (7.5, 3.5), (5.0, 4.5)]
    for x, y in coords1:
        # H+ circle (small red)
        h_circle = patches.Circle((x, y), 0.5, fc='#EF4444', ec='white', lw=1.5)
        ax1.add_patch(h_circle)
        ax1.text(x, y, 'H⁺', ha='center', va='center', color='white', fontweight='bold', fontsize=8)
        # Cl- circle (larger green)
        cl_circle = patches.Circle((x + 1.2, y - 0.4), 0.65, fc='#10B981', ec='white', lw=1.5)
        ax1.add_patch(cl_circle)
        ax1.text(x + 1.2, y - 0.4, 'Cl⁻', ha='center', va='center', color='white', fontweight='bold', fontsize=8)

    ax1.text(5, 1.2, '• ZERO intact HCl molecules remain\n• High [H⁺] concentration → Low pH (1–2)', ha='center', fontsize=8.5, color='#334155')

    # Weak Acid Panel (CH3COOH)
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    beaker2 = patches.FancyBboxPatch((0.5, 0.5), 9, 9, boxstyle="round,pad=0.2", fc='#FFFBEB', ec='#F59E0B', lw=2)
    ax2.add_patch(beaker2)
    ax2.text(5, 8.8, 'Weak Acid (e.g. CH₃COOH)', ha='center', fontweight='bold', fontsize=11, color='#92400E')
    ax2.text(5, 8.0, 'Partial Reversible Dissociation (~1%)', ha='center', fontweight='bold', fontsize=9.5, color='#D97706')
    ax2.text(5, 7.3, 'CH₃COOH ⇌ H⁺ + CH₃COO⁻', ha='center', fontweight='bold', fontsize=9, color='#0F172A')

    # Draw mostly intact molecules and only ONE dissociated pair
    coords_intact = [(3.0, 5.5), (7.0, 5.8), (3.0, 3.2), (6.8, 3.2)]
    for x, y in coords_intact:
        mol = patches.FancyBboxPatch((x-0.9, y-0.35), 1.8, 0.7, boxstyle="round,pad=0.1", fc='#FCD34D', ec='#B45309', lw=1)
        ax2.add_patch(mol)
        ax2.text(x, y, 'CH₃COOH', ha='center', va='center', color='#78350F', fontweight='bold', fontsize=7.5)

    # 1 dissociated pair
    h_c = patches.Circle((5.0, 4.6), 0.5, fc='#EF4444', ec='white', lw=1.5)
    ax2.add_patch(h_c)
    ax2.text(5.0, 4.6, 'H⁺', ha='center', va='center', color='white', fontweight='bold', fontsize=8)

    ax2.text(5, 1.2, '• >99% molecules stay INTACT\n• Low [H⁺] concentration → Moderate pH (3–5)', ha='center', fontsize=8.5, color='#334155')

    plt.tight_layout()
    plt.savefig('visual_acid_dissociation.png', bbox_inches='tight')
    plt.savefig('visual_acid_dissociation.svg', bbox_inches='tight')
    plt.close()

    # =========================================================================
    # 3. TITRATION 4-STEP MOLE PATHWAY INFOGRAPHIC
    # =========================================================================
    fig, ax = plt.subplots(figsize=(10, 3.5), dpi=250)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 4)
    ax.axis('off')

    steps = [
        ("Step 1: Titre Volume", "V(NaOH) in dm³\n= Titre ÷ 1000", "#EFF6FF", "#3B82F6"),
        ("Step 2: Moles of Known", "n(NaOH) = C × V\n= Moles of base", "#F0FDF4", "#10B981"),
        ("Step 3: Mole Ratio", "Balanced Equation\n1 NaOH : 1 HCl", "#FEF3C7", "#F59E0B"),
        ("Step 4: Concentration", "C(HCl) = n ÷ V\n= Unknown [HCl]", "#FAF5FF", "#8B5CF6")
    ]

    for idx, (title, desc, fc, ec) in enumerate(steps):
        x = 0.5 + idx * 2.4
        box = patches.FancyBboxPatch((x, 0.5), 2.1, 2.8, boxstyle="round,pad=0.15", fc=fc, ec=ec, lw=2)
        ax.add_patch(box)
        ax.text(x + 1.05, 2.8, title, ha='center', fontweight='bold', fontsize=9.5, color='#0F172A')
        ax.text(x + 1.05, 1.6, desc, ha='center', va='center', fontsize=8.5, fontweight='semibold', color='#334155')

        # Arrow between steps
        if idx < 3:
            ax.annotate('', xy=(x + 2.35, 1.9), xytext=(x + 2.15, 1.9), arrowprops=dict(arrowstyle='->', lw=2.5, color='#64748B'))

    plt.tight_layout()
    plt.savefig('visual_titration_pathway.png', bbox_inches='tight')
    plt.savefig('visual_titration_pathway.svg', bbox_inches='tight')
    plt.close()

    # =========================================================================
    # 4. CONSERVATION OF MASS: DUAL BALANCE COMPARISON
    # =========================================================================
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(9, 4.2), dpi=250)

    # Open Flask
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    card1 = patches.FancyBboxPatch((0.5, 0.5), 9, 9, boxstyle="round,pad=0.2", fc='#FEF2F2', ec='#EF4444', lw=2)
    ax1.add_patch(card1)
    ax1.text(5, 8.8, 'Open System (No Stopper)', ha='center', fontweight='bold', fontsize=11, color='#991B1B')
    
    # Balance base
    bal1 = patches.Rectangle((2.5, 2.0), 5.0, 1.5, fc='#334155', ec='#0F172A', lw=1.5)
    ax1.add_patch(bal1)
    # Digital readout
    readout1 = patches.Rectangle((3.5, 2.3), 3.0, 0.9, fc='#0F172A', ec='#38BDF8', lw=1)
    ax1.add_patch(readout1)
    ax1.text(5.0, 2.75, '123.20 g', ha='center', va='center', color='#38BDF8', fontweight='bold', fontsize=12)

    # Flask with bubbles leaving
    flask1 = patches.Polygon([[3.8, 3.6], [6.2, 3.6], [5.6, 6.0], [4.4, 6.0]], closed=True, fc='#E2E8F0', ec='#475569', lw=2)
    ax1.add_patch(flask1)
    ax1.text(5.0, 7.5, '🫧 🫧 🫧\nCO₂ gas escapes!', ha='center', color='#DC2626', fontweight='bold', fontsize=9.5)
    ax1.text(5.0, 1.0, 'Mass DECREASES by 2.20 g\n(Mass of escaped CO₂)', ha='center', fontweight='bold', fontsize=9, color='#B91C1C')

    # Closed Flask
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    card2 = patches.FancyBboxPatch((0.5, 0.5), 9, 9, boxstyle="round,pad=0.2", fc='#F0FDF4', ec='#10B981', lw=2)
    ax2.add_patch(card2)
    ax2.text(5, 8.8, 'Closed System (Sealed Bung)', ha='center', fontweight='bold', fontsize=11, color='#065F46')

    # Balance base
    bal2 = patches.Rectangle((2.5, 2.0), 5.0, 1.5, fc='#334155', ec='#0F172A', lw=1.5)
    ax2.add_patch(bal2)
    readout2 = patches.Rectangle((3.5, 2.3), 3.0, 0.9, fc='#0F172A', ec='#4ADE80', lw=1)
    ax2.add_patch(readout2)
    ax2.text(5.0, 2.75, '125.40 g', ha='center', va='center', color='#4ADE80', fontweight='bold', fontsize=12)

    # Flask with rubber stopper
    flask2 = patches.Polygon([[3.8, 3.6], [6.2, 3.6], [5.6, 6.0], [4.4, 6.0]], closed=True, fc='#E2E8F0', ec='#475569', lw=2)
    ax2.add_patch(flask2)
    stopper = patches.Rectangle((4.5, 6.0), 1.0, 0.6, fc='#78350F', ec='#451A03', lw=1)
    ax2.add_patch(stopper)
    ax2.text(5.0, 7.2, '🔒 Sealed Rubber Stopper\nCO₂ trapped inside', ha='center', color='#047857', fontweight='bold', fontsize=9)
    ax2.text(5.0, 1.0, 'Mass remains CONSTANT\nTotal Reactants = Total Products', ha='center', fontweight='bold', fontsize=9, color='#047857')

    plt.tight_layout()
    plt.savefig('visual_conservation_mass.png', bbox_inches='tight')
    plt.savefig('visual_conservation_mass.svg', bbox_inches='tight')
    plt.close()

    # =========================================================================
    # 5. SINGLE DISPLACEMENT ELECTRON LEAP (Atomic Level)
    # =========================================================================
    fig, ax = plt.subplots(figsize=(8, 4.2), dpi=250)
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 6)
    ax.axis('off')

    bg_disp = patches.FancyBboxPatch((0.2, 0.2), 9.6, 5.6, boxstyle="round,pad=0.2", fc='#F8FAFC', ec='#CBD5E1', lw=1.5)
    ax.add_patch(bg_disp)

    ax.text(5, 5.3, 'Sub-Microscopic Electron Transfer in Single Displacement', ha='center', fontweight='bold', fontsize=11, color='#0F172A')

    # Zinc Metal Atom (Loses 2e-)
    zn_circle = patches.Circle((2.5, 3.0), 1.2, fc='#94A3B8', ec='#475569', lw=2.5)
    ax.add_patch(zn_circle)
    ax.text(2.5, 3.0, 'Zn(s)\nAtom', ha='center', va='center', fontweight='bold', fontsize=10, color='white')
    ax.text(2.5, 1.2, 'OXIDATION\nZn → Zn²⁺ + 2e⁻\n(Loses 2 valence e⁻)', ha='center', fontweight='bold', fontsize=8.5, color='#B91C1C')

    # Copper Ion (Gains 2e-)
    cu_circle = patches.Circle((7.5, 3.0), 1.2, fc='#38BDF8', ec='#0284C7', lw=2.5)
    ax.add_patch(cu_circle)
    ax.text(7.5, 3.0, 'Cu²⁺(aq)\nIon', ha='center', va='center', fontweight='bold', fontsize=10, color='white')
    ax.text(7.5, 1.2, 'REDUCTION\nCu²⁺ + 2e⁻ → Cu(s)\n(Deposits brown solid)', ha='center', fontweight='bold', fontsize=8.5, color='#0369A1')

    # Electron Transfer Curved Arrow
    ax.annotate(
        '', xy=(6.2, 3.4), xytext=(3.8, 3.4),
        arrowprops=dict(arrowstyle='->', connectionstyle="arc3,rad=-0.3", lw=3.5, color='#EAB308')
    )
    ax.text(5.0, 4.3, '2 Valence Electrons Leap (2e⁻)', ha='center', fontweight='bold', fontsize=9.5, color='#B45309')

    plt.tight_layout()
    plt.savefig('visual_electron_leap.png', bbox_inches='tight')
    plt.savefig('visual_electron_leap.svg', bbox_inches='tight')
    plt.close()

    print("All 5 vector SVG and high-DPI diagrams created successfully!")

if __name__ == "__main__":
    generate_svg_assets()
