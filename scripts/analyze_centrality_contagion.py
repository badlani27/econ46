import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
import os

def ensure_directories():
    """Ensure output directories exist"""
    for directory in ['outputs/text_files', 'outputs/figures']:
        os.makedirs(directory, exist_ok=True)

def analyze_bilateral_trade_impact(df):
    """Analyze how changes in central countries' trade affected their partners"""
    
    # Identify top central countries pre-crisis (2007)
    pre_crisis = df[df['t'] == 2007]
    top_central = pre_crisis.nlargest(10, 'Out-eigenvector')[['iso3', 'country', 'Out-eigenvector']]
    
    # Define crisis periods
    periods = {
        'pre_crisis': 2007,
        'crisis_peak': 2008,
        'post_crisis': 2009
    }
    
    trade_impact_results = {}
    
    for central_country in top_central['iso3']:
        partner_effects = []
        
        for period, year in periods.items():
            year_data = df[df['t'] == year]
            
            # Get central country's trade data
            central_data = year_data[year_data['iso3'] == central_country]
            
            # Calculate bilateral trade relationships
            for _, partner in year_data.iterrows():
                if partner['iso3'] != central_country:
                    # Calculate bilateral trade volume and changes
                    trade_effect = {
                        'year': year,
                        'period': period,
                        'source_country': central_country,
                        'target_country': partner['iso3'],
                        'bilateral_trade': central_data['Out-strength'].values[0] * partner['In-strength'],
                        'target_total_trade': partner['Out-strength'] + partner['In-strength'],
                        'trade_dependence': (central_data['Out-strength'].values[0] * partner['In-strength']) / 
                                         (partner['Out-strength'] + partner['In-strength'])
                    }
                    partner_effects.append(trade_effect)
        
        trade_impact_results[central_country] = pd.DataFrame(partner_effects)
    
    return trade_impact_results, top_central

def calculate_contagion_metrics(trade_impact_results):
    """Calculate metrics for trade contagion effects"""
    contagion_metrics = {}
    
    for country, data in trade_impact_results.items():
        # Calculate trade impact metrics
        period_impacts = data.groupby('period').agg({
            'trade_dependence': ['mean', 'std', 'max'],
            'bilateral_trade': ['sum', 'mean'],
            'target_total_trade': 'mean'
        })
        
        # Calculate year-over-year changes
        yoy_changes = {}
        for period in ['crisis_peak', 'post_crisis']:
            prev_period = 'pre_crisis' if period == 'crisis_peak' else 'crisis_peak'
            
            # Get data for current and previous periods
            current = data[data['period'] == period].set_index('target_country')
            previous = data[data['period'] == prev_period].set_index('target_country')
            
            # Align the indices before comparison
            common_countries = current.index.intersection(previous.index)
            current_aligned = current.loc[common_countries]
            previous_aligned = previous.loc[common_countries]
            
            # Calculate changes in trade volumes
            yoy_changes[period] = {
                'avg_trade_change': ((current['bilateral_trade'].mean() / 
                                    previous['bilateral_trade'].mean()) - 1) * 100,
                'affected_partners': (current_aligned['trade_dependence'] < 
                                    previous_aligned['trade_dependence']).sum()
            }
        
        contagion_metrics[country] = {
            'period_impacts': period_impacts,
            'yoy_changes': yoy_changes
        }
    
    return contagion_metrics

