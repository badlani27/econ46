import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
from scipy import stats
import os

def analyze_emerging_markets_trends(df):
    """Analyze emerging markets trade patterns and network position"""
    # Define emerging markets
    emerging_markets = {
        'BRICS': ['BRA', 'RUS', 'IND', 'CHN', 'ZAF'],
        'Next-11': ['IDN', 'TUR', 'MEX', 'PHL', 'VNM', 'BGD', 'EGY', 'IRN', 'NGA', 'PAK', 'KOR'],
        'MINT': ['MEX', 'IDN', 'NGA', 'TUR']
    }
    
    results = {}
    for group_name, countries in emerging_markets.items():
        yearly_metrics = []
        for year in range(1995, 2011):
            year_data = df[df['t'] == year]
            group_data = year_data[year_data['iso3'].isin(countries)]
            
            metrics = {
                'year': year,
                'avg_out_strength': group_data['Out-strength'].mean(),
                'avg_out_degree': group_data['Out-degree'].mean(),
                'avg_eigenvector': group_data['Out-eigenvector'].mean(),
                'total_trade': group_data['Out-strength'].sum(),
                'network_centrality': group_data['Out-closenness'].mean()
            }
            yearly_metrics.append(metrics)
        results[group_name] = pd.DataFrame(yearly_metrics)
    
    return results

def analyze_regional_integration(df):
    """Analyze regional integration patterns"""
    regions = {
        'East Asia': ['CHN', 'JPN', 'KOR', 'TWN', 'HKG', 'SGP'],
        'Southeast Asia': ['IDN', 'MYS', 'THA', 'VNM', 'PHL'],
        'Europe': ['DEU', 'FRA', 'GBR', 'ITA', 'ESP', 'NLD'],
        'North America': ['USA', 'CAN', 'MEX']
    }
    
    results = {}
    for region_name, countries in regions.items():
        yearly_metrics = []
        for year in range(2007, 2011):
            year_data = df[df['t'] == year]
            region_data = year_data[year_data['iso3'].isin(countries)]
            
            metrics = {
                'year': year,
                'trade_density': region_data['Out-degree'].mean() / len(region_data),
                'network_centrality': region_data['Out-closenness'].mean(),
                'intra_regional_trade': region_data['Out-strength'].sum(),
                'num_countries': len(region_data)
            }
            yearly_metrics.append(metrics)
        results[region_name] = pd.DataFrame(yearly_metrics)
    
    return results

def create_visualization_1(emerging_results):
    """Create visualization of emerging markets evolution"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot trade strength evolution for each group
    for group, data in emerging_results.items():
        ax1.plot(data['year'], data['avg_out_strength'], label=group, marker='o')
        ax2.plot(data['year'], data['avg_out_degree'], label=group, marker='o')
        ax3.plot(data['year'], data['avg_eigenvector'], label=group, marker='o')
        ax4.plot(data['year'], data['network_centrality'], label=group, marker='o')
    
    ax1.set_title('Trade Strength Evolution')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Average Out-Strength')
    ax1.legend()
    ax1.grid(True)
    
    ax2.set_title('Network Connectivity')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Average Out-Degree')
    ax2.legend()
    ax2.grid(True)
    
    ax3.set_title('Network Importance')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Average Eigenvector Centrality')
    ax3.legend()
    ax3.grid(True)
    
    ax4.set_title('Network Position')
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Average Network Centrality')
    ax4.legend()
    ax4.grid(True)
    
    plt.tight_layout()
    return fig

def create_visualization_2(regional_results):
    """Create visualization of regional integration patterns"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    years = [2007, 2009, 2010]
    for region, data in regional_results.items():
        ax1.plot(data['year'], data['trade_density'], label=region, marker='o')
        ax2.plot(data['year'], data['network_centrality'], label=region, marker='o')
    
    ax1.set_title('Regional Trade Integration')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Trade Density')
    ax1.legend()
    ax1.grid(True)
    
    ax2.set_title('Regional Network Centrality')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Average Closeness Centrality')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    return fig

