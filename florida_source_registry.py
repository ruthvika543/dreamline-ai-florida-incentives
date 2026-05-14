import pandas as pd
from scraper import scrape_page_text
from ai_extractor import extract_incentive_data
from validator import validate_record

urls = [
    "https://www.irs.gov/credits-deductions/residential-clean-energy-credit",
    "https://www.irs.gov/credits-deductions/energy-efficient-home-improvement-credit",
    "https://mysafeflhome.com/",
    "https://floridaenergysaverprogram.fdacs.gov/",
    "https://www.floridahousing.org/programs/special-programs/ship---state-housing-initiatives-partnership-program",
    "https://www.floridahousing.org/buyers-renters/local-housing-programs",
    "https://www.tampaelectric.com/residential/saveenergy/rebates/",
    "https://www.fpl.com/save/programs.html",
    "https://www.duke-energy.com/home/products/home-energy-improvement",
    "https://www.duke-energy.com/home/products/florida-savings",
    "https://www.duke-energy.com/home/products/home-energy-check",
    "https://www.duke-energy.com/home/products/home-energy-improvement/heat-pump-water-heater",
    "https://www.duke-energy.com/home/products/smart-saver/windows",
    "https://www.tampa.gov/housing-and-community-development",
    "https://www.tampa.gov/housing-and-community-development/programs/residential-services",
    "https://www.tampa.gov/housing-and-community-development/apply-housing-rehabilitation-renovation-program-hrrp",
    "https://www.tampa.gov/cras/east-tampa/owner-occupied-rehabilitation-program",
    "https://www.tampa.gov/cras/community-redevelopment-areas/cra-housing-programs-initiatives",
    "https://www.hillsboroughcounty.org/en/residents/property-owners-and-renters/homeowners-and-neighborhoods/down-payment-assistance",
    "https://floridapace.gov/",
    "https://floridapace.gov/home-improvement/",
    "https://www.osceola.org/Doing-Business/Community-and-Economic-Development/Florida-PACE-Funding-Agency",
    "https://www.pascotaxes.com/faqs/pace-program/"
]

records = []

for url in urls:
    print(f"Processing: {url}")

    try:
        text = scrape_page_text(url)
        data = extract_incentive_data(text, url)
        data = validate_record(data)

        records.append(data)
        print("Success")

    except Exception as e:
        print(f"Failed: {url}")
        print(e)

df = pd.DataFrame(records)

columns = [
    "program_name",
    "state",
    "city",
    "incentive_type",
    "property_type",
    "description",
    "eligibility_criteria",
    "incentive_amount",
    "valid_until",
    "updated_at",
    "review_needed",
    "program_links"
]

for col in columns:
    if col not in df.columns:
        df[col] = None

df = df[columns]

df.to_csv("output/shivaani_extracted_florida_incentives.csv", index=False)

print("CSV created successfully!")
