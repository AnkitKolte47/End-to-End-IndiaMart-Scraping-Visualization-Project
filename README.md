🚀 Overview

The project follows a classic ETL (Extract, Transform, Load) pattern:

Extraction: Uses the Firecrawl API to navigate IndiaMART listings and extract structured JSON data using LLM-based schemas.

Transformation: Cleans and normalizes raw data (e.g., city extraction from location strings) and prepares it for analysis.

Visualization: A Streamlit web application displays key metrics and the final dataset in a user-friendly interface.
---------------------------------------------------------------------------------------------------------------------------------

🛠️ Tech Stack

Language: Python

Scraping: Firecrawl (LLM-based extraction)

Data Handling: Pandas, Pydantic, JSON

Frontend: Streamlit

Environment: Dotenv for API key management
--------------------------------------------------------------------------------------------------------------------------------

📂 Project Structure

indiamart_scrapper.py: The core engine that handles scraping logic, data normalization, and local file storage.

streamlit.py: The dashboard script that reads the processed data.json and renders metrics.

raw_data.txt: Intermediate storage for raw scraped results.

data.json: The final transformed dataset used by the dashboard.

readme.md : README.md helps to understand the structure of project and setup
---------------------------------------------------------------------------------------------------------------------------------

⚙️ Setup & Installation

Clone the repository:

Bash
git clone https://github.com/Ankit-Kolte/indiamart-scraper.git
cd indiamart-scraper
Install dependencies:

Bash
pip install firecrawl-py pydantic streamlit pandas python-dotenv
Environment Variables:
Create a .env file in the root directory and add your Firecrawl API Key:

Code snippet
FIRECRAWL_API_KEY=your_api_key_here (IMP : Firecrawl api needs credits you will get 500 free on new account )
📊 How to Run

```
Scraping started...
Data saved to data.json
```
1. Scrape Data
Run the scraper by providing a target IndiaMART URL and your API key via the command line:

Bash
python indiamart_scrapper.py --url "https://www.indiamart.com/isearch.php?s=industrial+pumps" --api_key "YOUR_KEY"

2. Launch Dashboard
Once the data.json file is generated, launch the Streamlit app:

Bash
streamlit run streamlit.py
-----------------------------------------------------------------------------------------------------------------------------

📈 Key Features

AI-Powered Extraction: Uses Pydantic schemas to ensure the scraper returns structured data like MOQ, delivery time, and technical specs.

Data Normalization: Automatically splits "City, State" strings to provide city-level analytics.

Dashboard Metrics: Visualizes total companies listed, unique products found, and city distribution.

Author: Ankit Kolte

Location: Pune, India

Education: B.Tech Student at Sushila Devi Bansal College of Engineering
