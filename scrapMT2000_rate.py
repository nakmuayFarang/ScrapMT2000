
# coding: utf-8

# In[1]:


#Scraper MuayThai2000
import re
from  datetime import datetime, timedelta
import urllib.request
from bs4 import BeautifulSoup
import json
import time
import random


# In[2]:


def scrapMT2000Rate():
    '''Function that scrap the rate page.
    http://www.muaythai2000.com/rate.php
    '''
    url = urllib.request.urlopen("http://www.muaythai2000.com/rate.php")
    soup = BeautifulSoup(url)
    #get the table
    table = soup.find_all('table')[1]
    
    #get table lines
    lines= table.find_all('tr')
    
    event = dict()
           
    #for each line get a json
    matchRate = dict()

    matchRate['scrapDate'] = datetime.strftime(datetime.now(),'%Y%m%d')

    match = 1
    for line in lines[1:]:
        #get col

        if len(line.find_all('tr') ) == 1:

            thisMatch = dict()

            col0 = line.find('td').find_all('span')[0].get('style').split(":")[1] 
            name0 = line.find('td').find_all('span')[0].text
            col1 = line.find('td').find_all('span')[1].get('style').split(":")[1] 
            name1 = line.find('td').find_all('span')[1].text
            weight = line.find_all('td')[1].text


            thisMatch[col0 + 'Corner'] = name0
            thisMatch[col1 + 'Corner'] = name1
            thisMatch["weight"] = weight


            rateLines = line.find_all('td')[2].find('table')#get rate array
            color = list( map(lambda s: s.find('span').get('style').split(';')[0].split(':')[1] , rateLines.find_all('td')  )  )
            rates = list( map(lambda s: s.find('span').text  , rateLines.find_all('td')  )  )

            thisMatch['cote'] = [ x + ':' + y  for x,y in zip(color,rates)]



            matchRate['คู่'+ str(match)] = thisMatch
            match+=1
  
    return(matchRate)
    
    


# In[3]:


z = scrapMT2000Rate()
file = open("./data/cotes/mt2000Cotes{}.json".format(datetime.now().strftime('%Y%m%d')),'w',encoding='utf-8')
json.dump(z,file, ensure_ascii=False)
file.close()