def perform_statistical_tests(df):
    """Perform detailed statistical analysis of trade patterns"""
    # Define periods
    pre_crisis = df[df['t'] == 2007]
    during_crisis = df[df['t'] == 2009]
    post_crisis = df[df['t'] == 2010]
    
    # Statistical tests for different market groups
    def market_group_analysis(countries, name):
        pre = pre_crisis[pre_crisis['iso3'].isin(countries)]['Out-strength']
        during = during_crisis[during_crisis['iso3'].isin(countries)]['Out-strength']
        post = post_crisis[post_crisis['iso3'].isin(countries)]['Out-strength']
        
        # T-tests
        t_stat_decline, p_val_decline = stats.ttest_ind(pre, during)
        t_stat_recovery, p_val_recovery = stats.ttest_ind(during, post)
        
        return {
            'group': name,
            'mean_pre': pre.mean(),
            'mean_during': during.mean(),
            'mean_post': post.mean(),
            'decline_t_stat': t_stat_decline,
            'decline_p_val': p_val_decline,
            'recovery_t_stat': t_stat_recovery,
            'recovery_p_val': p_val_recovery
        }
    
    # Analyze different market groups
    emerging_markets = {
        'BRICS': ['BRA', 'RUS', 'IND', 'CHN', 'ZAF'],
        'Next-11': ['IDN', 'TUR', 'MEX', 'PHL', 'VNM', 'BGD', 'EGY', 'IRN', 'NGA', 'PAK', 'KOR'],
        'Advanced': ['USA', 'DEU', 'JPN', 'GBR', 'FRA', 'ITA', 'CAN']
    }
    
    return {group: market_group_analysis(countries, group) 
            for group, countries in emerging_markets.items()}

def create_network_metrics_visualization(df):
    """Create visualization of network metrics evolution"""
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(15, 12))
    
    # Plot 1: Average Degree Evolution
    yearly_degree = df.groupby('t')['Out-degree'].mean()
    ax1.plot(yearly_degree.index, yearly_degree.values)
    ax1.set_title('Average Network Degree Evolution')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Average Degree')
    ax1.grid(True)
    
    # Plot 2: Network Density
    yearly_density = df.groupby('t')['Out-degree_percent'].mean()
    ax2.plot(yearly_density.index, yearly_density.values)
    ax2.set_title('Network Density Evolution')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Density')
    ax2.grid(True)
    
    # Plot 3: Centralization
    yearly_eigen = df.groupby('t')['Out-eigenvector'].mean()
    ax3.plot(yearly_eigen.index, yearly_eigen.values)
    ax3.set_title('Network Centralization')
    ax3.set_xlabel('Year')
    ax3.set_ylabel('Average Eigenvector Centrality')
    ax3.grid(True)
    
    # Plot 4: Regional Integration
    yearly_close = df.groupby('t')['Out-closenness'].mean()
    ax4.plot(yearly_close.index, yearly_close.values)
    ax4.set_title('Network Integration')
    ax4.set_xlabel('Year')
    ax4.set_ylabel('Average Closeness Centrality')
    ax4.grid(True)
    
    plt.tight_layout()
    return fig

