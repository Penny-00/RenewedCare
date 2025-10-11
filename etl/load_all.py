from .load_disease_indicators import load_all_disease_files
from .load_mortality_data import load_all_mortality_files
from .load_outbreak_reports import load_all_outbreak_files

if __name__ == "__main__":
    load_all_disease_files("data/processed/disease_indicators")
    load_all_mortality_files("data/processed/mortality")
    load_all_outbreak_files("data/processed/outbreaks")
