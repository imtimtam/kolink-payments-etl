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
    df.columns = [col.strip().lower() for col in df.columns]

    # DROP NA IF IMPORTANT VALUES MISSING, EX. CANNOT LINK TO PHYSICIANS
    subset = [
        "covered_recipient_npi",
        "total_amount_of_payment_usdollars",
        "date_of_payment",
    ]
    df = df.dropna(subset=subset)

    # FILTER PAYMENT NATURES SUCH AS FOOD AND DRINKS UNRELATED TO KOLINK
    if type.lower().startswith("g"):
        useful_natures = [
            "Compensation for services other than consulting, including serving as faculty or as a speaker at a venue other than a continuing education program",
            "Consulting Fee",
            "Education",
            "Honoraria",
            "Royalty or License",
            "Compensation for serving as faculty or as a speaker for a medical education program",
            "Long term medical supply or device loan",
            "Grant",
        ]

        df = df[df['nature_of_payment_or_transfer_of_value'].str.lower().isin([x.lower() for x in useful_natures])].copy()
        df.drop(columns=["nature_of_payment_or_transfer_of_value"], inplace=True)

        # ASSIGN TYPE TO SHOW DATA ORIGINS
        df.loc[:,"transaction_type"] = "general"
    else:
        df.loc[:,"transaction_type"] = "research"

    # LIGHT CLEANING
    df.loc[:,"covered_recipient_first_name"] = df["covered_recipient_first_name"].apply(normalize_names)
    df.loc[:,"covered_recipient_last_name"] = df["covered_recipient_last_name"].apply(normalize_names)

    df.loc[:,"recipient_city"] = df["recipient_city"].str.strip().str.title()
    df.loc[:,"recipient_state"] = df["recipient_state"].str.strip().str.upper()

    df.loc[:,"applicable_manufacturer_or_applicable_gpo_making_payment_name"] = df["applicable_manufacturer_or_applicable_gpo_making_payment_name"].str.strip()

    # ENSURE COLUMN ORDER
    column_order = [
        "covered_recipient_profile_id",
        "covered_recipient_npi",
        "covered_recipient_first_name",
        "covered_recipient_last_name",
        "recipient_city",
        "recipient_state",
        "applicable_manufacturer_or_applicable_gpo_making_payment_id",
        "applicable_manufacturer_or_applicable_gpo_making_payment_name",
        "name_of_drug_or_biological_or_device_or_medical_supply_1",
        "total_amount_of_payment_usdollars",
        "date_of_payment",
        "record_id",
        "program_year",
        "transaction_type"
    ]
    df = df[column_order]

    return df

def normalize_names(name: str) -> str:
    if isinstance(name, str):
        name = name.strip()
        if name.isupper():
            name = name.title()

        return name