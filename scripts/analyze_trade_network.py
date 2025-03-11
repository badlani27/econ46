import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx
import os

# Read the data
# df = pd.read_csv('Cepii_centrality_measures.csv', sep=';')

# 1. Analyze Top Economic Powers
def analyze_top_powers(df, year=2010, n=20):
    """Analyze top economic powers based on trade strength"""
    year_data = df[df['t'] == year].sort_values('Out-strength', ascending=False)
    top_powers = year_data[['country', 'Out-strength', 'Out-degree', 'Out-eigenvector']].head(n)
    return top_powers

# 2. Analyze Network Evolution
def analyze_network_evolution(df):
    """Analyze how network metrics evolved over time"""
    yearly_avg = df.groupby('t').agg({
        'Out-degree': 'mean',
        'In-degree': 'mean',
        'Out-strength': 'mean',
        'In-strength': 'mean',
        'Out-eigenvector': 'mean',
        'In-eigenvector': 'mean'
    }).reset_index()
    return yearly_avg

# 3. Crisis Impact Analysis
def analyze_crisis_impact(df):
    """Analyze impact of 2008 financial crisis"""
    pre_crisis = df[df['t'].isin([2006, 2007])]['Out-strength'].mean()
    during_crisis = df[df['t'].isin([2008, 2009])]['Out-strength'].mean()
    post_crisis = df[df['t'] == 2010]['Out-strength'].mean()
    
    return {
        'pre_crisis': pre_crisis,
        'during_crisis': during_crisis,
        'post_crisis': post_crisis,
        'crisis_impact': (during_crisis - pre_crisis) / pre_crisis * 100,
        'recovery': (post_crisis - during_crisis) / during_crisis * 100
    }

# 4. Regional Analysis
def analyze_regional_patterns(df, year=2010):
    """Analyze regional trade patterns"""
    # Define major regions (simplified)
    eu_countries = ['DEU', 'FRA', 'ITA', 'ESP', 'NLD']  # Example EU countries
    asia_pacific = ['CHN', 'JPN', 'KOR', 'SGP', 'AUS']  # Example Asia-Pacific countries
    north_america = ['USA', 'CAN', 'MEX']
    
    year_data = df[df['t'] == year]
    
    regional_stats = {
        'EU': year_data[year_data['iso3'].isin(eu_countries)]['Out-strength'].mean(),
        'Asia_Pacific': year_data[year_data['iso3'].isin(asia_pacific)]['Out-strength'].mean(),
        'North_America': year_data[year_data['iso3'].isin(north_america)]['Out-strength'].mean()
    }
    
    return regional_stats

def create_trade_network(df, year, threshold=90, top_n=20):
    """
    Create a network graph for a specific year
    threshold: percentile threshold for including edges (e.g., 90 means top 10% of trade relationships)
    top_n: number of top trading nations to label
    """
    # Get data for specific year
    year_data = df[df['t'] == year]
    
    # Create network
    G = nx.Graph()
    
    # Add nodes (countries)
    for _, row in year_data.iterrows():
        G.add_node(row['iso3'], 
                  country=row['country'],
                  out_strength=row['Out-strength'],
                  out_degree=row['Out-degree'])
    
    # Add edges for significant trade relationships
    strength_threshold = np.percentile(year_data['Out-strength'], threshold)
    significant_traders = year_data[year_data['Out-strength'] >= strength_threshold]['iso3'].tolist()
    
    # Add edges between significant trading partners
    for i in significant_traders:
        for j in significant_traders:
            if i < j:  # Avoid duplicate edges
                G.add_edge(i, j, weight=1)
    
    # Size nodes by their out-strength (normalized)
    max_strength = df['Out-strength'].max()  # Use global max for consistent scaling
    node_sizes = dict(zip(year_data['iso3'], 
                         2000 * year_data['Out-strength'] / max_strength))
    
    # Get top trading nations for labels
    top_traders = year_data.nlargest(top_n, 'Out-strength')[['iso3', 'country', 'Out-strength']].values.tolist()
    
    return G, node_sizes, top_traders

def analyze_network_changes(df, years=[2007, 2009, 2010]):
    """Analyze changes in network structure across years"""
    changes = []
    
    for year in years:
        year_data = df[df['t'] == year]
        
        # Get top 20 traders for the year
        top_20 = year_data.nlargest(20, 'Out-strength')[['country', 'Out-strength']]
        
        # Calculate network metrics
        avg_strength = year_data['Out-strength'].mean()
        median_strength = year_data['Out-strength'].median()
        total_strength = year_data['Out-strength'].sum()
        
        changes.append({
            'year': year,
            'top_20': top_20,
            'avg_strength': avg_strength,
            'median_strength': median_strength,
            'total_strength': total_strength
        })
    
    return changes

