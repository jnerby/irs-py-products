I used Python 3.8.9 to complete this challenge. I used Beautiful Soup for web scraping. Run "pip3 install -r requirements.txt" from the command line. Then run "python3 server.py."

This script has four helper functions and two primary functions. search_by_form_titles() is the function for Part 1, and download_forms() is the function for part 2. The first four functions (get_form_num(), get_title(), get_products(), and get_year()) are helper functions that parse data from irs.gov.

Parameters are passed to all six functions as arguments. I used json.dumps() to return a JSON string in Part 1.

I enjoyed this challenge overall. I feel it gave me a chance to demonstrate a few different Python skills. I appreciated the clear, concise directions.