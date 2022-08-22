
# Read files
with open("web/init_index.html", "r") as f:
    index_page = f.read()

# Overrite index.html
with open("web/index.html", "w") as output_html:
    output_html.write(index_page)
    
# LOG
print('File index.html cleaned.')
