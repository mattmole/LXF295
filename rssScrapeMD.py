import datetime
from bs4 import BeautifulSoup
import os
import feedparser

feedLink = "https://latenightlinux.com/feed/mp3"
basePath = '.'
showSlug = 'LateNightLinux'


feed = feedparser.parse(feedLink)
episodeAndLinks = {}
episodes = []

#Iterate through each episode
count = 0
for episode in feed.entries:
    discoLinkList = []
    episodeName = episode.title
    episodeLink = episode.link
    episodePublished = datetime.datetime.strptime(episode.published, "%a, %d %b %Y %H:%M:%S +0000")
    episodePublishedString = datetime.datetime.strptime(episode.published, "%a, %d %b %Y %H:%M:%S +0000").strftime("%d/%m/%Y")

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
                discoLink = {'text': discoveryText, 'link':discoveryLink}
                #print(discoLink)
                discoLinkList.append(discoLink)
        counter += 1
    if len(discoLinkList) > 0:
        episodes.append({'episodeName': episodeName, 'episodeLink': episodeLink, 'episodePublished':episodePublished,'episodePublishedString':episodePublishedString, 'discoLinkList':discoLinkList})


### pip install feedparser

#Now, write some files into a directory structure, detailing the links inside

if not(os.path.isdir(os.path.join(basePath,showSlug))):
    os.mkdir(os.path.join(basePath,showSlug))

for episode in episodes:
    #Create a folder for each year within the feed
    if not(os.path.isdir(os.path.join(basePath,showSlug,str(episode['episodePublished'].year)))):
        os.mkdir(os.path.join(basePath,showSlug,str(episode['episodePublished'].year)))
    #Create a file for each episode
    fw = open(os.path.join(basePath,showSlug,str(episode['episodePublished'].year),episode['episodeName']),'w')

    fw.write("# " + episode['episodeName']+os.linesep)
    fw.write("["+episode['episodeLink'] +"](" + episode['episodeLink']+")  "+os.linesep)
    fw.write(episode['episodePublishedString']+os.linesep)
    fw.write("## Discoveries"+os.linesep)
    print(episode['episodeName'], episode['episodeLink'], episode['episodePublished'])
    for disco in episode['discoLinkList']:
        print('\t',disco['text'],disco['link'])
        fw.write("* [" + disco['text']+'](' + disco['link']+')'+os.linesep)
    fw.close()
### dict_keys(['title', 'title_detail', 'links', 'link', 'published', 'published_parsed', 'id', 'guidislink', 'comments', 'wfw_commentrss', 'slash_comments', 'tags', 'summary', 'summary_detail', 'content', 'subtitle', 'subtitle_detail', 'authors', 'author', 'author_detail', 'image', 'itunes_duration'])