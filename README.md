# NBA-Scraping

## Description

While pandas has the **read_html()** function for reading html tables, I wanted to create my own method as a programming exercise. The function **getTables()** returns the html tables on a basketball-reference web page. There is one known bug, but please let me know if you find others :) .

## Functionality

Currently the repo contains a function for scraping html tables from https://www.basketball-reference.com. The html tables on a website are returned as pandas data frames. Functionality was originally written with [Season Summary Stats](https://www.basketball-reference.com/leagues/NBA_2025.html) page layout in mind. As such it does not yet work correctly on all pages, but fixes are in progress.

## Examples
See *Examples.py*


## Functions

The file NBA_Scraping.py contains *many* functions. Only the **primary functions** noted below are intended for use. Brief explanations are included, but consult the full documentation for details.

*Note: Many of the tables on basketball reference are not actually html tables.*

### Primary Functions
- **getTables(url)**
  -  returns a list of data frames corresponding to *all* html tables on a basketball-reference web page
  -  url must have an absolute path beginning with 'https://' or 'http://'
- **findHeader(string, df_list)**
  - looks for data frames with specific column names
  - returns data frames with column names containing a partial match to a string
- **findTables(url)**
  - wrapper for getTables() and findHeader()
  - will permit searching for particular tables with a single function call
  - **not yet implemented. currently only has pseudo code**

### Helper Functions
- The functions are not listed in this README. However NBA_Scraping.py has a section labeled "HELPER FUNCTIONS".



## Known issues
- Errors
  - Tables without \<th> \</th> head tags throw an AttributeError: NoneType. Fix in progress
 
  


## Future Updates

Other plans for this project:

- Database
  - add functionality to write html tables/data frames to SQLite database (local storage)
  - via Python sqlite3 library
- Data cleaning
  - adding the year to the data frame/database
  - adding whether a team made the playoffs
  - adding player awards(all star, mvp, etc.)
- Statistical Analysis
  - analyze 3pt trends in the NBA
  - possibly some predictive analyses...
   


