# coding: utf-8

# In[ ]:


#Scraper MuayThai2000
from  datetime import datetime
import urllib.request
from bs4 import BeautifulSoup
import json


# In[ ]:


def scrapChamp():
    '''This function get the list of muay thai champions'''
    
    def makeStadiumJson(soup):
        '''This function return for a stadium the champ's list'''

        def getWeight(block):
            '''This function return for a weight division the champ nam'''
            weight = block.find('p', {'class':'h25'}).text.split()[-2]
            return(weight)

        def makeblockJson(block):
            '''This function return for a weight division the ranking'''
            result = dict()    
            #champ detail: name/ get title inf, defense
            champDetail =  list( map( lambda s: s.find('span',{'class':'champDetail'}).text if s.find('span',{'class':'champDetail'})!=None else None ,block.find_all('p',{'class':'champHead'}))) 
            #challeneger
            challengers =  list(map(lambda s: s.text, block.find('ol',{'class':'champList'}).find_all('li')))
            result['Champ'] = champDetail[0]
            result['ChampDetail1'] = champDetail[1]

            try:
                result['ChampDetail2'] = champDetail[2]
            except:
                result['ChampDetail2'] = None
            
            challengers2 = dict()
            for i in challengers:
                challengers2[ challengers.index(i)+1] = i
            
            result['ranking']= challengers2
            return(result)


        result = dict()
        blocks = soup.find_all('div',{'class':'infoBox'})#bloc ranking

        for block in blocks:
            weight = getWeight(block)

            result[weight] = makeblockJson(block)  

        return(result)

    #Pametres of the website 
    stadiumWebPage = dict()
    stadiumWebPage['ลุมพินี'] = '1'#lumpinee
    stadiumWebPage['ราชดำเนิน'] = '2'#radjadamern
    stadiumWebPage['สยามอ้อมน้อย'] = '3'#siam omnoi
    stadiumWebPage['ช่อง7'] = '4'#chong 7
    stadiumWebPage['ประเทศไทย'] = '5'#thailand
    
    url = 'http://www.muaythai2000.com/champofstadium.php?stadium='
    
    
    result = dict()
    result['date'] = datetime.now().strftime('%Y%m%d')
    
    
    for cle in stadiumWebPage.keys():
        #loop through dictionnary keys
        url2 = url + stadiumWebPage[cle]#set url page link
        html = urllib.request.urlopen(url2)#get html code
        soup = BeautifulSoup(html)#instantiate soup object
        result[cle] = makeStadiumJson(soup)
    
    return(result)


# In[ ]:


#save file on disc
try:
    fileName = './data/champs/mt2000Champ_{}.json'.format(datetime.now().strftime('%Y%m%d'))
    file = open(fileName,'w', encoding='utf-8')
    json.dump(scrapChamp()  ,file, ensure_ascii=False)
    file.close()
except:
    file.close()

