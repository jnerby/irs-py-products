This project uses Python 3.8.9 and Beautiful Soup to scrape data from irs.gov's Prior Year Products page.
https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=&criteria=&resultsPerPage=25&isDescending=false

Run "pip3 install -r requirements.txt" from the command line.
Then run "python3 -i functions.py" from the command line to run Python interactively.

1) To view summary data about a list of forms, run "print(search_by_form_titles([forms]))." For example, the command 
"print(search_by_form_titles(['Form W-2', 'Publ 225']))" returns "[{"form_number": "Form W-2", "form_title": "Wage and Tax Statement (Info Copy Only)", "min_year": 1954, "max_year": 2022}, 
{"form_number": "Publ 225", "form_title": "Farmer's Tax Guide", "min_year": 1994, "max_year": 2021}]."

This function assumes that there are no more than 30,000 files on the IRS's PY Products page. At the time of submission, there were 20,805 files on the website. Given more time, I would try to optimize the runtime for webscraping. 

2) To download forms from irs.gov, run "download_forms(form, years)." For example, the command "download_forms("Form W-2", "1990-1995")" downloads four forms as PDFs to the downloads folder.

3) Run "python3 test_functions.py" in your terminal to run unit tests.

Given more time, I would implement more error handling and testing. I would add more detailed value errors or exceptions for invalid entries or entries that return no results. I would also potentially refactor this code to run from the command line, instead of running Python interactively.