# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

#参考 Web スクレイピング入門 — Python で行う Web Scraping ドキュメント	https://takahiromiura.github.io/web_scraping.html
url = "https://news.yahoo.co.jp/topics"
response = requests.get(url)
bs = BeautifulSoup(response.content, "lxml")
topics  = bs.select('.fl, .fr')


news_topics = {}
for news in topics: #リストの一つの要素に変数名newsを与え
    topic = news.select('li')[0].text #newsの0番目のliはトピック名なので、それをキーにする
    news_topics[topic] = [news_topic.text.replace('new','').replace('写真','').replace('動画','') for news_topic in news.select('li')[1:-2]]
    #キーtopicのvalueには news(liの配列)の1番目から最後から2番目（もっとみる)以外を取ってきたもの
    #の配列を作って与える
print(news_topics)

#pandasで読む
topics_dt = pd.DataFrame.from_dict(news_topics)
print(topics_dt)
topics_dt.to_csv("change.csv")
topics_dt.to_json("change.json",force_ascii=False)