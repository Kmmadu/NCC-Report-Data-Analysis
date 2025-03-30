# NCC Report Data Analysis

## Overview
This project processes and analyzes client data for the NCC Q4 2024 report. The dataset—merged from two separate tables (Corporate and Retail Clients)—contains information on bandwidth subscriptions, geographic regions, and customer connection statuses. The goal is to derive key insights such as total bandwidth allocation, customer counts, and regional bandwidth distribution. These insights are presented in an interactive Streamlit dashboard, and a detailed PDF report is generated to summarize the findings.

## Dataset
The merged dataset (`merged_clients.csv`) includes the following columns:
- **COMPANY NAME**
- **BRANCH/LOCATION NAME**
- **STATE**
- **REGION**
- **WAN/INTERNET CLIENT**
- **BANDWIDTH SUBSCRIPTION (Mbps)**
- **CUSTOMER STATUS**
- **CLIENT**
- **Client Type** (Note: The "CLIENT" and "Client Type" columns are redundant; data is standardized during preprocessing.)

## Project Workflow
1. **Data Loading & Cleaning:**  
   - Load the merged dataset from the CSV file.
   - Standardize values for client types and customer statuses.

2. **Interactive Dashboard:**  
   - Built with **Streamlit** and **Plotly Express**.
   - Sidebar filters allow users to select geographic regions, states, customer types, and connection statuses.
   - Key metrics (e.g., total bandwidth, active/inactive connections) are displayed in a grid format.
   - Visualizations include bar charts, pie charts, and treemaps.
   - Data export options enable users to download filtered data, the full dataset, and a PDF insights report.

3. **PDF Report Generation:**  
   - Calculate key bandwidth insights using **Pandas**.
   - Generate a comprehensive PDF report using **FPDF**.

## Tech Stack
- **Python** for data processing and scripting.
- **Pandas** for data manipulation.
- **Plotly Express** for interactive visualizations.
- **Streamlit** for building the interactive dashboard.
- **FPDF** for PDF report generation.

## Installation
1. **Clone the Repository:**
   ```bash
   git clone https://github.com/Kmmadu/NCC-Report-Data-Analysis.git
   cd NCC-Report-Data-Analysis
   ```
2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
source venv/bin/activate  
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Place the Dataset: Ensure merged_clients.csv is located in the data/ folder.
   ```bash
   streamlit run src/streamlit_ncc_dashboard.py
   ```


## Contributing
Contributions are welcome! Feel free to fork this repository and submit improvements.

## License
This project is licensed under the MIT License.

---
