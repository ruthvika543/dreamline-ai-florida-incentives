import pgeocode
import pandas as pd

nomi = pgeocode.Nominatim("us")

def get_florida_zips_by_city(city):
    all_zips = nomi._data

    results = all_zips[
        (all_zips["state_code"] == "FL") &
        (all_zips["place_name"].str.lower() == city.lower())
    ]

    return ",".join(sorted(results["postal_code"].astype(str).unique()))

def get_florida_zips_by_county(county):
    all_zips = nomi._data

    results = all_zips[
        (all_zips["state_code"] == "FL") &
        (all_zips["county_name"].str.lower().str.contains(county.lower(), na=False))
    ]

    return ",".join(sorted(results["postal_code"].astype(str).unique()))

def assign_zip_codes(record):
    city = str(record.get("city", "")).strip()
    state = str(record.get("state", "")).strip()
    program_name = str(record.get("program_name", "")).lower()
    link = str(record.get("program_links", "")).lower()

    if state.lower() == "florida" and city.lower() in ["statewide", "all florida", "florida", "nan", "none", ""]:
        return "All Florida ZIP Codes"

    if "mysafeflhome" in link or "irs.gov" in link:
        return "All Florida ZIP Codes"

    if "tampaelectric" in link or "teco" in program_name:
        return get_florida_zips_by_county("Hillsborough")

    if city and city.lower() not in ["nan", "none", "statewide", "all florida"]:
        zips = get_florida_zips_by_city(city)
        if zips:
            return zips

    return "Review Needed"
