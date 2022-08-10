from lxml import etree
import requests

pageLink = "https://www.mattmole.co.uk/LXF295/demo1.html"

#Load the HTML from the link 
page = requests.get(pageLink)
root = etree.HTML(page.content)

#Print the title in the terminal
print('Title: '+root.xpath('/html/head/title')[0].text)

#Perform a second XPath operation to return each paragraph of text and print it to the screen
for para in root.xpath('/html/body/p'):
    print('Para Text: '+para.text)
