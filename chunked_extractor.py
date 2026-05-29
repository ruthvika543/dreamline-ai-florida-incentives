def extract_with_chunking(page_text, url):
    """
    Process long pages in overlapping chunks, merge results
    """
    chunk_size = 8000
    overlap = 1000
    
    chunks = []
    for i in range(0, len(page_text), chunk_size - overlap):
        chunk = page_text[i:i + chunk_size]
        chunks.append(chunk)
    
    all_data = []
    for chunk in chunks:
        try:
            data = extract_incentive_data(chunk, url)
            all_data.append(data)
        except:
            continue
    
    # Merge: Take longest non-null value for each field
    merged = {}
    for field in ["description", "eligibility_criteria", "incentive_amount"]:
        candidates = [d.get(field) for d in all_data if d.get(field)]
        if candidates:
            # Pick the most detailed one (longest)
            merged[field] = max(candidates, key=len)
        else:
            merged[field] = None
    
    # For other fields, take first non-null
    for field in ["program_name", "state", "city", "zip_codes", "incentive_type", "property_type"]:
        for d in all_data:
            if d.get(field):
                merged[field] = d.get(field)
                break
    
    return merged