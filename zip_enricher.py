from source_registry import URL_RECORDS

URL_LOOKUP = {item["url"]: item for item in URL_RECORDS}


def clean_city_zip(record, url):
    meta = URL_LOOKUP.get(url, {})

    record["city"] = meta.get("city", "Review Needed")
    record["zip_codes"] = meta.get("zip_codes", "Review Needed")
    record["source_type"] = meta.get("source_type", "generic")
    record["program_links"] = url

    if record["city"] == "Review Needed" or record["zip_codes"] == "Review Needed":
        record["review_needed"] = "Yes"
    else:
        record["review_needed"] = "No"

    return record