def plot_network_comparison(df):
    """Plot network graphs for pre, during, and post crisis"""
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(24, 10))
    
    # Create networks for each period
    G_pre, sizes_pre, labels_pre = create_trade_network(df, 2007)
    G_during, sizes_during, labels_during = create_trade_network(df, 2009)
    G_post, sizes_post, labels_post = create_trade_network(df, 2010)
    
    # Layout for consistent positioning
    pos = nx.spring_layout(G_pre, k=2, iterations=50, seed=42)
    
    # Function to create node labels (only for top traders)
    def get_labels(G, top_traders):
        return {node: f"{node}\n({country})" for node, country, _ in top_traders}
    
    # Plot pre-crisis network
    nx.draw_networkx_edges(G_pre, pos, ax=ax1, alpha=0.2)
    nx.draw_networkx_nodes(G_pre, pos, ax=ax1,
                          node_size=[sizes_pre.get(node, 100) for node in G_pre.nodes()],
                          node_color='lightblue',
                          alpha=0.7)
    nx.draw_networkx_labels(G_pre, pos, ax=ax1,
                           labels=get_labels(G_pre, labels_pre),
                           font_size=6)
    ax1.set_title('Pre-Crisis (2007)')
    
    # Plot during-crisis network
    nx.draw_networkx_edges(G_during, pos, ax=ax2, alpha=0.2)
    nx.draw_networkx_nodes(G_during, pos, ax=ax2,
                          node_size=[sizes_during.get(node, 100) for node in G_during.nodes()],
                          node_color='lightcoral',
                          alpha=0.7)
    nx.draw_networkx_labels(G_during, pos, ax=ax2,
                           labels=get_labels(G_during, labels_during),
                           font_size=6)
    ax2.set_title('During Crisis (2009)')
    
    # Plot post-crisis network
    nx.draw_networkx_edges(G_post, pos, ax=ax3, alpha=0.2)
    nx.draw_networkx_nodes(G_post, pos, ax=ax3,
                          node_size=[sizes_post.get(node, 100) for node in G_post.nodes()],
                          node_color='lightgreen',
                          alpha=0.7)
    nx.draw_networkx_labels(G_post, pos, ax=ax3,
                           labels=get_labels(G_post, labels_post),
                           font_size=6)
    ax3.set_title('Post-Crisis (2010)')
    
    # Add detailed legend
    legend_text = (
        'Node size represents trade strength (globally normalized)\n'
        'Labels shown for top 20 trading nations\n'
        'Edges connect significant trading partners'
    )
    plt.figtext(0.02, 0.02, legend_text, fontsize=10)
    
    plt.tight_layout()
    return fig

def analyze_regional_impact(df, years=[2007, 2009, 2010]):
    """Analyze regional trade patterns during crisis"""
    # Define regions
    regions = {
        'North America': ['USA', 'CAN', 'MEX'],
        'Western Europe': ['DEU', 'FRA', 'GBR', 'ITA', 'ESP', 'NLD', 'BEL', 'CHE', 'SWE'],
        'East Asia': ['CHN', 'JPN', 'KOR', 'TWN', 'HKG', 'SGP'],
        'Emerging Markets': ['BRA', 'RUS', 'IND', 'ZAF', 'TUR', 'IDN', 'THA', 'MYS'],
        'Oil Exporters': ['SAU', 'ARE', 'KWT', 'QAT', 'IRN', 'VEN', 'NGA']
    }
    
    regional_changes = {}
    for region_name, countries in regions.items():
        yearly_stats = []
        for year in years:
            year_data = df[df['t'] == year]
            region_data = year_data[year_data['iso3'].isin(countries)]
            
            stats = {
                'year': year,
                'avg_strength': region_data['Out-strength'].mean(),
                'total_strength': region_data['Out-strength'].sum(),
                'internal_trade': region_data['Out-strength'].sum() / year_data['Out-strength'].sum(),
                'countries': len(region_data)
            }
            yearly_stats.append(stats)
        
        regional_changes[region_name] = yearly_stats
    
    return regional_changes

def ensure_directories():
    """Ensure output directories exist"""
    for directory in ['outputs/text_files', 'outputs/figures']:
        os.makedirs(directory, exist_ok=True)

