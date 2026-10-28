import xlsxwriter
import math

def create_interactive_sheets(filename="Interactive_Science_Lab.xlsx"):
    wb = xlsxwriter.Workbook(filename)

    # --- FORMATS ---
    title_fmt = wb.add_format({
        'bold': True, 'font_size': 16, 'font_color': '#FFFFFF',
        'bg_color': '#1E3A8A', 'align': 'center', 'valign': 'vcenter'
    })
    section_fmt = wb.add_format({
        'bold': True, 'font_size': 12, 'font_color': '#1E3A8A',
        'bg_color': '#DBEAFE', 'bottom': 2, 'bottom_color': '#1E3A8A'
    })
    header_fmt = wb.add_format({
        'bold': True, 'font_color': '#FFFFFF', 'bg_color': '#2563EB',
        'align': 'center', 'valign': 'vcenter', 'border': 1
    })
    input_label_fmt = wb.add_format({'bold': True, 'valign': 'vcenter'})
    input_box_fmt = wb.add_format({
        'bold': True, 'bg_color': '#FEF08A', 'font_color': '#854D0E',
        'border': 2, 'border_color': '#EAB308', 'align': 'center', 'valign': 'vcenter'
    })
    calc_fmt = wb.add_format({
        'bold': True, 'bg_color': '#DCFCE7', 'font_color': '#166534',
        'border': 1, 'border_color': '#22C55E', 'align': 'center', 'valign': 'vcenter',
        'num_format': '0.00'
    })
    cell_border = wb.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter'})
    cell_num = wb.add_format({'border': 1, 'align': 'center', 'valign': 'vcenter', 'num_format': '0.00'})

    # ==========================================
    # SHEET 1: ⚡ PHYSICS - PROJECTILE MOTION
    # ==========================================
    ws_phys = wb.add_worksheet("⚡ Projectile Motion")
    ws_phys.set_column('A:A', 4)
    ws_phys.set_column('B:B', 22)
    ws_phys.set_column('C:C', 14)
    ws_phys.set_column('D:D', 18)
    ws_phys.set_column('E:E', 14)
    ws_phys.set_column('F:H', 12)

    # Title
    ws_phys.merge_range('B2:H2', "⚡ Interactive Projectile Motion Simulator", title_fmt)
    ws_phys.set_row(1, 35)

    # Inputs
    ws_phys.merge_range('B4:D4', "1. Experiment Inputs (Edit Yellow Cells)", section_fmt)
    ws_phys.write('B5', "Initial Velocity (v₀, m/s):", input_label_fmt)
    ws_phys.write('C5', 25.0, input_box_fmt)
    
    ws_phys.write('B6', "Launch Angle (θ, degrees):", input_label_fmt)
    ws_phys.write('C6', 45.0, input_box_fmt)

    ws_phys.write('B7', "Gravity (g, m/s²):", input_label_fmt)
    ws_phys.write('C7', 9.81, input_box_fmt)

    # Data Validation for angle (0 to 90 degrees)
    ws_phys.data_validation('C6', {
        'validate': 'decimal',
        'criteria': 'between',
        'minimum': 1,
        'maximum': 89,
        'input_title': 'Launch Angle',
        'input_message': 'Enter angle between 1° and 89°'
    })

    # Computed Outputs
    ws_phys.merge_range('B9:D9', "2. Calculated Physical Quantities", section_fmt)
    
    ws_phys.write('B10', "Total Flight Time (s):", input_label_fmt)
    ws_phys.write_formula('C10', '=2 * C5 * SIN(RADIANS(C6)) / C7', calc_fmt)

    ws_phys.write('B11', "Maximum Height (m):", input_label_fmt)
    ws_phys.write_formula('C11', '=(C5 * SIN(RADIANS(C6)))^2 / (2 * C7)', calc_fmt)

    ws_phys.write('B12', "Total Range / Distance (m):", input_label_fmt)
    ws_phys.write_formula('C12', '=(C5^2 * SIN(2 * RADIANS(C6))) / C7', calc_fmt)

    ws_phys.write('B13', "Initial Vx (Horizontal, m/s):", input_label_fmt)
    ws_phys.write_formula('C13', '=C5 * COS(RADIANS(C6))', calc_fmt)

    ws_phys.write('B14', "Initial Vy (Vertical, m/s):", input_label_fmt)
    ws_phys.write_formula('C14', '=C5 * SIN(RADIANS(C6))', calc_fmt)

    # Trajectory Simulation Table
    ws_phys.merge_range('F4:H4', "3. Trajectory Points", section_fmt)
    ws_phys.write('F5', "Time (s)", header_fmt)
    ws_phys.write('G5', "X Position (m)", header_fmt)
    ws_phys.write('H5', "Y Position (m)", header_fmt)

    # Generate 21 sample steps
    for i in range(21):
        row = 6 + i
        frac = i / 20.0
        ws_phys.write_formula(row, 5, f'=ROUND($C$10 * {frac}, 2)', cell_num)
        ws_phys.write_formula(row, 6, f'=$C$13 * F{row+1}', cell_num)
        ws_phys.write_formula(row, 7, f'=MAX(0, ($C$14 * F{row+1}) - (0.5 * $C$7 * (F{row+1}^2)))', cell_num)

    # Embedded Scatter Chart
    chart = wb.add_chart({'type': 'scatter', 'subtype': 'smooth'})
    chart.add_series({
        'name':       'Trajectory (Flight Path)',
        'categories': "='⚡ Projectile Motion'!$G$6:$G$26",
        'values':     "='⚡ Projectile Motion'!$H$6:$H$26",
        'line':       {'color': '#2563EB', 'width': 2.5},
    })
    chart.set_title({'name': 'Interactive Flight Path (X vs Y)'})
    chart.set_x_axis({'name': 'Horizontal Distance (m)'})
    chart.set_y_axis({'name': 'Height (m)'})
    chart.set_legend({'position': 'none'})
    chart.set_size({'width': 480, 'height': 300})
    ws_phys.insert_chart('B16', chart)


    # ==========================================
    # SHEET 2: 🧬 BIOLOGY - GENETICS (PUNNETT SQUARE)
    # ==========================================
    ws_bio = wb.add_worksheet("🧬 Genetics & Punnett")
    ws_bio.set_column('A:A', 4)
    ws_bio.set_column('B:B', 22)
    ws_bio.set_column('C:E', 14)
    ws_bio.set_column('F:H', 16)

    bio_title_fmt = wb.add_format({
        'bold': True, 'font_size': 16, 'font_color': '#FFFFFF',
        'bg_color': '#065F46', 'align': 'center', 'valign': 'vcenter'
    })
    bio_sec_fmt = wb.add_format({
        'bold': True, 'font_size': 12, 'font_color': '#065F46',
        'bg_color': '#D1FAE5', 'bottom': 2, 'bottom_color': '#065F46'
    })
    gamete_fmt = wb.add_format({
        'bold': True, 'bg_color': '#A7F3D0', 'font_color': '#065F46',
        'border': 1, 'align': 'center', 'valign': 'vcenter', 'font_size': 14
    })
    offspring_fmt = wb.add_format({
        'bold': True, 'bg_color': '#ECFDF5', 'font_color': '#047857',
        'border': 2, 'align': 'center', 'valign': 'vcenter', 'font_size': 14
    })

    # Title
    ws_bio.merge_range('B2:G2', "🧬 Interactive Monohybrid Punnett Square", bio_title_fmt)
    ws_bio.set_row(1, 35)

    # Parental Selection
    ws_bio.merge_range('B4:D4', "1. Select Parental Genotypes", bio_sec_fmt)
    ws_bio.write('B5', "Parent 1 Genotype:", input_label_fmt)
    ws_bio.write('C5', "Aa", input_box_fmt)
    ws_bio.write('B6', "Parent 2 Genotype:", input_label_fmt)
    ws_bio.write('C6', "Aa", input_box_fmt)

    # Dropdowns for Genotypes
    for cell in ['C5', 'C6']:
        ws_bio.data_validation(cell, {
            'validate': 'list',
            'source': ['AA', 'Aa', 'aa'],
            'input_title': 'Genotype',
            'input_message': 'Choose AA, Aa, or aa'
        })

    # Extracted Gametes (hidden logic formulas)
    ws_bio.write('C8', '=MID(C5, 1, 1)', gamete_fmt) # Parent 1 Allele 1
    ws_bio.write('D8', '=MID(C5, 2, 1)', gamete_fmt) # Parent 1 Allele 2
    ws_bio.write('B9', '=MID(C6, 1, 1)', gamete_fmt) # Parent 2 Allele 1
    ws_bio.write('B10', '=MID(C6, 2, 1)', gamete_fmt) # Parent 2 Allele 2

    # Punnett Square Grid
    ws_bio.write_formula('C9', '=C8 & B9', offspring_fmt)
    ws_bio.write_formula('D9', '=D8 & B9', offspring_fmt)
    ws_bio.write_formula('C10', '=C8 & B10', offspring_fmt)
    ws_bio.write_formula('D10', '=D8 & B10', offspring_fmt)

    # Phenotypic & Genotypic Outcomes
    ws_bio.merge_range('F4:H4', "2. Expected Ratios", bio_sec_fmt)
    ws_bio.write('F5', "Genotype Ratio", header_fmt)
    ws_bio.write('G5', "Count (/4)", header_fmt)
    ws_bio.write('H5', "Percentage", header_fmt)

    ws_bio.write('F6', "Homozygous Dominant (AA)", input_label_fmt)
    ws_bio.write_formula('G6', '=COUNTIF(C9:D10, "AA")', cell_border)
    ws_bio.write_formula('H6', '=G6 / 4', wb.add_format({'border': 1, 'align': 'center', 'num_format': '0.0%'}))

    ws_bio.write('F7', "Heterozygous (Aa / aA)", input_label_fmt)
    ws_bio.write_formula('G7', '=COUNTIF(C9:D10, "Aa") + COUNTIF(C9:D10, "aA")', cell_border)
    ws_bio.write_formula('H7', '=G7 / 4', wb.add_format({'border': 1, 'align': 'center', 'num_format': '0.0%'}))

    ws_bio.write('F8', "Homozygous Recessive (aa)", input_label_fmt)
    ws_bio.write_formula('G8', '=COUNTIF(C9:D10, "aa")', cell_border)
    ws_bio.write_formula('H8', '=G8 / 4', wb.add_format({'border': 1, 'align': 'center', 'num_format': '0.0%'}))

    # Phenotype summary
    ws_bio.merge_range('F10:H10', "3. Phenotypic Expression (A = Dominant)", bio_sec_fmt)
    ws_bio.write('F11', "Dominant Trait (Purple Flower)", input_label_fmt)
    ws_bio.write_formula('G11', '=G6 + G7', calc_fmt)
    ws_bio.write_formula('H11', '=G11 / 4', wb.add_format({'border': 1, 'align': 'center', 'num_format': '0.0%'}))

    ws_bio.write('F12', "Recessive Trait (White Flower)", input_label_fmt)
    ws_bio.write_formula('G12', '=G8', calc_fmt)
    ws_bio.write_formula('H12', '=G12 / 4', wb.add_format({'border': 1, 'align': 'center', 'num_format': '0.0%'}))


    # ==========================================
    # SHEET 3: 🧪 POPULATION ECOLOGY (LOGISTIC GROWTH)
    # ==========================================
    ws_eco = wb.add_worksheet("🌱 Population Ecology")
    ws_eco.set_column('A:A', 4)
    ws_eco.set_column('B:B', 22)
    ws_eco.set_column('C:C', 14)
    ws_eco.set_column('D:D', 4)
    ws_eco.set_column('E:F', 14)

    eco_title_fmt = wb.add_format({
        'bold': True, 'font_size': 16, 'font_color': '#FFFFFF',
        'bg_color': '#78350F', 'align': 'center', 'valign': 'vcenter'
    })
    eco_sec_fmt = wb.add_format({
        'bold': True, 'font_size': 12, 'font_color': '#78350F',
        'bg_color': '#FEF3C7', 'bottom': 2, 'bottom_color': '#78350F'
    })

    ws_eco.merge_range('B2:F2', "🌱 Logistic Population Growth Model (dN/dt)", eco_title_fmt)
    ws_eco.set_row(1, 35)

    ws_eco.merge_range('B4:C4', "Parameters", eco_sec_fmt)
    ws_eco.write('B5', "Initial Population (N₀):", input_label_fmt)
    ws_eco.write('C5', 20, input_box_fmt)
    ws_eco.write('B6', "Carrying Capacity (K):", input_label_fmt)
    ws_eco.write('C6', 500, input_box_fmt)
    ws_eco.write('B7', "Growth Rate (r):", input_label_fmt)
    ws_eco.write('C7', 0.25, input_box_fmt)

    ws_eco.merge_range('E4:F4', "Population vs Time", eco_sec_fmt)
    ws_eco.write('E5', "Time (Generations)", header_fmt)
    ws_eco.write('F5', "Population (N)", header_fmt)

    # N(t) = K / (1 + ((K - N0)/N0) * e^(-r*t))
    for t in range(25):
        r_idx = 6 + t
        ws_eco.write(r_idx, 4, t, cell_border)
        ws_eco.write_formula(r_idx, 5, f'=ROUND($C$6 / (1 + (($C$6 - $C$5)/$C$5) * EXP(-$C$7 * E{r_idx+1})), 0)', cell_border)

    eco_chart = wb.add_chart({'type': 'line'})
    eco_chart.add_series({
        'name':       'Population (N)',
        'categories': "='🌱 Population Ecology'!$E$6:$E$30",
        'values':     "='🌱 Population Ecology'!$F$6:$F$30",
        'line':       {'color': '#16A34A', 'width': 2.5},
    })
    eco_chart.set_title({'name': 'S-Curve: Population Approaching Carrying Capacity (K)'})
    eco_chart.set_x_axis({'name': 'Time (Generations)'})
    eco_chart.set_y_axis({'name': 'Population (N)'})
    eco_chart.set_legend({'position': 'none'})
    eco_chart.set_size({'width': 450, 'height': 280})
    ws_eco.insert_chart('B10', eco_chart)

    wb.close()
    print(f"Workbook '{filename}' generated successfully!")

if __name__ == "__main__":
    create_interactive_sheets()
