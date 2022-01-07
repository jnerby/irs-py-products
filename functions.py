import requests
import json
import os
import sys
from bs4 import BeautifulSoup
from logging import raiseExceptions

def download_forms(form, years):
# def download_forms(form, years):
    """Downloads and saves forms to a downloads folder in current working dir"""
    path = os.getcwd()+'/downloads'

    # Initialize first row to 0
    url_first_row = 0

    while True:
        if url_first_row > 1000:
            break
        
        # Get all products from url 
        url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow={str(url_first_row)}&sortColumn=sortOrder&value={form}&criteria=formNumber&resultsPerPage=200&isDescending=false"
        products = get_products(url)

        # Generate PDF for each product
        for product in products:
            generate_form_pdf(product, form, years)

        # Check next 200 results
        url_first_row += 200


def generate_form_pdf(product, form, years):
    path = os.getcwd()+'/downloads'

    form_num = get_form_num(product)

    # Check form name matches passed in term exactly
    if form_num == form:
        year = get_year(product)
        if year in years:
            # generate_pdf(product, form_num, year)
            # # Get file link
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

    ##### get_products not explicitly handling case for 200, raise exception if get_products does anything weird
        #### consider writing test
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

def get_product_data(form):
    # Initialize empty dict for each form's results, vars for form name and title upon match
    form_details = {}
    form_num_for_dict = ''
    form_title_for_dict = ''
    # Initialize empty set for form_years. Get min and max for dict
    all_form_years = set()

    # Set index of first row to 0 to loop through all result pages
    url_first_row = 0
    # While loop to scrape all result pages (at least first 1000 results)
    while True:
        #### try making results per page bigger. maybe so many forms that not running infin but just long runtime
        if url_first_row > 1000:
            break

        # Generate dynamic URL to search for each form name and call get_products
        url = f"https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow={str(url_first_row)}&sortColumn=sortOrder&value={form}&criteria=formNumber&resultsPerPage=200&isDescending=false"           
        prods = get_products(url)
        
        # Loop through products
        for prod in prods:
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

        # Increment first row to search next 200 results
        url_first_row += 200

    # Generate dict for each form
    form_details = {
        'form_number': form_num_for_dict, 
        'form_title': form_title_for_dict.strip(),
        'min_year': min(all_form_years),
        'max_year': max(all_form_years)
        }
    
    return form_details

def search_by_form_titles(forms: list) -> json:
    """Returns JSON object w/ form number, title, min and max year for forms in list
    """
    # Initialize empty list to return with results from all forms
    result = []

    # Loop over form titles passed in
    for form in forms:
        # Append each form dict to result list
        result.append(get_product_data(form))

    # Return result as JSON object
    return json.dumps(result)




