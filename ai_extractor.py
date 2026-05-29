import os
import json
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def clean_json_response(text):
    text = text.strip()

    if text.startswith("```json"):
        text = text.replace("```json", "").replace("```", "").strip()
    elif text.startswith("```"):
        text = text.replace("```", "").strip()

    return text

def extract_incentive_data(page_text, url):
    prompt = f"""
Extract structured incentive program data from this webpage text.

Return ONLY valid JSON.

Fields:
- program_name: Title of the main incentive program
- state: State(s) where program is valid
- city: City/cities where program is valid
- zip_codes: Specific ZIP codes covered
- incentive_type: One of: Grants, Rebates, Finance Solutions, Tax Credits, Investments
- property_type: Type of property (Residential, Commercial, Multifamily, etc.)
- description: DETAILED 2-3 sentence summary of what the program offers and who it helps
- eligibility_criteria: SPECIFIC requirements including:
  * Income limits (e.g., "80% Area Median Income", "Low-income households")
  * Property requirements (e.g., "Owner-occupied single-family homes")
  * Location requirements
  * Any other qualification criteria
- incentive_amount: Dollar amounts, percentages, or ranges (e.g., "$5,000", "Up to $10,000", "30% tax credit")
- valid_until: Expiration date or deadline
- updated_at: Date information was last updated
- review_needed: "Yes" if any critical field is unclear or missing, otherwise "No"
- program_links: {url}

Rules:
- For description: Extract or summarize the main program benefits and purpose
- For eligibility_criteria: Look for income limits, property type, residency requirements, age requirements
- If statewide coverage, zip_codes = "All Florida ZIP Codes"
- If any field is truly missing → null
- Be as specific as possible, avoid vague terms

EXAMPLES:

Good eligibility_criteria:
"Homeowners with household income at or below 80% Area Median Income (AMI), owner-occupied single-family homes, current on property taxes and mortgage payments"

Bad eligibility_criteria:
"Homeowners only"

Good description:
"Provides forgivable loans up to $20,000 for low-income homeowners to repair health and safety code violations including roof repairs, electrical systems, and plumbing issues"

Bad description:
"Housing repair program"

Now extract from this text:

TEXT:
{page_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Extract clean JSON only."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )

    content = response.choices[0].message.content

    data = json.loads(clean_json_response(content))

    if isinstance(data, list):
        if len(data) > 0:
            data = data[0]
        else:
            data = {}

    return data
