import json
import os
from helpers import generate_form_pdf, get_form_years_from_year_range, get_path_from_form_name, get_product_data, get_products

def download_forms(form: str, year_range: str):
    """Downloads and saves forms to a downloads folder in current working dir"""
    path = get_path_from_form_name(form)


    years = get_form_years_from_year_range(year_range)
    # Initialize first row to 0
    url_first_row = 0

    while True:
        if url_first_row > 25000:
            break
        
        # Get all products from url 
        url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow={str(url_first_row)}&sortColumn=sortOrder&value={form}&criteria=formNumber&resultsPerPage=200&isDescending=false"
        products = get_products(url)

        # Generate PDF for each product
        for product in products:
            generate_form_pdf(product, form, years)

        # Check next 10000 results
        url_first_row += 10000


def search_by_form_titles(forms):
    """Returns JSON object w/ form number, title, min and max year for forms in list"""

    # Initialize empty list to return with results from all forms
    result = []

    # Loop over form titles passed in
    for form in forms:
        # Append each form dict to result list
        result.append(get_product_data(form))

    # Return result as JSON object
    return json.dumps(result)