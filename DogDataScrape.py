# -*- coding: utf-8 -*-
"""
Created on Fri Mar 17 09:20:16 2017

@author: G
"""

from bs4 import BeautifulSoup
import requests
import pandas as pd
#define the function I need
from bs4 import *
from bs4 import NavigableString
import re


url = "http://www.akc.org/content/news/articles/most-popular-dog-breeds-full-ranking-list/"
r = requests.get(url)
data = r.text
soup = BeautifulSoup(data, "lxml")

table = soup.find_all('table')[0]
rows = table.find_all('tr')[1:]

dataf = {
    'breeds' : [],
    'rank2016' : [],
    'rank2015' : [],
    'rank2014' : [],
    'rank2013' : []
    }

for row in rows:
        cols = row.find_all('td')
        dataf['breeds'].append( cols[0].get_text())
        dataf['rank2016'].append(cols[1].get_text())
        dataf['rank2015'].append(cols[2].get_text())
        dataf['rank2014'].append(cols[3].get_text())
        dataf['rank2013'].append(cols[3].get_text())

dogData = pd.DataFrame( dataf )

#find the links in the table        
links = table.findAll('a')

# make a table for the details
details = {
        'Personality' : [],
        'Energy Level' : [],
        'Good with Children' : [],
        'Good with other Dogs' : [],
        'Shedding' : [],
#==============================================================================
#         'Grooming' : [],
#==============================================================================
        'Trainability' : [],
        'Height' : [],
        'Weight' : [],    
        'Life Expectancy' : [],
        'Barking Level' : []                   
        }


def get_section_text(text):
    section = soup.find(text=text)
#==============================================================================
#     if not section:
#         raise ValueError("Section not found")
#         print(url)
#==============================================================================
    texts = []
    for item in section.parent.find_next_siblings():
        if item.name == 'strong':
            break
        text_before = item.previous_sibling
        if isinstance(text_before, NavigableString):
            texts.append(text_before)

    return ' '.join(texts)
section = soup.find(text='Shedding:')
print(section)
#load the URLs    
#Seeing a lot of errors, but will later resolve them
#Dropping Grooming Variable for now
for a in table.find_all('a', href=True):
    url = a['href']
    r = requests.get(url)
    data = r.text
    soup = BeautifulSoup(data, "lxml")
    part = soup.find("div", {"class": "breed-details__main"})
    
    if soup.find("strong", text=re.compile("Personality:")) is None:
        details['Personality'].append('None')
    else:
        details['Personality'].append(soup.find("strong", text=re.compile("Personality:")).next_sibling.strip())
    if soup.find("strong", text=re.compile("Energy Level:")) is None:
        details['Energy Level'].append('None')
    else:
        details['Energy Level'].append(soup.find("strong", text=re.compile("Energy Level:")).next_sibling.strip())
    if soup.find("strong", text=re.compile("Good with Children:")) is None:
        details['Good with Children'].append('None')
    else:
        details['Good with Children'].append(soup.find("strong", text=re.compile("Good with Children:")).next_sibling.strip())
    if soup.find("strong", text=re.compile("Good with other Dogs:")) is None:
        details['Good with other Dogs'].append('None')
    else:
        details['Good with other Dogs'].append(soup.find("strong", text=re.compile("Good with other Dogs:")).next_sibling.strip())
    if soup.find("strong", text=re.compile("Shedding:")) is None:
        details['Shedding'].append('None')
    else:
        details['Shedding'].append(soup.find("strong", text=re.compile("Shedding:")).next_sibling.strip())
#==============================================================================
#     if soup.find("strong", text=re.compile("Grooming:")) is None:
#         details['Grooming'].append('None')
#     elif soup.find("strong", text=re.compile("Grooming:")).next_sibling is None:
#         details['Grooming'].append(soup.find("strong", text=re.compile("Grooming:")).next_sibling.next_sibling.strip())
#     else:
#         details['Grooming'].append(soup.find("strong", text=re.compile("Grooming:")).next_sibling.strip())
#==============================================================================
    if soup.find("strong", text=re.compile("Trainability:")) is None:
        details['Trainability'].append('None')
    else:
        details['Trainability'].append(soup.find("strong", text=re.compile("Trainability:")).next_sibling.strip())
    if soup.find("strong", text=re.compile("Height:")) is None:
        details['Height'].append('None')
    else:
        details['Height'].append(soup.find("strong", text=re.compile("Height:")).next_sibling.strip())
    if soup.find("strong", text=re.compile("Weight:")) is None:
        details['Weight'].append('None')
    else:
        details['Weight'].append(soup.find("strong", text=re.compile("Weight:")).next_sibling.strip())
    if soup.find("strong", text=re.compile("Life Expectancy:")) is None:
        details['Life Expectancy'].append('None')
    else:
        details['Life Expectancy'].append(soup.find("strong", text=re.compile("Life Expectancy:")).next_sibling.strip())
    if soup.find("strong", text=re.compile("Barking Level:")) is None:
        details['Barking Level'].append('None')
    else:
        details['Barking Level'].append(soup.find("strong", text=re.compile("Barking Level:")).next_sibling.strip())

dogdetails = pd.DataFrame( details )

alldogs = dogData.join(dogdetails, how='inner')

#Energy Level is Unique to Each
alldogs['Energy Level'].unique
#Check Barking - A few levels
alldogs['Barking Level'].unique 
#try to extract height from string to number
# Use the low end of male height 
alldogs['Height1'] = alldogs['Height'].str.extract('(\d+)',expand=True)
#LifeExpectancy - using lower bound
alldogs['Life'] = alldogs['Life Expectancy'].str.extract('(\d+)',expand=True)
#Weight - using lower bound of male weight 
alldogs['Weight1'] = alldogs['Weight'].str.extract('(\d+)',expand=True)

alldogs.to_csv("AKC_Dog_Information.csv")
dogData.to_csv("AKC_Dog_Registrations.csv")