def analyze_network_metrics(df):
    """Analyze network metrics and generate results"""
    results = pd.DataFrame()
    
    # Get network evolution metrics
    network_evolution = analyze_network_evolution(df)
    
    # Get crisis impact metrics
    crisis_metrics = analyze_crisis_impact(df)
    
    # Get regional patterns
    regional_patterns = analyze_regional_patterns(df)
    
    # Get regional impact analysis
    regional_impact = analyze_regional_impact(df)
    
    # Combine results into a single DataFrame
    results['network_evolution'] = network_evolution['Out-strength']
    results['crisis_impact'] = pd.Series(crisis_metrics)
    results['regional_patterns'] = pd.Series(regional_patterns)
    
    # Create text report
    with open('outputs/text_files/trade_network_analysis.txt', 'w') as f:
        f.write("TRADE NETWORK ANALYSIS\n")
        f.write("=====================\n\n")
        
        f.write("1. Network Evolution\n")
        f.write("-----------------\n")
        f.write(network_evolution.to_string())
        f.write("\n\n")
        
        f.write("2. Crisis Impact\n")
        f.write("--------------\n")
        for key, value in crisis_metrics.items():
            f.write(f"{key}: {value:.2f}\n")
        f.write("\n")
        
        f.write("3. Regional Analysis\n")
        f.write("------------------\n")
        for region, value in regional_patterns.items():
            f.write(f"{region}: {value:.2f}\n")
        f.write("\n")
        
        f.write("4. Regional Impact Over Time\n")
        f.write("-------------------------\n")
        for region, stats in regional_impact.items():
            f.write(f"\n{region}:\n")
            for year_stat in stats:
                f.write(f"  Year {year_stat['year']}:\n")
                f.write(f"    Average Strength: {year_stat['avg_strength']:.2f}\n")
                f.write(f"    Total Strength: {year_stat['total_strength']:.2f}\n")
                f.write(f"    Internal Trade: {year_stat['internal_trade']:.2%}\n")
    
    # Create visualizations
    global fig1, fig2
    fig1 = plot_network_evolution(df)
    fig2 = plot_network_comparison(df)
    
    return results

def main():
    # Ensure directories exist
    ensure_directories()
    
    # Load data from data directory
    df = pd.read_csv('data/Cepii_centrality_measures.csv', sep=';')
    
    # Generate results
    network_results = analyze_network_metrics(df)
    
    # Save text outputs to correct directory
    network_results.to_csv('outputs/text_files/network_analysis_results.csv')
    
    # Save figures to correct directory
    fig1.savefig('outputs/figures/network_evolution.png', dpi=300, bbox_inches='tight')
    fig2.savefig('outputs/figures/trade_network_comparison.png', dpi=300, bbox_inches='tight')

def plot_network_evolution(df):
    """Plot network evolution metrics"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Plot network density over time
    yearly_density = df.groupby('t')['Out-degree'].mean()
    ax1.plot(yearly_density.index, yearly_density.values, marker='o')
    ax1.set_title('Network Density Evolution')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Average Degree')
    ax1.grid(True)
    
    # Plot centralization over time
    yearly_central = df.groupby('t')['Out-eigenvector'].mean()
    ax2.plot(yearly_central.index, yearly_central.values, marker='o', color='orange')
    ax2.set_title('Network Centralization Evolution')
    ax2.set_xlabel('Year')
    ax2.set_ylabel('Average Eigenvector Centrality')
    ax2.grid(True)
    
    plt.tight_layout()
    return fig

def plot_regional_trade(regional_results):
    """Plot regional trade patterns"""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    
    # Prepare data for plotting
    regions = list(regional_results.keys())
    years = [2007, 2009, 2010]
    
    # Plot total trade by region
    for region in regions:
        trade_values = [next(x for x in regional_results[region] if x['year'] == year)['total_strength'] 
                       for year in years]
        ax1.plot(years, trade_values, marker='o', label=region)
    
    ax1.set_title('Regional Trade Volume Evolution')
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Total Trade Strength')
    ax1.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax1.grid(True)
    
    plt.tight_layout()
    return fig

def plot_top_powers_evolution(df):
    """Plot evolution of top economic powers"""
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Get top 10 countries in 2007
    top_10_2007 = df[df['t'] == 2007].nlargest(10, 'Out-strength')['iso3'].unique()
    
    # Plot their evolution
    for country in top_10_2007:
        country_data = df[df['iso3'] == country]
        ax.plot(country_data['t'], country_data['Out-strength'], marker='o', label=country)
    
    ax.set_title('Evolution of Top 10 Economic Powers')
    ax.set_xlabel('Year')
    ax.set_ylabel('Trade Strength')
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True)
    
    plt.tight_layout()
    return fig

if __name__ == "__main__":
    main() 