def create_impact_visualizations(trade_impact_results, top_central, contagion_metrics):
    """Create visualizations for trade impact analysis"""
    # Figure 1: Trade Impact Network
    plt.figure(figsize=(15, 10))
    
    # Create network visualization showing trade dependencies
    G = nx.DiGraph()
    
    # Add edges based on trade dependencies
    for country, data in trade_impact_results.items():
        crisis_data = data[data['period'] == 'crisis_peak']
        for _, row in crisis_data.nlargest(5, 'trade_dependence').iterrows():
            G.add_edge(row['source_country'], row['target_country'], 
                      weight=row['trade_dependence'])
    
    pos = nx.spring_layout(G, k=2)
    
    # Draw the network
    nx.draw_networkx(G, pos, 
                    node_color='lightblue',
                    node_size=1000,
                    with_labels=True,
                    font_size=8)
    
    plt.title('Crisis Period Trade Dependencies\n(Top 5 partners per central country)')
    plt.savefig('outputs/figures/trade_impact_network.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # Figure 2: Trade Impact Changes
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot 1: Trade Volume Changes
    changes_data = []
    for country in top_central['iso3']:
        changes_data.append({
            'country': country,
            'crisis_impact': contagion_metrics[country]['yoy_changes']['crisis_peak']['avg_trade_change'],
            'post_crisis_recovery': contagion_metrics[country]['yoy_changes']['post_crisis']['avg_trade_change']
        })
    
    changes_df = pd.DataFrame(changes_data)
    changes_df.plot(x='country', y=['crisis_impact', 'post_crisis_recovery'], 
                   kind='bar', ax=ax1)
    ax1.set_title('Trade Volume Changes')
    ax1.set_ylabel('Percent Change')
    ax1.tick_params(axis='x', rotation=45)
    
    # Plot 2: Affected Partners
    affected_data = []
    for country in top_central['iso3']:
        affected_data.append({
            'country': country,
            'crisis_affected': contagion_metrics[country]['yoy_changes']['crisis_peak']['affected_partners'],
            'post_crisis_affected': contagion_metrics[country]['yoy_changes']['post_crisis']['affected_partners']
        })
    
    affected_df = pd.DataFrame(affected_data)
    affected_df.plot(x='country', y=['crisis_affected', 'post_crisis_affected'], 
                    kind='bar', ax=ax2)
    ax2.set_title('Number of Affected Trading Partners')
    ax2.set_ylabel('Count')
    ax2.tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.savefig('outputs/figures/trade_impact_changes.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    # Ensure directories exist
    ensure_directories()
    
    # Load data
    df = pd.read_csv('data/Cepii_centrality_measures.csv', sep=';')
    
    # Analyze bilateral trade impacts
    trade_impact_results, top_central = analyze_bilateral_trade_impact(df)
    contagion_metrics = calculate_contagion_metrics(trade_impact_results)
    
    # Create visualizations
    create_impact_visualizations(trade_impact_results, top_central, contagion_metrics)
    
    # Save analysis results
    with open('outputs/text_files/centrality_contagion_analysis.txt', 'w') as f:
        f.write("CENTRALITY-BASED CONTAGION ANALYSIS\n")
        f.write("=================================\n\n")
        
        f.write("1. Top Central Countries (2007)\n")
        f.write("--------------------------\n")
        f.write(top_central.to_string())
        f.write("\n\n")
        
        f.write("2. Trade Impact Analysis\n")
        f.write("----------------------\n")
        for country in top_central['iso3']:
            f.write(f"\n{country}:\n")
            
            # Crisis period impact
            crisis_change = contagion_metrics[country]['yoy_changes']['crisis_peak']
            f.write(f"  Crisis Impact (2007-2008):\n")
            f.write(f"    - Average trade volume change: {crisis_change['avg_trade_change']:.2f}%\n")
            f.write(f"    - Affected trading partners: {crisis_change['affected_partners']}\n")
            
            # Post-crisis recovery
            post_crisis = contagion_metrics[country]['yoy_changes']['post_crisis']
            f.write(f"  Post-Crisis Recovery (2008-2009):\n")
            f.write(f"    - Average trade volume change: {post_crisis['avg_trade_change']:.2f}%\n")
            f.write(f"    - Affected trading partners: {post_crisis['affected_partners']}\n")
            
            # Trade dependency statistics
            period_impacts = contagion_metrics[country]['period_impacts']
            f.write("  Trade Dependency Statistics:\n")
            f.write(f"    {period_impacts.to_string()}\n")
        
        f.write("\n3. Key Findings\n")
        f.write("-------------\n")
        f.write("- Trade dependency analysis shows how central countries' trade patterns affected their partners\n")
        f.write("- The analysis captures both direct trade volume changes and partner country dependencies\n")
        f.write("- Visualizations show the network of trade dependencies and impact changes over time\n")

if __name__ == "__main__":
    main() 