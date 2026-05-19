#!/usr/bin/env python3
"""
Shock Wave Analysis in Aluminum - REAL DATA
Post-processing script for LAMMPS simulation
Rania Zaier - May 2026
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams
import sys

# Publication-quality settings
rcParams['font.family'] = 'sans-serif'
rcParams['font.size'] = 11
rcParams['axes.linewidth'] = 1.2

def parse_lammps_log(filename='log.lammps'):
    """Extract thermodynamic data from LAMMPS log file"""
    data = {'Step': [], 'Temp': [], 'Press': [], 'PotEng': [], 'KinEng': []}
    
    with open(filename, 'r') as f:
        lines = f.readlines()
    
    reading_data = False
    for line in lines:
        # More flexible header detection
        if 'Step' in line and 'Temp' in line and 'Press' in line:
            reading_data = True
            continue
        if reading_data and ('Loop time' in line or 'Total wall time' in line):
            break
        if reading_data:
            parts = line.split()
            if len(parts) >= 6:
                try:
                    data['Step'].append(int(parts[0]))
                    data['Temp'].append(float(parts[1]))
                    data['Press'].append(float(parts[2]))
                    data['PotEng'].append(float(parts[3]))
                    data['KinEng'].append(float(parts[4]))
                except ValueError:
                    continue
    
    return {k: np.array(v) for k, v in data.items()}

def plot_pressure_evolution(data):
    """Plot pressure evolution over time"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    time_ps = data['Step'] * 0.001  # Convert to picoseconds
    pressure_gpa = data['Press'] / 10000  # Convert bar to GPa
    
    ax.plot(time_ps, pressure_gpa, linewidth=2.5, color='#A23B72', 
            label='System pressure')
    
    ax.set_xlabel('Time (ps)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Pressure (GPa)', fontsize=13, fontweight='bold')
    ax.set_title('Pressure Evolution During Shock Wave Propagation\nAluminum - LAMMPS Simulation', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=11, frameon=True, shadow=True)
    
    plt.tight_layout()
    plt.savefig('pressure_evolution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: pressure_evolution.png")

def plot_temperature_evolution(data):
    """Plot temperature evolution"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    time_ps = data['Step'] * 0.001
    
    ax.plot(time_ps, data['Temp'], linewidth=2.5, color='#2E86AB',
            label='System temperature')
    ax.axhline(y=300, color='gray', linestyle='--', linewidth=1, 
               alpha=0.5, label='Initial temp (300K)')
    
    ax.set_xlabel('Time (ps)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Temperature (K)', fontsize=13, fontweight='bold')
    ax.set_title('Temperature Evolution During Shock Wave Propagation\nAluminum - LAMMPS Simulation', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=11, frameon=True, shadow=True)
    
    plt.tight_layout()
    plt.savefig('temperature_evolution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: temperature_evolution.png")

def plot_energy_evolution(data):
    """Plot potential and kinetic energy"""
    fig, ax = plt.subplots(figsize=(10, 6))
    
    time_ps = data['Step'] * 0.001
    
    ax.plot(time_ps, data['PotEng'], linewidth=2.5, color='#F18F01',
            label='Potential Energy', alpha=0.8)
    ax.plot(time_ps, data['KinEng'], linewidth=2.5, color='#06A77D',
            label='Kinetic Energy', alpha=0.8)
    ax.plot(time_ps, data['PotEng'] + data['KinEng'], linewidth=2,
            color='black', linestyle='--', label='Total Energy', alpha=0.6)
    
    ax.set_xlabel('Time (ps)', fontsize=13, fontweight='bold')
    ax.set_ylabel('Energy (eV)', fontsize=13, fontweight='bold')
    ax.set_title('Energy Evolution During Shock Wave Propagation\nAluminum - LAMMPS Simulation', 
                 fontsize=14, fontweight='bold', pad=15)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=11, frameon=True, shadow=True)
    
    plt.tight_layout()
    plt.savefig('energy_evolution.png', dpi=300, bbox_inches='tight')
    print("✓ Saved: energy_evolution.png")

def print_summary(data):
    """Print simulation summary statistics"""
    print("\n" + "="*60)
    print("SIMULATION SUMMARY")
    print("="*60)
    print(f"Total timesteps:     {len(data['Step'])}")
    print(f"Simulation time:     {data['Step'][-1] * 0.001:.1f} ps")
    print(f"\nInitial temperature: {data['Temp'][0]:.1f} K")
    print(f"Final temperature:   {data['Temp'][-1]:.1f} K")
    print(f"Max temperature:     {data['Temp'].max():.1f} K")
    print(f"\nInitial pressure:    {data['Press'][0]/10000:.2f} GPa")
    print(f"Max pressure:        {data['Press'].max()/10000:.2f} GPa")
    print(f"Final pressure:      {data['Press'][-1]/10000:.2f} GPa")
    print("="*60 + "\n")

def main():
    print("="*60)
    print("Shock Wave Analysis - Aluminum")
    print("LAMMPS Simulation Post-Processing")
    print("="*60)
    print()
    
    # Parse log file
    print("Reading log.lammps...")
    try:
        data = parse_lammps_log('log.lammps')
        if len(data['Step']) == 0:
            print("✗ No data found in log file!")
            sys.exit(1)
        print(f"✓ Loaded {len(data['Step'])} timesteps")
    except Exception as e:
        print(f"✗ Error reading log file: {e}")
        sys.exit(1)
    
    # Print summary
    print_summary(data)
    
    # Generate plots
    print("Generating analysis plots...")
    plot_pressure_evolution(data)
    plot_temperature_evolution(data)
    plot_energy_evolution(data)
    
    print("\n" + "="*60)
    print("Analysis complete!")
    print("Generated files:")
    print("  - pressure_evolution.png")
    print("  - temperature_evolution.png")
    print("  - energy_evolution.png")
    print("="*60)

if __name__ == "__main__":
    main()