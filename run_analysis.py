import os
import sys
import time
from datetime import datetime

def ensure_directories():
    """Create all necessary directories"""
    directories = [
        'data',
        'scripts',
        'outputs/text_files',
        'outputs/figures'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)

def combine_text_reports():
    """Combine all text reports into a single comprehensive report"""
    text_files = {
        'crisis_impact_analysis.txt': '1. CRISIS IMPACT ANALYSIS',
        'trade_network_analysis.txt': '2. TRADE NETWORK ANALYSIS',
        'statistical_analysis.txt': '3. STATISTICAL ANALYSIS',
        'statistical_analysis_results.txt': '4. DETAILED STATISTICAL RESULTS',
        'emerging_markets_report.txt': '5. EMERGING MARKETS ANALYSIS',
        'findings.txt': '6. KEY FINDINGS'
    }
    
    print("\nCombining text reports...")
    
    report_content = [
        "="*80,
        "COMPREHENSIVE TRADE NETWORK ANALYSIS REPORT",
        "="*80,
        f"\nGenerated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n",
        "="*80 + "\n\n"
    ]
    
    for filename, section_title in text_files.items():
        filepath = os.path.join('outputs/text_files', filename)
        if os.path.exists(filepath):
            report_content.extend([
                "="*80,
                section_title,
                "="*80 + "\n"
            ])
            
            with open(filepath, 'r') as f:
                report_content.append(f.read().strip())
            report_content.append("\n\n")
            print(f"✓ Added {filename}")
        else:
            print(f"⚠ Warning: {filename} not found")
    
    # Save comprehensive report
    comprehensive_report_path = 'outputs/text_files/comprehensive_report.txt'
    with open(comprehensive_report_path, 'w') as f:
        f.write('\n'.join(report_content))
    
    print(f"\n✓ Comprehensive report saved to: {comprehensive_report_path}")

def print_section(title):
    """Print a formatted section title"""
    print("\n" + "="*80)
    print(f" {title} ".center(80, "="))
    print("="*80 + "\n")

def run_script(script_name):
    """Run a Python script and return its exit code"""
    print(f"Running {script_name}...")
    start_time = time.time()
    
    # Run the script
    exit_code = os.system(f"python scripts/{script_name}")
    
    # Calculate execution time
    execution_time = time.time() - start_time
    
    if exit_code == 0:
        print(f"✓ {script_name} completed successfully in {execution_time:.2f} seconds")
    else:
        print(f"✗ {script_name} failed with exit code {exit_code}")
    
    return exit_code

def main():
    print_section("Trade Network Analysis Pipeline")
    print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Ensure directories exist
    print("\nSetting up directories...")
    ensure_directories()
    print("✓ Directories created")
    
    # List of analysis scripts to run
    analysis_scripts = [
        'analyze_trade_network.py',
        'analyze_emerging_markets.py',
        'analyze_policy_impacts.py',
        'analyze_centrality_contagion.py'
    ]
    
    # Run each analysis script
    print_section("Running Analysis Scripts")
    
    failed_scripts = []
    for script in analysis_scripts:
        if run_script(script) != 0:
            failed_scripts.append(script)
    
    # Combine text reports
    if not failed_scripts:
        print_section("Generating Comprehensive Report")
        combine_text_reports()
    
    # Print summary
    print_section("Analysis Complete")
    print(f"Finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if failed_scripts:
        print("\nWarning: The following scripts failed:")
        for script in failed_scripts:
            print(f"  - {script}")
        sys.exit(1)
    else:
        print("\nAll analyses completed successfully!")
        print("\nOutput files can be found in:")
        print("  - outputs/text_files/comprehensive_report.txt  (Combined analysis report)")
        print("  - outputs/text_files/                         (Individual analysis files)")
        print("  - outputs/figures/                            (Visualizations)")
        sys.exit(0)

if __name__ == "__main__":
    main() 