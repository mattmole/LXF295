from bs4 import BeautifulSoup
import os
import feedparser

feedLink = "https://latenightlinux.com/feed/mp3"

feed = feedparser.parse(feedLink)

#Iterate through each episode
count = 0
for episode in feed.entries:
    episodeName = episode.title
    episodeLink = episode.link

    page_soup = BeautifulSoup(episode.content[0].value, "html.parser")

    #Find the rows in the encoded content that referencies discoveries and feedback
    lowCount = -1
    highCount = -1
    counter = 0
    for row in page_soup:
        if row.text == 'Discoveries':
            lowCount = counter
        if row.text =='Feedback' or row.text == "KDE Korner":
            highCount = counter
        counter += 1

    #Now print discoveries, using the values from the previous loop
    counter = 0
    for row in page_soup:
        if counter < highCount and counter > lowCount and lowCount > -1:
            if row.text.strip() != '':
                discoveryLink = 'No link available'
                try:
                    discoveryLink = row.find('a')['href']
                except:
                    pass
                discoveryText = row.text
                print(discoveryText, discoveryLink)
        counter += 1