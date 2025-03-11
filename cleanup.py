import os
import shutil
from datetime import datetime

def setup_directories():
    """Create output directories if they don't exist"""
    for directory in ['outputs/text_files', 'outputs/figures', 'data', 'scripts']:
        os.makedirs(directory, exist_ok=True)

def cleanup_files():
    """Move files to appropriate directories and create backup of existing files"""
    # Define file types
    script_files = [
        'analyze_trade_network.py',
        'analyze_emerging_markets.py',
        'analyze_policy_impacts.py'
    ]
    
    text_files = [
        'findings.txt',
        'statistical_analysis_results.txt',
        'emerging_markets_report.txt',
        'detailed_analysis_results.txt',
        'crisis_impact_analysis.txt'
    ]
    
    csv_outputs = [
        'regional_resilience_metrics.csv',
        'regional_analysis_results.csv',
        'policy_analysis_results.csv'
    ]
    
    data_files = [
        'Cepii_centrality_measures.csv'
    ]
    
    figure_files = [
        'network_evolution.png',
        'regional_trade.png',
        'top_powers_evolution.png',
        'trade_network_comparison.png',
        'regional_analysis.png',
        'trade_network_evolution.png',
        'sectoral_analysis_basic.png',
        'sectoral_analysis_advanced.png',
        'financial_integration.png',
        'emerging_markets_evolution.png',
        'regional_integration_patterns.png',
        'network_metrics_evolution.png'
    ]
    
    # Create timestamp for backups
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Move script files
    for file in script_files:
        if os.path.exists(file):
            dest_path = f'scripts/{file}'
            if os.path.exists(dest_path):
                backup_path = f'scripts/backup_{timestamp}_{file}'
                shutil.move(dest_path, backup_path)
                print(f"Created backup: {backup_path}")
            shutil.move(file, dest_path)
            print(f"Moved {file} to scripts/")
    
    # Move text files
    for file in text_files:
        if os.path.exists(file):
            dest_path = f'outputs/text_files/{file}'
            if os.path.exists(dest_path):
                backup_path = f'outputs/text_files/backup_{timestamp}_{file}'
                shutil.move(dest_path, backup_path)
                print(f"Created backup: {backup_path}")
            shutil.move(file, dest_path)
            print(f"Moved {file} to outputs/text_files/")
    
    # Move CSV output files
    for file in csv_outputs:
        if os.path.exists(file):
            dest_path = f'outputs/text_files/{file}'
            if os.path.exists(dest_path):
                backup_path = f'outputs/text_files/backup_{timestamp}_{file}'
                shutil.move(dest_path, backup_path)
                print(f"Created backup: {backup_path}")
            shutil.move(file, dest_path)
            print(f"Moved {file} to outputs/text_files/")
    
    # Move data files
    for file in data_files:
        if os.path.exists(file):
            dest_path = f'data/{file}'
            if os.path.exists(dest_path):
                backup_path = f'data/backup_{timestamp}_{file}'
                shutil.move(dest_path, backup_path)
                print(f"Created backup: {backup_path}")
            shutil.move(file, dest_path)
            print(f"Moved {file} to data/")
            
    # Move figure files
    for file in figure_files:
        if os.path.exists(file):
            dest_path = f'outputs/figures/{file}'
            if os.path.exists(dest_path):
                backup_path = f'outputs/figures/backup_{timestamp}_{file}'
                shutil.move(dest_path, backup_path)
                print(f"Created backup: {backup_path}")
            shutil.move(file, dest_path)
            print(f"Moved {file} to outputs/figures/")

def main():
    print("Starting cleanup process...")
    
    # Create directories
    setup_directories()
    print("Created output directories")
    
    # Move files
    cleanup_files()
    
    print("\nCleanup complete!")
    print("Check README.md for project structure and file descriptions")

if __name__ == "__main__":
    main() 