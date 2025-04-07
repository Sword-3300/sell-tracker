# Store Sales Analysis
## Overview
This project analyzes store sales data, calculates the total revenue of all sold products within a given period, and generates a structured JSON database containing the sales analysis. The goal is to provide insights into sales trends by aggregating data and performing basic analysis, such as total sales, category-based performance, and product-level insights.

## How to Use
- Input sales data in the format:
`NAME:PRICE_PER_UNIT:QUANTITY:CATEGORY`  
Example: `Apples:5:20:Fruits`  
- The script will analyze the provided data and generate summary tables.  
- A JSON file containing all the analyzed sales information will be created for future reference.

## Functionality
- Sales Data Analysis:
   Lists all products.
   Calculates the overall price of all sold products.
   Determines the average price of sold products.
- Category-Based Division:
   Groups products by category.
   Lists all products in each category.
   Calculates the overall price for each category.
   Determines the average price of sold products within each category.
- JSON Report Generation: Saves the analysis in a structured JSON file for further processing.
- Product-Level Insights: Provides details on each product’s contribution to total sales.

## Installation
1. Clone the repository(powershell)  
`git clone https://github.com/Sword-3300/sell-tracker.git`
2. Install the requirements (python console)  
`pip install -r requirements.txt`
3. Go to the script directory (cmd or powershell [recommended])  
`cd [script directory]`
4. Run `main.py` (cmd or powershell [recommended])  
`python main.py`
