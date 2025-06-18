## functions for scraping data from www.basketball-reference.com
## goal: pull html tables for advanced team offense stats or other stats
## using requests library for http requests
## using BeautifulSoup to scrape html tables
## Using lxml parser
from types import NoneType

## table is exported to a pandas data frame
## pandas has a read html function but i wanted to write my own as an exercise

# dependencies
import pandas
import lxml
from bs4 import BeautifulSoup
import requests
import re

# code for scraping html tables from basketball-reference.com
# bref uses html tables
# note bref_url_25 is for 2024-2025 season

#bref link
bref_url_25 = 'https://www.basketball-reference.com/leagues/NBA_2025.html'



######## helper functions

def get_html_req(bref_url):
     """
     Takes the given url and uses the requests library to extract
     the site as an html tree. Returns the site in html doc form.

     Note: URL must be an absolute path (i.e. begin with 'http://'
     or 'https://'

     :param bref_url: url to https://www.basketball-reference.com
     :return: html text tree from website
     """

     # using try/except to handle generic request errors
     # inner if/else handles 404 error

     try:
          response = requests.get(bref_url)
          html_data = response.text
          if response.status_code == 200:
               return html_data            # return successful response content as text
          elif response.status_code == 404:
               raise Exception(f'{response.status_code} error: Page not found')

     except requests.exceptions.RequestException:
          raise Exception('An error occurred with your request.')






def get_html_tree(html_obj):
     """

     :param html_obj: an html doc from html_req()
     :return: a BeautifulSoup object representing an html tree
     """

     soup = BeautifulSoup(html_obj, 'lxml')
     return soup

def bref_html(bref_url):
     """
     Takes a link to basketball-reference.com and returns a parsed
     BeautifulSoup html webpage object to be used for scraping.

     This function is a wrapper for get_html_req() and get_html_tree().

     :param bref_url:
     :return: BeautifulSoup object corresponding to an html webpage
     """

     # make and request and parse html tree
     html_data = get_html_req(bref_url)
     html_tree = get_html_tree(html_data)

     return html_tree

def scrapeTables(bref_url):
     """
     Converts url into a BeautifulSoup html tree and return a results set
     of html tables within the tree.

     This is a wrapper for bref_html

     :param bref_url: link to a basketball-reference.com url
     :return: a BeautifulSoup results set containing all tables within the url
     """

     # get html tree for website
     html_tree = bref_html(bref_url)

     # get table(s) on html page and return a message if no table is found
     try:
         bref_tables = html_tree.find_all(name = "table")   # check for multiple tables
     except:
          try:
               bref_tables = html_tree.find(name = "table") # check for single table
          except:
               raise ValueError('No html tables found on page.')

     return bref_tables



def getTableHeaders(bref_thead):
     """
     Takes html strings enclosed in thead tags (e.g. <thead>...</thead>) and
     finds header names for html table. Note that this code is formed using the html
     structure from certain tables on basketball-reference and will not work
     on other sites

     Note: If there are multiple header rows, the header row closest to the table
     data (e.g. highest index) is taken as the header row.

     Returns a list of strings that can be set as column names for a table

     :param bref_thead: a BeautifulSoup object created with thead tags
     :return: list of strings to serve as column headers
     """

     # get header rows and choose last row
     # this is based on the html structure of the site in question
     header_rows = bref_thead.find_all(name = "tr")
     header_row = header_rows[-1]

     # get headers
     header_row = header_row.find_all(name = "th")
     headers = [header.text for header in header_row]

     return headers


def tbody2df(bref_tbody):
     """
     Takes html strings enclosed in tbody tags (e.g. <tbody>...</tbody>) and
     constructs a data frame. Note that this code is formed using the html
     structure from certain tables on basketball-reference and will not work
     on other sites

     Returns a data frame-- with no columns names

     :param bref_tbody: a BeautifulSoup object created with tbody tags
     :return: html table as a pandas data frame w/o column names
     """

     # get table rows
     df_rows = []  # list of lists. each sublist corresponds to a df row
     table_row_list = bref_tbody.find_all(name ="tr")
     for row in table_row_list:
          row_cells = row.find_all(name = ["th","td"])   # get header or cell tags in row
          cell_data = [cell.text for cell in row_cells]  # create list of text in row
          df_rows.append(cell_data)

     temp_df = pandas.DataFrame(df_rows)
     return temp_df


def table2df(bref_table):
     """
     Takes a BeautifulSoup html object from Basketball-Reference.com corresponding to
     a *single* html table and scrapes the object to create a pandas data frame from
     the table. Uses headers within the html tree to name columns. The table should be
     enclosed in a single set of <table>...</table> tags.

     Note that this code is formed using the html table structure from certain tables on
     basketball-reference and may not work on other sites.


     :param bref_soup: a BeautifulSoup html object
     :return: a pandas data frame
     """
     # TODO: Add error handling for tables lacking <th> </th> head tags

     # get thead and tbody tags. use find() not find_all since this is assumed to be a single table
     bref_thead = bref_table.find(name="thead")   # thead tags give col header names
     bref_tbody = bref_table.find(name="tbody")

     # get column names and data frame
     df_cols = getTableHeaders(bref_thead)
     bref_df = tbody2df(bref_tbody)
     bref_df.columns = df_cols

     return bref_df

##### END HELPERS

