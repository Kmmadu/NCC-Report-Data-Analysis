import pandas as pd
from fpdf import FPDF

# -----------------------------
# Data Loading and Preprocessing
# -----------------------------
def load_merged_data(file_path):
    """
    Load and preprocess the merged client dataset.

    Parameters:
        file_path (str): Path to the merged_clients.csv file.

    Returns:
        pd.DataFrame: The loaded DataFrame with bandwidth values converted to numeric.
    """
    df = pd.read_csv(file_path)
    # Convert the 'BANDWIDTH SUBSCRIPTION (Mbps)' column to numeric.
    df["BANDWIDTH SUBSCRIPTION (Mbps)"] = pd.to_numeric(df["BANDWIDTH SUBSCRIPTION (Mbps)"], errors="coerce")
    return df

# Load the merged data file.
file_path = "data/merged_clients.csv"  # Update the path if necessary
df = load_merged_data(file_path)

# -----------------------------
# Calculate Insights
# -----------------------------
# 1. Total Bandwidth allocated by Network Type
bandwidth_by_network = df.groupby("WAN/INTERNET CLIENT")["BANDWIDTH SUBSCRIPTION (Mbps)"].sum()
bandwidth_by_network_dict = bandwidth_by_network.to_dict()

# 2. Total Bandwidth allocated to Corporate Clients
corporate_bandwidth = df[df["CLIENT"].str.strip() == "Corporate"]["BANDWIDTH SUBSCRIPTION (Mbps)"].sum()

# 3. Total Bandwidth allocated to Retail Clients
retail_bandwidth = df[df["CLIENT"].str.strip() == "Retail"]["BANDWIDTH SUBSCRIPTION (Mbps)"].sum()

# 4. Total Bandwidth consumed per Region
bandwidth_by_region = df.groupby("REGION")["BANDWIDTH SUBSCRIPTION (Mbps)"].sum()

# 5. Average Bandwidth per Client
avg_bandwidth = df["BANDWIDTH SUBSCRIPTION (Mbps)"].mean()

# 6. Top 5 States with Highest Bandwidth Allocation
bandwidth_by_state = df.groupby("STATE")["BANDWIDTH SUBSCRIPTION (Mbps)"].sum().nlargest(5)

# 7. Active vs. Inactive Bandwidth Consumption (Optional)
active_bandwidth = df[df["CUSTOMER STATUS"].str.strip() == "Connected"]["BANDWIDTH SUBSCRIPTION (Mbps)"].sum()
inactive_bandwidth = df[df["CUSTOMER STATUS"].str.strip() == "Disconnected"]["BANDWIDTH SUBSCRIPTION (Mbps)"].sum()

# -----------------------------
# Generate PDF Report using FPDF
# -----------------------------
class InsightsPDF(FPDF):
    def header(self):
        """
        Create a header for each page of the PDF.
        """
        self.set_font("Helvetica", "B", 16)
        self.cell(0, 10, "NCC Report - Bandwidth Insights", ln=True, align="C")
        self.ln(5)
        
    def add_section(self, title, content):
        """
        Add a section with a title and corresponding content.

        Parameters:
            title (str): Section title.
            content (str): Section content.
        """
        self.set_font("Helvetica", "B", 14)
        self.cell(0, 10, title, ln=True)
        self.ln(2)
        self.set_font("Helvetica", "", 12)
        self.multi_cell(0, 8, content)
        self.ln(5)

# Prepare content for the PDF report.
report_content = ""

# Insight 1: Bandwidth by Network Type
report_content += "Total Bandwidth allocated by Network Type:\n"
for network, bandwidth in bandwidth_by_network_dict.items():
    report_content += f"  {network}: {bandwidth} Mbps\n"
report_content += "\n"

# Insight 2: Bandwidth for Corporate vs Retail Clients
report_content += f"Total Bandwidth allocated to Corporate Clients: {corporate_bandwidth} Mbps\n"
report_content += f"Total Bandwidth allocated to Retail Clients: {retail_bandwidth} Mbps\n\n"

# Insight 3: Bandwidth by Region
report_content += "Total Bandwidth consumed per Region:\n"
for region, bandwidth in bandwidth_by_region.items():
    report_content += f"  {region}: {bandwidth} Mbps\n"
report_content += "\n"

# Insight 4: Average Bandwidth per Client
report_content += f"Average Bandwidth per Client: {avg_bandwidth:.2f} Mbps\n\n"

# Insight 5: Top 5 States with Highest Bandwidth Allocation
report_content += "Top 5 States with Highest Bandwidth Allocation:\n"
for state, bandwidth in bandwidth_by_state.items():
    report_content += f"  {state}: {bandwidth} Mbps\n"
report_content += "\n"

# Insight 6: Active vs. Inactive Bandwidth Consumption
report_content += "Active vs. Inactive Bandwidth Consumption:\n"
report_content += f"  Active Customers: {active_bandwidth} Mbps\n"
report_content += f"  Inactive Customers: {inactive_bandwidth} Mbps\n"

# Create and populate the PDF
pdf = InsightsPDF()
pdf.add_page()
pdf.add_section("Bandwidth Insights", report_content)

# Save the PDF report
pdf_filename = "Insights.pdf"
pdf.output(pdf_filename)

print(f"PDF report generated and saved as {pdf_filename}")
