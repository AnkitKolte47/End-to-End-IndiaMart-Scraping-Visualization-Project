import os
import json
from dotenv import load_dotenv
from firecrawl import FirecrawlApp
from pydantic import BaseModel, Field
from typing import List, Optional
import re
import statistics
from collections import Counter
import pandas as pdt
import argparse

base_url = "https://www.indiamart.com"

load_dotenv()
app = FirecrawlApp(api_key=os.getenv("FIRECRAWL_API_KEY"))

class ProductLink(BaseModel):
    company: str
    product: str
    location: str
    product_url: str = Field(description="The full URL link to the product's detail page")

class ProductLinkList(BaseModel):
    products: List[ProductLink]

class TechnicalDetails(BaseModel):
    specifications: str = Field(description="Technical specifications table or list")
    moq: Optional[str] = Field(None, description="Minimum Order Quantity")
    delivery_time: Optional[str] = Field(None, description="How long it takes to deliver")

# it will run first time only
def get_data_from_scrapping(url):
    print("PHASE 1: Harvesting links from IndiaMART listing page...")

    harvest_result = app.scrape(
        url=url,
        formats=[{
            "type": "json",
            "schema": ProductLinkList.model_json_schema(),
            "prompt": "Extract the company name, product title, location, and the direct URL link for every product card."
        }]
    )

    if harvest_result and harvest_result.json:
        listing_data = harvest_result.json.get("products", [])
    else:
        listing_data = []
        print("Warning: No data found in Phase 1.")    
    return listing_data
# IT will run first time only 
def write_data_into_file(file_name, listing_data):
    with open(file_name, "w") as f:
        f.write(str(listing_data))

## IT will run second time only
def get_data_from_file(file_name):
    with open(file_name, "r") as f:
        reader = f.read()

    listing_data = eval(reader)
    return listing_data

## IT will run first time only
def scrapping_data(url):
    final_deep_dataset = []
    file_name = "raw_data.txt"

    listing_data = get_data_from_scrapping(url)
    write_data_into_file(file_name, listing_data)
    ## run second time only
    listing_data = get_data_from_file(file_name)

    for item in listing_data:
        target_url = item['product_url']
        # Ensure URL is absolute (IndiaMART sometimes uses relative links)
        if not target_url.startswith("https"):
            target_url = "https://www.indiamart.com" + target_url

        print(f"--- Going Inside: {item['product']} ---")
    
        try:
            # FIX: Use 'scrape' here as well
            detail_result = app.scrape(
                url=target_url,
                formats=[{
                    "type": "json",
                    "schema": TechnicalDetails.model_json_schema(),
                    "prompt": "Extract the technical specifications, MOQ, and delivery time."
                }]
            )
        
            # Merge basic info with the deep info
            deep_info = detail_result.json if detail_result and detail_result.json else {}
            combined_entry = {
                "basic_info": item,
                "deep_technical_data": deep_info
            }
            final_deep_dataset.append(combined_entry)
        
        except Exception as e:
            print(f"Error scraping {target_url}: {e}")

    print("Length of final dataset:", len(final_deep_dataset))

    return final_deep_dataset
# It will run second time only 
def normalize_city(location):
    """Splits 'City, State' and returns just the City."""
    if not location:
        return "Unknown"
    # Example: "Bhiwadi , Rajasthan" -> "Bhiwadi"
    return location.split(",")[0].strip().title()

# It will run second timie only
def extract_from_specs(specs_string, key_name):
    """Extracts values from the Markdown table format."""
    if not specs_string:
        return "Not Specified"
    pattern = rf"\|\s*{key_name}\s*\|\s*([^|]+)\s*\|"
    match = re.search(pattern, specs_string, re.IGNORECASE)
    return match.group(1).strip() if match else "Not Specified"

#--- 2. ANALYSIS FUNCTIONS ---
#IT will run second time only
def count_companies_by_city(cleaned_data):
    """Returns unique company counts per city."""
    city_map = {}
    for d in cleaned_data:
        city = d["city"]
        company = d["company"]
        if city not in city_map:
            city_map[city] = set()
        city_map[city].add(company)
    return {city: len(companies) for city, companies in city_map.items()}
# IT will run second time only
def count_of_products_per_company(cleaned_data):
    """Return product name with its count."""

    product_count = {}

    for d in cleaned_data:
        product = d["product"]

        if product not in product_count:
            product_count[product] = 0

        product_count[product] += 1

    return product_count
#--  TRANSFORMATION LOGIC ---
#IT will run second time only
def transform_deep_data(raw_list):
    print("Transform function started")
    records = []
    for item in raw_list:
        print("calling normalize city function to flat the location")
        records.append({
            "company":      item.get("company", "Unknown"),
            "location":     item.get("location"),
            "product":      item.get("product", "Unknown"),
            "city":         normalize_city(item.get("location"))
        })
    return records

if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="Firecrawl scraper")
        parser.add_argument("--url", required=True, help="Enter the product url")
        parser.add_argument("--api_key", required=True, help="Enter your Firecrawl API")
        args = parser.parse_args()
        raw_dataset_file_name = "raw_data.txt"
        raw_dataset = scrapping_data(args.url)
        write_data_into_file(raw_dataset_file_name, raw_dataset)
    #     dataset = get_data_from_file(raw_dataset_file_name)
    #     transformed_data = transform_deep_data(dataset)
    #     print(transformed_data)
    #     companies_count_city = count_companies_by_city(transformed_data)
    #     count_products_company = count_of_products_per_company(transformed_data)
    #     with open("data.json",'w') as file:
    #         json.dump(transformed_data, file, indent=2)
    #     print(companies_count_city)
    #     print(count_products_company)

    except Exception as e:
        print("Error in processing :", str(e))