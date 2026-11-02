from scripts.extract_usgs_historical_earthquake_data import (
    extract_earthquake_data_by_year,
)
from scripts.transform_earthquake_data import transform_earthquake_data
from scripts.load_data_postgis import load_earthquake_data, load_fault_data
from scripts.transform_fault_data import transform_fault_data


def run_etl():
    print("Starting ETL!")
    extract_earthquake_data_by_year()
    transform_earthquake_data()
    transform_fault_data()
    load_earthquake_data()
    load_fault_data()


if __name__ == "__main__":
    run_etl()
