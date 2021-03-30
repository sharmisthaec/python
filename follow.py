from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep, strftime
from random import randint,choice
import pandas as pd
from selenium.webdriver.chrome.options import Options
import tweepy

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")


webdriver = webdriver.Chrome(options=chrome_options,executable_path='/usr/local/bin/chromedriver')
sleep(3)
webdriver.get('https://www.instagram.com/accounts/login/?source=auth_switcher')
sleep(5)


username = webdriver.find_element_by_name('username')
username.send_keys('limevilleofficial')
password = webdriver.find_element_by_name('password')
password.send_keys('Ic_ndoit2')

button_login = webdriver.find_element_by_class_name("L3NKy")
button_login.click()
sleep(5)



hashtag_list = ['quotesdaily', 'quotes', 'motivationalquotes', 'quotestoliveby','lovequotes','love',]
hashtag=choice(hashtag_list)
data= pd.read_csv('insta.csv')
prev_user_list = list(data['0'])
new_followed = []
username=[]

webdriver.get('https://www.instagram.com/explore/tags/'+ hashtag + '/')
sleep(5)
first_thumbnail = webdriver.find_element_by_xpath('//*[@id="react-root"]/section/main/article/div[1]/div/div/div[1]/div[1]/a/div')
first_thumbnail.click()
sleep(randint(3,4))
likes_button = webdriver.find_element_by_xpath('//*[@class="Nm9Fw"]/button')
likes_button.click()
sleep(randint(5,6))


scr1 = webdriver.find_element_by_xpath('//*[@class="_1XyCr"]/div[2]/div')
for i in range(2):
        
        
        webdriver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", scr1)
        sleep(randint(4,5))
        
        for i in range(10):
            username.append(webdriver.find_elements_by_class_name('MBL3Z')[i].text)
            
        sleep(randint(6,7))
        



for user in username:
    if user in prev_user_list:
        username.remove(user)



sleep(randint(3,4))
num=randint(len(username)-10,len(username))
for i in range(num):
    webdriver.get('https://www.instagram.com/'+ username[i] + '/')
    sleep(randint(4,7))
    try:
    
        follow_button = webdriver.find_element_by_xpath('//*[@class="nZSzR"]/div/div/span/span/button')
    
    except:
    
        follow_button = webdriver.find_element_by_xpath('//*[@class="nZSzR"]/div/button')
    follow_button.click()
    sleep(randint(4,8))
    new_followed.append(username[i])
    
for i in range(len(new_followed)):
    prev_user_list.append(new_followed[i])
    
updated_user_df = pd.DataFrame(prev_user_list)
updated_user_df.to_csv('insta.csv')

data= pd.read_csv('insta.csv')




auth = tweepy.OAuthHandler("12NntjNIwVli7TquB6WGD5INY","988PZtGOPtHTmLy0ovs7mjignQHS64GarTuNDf0nbxGZDWcTF6")
auth.set_access_token("917145573173501952-qZrA6jHJYa4brygKLpqkBHilA0K7JYM","atCbiy5PbfgyS8AHclcHpzaSIz2h1ipauxjR7kQmoUInh")
api = tweepy.API(auth)

data_t= pd.read_csv('twitter.csv')
prev_t_user_list = list(data_t['0'])


from datetime import datetime
day_name=datetime.today().strftime('%A')
key=["Morning","Vibes","Motivation","Thoughts","Quotes"]
select_key=choice(key)
select_tag='#'+day_name+select_key



t_user=[]
for tweet in tweepy.Cursor(api.search, q=select_tag).items(20):
    t_user.append(tweet.user.screen_name)
userlist=list(set(t_user))    


for user in userlist:
    if user in prev_t_user_list:
        userlist.remove(user)



num_t=randint(len(userlist)-10,len(userlist))
new_followed_t=[]
sleep(randint(5,6))
for i in range(num_t):
    res=api.create_friendship(userlist[i])
    sleep(randint(4,8))
    new_followed_t.append(userlist[i])
    
for i in range(num_t):
    prev_t_user_list.append(new_followed_t[i])
    
updated_user_df_t = pd.DataFrame(prev_t_user_list)
updated_user_df_t.to_csv('twitter.csv')

data_t= pd.read_csv('twitter.csv')


