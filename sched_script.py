import requests
from bs4 import BeautifulSoup
import facebook
import random
import os
import tweepy
import instabot
from py3pin.Pinterest import Pinterest
from datetime import datetime



quotes_url= 'https://www.limeville.com/category/all-quotes/page/'+str(random.choice(list(range(1,26))))
shayari_url='https://www.limeville.com/category/all-shayari/page/'+str(random.choice(list(range(1,20))))
status_url='https://www.limeville.com/category/all-status/page/'+str(random.choice(list(range(1,12))))

scrap_url=random.choice([quotes_url,shayari_url,status_url])


scrap_page=requests.get(scrap_url)
soup=BeautifulSoup(scrap_page.text,"html.parser")
post_url=[]
for post in soup.find_all('article', class_='post'):

        post_url.append(post.find('h2', class_='entry-title').a["href"])
current_post_url=random.choice(post_url)






url=requests.get(current_post_url)
soup=BeautifulSoup(url.text,"html.parser")
post = soup.find('article', class_='post')
content = post.find('div', class_='entry-content').p.text.strip()
thumb = post.find('div', class_='entry-thumbnail').img['data-src']
tags=post.find_all('span',class_='tags-links')
tag_list=[]
for tag in tags:
    links = tag.find_all('a')
    for link in links:
        tag_list.append(link.text.strip())

c=""
for item in tag_list:
	
	c=c+" "+"#"+str(item)

    
entry_footer=soup.find('footer', class_='entry-footer')
title = entry_footer.find('a').text.strip()
hashtitle="#"+title.replace(' ','')
img=requests.get(thumb, stream=True).raw

day_name=datetime.today().strftime('%A')
key=["Morning","Vibes","Motivation","Thoughts","Quotes"]
todays_tags=" ".join(map(lambda x:'#'+day_name+x,key))

msg=content+" "+c+' '+todays_tags+' '+hashtitle+" via limeville.com"



# # Facebook




group_id="1542934925806610"
token="EAAcopOZB7ZBfABACJIRXrZABuv0dR6wDkZCAZCZAeI735JusvzcG104lFuSUUhHl3WIZBalZBVSZCzruOZAUZAcRq2XuOWrSq3TGq6JZAir9S5s2quqpoHkQQXL6LXz3xJDtgiNELCZA2VepFLZBAtM9dpZBugb5jDWYoYSGUi25ZCUMiFxgqwZDZD"
fb = facebook.GraphAPI(access_token=token)
fb.put_photo(image=img, message=msg, album_path=group_id + "/photos")


# # Tweeter




auth = tweepy.OAuthHandler("12NntjNIwVli7TquB6WGD5INY","988PZtGOPtHTmLy0ovs7mjignQHS64GarTuNDf0nbxGZDWcTF6")
auth.set_access_token("917145573173501952-qZrA6jHJYa4brygKLpqkBHilA0K7JYM","atCbiy5PbfgyS8AHclcHpzaSIz2h1ipauxjR7kQmoUInh")
api = tweepy.API(auth)

temp = 'temp.jpg'
request = requests.get(thumb, stream=True)

with open(temp, 'wb') as image:
    for chunk in request:
        image.write(chunk)

api.update_with_media(temp, status=msg)
os.remove(temp)


# # Instagram



bot = instabot.Bot()   
bot.login(username = "limevilleofficial", password = "Ic_ndoit2") 
temp = 'temp.jpg'
request = requests.get(thumb, stream=True)

with open(temp, 'wb') as image:
    for chunk in request:
        image.write(chunk)
bot.upload_photo(temp, caption =msg) 
os.remove(temp+".REMOVE_ME")


# # Pinterest



pinterest = Pinterest(email='info@limeville.com', 
			password='Ic_ndoit2', 
			username='limevilleofficial', 
			cred_root='cred_dir')

pinterest.login()
pinterest.pin(board_id="802203821065010593", 
			image_url=thumb, 
			description=msg,
            title=title,
			link=current_post_url)
            
