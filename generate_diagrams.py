import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

def generate_clean_diagrams():
    plt.rcParams['font.family'] = 'DejaVu Sans'

    # ==========================================
    # 1. pH SCALE DIAGRAM
    # ==========================================
    fig, ax = plt.subplots(figsize=(10, 3.0), dpi=200)
    ax.set_xlim(-0.5, 14.5)
    ax.set_ylim(-1.4, 2.6)
    ax.axis('off')

    colors = [
        '#EF4444', '#F87171', '#FB923C', '#FBBF24', '#FDE047', 
        '#FEF08A', '#A3E635', '#22C55E', '#10B981', '#14B8A6', 
        '#06B6D4', '#3B82F6', '#6366F1', '#8B5CF6', '#6D28D9'
    ]

    for i in range(15):
        rect = patches.Rectangle((i - 0.45, 0.4), 0.9, 0.8, color=colors[i], ec='white', lw=1.5)
        ax.add_patch(rect)
        ax.text(i, 0.8, str(i), ha='center', va='center', color='white' if i not in [4,5,6] else '#1E293B', fontweight='bold', fontsize=11)

    ax.annotate('', xy=(-0.4, 1.4), xytext=(6.4, 1.4), arrowprops=dict(arrowstyle='<->', color='#DC2626', lw=2))
    ax.text(3.0, 1.6, 'ACIDIC (Excess H+ / H3O+)', ha='center', color='#DC2626', fontweight='bold', fontsize=10.5)

    ax.text(7.0, 1.6, 'NEUTRAL\n([H+]=[OH-])', ha='center', color='#16A34A', fontweight='bold', fontsize=9.5)

    ax.annotate('', xy=(7.6, 1.4), xytext=(14.4, 1.4), arrowprops=dict(arrowstyle='<->', color='#4F46E5', lw=2))
    ax.text(11.0, 1.6, 'ALKALINE / BASIC (Excess OH-)', ha='center', color='#4F46E5', fontweight='bold', fontsize=10.5)

    benchmarks = [
        (0.0, "Battery\nAcid", -0.65),
        (1.5, "Stomach\nAcid", -0.65),
        (2.5, "Lemon\nJuice", -0.65),
        (3.5, "Vinegar\n(CH3COOH)", -0.65),
        (5.0, "Black\nCoffee", -0.65),
        (7.0, "Pure\nWater", -0.65),
        (7.4, "Human\nBlood", -1.1),
        (9.0, "Baking\nSoda", -0.65),
        (11.5, "Household\nAmmonia", -0.65),
        (13.0, "Bleach\n(NaOCl)", -0.65),
        (14.0, "Drain\nCleaner", -0.65)
    ]

    for x_val, text, y_val in benchmarks:
        ax.plot([x_val, x_val], [0.35, 0.0], color='#94A3B8', lw=1, ls='--')
        ax.text(x_val, y_val, text, ha='center', va='top', fontsize=8, color='#0F172A', fontweight='semibold')

    plt.tight_layout()
    plt.savefig('diagram_ph_scale.png', bbox_inches='tight')
    plt.close()

    # ==========================================
    # 2. PERIODIC TRENDS DIAGRAM
    # ==========================================
    fig, ax = plt.subplots(figsize=(7.5, 4.0), dpi=200)
    ax.set_xlim(-0.5, 10.5)
    ax.set_ylim(-0.5, 6.5)
    ax.axis('off')

    s_block = patches.Rectangle((0.5, 1.0), 1.5, 4.5, facecolor='#DBEAFE', edgecolor='#2563EB', lw=2, alpha=0.9)
    ax.add_patch(s_block)
    ax.text(1.25, 3.25, 's-block\n(Metals)\nGp 1 & 2', ha='center', va='center', fontweight='bold', fontsize=10, color='#1E40AF')

    d_block = patches.Rectangle((2.3, 1.0), 3.8, 2.5, facecolor='#FEF3C7', edgecolor='#D97706', lw=2, alpha=0.9)
    ax.add_patch(d_block)
    ax.text(4.2, 2.25, 'd-block (Transition Metals)\nVariable Oxidation States', ha='center', va='center', fontweight='bold', fontsize=9.5, color='#B45309')

    p_block = patches.Rectangle((6.4, 1.0), 3.2, 4.5, facecolor='#D1FAE5', edgecolor='#059669', lw=2, alpha=0.9)
    ax.add_patch(p_block)
    ax.text(8.0, 3.25, 'p-block\nNon-Metals\n& Halogens', ha='center', va='center', fontweight='bold', fontsize=10, color='#065F46')

    ax.annotate(
        '', xy=(0.5, 0.4), xytext=(9.6, 0.4),
        arrowprops=dict(arrowstyle='->', lw=3.5, color='#DC2626')
    )
    ax.text(5.05, 0.05, 'METALLIC REACTIVITY & ATOMIC RADIUS INCREASES (<- and down)', ha='center', color='#DC2626', fontweight='bold', fontsize=8.5)

    ax.annotate(
        '', xy=(9.6, 5.8), xytext=(0.5, 5.8),
        arrowprops=dict(arrowstyle='->', lw=3.5, color='#4338CA')
    )
    ax.text(5.05, 6.15, 'NON-METALLIC REACTIVITY & IONIZATION ENERGY INCREASES (-> and up)', ha='center', color='#4338CA', fontweight='bold', fontsize=8.5)

    plt.tight_layout()
    plt.savefig('diagram_periodic_trends.png', bbox_inches='tight')
    plt.close()

    # ==========================================
    # 3. EXOTHERMIC ENERGY PROFILE (NEUTRALIZATION)
    # ==========================================
    fig, ax = plt.subplots(figsize=(6.5, 4.0), dpi=200)
    x = np.linspace(0, 10, 300)
    y = 6.0 + 3.0 * np.exp(-((x - 4.5)**2) / 1.2) - 3.5 / (1 + np.exp(-2.5 * (x - 5.5)))

    ax.plot(x, y, color='#DC2626', lw=3.5)
    ax.set_xlim(-0.5, 11)
    ax.set_ylim(0, 10.5)

    ax.plot([0, 2.5], [6.0, 6.0], color='#1E293B', lw=2, ls='--')
    ax.text(1.25, 6.3, 'Reactants:\nH+(aq) + OH-(aq)', ha='center', va='bottom', fontweight='bold', fontsize=9.5, color='#1E3A8A')

    ax.plot([7.5, 10.0], [2.5, 2.5], color='#1E293B', lw=2, ls='--')
    ax.text(8.75, 2.8, 'Products:\nH2O(l) + Salt', ha='center', va='bottom', fontweight='bold', fontsize=9.5, color='#065F46')

    ax.annotate('', xy=(4.5, 8.8), xytext=(4.5, 6.0), arrowprops=dict(arrowstyle='<->', color='#D97706', lw=2))
    ax.text(4.7, 7.4, 'Activation Energy (Ea)\nBond Breaking', color='#B45309', fontweight='bold', fontsize=8.5)

    ax.annotate('', xy=(8.0, 2.5), xytext=(8.0, 6.0), arrowprops=dict(arrowstyle='<->', color='#2563EB', lw=2.5))
    ax.text(8.2, 4.25, 'Delta H = -57.1 kJ/mol\n(EXOTHERMIC\nHeat Released)', color='#1D4ED8', fontweight='bold', fontsize=9)

    ax.set_title('Exothermic Neutralization Energy Profile', fontweight='bold', fontsize=11, pad=10, color='#0F172A')
    ax.set_xlabel('Reaction Progress', fontweight='bold', fontsize=9.5)
    ax.set_ylabel('Potential Energy (kJ/mol)', fontweight='bold', fontsize=9.5)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    plt.tight_layout()
    plt.savefig('diagram_energy_profile.png', bbox_inches='tight')
    plt.close()

    # ==========================================
    # 4. GAS CONFIRMATION TESTS (3 PANELS)
    # ==========================================
    fig, axes = plt.subplots(1, 3, figsize=(10, 3.0), dpi=200)

    # Panel 1: Hydrogen Pop Test
    ax1 = axes[0]
    ax1.set_xlim(0, 10)
    ax1.set_ylim(0, 10)
    ax1.axis('off')
    card1 = patches.FancyBboxPatch((0.5, 0.5), 9, 9, boxstyle="round,pad=0.2", fc='#EFF6FF', ec='#3B82F6', lw=2)
    ax1.add_patch(card1)
    ax1.text(5, 8.5, '1. Hydrogen (H2)', ha='center', fontweight='bold', fontsize=11, color='#1D4ED8')
    ax1.text(5, 7.0, 'Squeaky "POP" Test', ha='center', fontweight='bold', fontsize=10, color='#0F172A')
    ax1.text(5, 3.8, '[Burning Splint]\nHeld at test tube mouth.\n\nRapid combustion:\n2 H2(g) + O2(g) -> 2 H2O(l)\nProduces sharp squeaky POP!', ha='center', va='center', fontsize=8.5, color='#334155')

    # Panel 2: Carbon Dioxide Limewater Test
    ax2 = axes[1]
    ax2.set_xlim(0, 10)
    ax2.set_ylim(0, 10)
    ax2.axis('off')
    card2 = patches.FancyBboxPatch((0.5, 0.5), 9, 9, boxstyle="round,pad=0.2", fc='#F0FDF4', ec='#10B981', lw=2)
    ax2.add_patch(card2)
    ax2.text(5, 8.5, '2. Carbon Dioxide (CO2)', ha='center', fontweight='bold', fontsize=11, color='#047857')
    ax2.text(5, 7.0, 'Limewater Cloudiness', ha='center', fontweight='bold', fontsize=10, color='#0F172A')
    ax2.text(5, 3.8, '[Delivery Tube]\nBubbled into clear Ca(OH)2.\n\nTurns MILKY / CLOUDY\nWhite precipitate forms:\nCO2 + Ca(OH)2 -> CaCO3(s) + H2O', ha='center', va='center', fontsize=8.5, color='#334155')

    # Panel 3: Ammonia Gas Damp Litmus Test
    ax3 = axes[2]
    ax3.set_xlim(0, 10)
    ax3.set_ylim(0, 10)
    ax3.axis('off')
    card3 = patches.FancyBboxPatch((0.5, 0.5), 9, 9, boxstyle="round,pad=0.2", fc='#FAF5FF', ec='#8B5CF6', lw=2)
    ax3.add_patch(card3)
    ax3.text(5, 8.5, '3. Ammonia (NH3)', ha='center', fontweight='bold', fontsize=11, color='#6D28D9')
    ax3.text(5, 7.0, 'Damp Red Litmus Test', ha='center', fontweight='bold', fontsize=10, color='#0F172A')
    ax3.text(5, 3.8, '[Damp Litmus Paper]\nHeld over reaction tube.\n\nTURNS BLUE!\nOnly common alkaline gas:\nNH3 + H2O <-> NH4+ + OH-', ha='center', va='center', fontsize=8.5, color='#334155')

    plt.tight_layout()
    plt.savefig('diagram_gas_tests.png', bbox_inches='tight')
    plt.close()

    print("Clean diagrams re-generated successfully!")

if __name__ == "__main__":
    generate_clean_diagrams()
