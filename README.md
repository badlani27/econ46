# Trade Network Analysis Project

This project analyzes international trade networks using CEPII data, focusing on the impact of the 2008 financial crisis.

## Directory Structure and File Descriptions

### Root Directory
- `run_analysis.py`: Master script that orchestrates all analyses and generates reports
- `cleanup.py`: Utility script for organizing files into appropriate directories

### /scripts
- `analyze_trade_network.py`: Analyzes network structure, evolution, and crisis impact
- `analyze_emerging_markets.py`: Focuses on BRICS, Next-11, and regional performance
- `analyze_policy_impacts.py`: Evaluates policy effectiveness and sectoral resilience

### /data
- `Cepii_centrality_measures.csv`: Primary dataset containing:
  - Country trade relationships
  - Network centrality measures
  - Annual trade volumes
  - Regional indicators

### /outputs/text_files
1. **Analysis Reports**
   - `comprehensive_report.txt`: Combined analysis from all modules, organized by topic
   - `trade_network_analysis.txt`: Detailed network metrics and evolution over time
   - `emerging_markets_report.txt`: Analysis of emerging market performance and resilience
   - `crisis_impact_analysis.txt`: Specific analysis of 2008 crisis effects

2. **Statistical Results**
   - `statistical_analysis_results.txt`: Results of statistical tests including:
     - ANOVA results
     - Tukey HSD test outcomes
     - Significance levels
   - `detailed_analysis_results.txt`: In-depth metrics and calculations

3. **Data Outputs**
   - `network_analysis_results.csv`: Network metrics by year and country
   - `policy_analysis_results.csv`: Policy effectiveness measurements
   - `regional_resilience_metrics.csv`: Regional performance indicators

4. **Summary Files**
   - `findings.txt`: Key findings and conclusions
   - `statistical_analysis.txt`: Statistical methodology and interpretations

### /outputs/figures
1. **Network Visualizations**
   - `network_evolution.png`: Time series of network metrics
   - `trade_network_comparison.png`: Pre/during/post crisis network structure

2. **Regional Analysis**
   - `regional_trade.png`: Regional trade patterns
   - `regional_integration_patterns.png`: Integration metrics by region

3. **Market Analysis**
   - `emerging_markets_evolution.png`: BRICS and Next-11 performance
   - `sectoral_analysis_basic.png`: Basic sectoral metrics
   - `sectoral_analysis_advanced.png`: Advanced sectoral analysis

4. **Financial Analysis**
   - `financial_integration.png`: Financial sector integration metrics

## Analysis Methods

### 1. Network Analysis
- **Network Metrics**
  - Out-degree: Number of trading partners
  - Out-strength: Total trade volume
  - Eigenvector centrality: Country's importance in network
  
- **Crisis Impact Measures**
  ```
  Example from trade_network_analysis.txt:
  pre_crisis: 245.67
  during_crisis: 198.34
  crisis_impact: -19.27%
  recovery: 15.89%
  ```

### 2. Regional Analysis
- **Regional Classifications**
  - East Asia: CHN, JPN, KOR, TWN, HKG, SGP
  - Southeast Asia: IDN, MYS, THA, VNM, PHL
  - Western Europe: DEU, FRA, GBR, ITA, ESP, NLD
  - North America: USA, CAN, MEX

- **Resilience Metrics**
  ```
  Example from statistical_analysis_results.txt:
  Region: East Asia
    Trade Decline: -15.4%
    Recovery Speed: +23.7%
    Internal Trade: 45.2%
  ```

### 3. Emerging Markets
- **Market Groups**
  - BRICS: Brazil, Russia, India, China, South Africa
  - Next-11: Bangladesh, Egypt, Indonesia, Iran, Mexico, Nigeria, Pakistan, Philippines, Turkey, South Korea, Vietnam
  - MINT: Mexico, Indonesia, Nigeria, Turkey

- **Performance Metrics**
  ```
  Example from emerging_markets_report.txt:
  BRICS Performance:
    Network Integration: +12.3%
    Trade Resilience: 0.89
    Recovery Rate: +18.4%
  ```

## Project Structure 

## Usage

## Backup System
- Backup files are created automatically with timestamp prefixes
- Example: `backup_20250311_141348_statistical_analysis_results.txt`
- Backups are stored in the same directory as the original files
- Naming format: `backup_YYYYMMDD_HHMMSS_originalfilename`

## Output Format Specifications
1. **Text Reports**
   - UTF-8 encoded
   - Structured with clear section headers
   - Include timestamps and version information

2. **CSV Files**
   - Comma-separated
   - Include headers
   - ISO date formats
   - Missing values marked as NA

3. **Figures**
   - PNG format
   - 300 DPI resolution
   - 15x6 or 15x12 inches
   - Clear labels and legends

## Notes
- All outputs are automatically organized into appropriate directories
- The comprehensive report is regenerated with each analysis run
- Visualizations are optimized for both screen viewing and printing
- Statistical results include confidence intervals and p-values 