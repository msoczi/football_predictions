
import sys

LEAGUE = str(sys.argv[1])

# Read files
with open("web/index.html", "r") as f:
    index_page = f.read()

with open("output_tables/"+LEAGUE+".html", "r") as f:
    table_with_predictions = f.read()

# Split index.html
#league_split = index_page.split('<h4>Premier League</h4>', 1)
league_split = index_page.split(f'<!-- {LEAGUE} -->', 1)

# Add table in right place
new_index_html = league_split[0]+'<!-- '+LEAGUE+' -->\n'+table_with_predictions+'\n'+league_split[1]

# Overrite index.html
with open("web/index.html", "w") as output_html:
    output_html.write(new_index_html)
    
# LOG
print(f'Table {LEAGUE} has been added to the index.html file.')
