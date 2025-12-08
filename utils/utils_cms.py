import pandas as pd
from pathlib import Path

def read_cms_files(file_path: str, type: str) -> pd.DataFrame:
    usecols = [
        "Covered_Recipient_Profile_ID",
        "Covered_Recipient_NPI",
        "Covered_Recipient_First_Name",
        "Covered_Recipient_Last_Name",

        "Recipient_City",
        "Recipient_State",

        "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID",
        "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name",
        "Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_1",

        "Total_Amount_of_Payment_USDollars",
        "Date_of_Payment",
        "Record_ID",
        "Program_Year",
    ]
    
    dtype_map = {
        "Covered_Recipient_Profile_ID" : "Int64",
        "Covered_Recipient_NPI" : "Int64",
        "Covered_Recipient_First_Name" : "object",
        "Covered_Recipient_Last_Name" : "object",

        "Recipient_City" : "object",
        "Recipient_State" : "object",

        "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_ID" : "Int64",
        "Applicable_Manufacturer_or_Applicable_GPO_Making_Payment_Name" : "object",
        "Name_of_Drug_or_Biological_or_Device_or_Medical_Supply_1" : "object",

        "Total_Amount_of_Payment_USDollars" : "Float64",
        "Record_ID" : "Int64",
        "Program_Year" : "Int64",
    }

    if type.lower().startswith("g"):
        usecols.append("Nature_of_Payment_or_Transfer_of_Value")
        dtype_map["Nature_of_Payment_or_Transfer_of_Value"] = "object"

    df = pd.read_csv(file_path, usecols=usecols, dtype=dtype_map, parse_dates=["Date_of_Payment"], low_memory=False)
    return df

def clean_cms_files(df: pd.DataFrame, type: str) -> pd.DataFrame:
    pass