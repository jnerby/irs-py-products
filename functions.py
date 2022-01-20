import requests
import json
import os
# import sys
from bs4 import BeautifulSoup
from logging import raiseExceptions

def download_forms(form: str, year_range: str):
    """Downloads and saves forms to a downloads folder in current working dir"""
    path = os.getcwd()+'/downloads'

    years = get_form_years_from_year_range(year_range)
    # Initialize first row to 0
    url_first_row = 0

    while True:
        if url_first_row > 30000:
            break
        
        # Get all products from url 
        url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow={str(url_first_row)}&sortColumn=sortOrder&value={form}&criteria=formNumber&resultsPerPage=200&isDescending=false"
        products = get_products(url)

        # Generate PDF for each product
        for product in products:
            generate_form_pdf(product, form, years)

        # Check next 10000 results
        url_first_row += 10000


def get_form_years_from_year_range(year_range: str) -> list:
    """Returns list of years that fall within requested range"""
    # if no year range entered, return empty list
    if not year_range:
        return []

    # split year ranget to min and max year
    min_max_year = year_range.split("-")

    # if min year entered incorrectly, return empty list
    if len(min_max_year[0]) != 4:
        return []
    # if max year is entered, check if entered correctly
    if len(min_max_year) == 2 and len(min_max_year[1]) != 4:
        return []

    # if user only entered one year
    if len(min_max_year) == 1:
        min_year = min_max_year[0]
        years = [int(min_year)]
    # if user entered year range correctly
    elif len(min_max_year) == 2:
        min_year = int(min_max_year[0])
        max_year = int(min_max_year[1])
        years = list(range(min_year, max_year + 1))
    else:
        return []

    return years

def generate_form_pdf(product: str, form: str, years: list):
    """Generates and saves a PDF to local directory's downloads folder"""
    path = os.getcwd()+'/downloads'

    form_num = get_form_num(product)

    # Check form name matches passed in term exactly
    if form_num == form:
        year = get_year(product)
        if year in years:
            # Get file link
            file_url = product.find('a').get('href')
            # Generate file name
            file_name = os.path.join(path, f"{form_num} - {year}")
            # Get response for form's url
            file_res = requests.get(file_url)
            
            # Open empty PDF file
            pdf = open(f"{file_name}.pdf", 'wb')
            # Write PDF contents to empty PDF
            pdf.write((file_res).content)
            pdf.close()


def get_form_num(prod: str) -> str:
    """Returns form number"""
    # Get anchor
    child = prod.find('a')
    # Encode anchor to get form_name as bytes
    form_bytes = child.encode_contents()
    # Convert form_bytes to string
    form_num = form_bytes.decode('utf-8')

    return form_num


def get_products(url: str) -> list:
    """Returns form product names from search results"""
    res = requests.get(url)
    # Get products if status is OK
    if res.status_code == 200:
        # Parse html to get soup
        soup = BeautifulSoup(res.content, "html.parser")
        # Get all table data based in leftmost column
        product_numbers = soup.find_all("td", class_="LeftCellSpacer")
        return product_numbers
    else:
        raiseExceptions('Not found')


def get_title(prod: str) -> str:
    """Returns form title"""
    # Get parent row for matches
    tr = prod.parent
    # Get middle column to get form title
    title_data = tr.find('td', class_="MiddleCellSpacer")
    # Get contents of middle column
    title_bytes = title_data.encode_contents()
    # Decode to string
    form_title = title_bytes.decode('utf-8')

    return form_title

def get_product_data(form: str) -> dict:
    """Returns dictionary with a single form's num, title, min and max year"""
    # Initialize empty dict for each form's results, vars for form name and title upon match
    form_details = {}
    form_num_for_dict = ''
    form_title_for_dict = ''
    # Initialize empty set for form_years. Get min and max for dict
    all_form_years = set()
 
    products = scrape_product_data(form)

    # Loop through products
    for prod in products:
        form_num = get_form_num(prod)
        # Check form name matches passed in term exactly
        if form_num == form:
            # Update form number value for result dict
            form_num_for_dict = form_num    
            # Update form title value for result dict
            form_title_for_dict = get_title(prod)
            # Add form year to form_years set
            year = get_year(prod)
            all_form_years.add(year)
            
    # if no matches found, returns an empty dictionary
    if len(all_form_years) == 0:
        return {}

    # Generate dict for each form
    form_details = {
        'form_number': form_num_for_dict, 
        'form_title': form_title_for_dict.strip(),
        'min_year': min(all_form_years),
        'max_year': max(all_form_years)
        }
    
    return form_details

def get_year(prod: str) -> int:
    """Return form year"""
    # Get parent row for matches
    tr = prod.parent
    # Get right column to get form title
    year_data = tr.find('td', class_="EndCellSpacer")
    # Get contents of middle column
    year_bytes = year_data.encode_contents()
    # Decode to string
    form_year = year_bytes.decode('utf-8')

    return int(form_year)

def scrape_product_data(form: str) -> list:
    """Returns list of products that match form number"""
    # Set index of first row to 0 to loop through all result pages
    url_first_row = 0
    products = []
    # While loop to scrape all result pages (at least first 30,000 results)
    while True:
        if url_first_row > 30000:
            break

        # Generate dynamic URL to search for each form name and call get_products
        url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow={str(url_first_row)}&sortColumn=sortOrder&value={form}&criteria=formNumber&resultsPerPage=200&isDescending=false"           
        products.extend(get_products(url))

        # Increment first row to search next 10,000 results
        url_first_row += 10000

    return products

def search_by_form_titles(forms: list) -> json:
    """Returns JSON object w/ form number, title, min and max year for forms in list"""
    # Initialize empty list to return with results from all forms
    result = []

    # Loop over form titles passed in
    for form in forms:
        # Append each form dict to result list
        result.append(get_product_data(form))

    # Return result as JSON object
    return json.dumps(result)