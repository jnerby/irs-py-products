import requests
import json
import os
from bs4 import BeautifulSoup

def get_form_num(prod):
    """Returns form number"""
    # Get anchor
    child = prod.find('a')
    # Encode anchor to get form_name as bytes
    form_bytes = child.encode_contents()
    # Convert form_bytes to string
    form_num = form_bytes.decode('utf-8')

    return form_num


def get_title(prod):
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


def get_products(url):
    """Returns form product names from search results"""
    res = requests.get(url)
    # Get products if status is OK
    if res.status_code == 200:
        # Parse html to get soup
        soup = BeautifulSoup(res.content, "html.parser")
        # Get all table data based in leftmost column
        prod_nums = soup.find_all("td", class_="LeftCellSpacer")

        return prod_nums


def get_year(prod):
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


def search_by_form_titles(forms):
    """Returns JSON object w/ form number, title, min and max year for forms in list"""
    # Initialize empty list to return with results from all forms
    result = []
    # Loop over form titles passed in
    for form in forms:
        # Initialize empty dict for each form's results, vars for form name and title upon match
        form_dict = {}
        num = ''
        title = ''

        # Initialize empty set for form_years. Get min and max for dict
        form_years = set()
        # Set index of first row to 0 to loop through all result pages
        first_row = 0

        # While loop to scrape all result pages (at least first 1000 results)
        while True:
            # Break after querying first 1000 rows
            if first_row > 1000:
                break

            # Generate dynamic URL to search for each form name and call get_products
            url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow='+str(first_row)+'&sortColumn=sortOrder&value='+form+'&criteria=formNumber&resultsPerPage=200&isDescending=false'           
            prods = get_products(url)

            # Loop through products
            for prod in prods:
                form_num = get_form_num(prod)
                # Check form name matches passed in term exactly
                if form_num == form:
                    # Update form number value for result dict
                    num = form_num    

                    # Update form title value for result dict
                    title = get_title(prod)
                    
                    # Add form year to form_years set
                    year = get_year(prod)
                    form_years.add(year)

            # Increment first row to search next 200 results
            first_row += 200

        # Generate dict for each form
        form_dict = {
            'form_number': num, 
            'form_title': title.strip(),
            'min_year': min(form_years),
            'max_year': max(form_years)
            }

        # Append each form dict to result list
        result.append(form_dict)

    # Return result as JSON object
    return json.dumps(result)

def download_forms(form, years):
# def download_forms(form, years):
    """Downloads and saves forms to a downloads folder in current working dir"""
    path = os.getcwd()+'/downloads'

    # Initialize first row to 0
    first_row = 0

    while True:
        if first_row > 1000:
            break

        url = 'https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow='+str(first_row)+'&sortColumn=sortOrder&value='+form+'&criteria=formNumber&resultsPerPage=200&isDescending=false'

        # Get URL search result products
        prods = get_products(url)

        # Loop through search result products
        for prod in prods:
            form_num = get_form_num(prod)

            # Check form name matches passed in term exactly
            if form_num == form:
                year = get_year(prod)
                if year in years:
                    # Get file link
                    file_url = prod.find('a').get('href')
                    # Generate file name
                    file_name = os.path.join(path, f"{form_num} - {year}")
                    # Get response for form's url
                    file_res = requests.get(file_url)
                    
                    # Open empty PDF file
                    pdf = open(f"{file_name}.pdf", 'wb')
                    # Write PDF contents to empty PDF
                    pdf.write((file_res).content)
                    pdf.close()

        # Increment first_row to search next 200 results
        first_row += 200