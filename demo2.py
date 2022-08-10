from lxml import etree
import requests

pageLink = "https://www.mattmole.co.uk/LXF295/demo2.html"

#Load the HTML from the link 
page = requests.get(pageLink)
root = etree.HTML(page.content)

#Return each row from the table
tableRows = root.xpath('//tr')

#Iterate through each returned row and display the rowCount
rowCount = 1
for row in tableRows:
    rowText = 'Row '+ str(rowCount) + ':'
    #Iterate through each returned column and display the text
    for column in row:
        rowText += column.text + ','
    print(rowText)
    rowCount += 1