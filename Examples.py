
# Example usage of getTables() and findHeader()

import pandas
import NBA_Scraping as scrape

# scrape data from 2025 NBA Team Summary Stats page
NBA_2025_tables = scrape.getTables('https://www.basketball-reference.com/leagues/NBA_2025.html')

# filter tables found above for tables containing "ortg" as a column name
# "ortg" is offensive rating which is an advanced team statistic
NBA_2025_ORTG_tables = scrape.findHeader('Ortg', NBA_2025_tables)
print(NBA_2025_ORTG_tables[0])

# scrape data from 2025 Golden State Warriors Summary Stats page
GSW_2025_tables = scrape.getTables("https://www.basketball-reference.com/teams/GSW/2025.html")

# check number of tables
print(len(GSW_2025_tables))

#######

# Example of failed usage
# getTables() throws AttributeError: 'NoneType' object
# working on a fix
pbp_url = 'https://www.basketball-reference.com/boxscores/pbp/202506160OKC.html'
pbp_table = scrape.getTables(pbp_url)