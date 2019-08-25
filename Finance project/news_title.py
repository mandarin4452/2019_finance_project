from selenium import webdriver
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from konlpy.tag import Twitter
from collections import Counter
import pandas as pd
import numpy as np
import sys
from PIL import Image
engine = Twitter()

list_tag = [u'Noun', u'Adjective',u'Verb']

final_sentiment = 'NEU'
final_sentiment_rate = 0
text_data = []
file_name = ''
pos = 0
neg = 0
neu = 0
counter = 0

def crawling(text):
    search_text = text
    global file_name
    file_name = search_text + '.txt'

    driver = webdriver.PhantomJS('C:\Finance project\phantomjs/bin/phantomjs')


    driver.implicitly_wait(3)
    driver.get('https://finance.naver.com/news/news_search.nhn')

    driver.find_element_by_name('q').send_keys(search_text)
    driver.find_element_by_xpath('//*[@id="contentarea_left"]/form/div/div/div/input[2]').click()

    cur_url = driver.current_url



    f = open(file_name,'w')

    for i in range(10):
        nex_url = str(cur_url) + str('&page=' + str(i + 1))
        driver.get(nex_url)
        html = driver.page_source
        soup = BeautifulSoup(html,'html.parser')
        title1 = soup.select('dt.articleSubject')
        title2 = soup.select('dd.articleSubject')

        for sub in title1:
            #print(sub.text)
            f.write(str(sub.text) + '\n')
        for sub in title2:
            #print(sub.text)
            f.write(str(sub.text) + '\n')
    f.close()




def preprocessing():
    f = open(file_name,'r')
    line = f.readline()
    global text_data

    for line in f:
        if line == '\n':
            continue
        else :
            line_parse = engine.pos(line)
            for i in line_parse:
                if i[1] in list_tag:
                    #text_data.append(i[0] + '/' + i[1])
                    text_data.append(i[0])

    f.close()





def pros_and_cons():

    data = pd.read_csv('C:\Finance project\polarity.csv', names = ['Word', 'Degree'], encoding = 'cp949', header = 0)
    # encoding : Windows : cp949 / others : utf-8 ----- need to modify according to os
    overall = data['Word'].tolist()
    sentiment = data['Degree'].tolist()

    global pos
    pos = 0
    global neg
    neg = 0
    global neu
    neu = 0
    global counter
    Counter = 0
    global text_data
    for word in text_data:
        i  = 0 # index
        for key in overall:
            if word in key:
                sent = sentiment[i]
                if sent == "POS":
                    pos += 1
                elif sent == "NEG" :
                    neg += 1
                elif sent == "NEUT" :
                    neu += 1

                counter += 1
                break
            i += 1
    print("Total matched words : " + str(counter))
    print("Positive words : " + str(pos))
    print("Negative words : " + str(neg))
    print("Neutral words : " + str(neu))
    f = open('posibility.txt','w')
    if pos > neg and pos > neu:
        print(str(pos/counter * 100) + "% 확률로 긍정")
        final_sentiment = "POS"
        final_sentiment_rate = pos/counter
        f.write(str(pos/counter * 100))
        f.close()
    elif neg > pos and neg > neu:
        print(str(neg/counter * 100) + "% 확률로 부정")
        final_sentiment = "NEG"
        final_sentiment_rate = neg/counter
        f.write(str(neg/counter * 100))
        f.close()
    elif neu > neg and neu > pos:
        print(str(neu/counter * 100) + "% 확률로 중립")
        final_sentiment = "NEU"
        final_sentiment_rate = neu/counter
        f.write(str(neu/counter * 100))
        f.close()




def create_wordcloud(text):
    search_text = text
    color = ''
    if final_sentiment == 'POS':
        color = 'spring'
    elif final_sentiment == 'NEG':
        color = 'OrRd'
    elif final_sentiment == 'NEU' :
        color = 'Oranges'

    wordcloud = WordCloud(
    font_path = 'gulim.ttc',
    background_color = 'white',
    relative_scaling = 0.2,
    max_font_size = 150,
    min_font_size = 30,
    colormap = color, # 긍부정에 따른 색상 변화
    width = 800,
    height = 800)
    text = open(file_name).read()
    wordcloud = wordcloud.generate(text)
    fig = plt.figure(figsize = (12,12))

    plt.imshow(wordcloud)
    plt.axis('off')
    wordcloud_file = search_text + '.png'
    fig.savefig(wordcloud_file)
    fore_img = Image.open(wordcloud_file)
    fore_img = fore_img.resize((600,600))
    fore_img.save(wordcloud_file)
    print("Image Saved")

def main(text):
    print("##### Crawling #####")
    crawling(text)
    print("#### Preprocessing Data ####")
    preprocessing()
    print("### Sentiment Analyzing ###")
    pros_and_cons()
    print("## Creating WordCloud ##")
    create_wordcloud(text)
