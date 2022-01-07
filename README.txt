This project uses Python 3.8.9 and Beautiful Soup to scrape data from irs.gov's Prior Year Products page.
https://apps.irs.gov/app/picklist/list/priorFormPublication.html?indexOfFirstRow=0&sortColumn=sortOrder&value=&criteria=&resultsPerPage=25&isDescending=false

Run "pip3 install -r requirements.txt" from the command line.
Then run "python3 -i function.py" from the command line to run Python interactively.

1) To view summary data about a list of forms, run "print(search_by_form_titles([forms]))." For example, the command 
"print(search_by_form_titles(['Form W-2', 'Publ 225']))" returns "[{"form_number": "Form W-2", "form_title": "Wage and Tax Statement (Info Copy Only)", "min_year": 1954, "max_year": 2022}, 
{"form_number": "Publ 225", "form_title": "Farmer's Tax Guide", "min_year": 1994, "max_year": 2021}]."

2) To download forms from irs.gov, run "download_forms(form, years)." For example, the command "download_forms("Form W-2", [1990, 1995, 2000, 2005])" downloads four forms as PDFs to the downloads folder.

### put everything in single helper method to search by single form title, return union of all forms *****
### separate downloading of HTML from searching for forms. always looking at all of HTML, so makes sense to sep downloading from scanning
### faster than loading HTML for each form. can detect when done loading HTML, won't have to worry about finding min year from empty search res


### loop that fetches data from external system likely to have errors. put in sep function and test it
### make num of search results per page a variable and adjust it. try 1000, reduce # of HTTP calls to make
### write tests - would be very good to show unittests. use pytest
    ## write unittest for everything but HTTP request part
### make multiple HTTP calls - check out string io - important for performance with big strings
    ## can also keep appending res to list and join at end
    ### use longer, more descriptive variable names, no upside to short var names
### unittests - think about diff ways code could break, diff error conditions


#### try making results per page bigger. maybe so many forms that not running infin but just long runtime