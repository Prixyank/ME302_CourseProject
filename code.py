import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def solve_me302_project(file_path):
    try:
        df = pd.read_excel(file_path)
    except:
        return
        
    col_mdot = [c for c in df.columns if 'mdot' in c.lower()][0]
    col_tr = [c for c in df.columns if 't0' in c.lower() or 'temp' in c.lower()][0]
    col_pr = [c for c in df.columns if 'p0' in c.lower() or 'press' in c.lower()][0]
    
    max_s = 0
    best_point = None
    best_p01 = 0
    
    for _, row in df.iterrows():
        mdot_ref = row[col_mdot]
        TR = row[col_tr]
        PR = row[col_pr]
        
        if PR < 1.06866:
            continue
            
        s_calc = 0.21270 * np.sqrt((mdot_ref * np.sqrt(TR)) / PR)
        
        s_max_pressure = 0.65654 * np.sqrt(TR)
        if s_calc > s_max_pressure:
            continue
            
        if s_calc > 1.0:
            s_calc = 1.0
            
        if s_calc > max_s:
            max_s = s_calc
            best_point = (mdot_ref, TR, PR)
            best_p01 = 158.13 * np.sqrt(TR) / (s_calc * PR)
            
    if best_point:
        print(f"1. Maximum Scale (s): {max_s:.4f}")
        print(f"2. Inlet Stagnation Pressure (p01): {best_p01:.2f} kPa")
        print(f"3. Compressor Operating Point:")
        print(f"   - mdot_ref: {best_point[0]:.4f} kg/s")
        print(f"   - T0 ratio: {best_point[1]:.4f}")
        print(f"   - p0 ratio: {best_point[2]:.4f}")
        
        plt.figure(figsize=(9, 6))
        plt.plot(df[col_mdot], df[col_pr], 'o', color='orange', label='Compressor Characteristic Curve')
        plt.plot(best_point[0], best_point[2], '*', color='green', markersize=18, label='Optimal Point (Max Scale)')

        plt.title('Compressor Operating Curve (ME302 Project)', fontsize=14)
        plt.xlabel(r'Reference Mass Flow Rate ($\dot{m}_{ref}$)', fontsize=12)
        plt.ylabel('Stagnation Pressure Ratio ($p_{02}/p_{01}$)', fontsize=12)
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.legend(fontsize=11)
        plt.tight_layout()
        plt.savefig('ME302_Compressor_Curve.png', dpi=300)
        plt.show()

solve_me302_project('compressor_map.xlsx')