def analyze_regional_resilience(df):
    """Analyze regional resilience metrics"""
    regions = {
        'East Asia': ['CHN', 'JPN', 'KOR', 'TWN', 'HKG', 'SGP'],
        'Southeast Asia': ['IDN', 'MYS', 'THA', 'VNM', 'PHL'],
        'Europe': ['DEU', 'FRA', 'GBR', 'ITA', 'ESP', 'NLD'],
        'North America': ['USA', 'CAN', 'MEX']
    }
    
    resilience_metrics = {}
    for region, countries in regions.items():
        region_data = df[df['iso3'].isin(countries)]
        
        # Calculate various resilience metrics
        pre_crisis = region_data[region_data['t'] == 2007]['Out-strength'].mean()
        crisis_min = region_data[region_data['t'].isin([2008, 2009])]['Out-strength'].min()
        post_crisis = region_data[region_data['t'] == 2010]['Out-strength'].mean()
        
        resilience_metrics[region] = {
            'decline_depth': (crisis_min - pre_crisis) / pre_crisis,
            'recovery_speed': (post_crisis - crisis_min) / crisis_min,
            'final_recovery': (post_crisis - pre_crisis) / pre_crisis
        }
    
    return pd.DataFrame(resilience_metrics).T

def analyze_all_metrics(df):
    """Combine all analysis functions into one"""
    # Analyze emerging markets trends
    emerging_results = analyze_emerging_markets_trends(df)
    
    # Analyze regional integration
    regional_results = analyze_regional_integration(df)
    
    # Perform statistical tests
    stats_results = perform_statistical_tests(df)
    
    # Analyze regional resilience
    resilience_results = analyze_regional_resilience(df)
    
    # Create visualizations
    global fig1, fig2, network_metrics_fig  # Make these global so main() can access them
    fig1 = create_visualization_1(emerging_results)
    fig2 = create_visualization_2(regional_results)
    network_metrics_fig = create_network_metrics_visualization(df)
    
    return emerging_results, regional_results, stats_results, resilience_results

def generate_report(emerging_results, regional_results, stats_results):
    """Generate a text report summarizing the analysis results"""
    report = []
    
    # Header
    report.append("EMERGING MARKETS ANALYSIS REPORT")
    report.append("==============================\n")
    
    # Emerging Markets Analysis
    report.append("1. EMERGING MARKETS PERFORMANCE")
    report.append("------------------------------")
    for group, data in emerging_results.items():
        report.append(f"\n{group} Analysis:")
        report.append("-" * (len(group) + 10))
        latest_data = data.iloc[-1]
        report.append(f"Trade Strength: {latest_data['avg_out_strength']:.2f}")
        report.append(f"Network Connectivity: {latest_data['avg_out_degree']:.2f}")
        report.append(f"Network Centrality: {latest_data['network_centrality']:.2f}\n")
    
    # Statistical Analysis
    report.append("\n2. STATISTICAL ANALYSIS")
    report.append("----------------------")
    for group, stats in stats_results.items():
        report.append(f"\n{group}:")
        report.append(f"Crisis Impact: {((stats['mean_during'] - stats['mean_pre'])/stats['mean_pre']*100):.1f}%")
        report.append(f"Recovery: {((stats['mean_post'] - stats['mean_during'])/stats['mean_during']*100):.1f}%")
        report.append(f"Statistical Significance: p={stats['decline_p_val']:.3f}\n")
    
    return "\n".join(report)

def ensure_directories():
    """Ensure output directories exist"""
    for directory in ['outputs/text_files', 'outputs/figures']:
        os.makedirs(directory, exist_ok=True)

def main():
    # Ensure directories exist
    ensure_directories()
    
    # Load data from data directory
    df = pd.read_csv('data/Cepii_centrality_measures.csv', sep=';')
    
    # Generate results
    emerging_results, regional_results, stats_results, resilience_results = analyze_all_metrics(df)
    
    # Save text outputs to correct directory
    for group, data in emerging_results.items():
        data.to_csv(f'outputs/text_files/emerging_markets_{group.lower()}_analysis.csv')
    
    # Save figures to correct directory
    fig1.savefig('outputs/figures/emerging_markets_evolution.png', dpi=300, bbox_inches='tight')
    fig2.savefig('outputs/figures/regional_integration_patterns.png', dpi=300, bbox_inches='tight')
    network_metrics_fig.savefig('outputs/figures/network_metrics_evolution.png', dpi=300, bbox_inches='tight')

if __name__ == "__main__":
    results = main() 