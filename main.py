import os
import pandas as pd

from scraper import scrape_page_text
from ai_extractor import extract_incentive_data
from zip_enricher import clean_city_zip
from validator import validate_record
from source_registry import URL_RECORDS


# Create output folder if it does not exist
os.makedirs("output", exist_ok=True)


# Load URLs from source_registry.py
urls = [item["url"] for item in URL_RECORDS]


records = []

for url in urls:
    print(f"Processing: {url}")

    try:
        # Step 1: Scrape website text
        text = scrape_page_text(url)

        # Step 2: Use LLM parser to extract structured incentive data
        data = extract_incentive_data(text, url)

        # Step 3: Make sure program link is always the current URL
        data["program_links"] = url

        # Step 4: Add clean city, zip codes, and source type from source registry
        data = clean_city_zip(data, url)

        # Step 5: Validate missing fields / cleanup record
        data = validate_record(data)

        # Step 6: Save final record
        records.append(data)

        print("Success")

    except Exception as e:
        print(f"Failed: {url}")
        print(e)


# Convert extracted records into DataFrame
df = pd.DataFrame(records)


# Final CSV column order
columns = [
    "program_name",
    "state",
    "city",
    "zip_codes",
    "source_type",
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


# Add missing columns if LLM does not return something
for col in columns:
    if col not in df.columns:
        df[col] = None


# Reorder columns
df = df[columns]


# Save final CSV
output_file = "output/shivaani_extracted_florida_incentives.csv"
df.to_csv(output_file, index=False)


print("CSV created successfully!")
print(f"Total records created: {len(df)}")
print(f"Saved file: {output_file}")
