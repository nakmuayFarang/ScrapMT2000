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




urlRoot = 'http://www.muaythai2000.com/showresult.php?sdate=' # date m/dd/yyyy ou mm/dd/yyyy



def scrappMT2000Res(path, date):
    '''Function that scrap MT2000 result data.
	path is the url of the web page,
	date is the day we want to scrap
	This function return a dict object'''
    
    def getHtml(path,date):
        '''This function return the code of the web page'''
        url = date.strftime('%d/%m/%Y')
        if url[0] == '0' :
            url = url[1:]
        url = path + url
        #download HTML code
        pageHTML = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(pageHTML)
        return(soup)
 
    def makeMatchJson(matchLine,col):
        '''This function transform in dict match row'''
        if len(matchLine)==2:
            rowspan = list(map(lambda s: s.get('rowspan'),  matchLine[0].find_all('td')))
            red = list(map(lambda s: s.text,   matchLine[0].find_all('td')))
            blue= list(map(lambda s: s.text,   matchLine[1].find_all('td')))


        fight = dict()#Create fight dict
        fightBlue = dict()
        fightRed = dict()

        blueCounter = 0
        for redCounter in range( len(col) ):
            #Valeur en commun ligne ayant rowspan
            if rowspan[redCounter]== '2':
                fight[ col[redCounter] ] = red[redCounter]
            elif rowspan[redCounter]==None:
                fightRed[col[redCounter] ] = red[redCounter]
                fightBlue[ col[redCounter] ] = blue[blueCounter]
                blueCounter+=1

        fight['blueCorner'] = fightBlue 
        fight['redCorner'] = fightRed
        return(fight)

    def getMatch(soup):
        '''This function return match dict'''
        #table des resultats
        table2 = soup.find('table',{'class':'resulttv'})

        col = table2.find('tr').find_all('th')#First row of data
        col= list(map(lambda s: s.text.replace('\xa0',' ') ,col))#columns

        matchs = {}

        #blue and red identification
        matchLine = list()
        for line in table2.find_all('tr'):
            c = list(map(lambda s: s.get('style'),  line.find_all('td') ))
            try:
                if 'red' in c[1] :
                    matchLine.append(line)
                    fightNum = line.find_all("td")[0].text
                elif "blue"  in  c[0]:
                    matchLine.append(line)
                    matchs['คู่' + fightNum] = makeMatchJson(matchLine,col)#Json du match
                    matchLine = list()
                else:
                    color.append("noColor")
                    matchLine = list()
            except:
                matchLine = list()
        return(matchs)



    soup = getHtml(path,date)
    
    #test if this day stadium are closed
    if soup.find('table',{'class':'three'}).find('td').text!= 'ไม่มีข้อมูลการแข่งขัน':
        

        #event
        event = dict()
        eventLine = soup.find('table',{'class':'three'}).find_all('td')[1]
        eventLine = eventLine.get_text(separator="\n").replace('\xa0\n','').replace('\xa0','').split("\n")

        event["dateFarang"]= date.strftime('%Y%m%d')

        for data in eventLine:
            if "ศึก" in data:
                event["promotion"] = data
            elif "เวลา" in data: 
                event["dateTh"] = data
            elif "สนามมวยเวที" in data:
                event["stadium"] = data.split()[1]
            elif "ผู้จัดวิชิต" in data:
                event["promoterName"] = data.split()[1]
            elif "อัตราค่าเข้าชม" in data:
                data = data.replace( "อัตราค่าเข้าชม", '')
                event["entranceFees"]= [int(s) for s in data.replace('-',' ').replace('/',' ').split() if s.isdigit()]
            elif "ยอดรวมค่าเข้าชม" in data:
                data = data.replace("ยอดรวมค่าเข้าชม","")
                event["ยอดรวมค่าเข้าชม"] = [int(s) for s in data.replace(',','').split() if s.isdigit()][0]

        event["matchs"] = getMatch(soup)

        return(event)

    

#Run scrapper


try:
	dte = datetime.now()
	z = scrappMT2000Res(urlRoot, dte)
	if z != None:
		file = open('./data/result/mt2000Res{}.json'.format(dte.strftime('%Y%m%d')),'w',encoding='utf-8')
		json.dump(z,file, ensure_ascii=False)
		file.close()
