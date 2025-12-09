from datetime import datetime
import pandas as pd
from pathlib import Path

from utils.utils_cms import read_cms_files, clean_cms_files

years = range(2018, 2025)

for year in years:
    start_time = datetime.now()
    gen_file = Path(f"./data/general_payments") / f"cms_general_{year}.csv"
    res_file = Path(f"./data/research_payments") / f"cms_research_{year}.csv"

    if not gen_file.exists():
        print(f"General payments file path not found at: {gen_file}")
        continue
    if not res_file.exists():
        print(f"Research payments file path not found at: {res_file}")
        continue

    export_path = Path(f"./exports/cms_unified_{year}_test.csv")
    export_path.parent.mkdir(parents=True, exist_ok=True)

    gen_df = read_cms_files(gen_file, "g")
    res_df = read_cms_files(res_file, "r")

    gen_df = clean_cms_files(gen_df, "g")
    res_df = clean_cms_files(res_df, "r")

    unified_df = pd.concat([gen_df, res_df], ignore_index=True)
    unified_df.drop_duplicates(inplace=True)
    unified_df.to_csv(export_path, index=False, encoding="utf-8", date_format="%Y-%m-%d")

    end_time = datetime.now()
    elapsed_time = end_time - start_time
    print(f"Year {year} processed and saved to {export_path} (elapsed: {elapsed_time})")





