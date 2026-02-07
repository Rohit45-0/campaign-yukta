from openai import AzureOpenAI
import json
import os
import re
from pathlib import Path
from dotenv import load_dotenv

# Try to load .env from multiple locations (local dev vs cloud)
env_paths = [
    Path(__file__).resolve().parent.parent.parent / ".env",  # d:\Campaign\.env
    Path(__file__).resolve().parent.parent / ".env",         # campaign-ai/.env
    Path(__file__).resolve().parent / ".env",                # backend/.env
]
for env_path in env_paths:
    if env_path.exists():
        load_dotenv(dotenv_path=env_path)
        break

# Get credentials (works with both .env files and environment variables)
endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
api_key = os.getenv("AZURE_OPENAI_API_KEY")
api_version = os.getenv("AZURE_API_VERSION", "2024-02-15-preview")
deployment = os.getenv("AZURE_DEPLOYMENT_NAME", "gpt-4o")

print(f"[LLM] Endpoint: {endpoint}")
print(f"[LLM] API Key: {'***' + api_key[-4:] if api_key else 'NOT SET'}")
print(f"[LLM] Deployment: {deployment}")

if not endpoint or not api_key:
    raise Exception("Azure OpenAI credentials not found. Set environment variables or check .env file.")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

SCHEMA = """{
  "deal": {
    "deal_name": null,
    "deal_type": "",
    "advertiser_name": "",
    "client_name": null,
    "brand_name": "",
    "product_category": "",
    "agency_name": "",
    "tournament_name": "",
    "sales_person": "",
    "plant": null,
    "zone": null,
    "sales_group": null,
    "start_date": "",
    "end_date": "",
    "deal_currency": null,
    "execution_currency": "INR",
    "currency_conversion_rate": null,
    "booked_revenue": "",
    "discount_type": null,
    "discount": null,
    "booked_revenue_execution_currency_after_discount": null,
    "booked_revenue_deal_currency_after_discount": null
  },
  "placements": [
    {
      "billing_type": "Standard",
      "ad_server_name": null,
      "start_date": "",
      "end_date": "",
      "tournament_name": "",
      "buy_type": null,
      "ad_format": "",
      "ad_duration": "",
      "content_type": "",
      "spot_type": "Original",
      "platform": "",
      "match": "",
      "creative_id": null,
      "ro_number": null,
      "stream": null,
      "material_number": null,
      "booked_quantity": "",
      "bonus_quantity": null,
      "total_quantity": null,
      "rate": "",
      "booked_revenue": null,
      "campaign_name": null,
      "targeting": "",
      "campaign_manager": null,
      "client": null,
      "product_category": null,
      "brand_name": "",
      "targeting_comments": null,
      "placement_comments": null,
      "placement_name": null
    }
  ]
}"""

SYSTEM_PROMPT = f"""You are a document data extraction AI for advertising Deal Letters and Release Orders. Extract structured data for YuktaOne system.

EXTRACTION RULES:
1. Extract data EXACTLY as it appears in the document
2. For deal_type: Set "Agency" if agency name is present and not "Direct", otherwise set "Direct"
3. advertiser_name: Full legal name including suffix (Ltd., Pvt. Ltd., etc.)
4. agency_name: Full legal name including suffix, or empty if direct client
5. tournament_name: Extract from "ADVERTISING – SPOT BOOKING" section or document title
6. sales_person: Look for "Contact Person" under Star India Private Limited
7. start_date and end_date: Extract from "TERM OF THE AGREEMENT" section, format as YYYY-MM-DD
8. booked_revenue: Extract "Total Consideration" from CONSIDERATION section (numeric only)
9. For placements - extract each line item from "ADVERTISING – SPOT BOOKING" table:
   - ad_format: e.g., "Live + PPL", "Mid Roll", "Pre Roll"
   - ad_duration: Duration in seconds
   - content_type: e.g., "Live", "VOD", "Highlights"
   - platform: e.g., "JioHotstar - HHWeb", "JioHotstar - CTV"
   - match: Number of matches or match details
   - booked_quantity: Impressions or spots booked
   - rate: Unit rate/CPM
   - targeting: Geographic or demographic targeting
   - brand_name: Brand being advertised
10. If a field is not found, use null
11. Numbers must be numeric (remove commas, currency symbols)
12. Return ONLY valid JSON

OUTPUT SCHEMA:
{SCHEMA}

Return ONLY the JSON object, nothing else."""


def parse_document(text: str) -> dict:
    """Parse document text using Azure OpenAI and return structured JSON"""
    
    try:
        response = client.chat.completions.create(
            model=deployment,
            temperature=0,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Extract deal and placement data from this advertising document:\n\n{text}"}
            ]
        )
        
        content = response.choices[0].message.content.strip()
        print(f"[LLM] Response length: {len(content)} chars")
        
        # Remove markdown code fences if present
        if content.startswith("```"):
            first_newline = content.find("\n")
            last_fence = content.rfind("```")
            if last_fence > first_newline:
                content = content[first_newline+1:last_fence].strip()
        
        # Parse JSON
        data = json.loads(content)
        
        # Validate structure
        if "deal" not in data:
            data["deal"] = {}
        if "placements" not in data:
            data["placements"] = []
            
        return data
        
    except json.JSONDecodeError as e:
        print(f"[LLM] JSON parse error: {e}")
        print(f"[LLM] Raw content: {content[:500]}")
        raise Exception(f"Failed to parse LLM response as JSON: {str(e)}")
    except Exception as e:
        print(f"[LLM] Error: {e}")
        raise Exception(f"LLM processing failed: {str(e)}")
