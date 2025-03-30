import pandas as pd

def clean_df(df):
    """Clean the dataframe by removing empty rows and resetting index"""
    df = df.dropna(how='all')  # Remove completely empty rows
    df = df.reset_index(drop=True)
    return df

def process_excel_tables(file_path, sheet_name, header_marker="S/N"):
    try:
        # Read the entire sheet
        df_all = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        
        # Find header rows (more robust search)
        header_rows = df_all.index[df_all.iloc[:, 0].astype(str).str.strip() == header_marker].tolist()
        
        if len(header_rows) < 2:
            raise ValueError(f"Could not find two header rows with marker '{header_marker}'. Found {len(header_rows)} headers.")
        
        # Extract header
        header = df_all.iloc[header_rows[0]].tolist()
        
        # Extract first table
        df1 = df_all.iloc[header_rows[0]+1 : header_rows[1]].copy()
        df1.columns = header
        df1 = clean_df(df1)
        df1["Client Type"] = "Corporate"
        
        # Extract second table
        df2 = df_all.iloc[header_rows[1]+1:].copy()
        df2.columns = header
        df2 = clean_df(df2)
        df2["Client Type"] = "Retail"
        
        # Validate tables have data
        if len(df1) == 0 or len(df2) == 0:
            raise ValueError("One or both extracted tables are empty")
            
        # Combine tables
        merged_df = pd.concat([df1, df2], ignore_index=True)
        
        # Reset S/N if it exists
        if "S/N" in merged_df.columns:
            merged_df["S/N"] = range(1, len(merged_df)+1)
            
        return merged_df
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise

# Usage
try:
    file_path = "../data/NCC Q4 2024 (JAN - DEC) - END OF THE YEAR.xlsx"
    sheet_name = "Corporate and Retail Clients"
    
    result = process_excel_tables(file_path, sheet_name)
    result.to_csv("merged_clients.csv", index=False)
    print("Successfully created merged_clients.csv")
    
except Exception as e:
    print(f"Failed to process file: {str(e)}")