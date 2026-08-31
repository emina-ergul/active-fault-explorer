from pathlib import Path
import geopandas as gpd
import pandas as pd


def clean_slip_rate_value(value):
    if not value or value.lower() in ("none", "nan", "na"):
        return None
    if isinstance(value, str) and value not in ("", "None", "nan"):
        return str(value).strip()
    else:
        return float(value)


def transform_slip_rates(rates):
    net_slip_rate_most_likely_mm = None
    net_slip_rate_min_mm = None
    net_slip_rate_max_mm = None

    if pd.isna(rates):
        return None, None, None
    else:
        rates = rates.strip("()").split(",")

        while len(rates) < 3:
            rates.append(None)

        net_slip_rate_most_likely_mm = clean_slip_rate_value(rates[0])
        net_slip_rate_min_mm = clean_slip_rate_value(rates[1])
        net_slip_rate_max_mm = clean_slip_rate_value(rates[2])

    return net_slip_rate_most_likely_mm, net_slip_rate_min_mm, net_slip_rate_max_mm


def transform_fault_data():
    transformed_data = []

    gem_data = gpd.read_file("backend/data/gem/geojson/gem_active_faults.geojson")
    gem_data = gem_data.to_crs(epsg=4326)

    gem_data = gem_data[
        [
            "catalog_id",
            "catalog_name",
            "name",
            "slip_type",
            "last_movement",
            "net_slip_rate",
            "geometry",
        ]
    ]

    for i, row in gem_data.iterrows():
        if row["geometry"] is None:
            continue

        net_slip_rate_most_likely_mm, net_slip_rate_min_mm, net_slip_rate_max_mm = (
            transform_slip_rates(row["net_slip_rate"])
        )

        if pd.isna(row["last_movement"]) or row["last_movement"] in (
            "None",
            "nan",
            "NaN",
        ):
            row["last_movement"] = None

        row = {
            "catalog_id": row["catalog_id"],
            "catalog_name": row["catalog_name"],
            "name": row["name"],
            "slip_type": row["slip_type"],
            "last_movement": row["last_movement"],
            "net_slip_rate_most_likely_mm": net_slip_rate_most_likely_mm,
            "net_slip_rate_min_mm": net_slip_rate_min_mm,
            "net_slip_rate_max_mm": net_slip_rate_max_mm,
            "geometry": row["geometry"],
        }
        transformed_data.append(row)

    gdf = gpd.GeoDataFrame(transformed_data, geometry="geometry", crs="EPSG:4326")

    output_file = Path("backend/data/processed/faults/faults.geojson")
    output_file.parent.mkdir(parents=True, exist_ok=True)

    gdf.to_file(output_file, driver="GeoJSON")


if __name__ == "__main__":
    transform_fault_data()
