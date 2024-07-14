from flask import Flask, render_template, request
from .app import app, db
from .database.models import Property
from .utils import clean_data
import requests
from bs4 import BeautifulSoup

def fetch_properties(roll_no):
    url = f'https://valuation2017.durban.gov.za/FramePages/SearchResult.aspx?Roll={roll_no}&VolumeNo=01&RateNumber=&StreetNo=&StreetName=&Suburb=&ERF=&Portion=&DeedsTown=&SchemeName=&SectionNumber=&All=false'
    response = requests.get(url, verify=False)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    table = soup.find('table', class_='searchResultTable')
    properties = []
    
    if table:
        rows = table.find_all('tr')[3:]  # Skip the first three rows (header rows)
        for row in rows:
            cols = row.find_all('td')
            if len(cols) >= 8:
                rate_number = clean_data(cols[0].get_text())
                legal_description = clean_data(cols[1].get_text())
                address = clean_data(cols[2].get_text())
                first_owner = clean_data(cols[3].get_text())
                use_code = clean_data(cols[4].get_text())
                rating_category = clean_data(cols[5].get_text())
                market_value = float(clean_data(cols[6].get_text().replace(',', '').replace('R', '')))
                registered_extent = clean_data(cols[7].get_text())

                property_data = Property(
                    rate_number=rate_number,
                    legal_description=legal_description,
                    address=address,
                    first_owner=first_owner,
                    use_code=use_code,
                    rating_category=rating_category,
                    market_value=market_value,
                    registered_extent=registered_extent,
                    roll=roll_no
                )
                properties.append(property_data)
            else:
                print(f"Ignoring row due to insufficient columns: {cols}")
    
    return properties

def save_properties_to_db(properties):
    for property_data in properties:
        db.session.add(property_data)
    db.session.commit()

@app.route('/get_full_title_property', methods=['POST'])
def get_full_title_property():
    properties = fetch_properties(roll_no='1')
    save_properties_to_db(properties)
    return "Full Title Properties have been fetched and stored."

@app.route('/get_sectional_title_property', methods=['POST'])
def get_sectional_title_property():
    properties = fetch_properties(roll_no='2')
    save_properties_to_db(properties)
    return "Sectional Title Properties have been fetched and stored."
