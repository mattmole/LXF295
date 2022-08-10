from lxml import etree
import requests
import matplotlib.pyplot as plt

pageLink = "https://www.mattmole.co.uk/LXF295/index.html"

#Load the HTML from the link 
page = requests.get(pageLink)
root = etree.HTML(page.content)

#Return a list of colours from the table using XPath. Note that we request data from a table with a given id in the <table id=""> tag and a given column @id.
colours = root.xpath('/html/body/table[@id = "namesAndColours"]//td[@id = "colour"]')
#Iterate through each colour in the returned results and add to the dictionary if missing.
#If it is not missing, then increment it
colourCount = {}
for colour in colours:
    if colour.text not in colourCount:
        colourCount[colour.text] = 1
    else:
        colourCount[colour.text] += 1

#Return a list of names from the table using XPath. Note that we request data from a table with a given id in the <table id=""> tag and a given column @id.
names = root.xpath('/html/body/table[@id = "namesAndColours"]//td[@id = "name"]')
#Iterate through each name in the returned results and add to the dictionary if missing.
#If it is not missing, then increment it
nameCount = {}
for name in names:
    if name.text not in nameCount:
        nameCount[name.text] = 1
    else:
        nameCount[name.text] += 1

#Print both dictionaries
print(colourCount)
print(nameCount)

#Generate a pie chart of the colours
#Labels contains the name of each colour and uses a list, when returning the keys from the dictionary
labels = colourCount.keys()
#The values from the dictionary represents the count of each colour
sizes = colourCount.values()

#Create the pie chart and add the values and labels
fig1, ax1 = plt.subplots()
ax1.pie(sizes, labels=labels, autopct='%1.1f%%', colors=labels)
ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

#Save and display the plot on the screen
plt.savefig('pieChart.png')
plt.show()
