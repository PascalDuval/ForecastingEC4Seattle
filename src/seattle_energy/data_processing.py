from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW_DATA_PATH = ROOT / "data" / "raw" / "2016_Building_Energy_Benchmarking.csv"
OUTPUT_PATH = ROOT / "data" / "processed" / "feature_engineered_cleaned_for_bento.csv"
CURRENT_YEAR = 2016
USE_CATEGORIES = [
    "Hotel",
    "Office",
    "Retail Store",
    "Other",
    "Non-Refrigerated Warehouse",
    "K-12 School",
    "Medical Office",
    "Worship Facility",
]


def safe_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return np.nan


def build_feature_dataframe(raw: pd.DataFrame) -> pd.DataFrame:
    raw = raw.copy()

    raw["SiteEnergyUse(kBtu)"] = raw["SiteEnergyUse(kBtu)"].apply(safe_float)
    raw["Electricity(kBtu)"] = raw["Electricity(kBtu)"].apply(safe_float)
    raw["PropertyGFABuilding(s)"] = raw["PropertyGFABuilding(s)"].apply(safe_float)
    raw["PropertyGFAParking"] = raw["PropertyGFAParking"].apply(safe_float)
    raw["YearBuilt"] = raw["YearBuilt"].apply(safe_float)
    raw["NumberofFloors"] = raw["NumberofFloors"].apply(safe_float)

    raw = raw.dropna(subset=[
        "SiteEnergyUse(kBtu)",
        "Electricity(kBtu)",
        "PropertyGFABuilding(s)",
        "YearBuilt",
    ])

    raw = raw[raw["SiteEnergyUse(kBtu)"] > 0]
    raw = raw[raw["PropertyGFABuilding(s)"] > 0]

    raw["BuildingAge"] = CURRENT_YEAR - raw["YearBuilt"].astype(int)
    raw["log_surface"] = np.log1p(raw["PropertyGFABuilding(s)"])
    raw["surface_per_floor"] = raw.apply(
        lambda row: row["PropertyGFABuilding(s)"] / row["NumberofFloors"]
        if row["NumberofFloors"] > 0
        else row["PropertyGFABuilding(s)"],
        axis=1,
    )
    raw["has_parking"] = (raw["PropertyGFAParking"] > 0).astype(int)
    raw["percent_electricity"] = (
        raw["Electricity(kBtu)"] / raw["SiteEnergyUse(kBtu)"]
    ).clip(0, 1) * 100.0

    use_type = raw["LargestPropertyUseType"].fillna("Other")
    for category in USE_CATEGORIES:
        safe_name = category.replace(" ", "_").replace("-", "_")
        raw[f"Use_{safe_name}"] = (use_type == category).astype(int)

    raw["Use_Unknown"] = (~use_type.isin(USE_CATEGORIES)).astype(int)

    columns = [
        "OSEBuildingID",
        "Latitude",
        "Longitude",
        "YearBuilt",
        "NumberofFloors",
        "PropertyGFAParking",
        "PropertyGFABuilding(s)",
        "SiteEnergyUse(kBtu)",
        "TotalGHGEmissions",
        "BuildingAge",
        "log_surface",
        "surface_per_floor",
        "has_parking",
        "percent_electricity",
    ]

    one_hot_columns = [
        f"Use_{category.replace(' ', '_').replace('-', '_')}"
        for category in USE_CATEGORIES
    ]
    columns.extend(one_hot_columns)
    columns.append("Use_Unknown")

    return raw[columns].reset_index(drop=True)


def load_raw_data(path: Path = RAW_DATA_PATH) -> pd.DataFrame:
    return pd.read_csv(path, low_memory=False)


def save_processed_data(df: pd.DataFrame, path: Path = OUTPUT_PATH) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(path, index=False)


def main() -> None:
    print(f"Loading raw dataset from {RAW_DATA_PATH}")
    raw = load_raw_data()
    print("Transforming raw dataset into clean model features")
    processed = build_feature_dataframe(raw)
    save_processed_data(processed)
    print(f"Saved processed dataset to {OUTPUT_PATH}")
    print(f"Processed rows: {len(processed)}")


if __name__ == "__main__":
    main()
