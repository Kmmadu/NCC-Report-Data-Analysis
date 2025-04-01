import pandas as pd

def clean_df(df):
    """
    Clean the provided DataFrame by removing rows that are completely empty 
    and resetting the index.
    
    Parameters:
        df (pd.DataFrame): The DataFrame to clean.
    
    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    df = df.dropna(how='all')  # Remove rows that are completely empty.
    df = df.reset_index(drop=True)  # Reset the index for a clean DataFrame.
    return df

def process_excel_tables(file_path, sheet_name, header_marker="S/N"):
    """
    Process an Excel sheet containing two tables separated by a repeated header row.
    The function extracts both tables, cleans them, and merges them.
    
    Parameters:
        file_path (str): Path to the Excel file.
        sheet_name (str): Name of the sheet containing the tables.
        header_marker (str): Marker used to identify header rows (default is "S/N").
    
    Returns:
        pd.DataFrame: A merged DataFrame containing data from both tables.
    
    Raises:
        ValueError: If the expected header rows are not found or if one of the tables is empty.
    """
    try:
        # Read the entire sheet without assuming a header
        df_all = pd.read_excel(file_path, sheet_name=sheet_name, header=None)
        
        # Identify header rows by searching for the header marker in the first column.
        header_rows = df_all.index[df_all.iloc[:, 0].astype(str).str.strip() == header_marker].tolist()
        
        if len(header_rows) < 2:
            raise ValueError(f"Could not find two header rows with marker '{header_marker}'. Found {len(header_rows)} header row(s).")
        
        # Extract header values from the first header row.
        header = df_all.iloc[header_rows[0]].tolist()
        
        # Extract the first table (formerly Corporate Clients) 
        df1 = df_all.iloc[header_rows[0] + 1 : header_rows[1]].copy()
        df1.columns = header  # Set header for the first table.
        df1 = clean_df(df1)
        
        # Extract the second table (formerly Retail Clients)
        df2 = df_all.iloc[header_rows[1] + 1 :].copy()
        df2.columns = header  # Set header for the second table.
        df2 = clean_df(df2)
        
        # Validate that both tables have data
        if df1.empty or df2.empty:
            raise ValueError("One or both extracted tables are empty.")
            
        # Merge the two DataFrames into one
        merged_df = pd.concat([df1, df2], ignore_index=True)
        
        # If a column "S/N" exists, reset it to be sequential
        if "S/N" in merged_df.columns:
            merged_df["S/N"] = range(1, len(merged_df) + 1)
            
        return merged_df
        
    except Exception as e:
        print(f"Error processing file: {str(e)}")
        raise

# -------------------------------
# Main execution block
# -------------------------------
if __name__ == "__main__":
    try:
        # Define file path and sheet name for the Excel file.
        file_path = "../data/NCC Q4 2024 (JAN - DEC) - END OF THE YEAR.xlsx"
        sheet_name = "Corporate and Retail Clients"
        
        # Process the Excel tables and merge them.
        result = process_excel_tables(file_path, sheet_name)
        
        # Save the merged DataFrame to CSV.
        result.to_csv("merged_clients.csv", index=False)
        print("Successfully created merged_clients.csv")
        
    except Exception as e:
        print(f"Failed to process file: {str(e)}")
