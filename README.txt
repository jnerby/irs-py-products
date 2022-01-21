INSTRUCTIONS 
Run "pip3 install -r requirements.txt" from the command line.
Then run "python3 -i functions.py" from the command line to run Python interactively.

1) To view summary data about a list of forms, run "print(search_by_form_titles([forms]))," passing in a list of form names as a parameter. The function search_by_form_titles returns a JSON object. To view the JSON output easily in your terminal, you can print the returned JSON object. For example, the command
"print(search_by_form_titles(['Form W-2', 'Publ 225']))" returns "[{"form_number": "Form W-2", "form_title": "Wage and Tax Statement (Info Copy Only)", "min_year": 1954, "max_year": 2022},
{"form_number": "Publ 225", "form_title": "Farmer's Tax Guide", "min_year": 1994, "max_year": 2021}]." 
 
2) To download forms from irs.gov, run "python3 -i functions.py," then "download_forms(form, years)". For example, the command "download_forms("Form W-2", "1990-1995")" downloads six forms as PDFs to the downloads folder.
 
3) Run "python3 test_helpers.py" in your terminal to run three unit tests.


NOTES
I used Python 3.8.9 and Beautiful Soup for to complete this task.

Given more time, I would implement more error handling and testing. I would add more detailed value errors or exceptions for invalid entries or entries that return no results. I would also refactor this code to run from the command line using argparse, instead of running Python interactively.

The function in part 1 assumes that there are no more than 30,000 files on the IRS's PY Products page. At the time of submission, there were 20,805 files on the website. Given more time, I would try to optimize the runtime for web scraping.