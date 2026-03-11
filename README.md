# 🕷️ IndiaMART Supplier Intelligence Scraper

---

## 🚀 Overview

The project follows a classic **ETL (Extract, Transform, Load)** pattern:

- **Extraction:** Uses the Firecrawl API to navigate IndiaMART listings and extract structured JSON data using LLM-based schemas.
- **Transformation:** Cleans and normalizes raw data (e.g., city extraction from location strings) and prepares it for analysis.
- **Visualization:** A Streamlit web application displays key metrics and the final dataset in a user-friendly interface.

---

## 🛠️ Tech Stack

| Layer | Tool |
|---|---|
| Language | Python |
| Scraping | Firecrawl (LLM-based extraction) |
| Data Handling | Pandas, Pydantic, JSON |
| Frontend | Streamlit |
| Environment | Dotenv for API key management |

---

## 📂 Project Structure

```
indiamart-scraper/
│
├── indiamart_scrapper.py   # Core engine: scraping, normalization, file storage
├── streamlit.py            # Dashboard: reads data.json and renders metrics
├── raw_data.txt            # Intermediate storage for raw scraped results
├── data.json               # Final transformed dataset used by the dashboard
├── .env                    # API key (not committed to git)
└── README.md               # Project documentation
```

---

## ⚙️ Setup & Installation

**1. Clone the repository:**

```bash
git clone https://github.com/Ankit-Kolte/indiamart-scraper.git
cd indiamart-scraper
```

**2. Install dependencies:**

```bash
pip install firecrawl-py pydantic streamlit pandas python-dotenv
```

**3. Environment Variables:**

Create a `.env` file in the root directory and add your Firecrawl API key:

```env
FIRECRAWL_API_KEY=your_api_key_here
```

> ⚠️ **Note:** Firecrawl API needs credits. You get **500 free credits** on a new account.

---

## 📊 How to Run

### Step 1 — Scrape Data

Run the scraper by providing a target IndiaMART URL:

```bash
python indiamart_scrapper.py --url "https://www.indiamart.com/isearch.php?s=industrial+pumps" --api_key "YOUR_KEY"
```

This will:
- Scrape the listing page and collect all product links
- Visit each product's detail page to extract technical specs, MOQ, and delivery time
- Save the raw output to `raw_data.txt`

### Step 2 — Launch Dashboard

Once `data.json` is generated, launch the Streamlit app:

```bash
streamlit run streamlit.py
```

---

## 🔍 How It Works — Code Walkthrough

### Pydantic Schemas for Structured Extraction

The scraper uses two Pydantic models to define exactly what fields to extract:

```python
from pydantic import BaseModel, Field
from typing import List, Optional

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
```

---

### Phase 1 — Harvest Product Links from Listing Page

```python
def get_data_from_scrapping(url):
    harvest_result = app.scrape(
        url=url,
        formats=[{
            "type": "json",
            "schema": ProductLinkList.model_json_schema(),
            "prompt": "Extract the company name, product title, location, and the direct URL link for every product card."
        }]
    )
    if harvest_result and harvest_result.json:
        return harvest_result.json.get("products", [])
    return []
```

---

### Phase 2 — Deep Scrape Each Product Detail Page

```python
for item in listing_data:
    target_url = item['product_url']

    # Ensure URL is absolute
    if not target_url.startswith("https"):
        target_url = "https://www.indiamart.com" + target_url

    try:
        detail_result = app.scrape(
            url=target_url,
            formats=[{
                "type": "json",
                "schema": TechnicalDetails.model_json_schema(),
                "prompt": "Extract the technical specifications, MOQ, and delivery time."
            }]
        )
        deep_info = detail_result.json if detail_result and detail_result.json else {}
        combined_entry = {
            "basic_info": item,
            "deep_technical_data": deep_info
        }
        final_deep_dataset.append(combined_entry)

    except Exception as e:
        print(f"Error scraping {target_url}: {e}")
```

---

### Data Normalization — City Extraction

Splits `"Bhiwadi, Rajasthan"` → `"Bhiwadi"` for clean city-level grouping:

```python
def normalize_city(location):
    if not location:
        return "Unknown"
    return location.split(",")[0].strip().title()
```

---

### Extracting Values from Markdown Spec Tables

```python
import re

def extract_from_specs(specs_string, key_name):
    if not specs_string:
        return "Not Specified"
    pattern = rf"\|\s*{key_name}\s*\|\s*([^|]+)\s*\|"
    match = re.search(pattern, specs_string, re.IGNORECASE)
    return match.group(1).strip() if match else "Not Specified"
```

---

### Analysis — Companies per City

```python
def count_companies_by_city(cleaned_data):
    city_map = {}
    for d in cleaned_data:
        city = d["city"]
        company = d["company"]
        if city not in city_map:
            city_map[city] = set()
        city_map[city].add(company)   # set() prevents double-counting
    return {city: len(companies) for city, companies in city_map.items()}
```

---

### Analysis — Products per Company

```python
def count_of_products_per_company(cleaned_data):
    product_count = {}
    for d in cleaned_data:
        product = d["product"]
        if product not in product_count:
            product_count[product] = 0
        product_count[product] += 1
    return product_count
```

---

### Streamlit Dashboard

```python
import streamlit as st
import json
import pandas as pd

with open("data.json") as f:
    data = json.load(f)

st.set_page_config(page_title="Industrial Analysis", layout="wide")
st.title("IndiaMart Industries Stats")

df = pd.DataFrame(data)

st.subheader("📊 Key Metrics")
col1, col2, col3 = st.columns(3)

col1.metric("Total Companies Listed",         value=len(df))
col2.metric("Total Unique Products",          value=df['product'].nunique())
col3.metric("Total Cities with Suppliers",    value=df['city'].nunique())

st.divider()
st.table(df)
```

---

## 📈 Key Features

- **AI-Powered Extraction:** Uses Pydantic schemas to ensure the scraper returns structured data like MOQ, delivery time, and technical specs.
- **Two-Phase Scraping:** Listing page harvested first, then each product detail page visited individually — minimizing wasted API calls.
- **Fault-Tolerant:** Each detail page scrape is wrapped in `try/except` so one failure doesn't crash the entire run.
- **Data Normalization:** Automatically splits `"City, State"` strings to provide clean city-level analytics.
- **File Caching:** Raw results saved to `raw_data.txt` so the scraper doesn't need to re-run during development.
- **Dashboard Metrics:** Visualizes total companies listed, unique products found, and city distribution.

---

## 👤 Author

**Ankit Kolte**  
📍 Pune, India  
🎓 B.Tech Student at Sushila Devi Bansal College of Engineering  
🔗 [GitHub](https://github.com/Ankit-Kolte/indiamart-scraper)
