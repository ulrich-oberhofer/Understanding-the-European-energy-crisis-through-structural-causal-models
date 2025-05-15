"""
This module defines constants, dictionaries, and mappings related to energy generation and European bidding zones (BZNs).
Constants:
-----------
- ENERGY_CRISIS: A pandas Timestamp marking the start of the energy crisis (October 1, 2021, UTC).
Lists:
------
- EUROPEAN_BZN: A list of European bidding zones (BZNs) represented by their codes.
Dictionaries:
-------------
- GEN_COLUMN_MAP: Maps energy generation and consumption types to their corresponding column names in a dataset.
- GEN_COLUMN_MAP_ALT: A modified version of GEN_COLUMN_MAP that removes entries related to consumption and the phrase "Actual Aggregated".
- bzn_to_country: Maps bidding zone codes (BZNs) to their corresponding country codes.
- COUNTRY_CODE_TO_COUNTRY: Maps specific bidding zone codes to their corresponding country codes, consolidating sub-regions into a single country code.
Derived Variables:
------------------
- country_codes: A list of unique country codes derived from the `bzn_to_country` dictionary.
"""

import pandas as pd

ENERGY_CRISIS = pd.Timestamp("20211001", tz="UTC")

EUROPEAN_BZN = [
    "AT",
    "BE",
    "CZ",
    "HR",
    "DK_1",
    "DK_2",
    "EE",
    "FI",
    "FR",
    "DE_LU",
    "DE_AT_LU",
    "HU",
    "IT_SICI",
    "IT_CSUD",
    "IT_CNOR",
    "IT_SUD",
    "IT_SARD",
    "IT_NORD",
    "IT_CALA",
    "IT_ROSN",  # 4 hubs in Italy
    "IT_BRNN",
    "IT_FOGN",
    "IT_PRGP",
    "LV",
    "LT",
    "NL",
    "NO_1",
    "NO_2",
    "NO_3",
    "NO_4",
    "NO_5",
    "PL",
    "PT",
    "RO",
    "SK",
    "SI",
    "ES",
    "SE_1",
    "SE_2",
    "SE_3",
    "SE_4",
]

GEN_COLUMN_MAP = {
    "Biomass Actual Aggregated": "biomass_gen",
    "Biomass Actual Consumption": "biomass_cons",
    "Fossil Brown coal/Lignite Actual Aggregated": "lignite_gen",
    "Fossil Brown coal/Lignite Actual Consumption": "lignite_cons",
    "Fossil Coal-derived gas Actual Aggregated": "coal_derived_gas_gen",
    "Fossil Coal-derived gas Actual Consumption": "coal_derived_gas_cons",
    "Fossil Gas Actual Aggregated": "gas_gen",
    "Fossil Gas Actual Consumption": "gas_cons",
    "Fossil Hard coal Actual Aggregated": "hard_coal_gen",
    "Fossil Hard coal Actual Consumption": "hard_coal_cons",
    "Fossil Oil Actual Aggregated": "oil_gen",
    "Fossil Oil Actual Consumption": "oil_cons",
    "Fossil Oil shale Actual Aggregated": "oil_shale_gen",
    "Fossil Peat Actual Aggregated": "peat_gen",
    "Geothermal Actual Aggregated": "geothermal_gen",
    "Geothermal Actual Consumption": "geothermal_cons",
    "Hydro Pumped Storage Actual Aggregated": "hydro_storage_gen",
    "Hydro Pumped Storage Actual Consumption": "hydro_storage_cons",
    "Hydro Run-of-river and poundage Actual Aggregated": "run_off_gen",
    "Hydro Run-of-river and poundage Actual Consumption": "run_off_cons",
    "Hydro Water Reservoir Actual Aggregated": "hydro_reservoir_gen",
    "Hydro Water Reservoir Actual Consumption": "hydro_reservoir_cons",
    "Marine Actual Aggregated": "marine_gen",
    "Nuclear Actual Aggregated": "nuclear_gen",
    "Nuclear Actual Consumption": "nuclear_cons",
    "Other Actual Aggregated": "other_gen",
    "Other Actual Consumption": "other_cons",
    "Other renewable Actual Aggregated": "other_renew_gen",
    "Other renewable Actual Consumption": "other_renew_cons",
    "Solar Actual Aggregated": "solar_gen",
    "Solar Actual Consumption": "solar_cons",
    "Waste Actual Aggregated": "waste_gen",
    "Waste Actual Consumption": "waste_cons",
    "Wind Offshore Actual Aggregated": "wind_off_gen",
    "Wind Offshore Actual Consumption": "wind_off_cons",
    "Wind Onshore Actual Aggregated": "wind_on_gen",
    "Wind Onshore Actual Consumption": "wind_on_cons",
    "B i o m a s s": "alt_biomass_gen",
}

# remove entries with consumption and remove "actual aggregated"
GEN_COLUMN_MAP_ALT = {
    k.replace(" Actual Aggregated", ""): v
    for k, v in GEN_COLUMN_MAP.items()
    if "Aggregated" in k
}

bzn_to_country = {
    "bzn_at": "AT",
    "bzn_be": "BE",
    "bzn_cz": "CZ",
    "bzn_hr": "HR",
    "bzn_dk1": "DK_1",
    "bzn_dk2": "DK_2",
    "bzn_ee": "EE",
    "bzn_fi": "FI",
    "bzn_fr": "FR",
    "bzn_de-lu": "DE_LU",
    "bzn_hu": "HU",
    "bzn_it-sicily": "IT_SICI",
    "bzn_it-centre-south": "IT_CSUD",
    "bzn_it-centre-north": "IT_CNOR",
    "bzn_it-south": "IT_SUD",
    "bzn_it-sardinia": "IT_SARD",
    "bzn_it-north": "IT_NORD",
    "bzn_it-cala": "IT_CALA",
    "bzn_it-rosn": "IT_ROSN",
    "bzn_lv": "LV",
    "bzn_lt": "LT",
    "bzn_nl": "NL",
    "bzn_no1": "NO_1",
    "bzn_no2": "NO_2",
    "bzn_no3": "NO_3",
    "bzn_no4": "NO_4",
    "bzn_no5": "NO_5",
    "bzn_pl": "PL",
    "bzn_pt": "PT",
    "bzn_ro": "RO",
    "bzn_sk": "SK",
    "bzn_si": "SI",
    "bzn_es": "ES",
    "bzn_se1": "SE_1",
    "bzn_se2": "SE_2",
    "bzn_se3": "SE_3",
    "bzn_se4": "SE_4",
}

country_codes = []
for i in bzn_to_country.values():
    country_codes.append(i)


COUNTRY_CODE_TO_COUNTRY = {
    "DK_1": "DK",
    "DK_2": "DK",
    "DE_LU": "DE",
    "IT_SICI": "IT",
    "IT_CSUD": "IT",
    "IT_CNOR": "IT",
    "IT_SUD": "IT",
    "IT_SARD": "IT",
    "IT_NORD": "IT",
    "IT_CALA": "IT",
    "IT_ROSN": "IT",
    "NO_1": "NO",
    "NO_2": "NO",
    "NO_3": "NO",
    "NO_4": "NO",
    "NO_5": "NO",
    "SE_1": "SE",
    "SE_2": "SE",
    "SE_3": "SE",
    "SE_4": "SE",
}