####################################
####################################

##### MAIN FUNCTIONS

def getTables(bref_url):
     """
     Takes a url to basketball-reference.com and constructs a pandas
     dataframe for each html table.

     This function is a wrapper for various helper functions in this module.

     Note 1: URL must be an absolute path (i.e. begin with 'http://'
     or 'https://'

     Note 2: Many tables on basketball-referenc are not actually html tables.
     This function will not find them.

     :param bref_url: absolute url path to https://www.basketball-reference.com
     :return: list containing data frames made from html tables on website
     """

     # scrape html tables from url
     bref_tables = scrapeTables(bref_url)

     # create list of data frames from html tables
     df_list = []
     for table in bref_tables:
          df_list.append(table2df(table))

     return df_list

def findHeader(string, df_list):
     """
     Checks list of data frames to determine whether the table
     headers contain a particular string. Returns a list of data
     frames whose column headers contain a *partial* match to the
     desired string. Note, that the string is *NOT* case-sensitive.

     :param string: search string
     :param df_list: list of pandas data frames to check
     :return: list of data frames
     """

     # convert string to lower case
     string_lower = string.lower()

     # list to hold target data frames
     target_df_list = []

     # iterate over list of dfs and check headers
     for index,df in enumerate(df_list):

          # make column headers lowercase and check for string
          # add df to list if string is a partial match in any column header
          temp_col = df.columns[:]
          col_hd_low = [header.lower() for header in temp_col]
          if string_lower in col_hd_low:
               target_df_list.append(df_list[index])

     if len(target_df_list) == 0:
          raise ValueError('No data frame found')
     else:
          return target_df_list


def findTables(bref_url, header_search = []):
     """
     Given a URL from basketball-reference.com and an (optional)
     set of headers to search for, returns the corresponding
     html tables as pandas data frames

     Returns all tables if header_search list is empty

     Note: URL must be an absolute path (i.e. begin with 'http://'
     or 'https://'

     :param bref_url: website url
     :param header_search: list indicating desired column header in data frame
     :return: collection of data frames containing desired tables
     """

     # TODO: Implement function that wraps getTables() and findHeader()

     # pseudocode

     # if header_search list is empty
          # return getTables() (i.e. return all tables)

     # else
          # call getTables()
          # iterate over header_search list
               # call findHeader() for each element

     # decide how to return desired data frames
     # list?
     # dict mapping search string to list of data frames?

     pass


#################################
# not using the get_tbody_headers() function below as we can scrape tags directly using <thead> and <th> tags
# additionally the function has some bugs; however, writing it was useful for helping me learn
# to scrape tag attributes specifically the 'data-stat' tag contains information equivalent to
# some header names

# Note: must use regular expressions to search for attributes. attributes cannot be
# searched using strings (unlike the 'name' parameter). Some information may only be available
# via tag attributes


def get_tbody_headers(bref_tbody):
     """
     Pulls header names for columns from the attribute 'data-stat' in
     bref tables. Function will not work if "data-stat" attribute does
     not exist

     :param bref_tbody: a BeautifulSoup object created with tbody tags
     :return: list containing headers names
     """

     # Get data-stat attribute in all tbody tags to find headers
     table_header_list = bref_tbody.find_all(attrs={"data-stat": re.compile('^[a-zA-Z]')})

     # get unique headers
     headers = []
     # note these are not the exact table headers. the tag attribute is slightly different from the column name
     # dummy headers exist for blank columns. these can repeat but other headers should be unique
     for tag in table_header_list:
          header = tag['data-stat']
          if header not in headers or header == 'DUMMY':
               headers.append(header)
          elif header in headers:
               break

     return headers

# test_headers10 = get_tbody_headers(bref_tbody[10])
# print('testing headers table 10:',test_headers10)


# checking if a table has the offensive rating tag attribute "off_rtg"


######################### testing code

# get html data from url
# bref_data = requests.get(bref_url_25).text





# create parsing object
# bref_soup = BeautifulSoup(bref_data,'lxml')

# parsing using beautiful soup
# bref_table = bref_soup.find_all(name = "table")
# bref_thead = bref_soup.find_all(name = "thead")
# bref_tbody = bref_soup.find_all(name = "tbody")
# print('num tables:',len(bref_tbody))
# print('num thead:',len(bref_tbody))
# print('num tbody:',len(bref_tbody))

# parsing table 11

# print(bref_tbody[10])
#print(bref_tables[0])

# make tags with header names
# data-stat attribute contains a string corresponding to column header
# extract using a regular expression
# print(bref_tbody[10].find_all(attrs={"data-stat":re.compile('^[a-zA-Z]')})[0]['data-stat'])
# table_10_header_list = bref_tbody[10].find_all(attrs={"data-stat":re.compile('^[a-zA-Z]')})


# testing2 = pandas.read_html("https://www.basketball-reference.com/teams/GSW/2025.html")
# print(len(testing2))

# response = requests.get('https://www.basketball-reference.com/teams/GSW/2025.html')
#
# soup = BeautifulSoup(response.text, 'html.parser')
# comments = soup.find_all(string=lambda text: isinstance(text, Comment))
#
# tables = []
# for each in comments:
#     if 'table' in each:
#         try:
#             tables.append(pandas.read_html(each)[0])
#         except:
#             continue
#
# print(tables[-1].loc[1:])