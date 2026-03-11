# IndiaMART Supplier Intelligence Scraper

---

This IndiaMart Scraper project follows a classic **ETL (Extract, Transform, Load)** pattern:

- **Extraction:** Uses the Firecrawl API to navigate IndiaMART listings and extract structured JSON data using LLM-based schemas.
- **Transformation:** Cleans and normalizes raw data (e.g., city extraction from location strings) and prepares it for analysis.
- **Visualization:** A Streamlit web application displays key metrics and the final dataset in a user-friendly interface.

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python |
| Scraping | Firecrawl (LLM-based extraction) |
| Data Handling | Pandas, Pydantic, JSON |
| Frontend | Streamlit |
| Environment | Dotenv for API key management |

---

## Project Structure

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

## Setup & Installation

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

## How to Run

### Step 1 — Scrape Data

Run the scraper by providing a target IndiaMART URL:

```bash
python indiamart_scrapper.py --url "https://www.indiamart.com/isearch.php?s=industrial+pumps" --api_key "YOUR_KEY"
```

This will:
- Scrape the listing page and collect all product links
- Visit each product's detail page to extract product details
- Save the raw output to `raw_data.txt`

### Step 2 — Launch Dashboard

Once `data.json` is generated, launch the Streamlit app:

```bash
streamlit run streamlit.py
```  
