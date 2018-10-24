import requests
from bs4 import BeautifulSoup
import csv
import time
from datetime import datetime

target_url =  "http://www.nikkei.com/markets/kabu/"
r = requests.get(target_url)
#requestsを使って、webから取得

soup = BeautifulSoup(r.text,'lxml')
#要素を抽出
#beautifulsoupオブジェクトとしてhtml文書が帰ってくる

print(soup.title.string)

# ここから株価を取得する
# 株価そのものはspan.mkc-stock_pricesに入っている
# dl.mkc-moveのdtとddに始値,高値,安値が入っている

#spanが全て摘出された配列を取得
span = soup.find_all("span")
#からの文字列を返して
nikkei_heikin=""

#forぶんで全てのspan要素の中からClass="mkc-stock_prices"を探す
for tag in span:
    #class設定のないときは、tag.get("class").pop(0)を行うことができないので、tryする
    try:
        #tagの中からclass="n"のnを取ってくる.複数classが設定されている可能性があるので。
        #get関数では配列で返ってくる。なのでpot(0)で一番最初を取得
        string_ = tag.get("class").pop(0)
        #※stringは予約語なので、＿で重複を避ける
        #摘出したclassの文字列がmkc-stock_pricesかを調べる
        if string_ in "mkc-stock_prices":
            nikkei_heikin = tag.string
            break

    except:
        pass
        #passは何もしない

#nikkei_heikin ="日経平均:"+nikkei_heikin
#参考ではこれを1時間おきに取得して自動でcsv書き込みをしていたけど、ここでは一時的に
#株価、始値、高値、安値をセットで記録するにとどめる。

#まずはdl.mkc-moveを取得する

dl = soup.find_all("dl")

nikkei_hajimene = ""
nikkei_takane = ""
nikkei_yasune = ""

for tag in dl:
    try:
        string_ = tag.get("class").pop(0)
        if string_ in "mkc-move":
            nikkei_hajimene = tag.find_all("dd").pop(0).string
            nikkei_takane= tag.find_all("dd").pop(1).string
            nikkei_yasune = tag.find_all("dd").pop(2).string
            break
    except:
        pass

# nikkei_hajimene = "日経始値:"+nikkei_hajimene
# nikkei_takane= "日経高値:"+nikkei_takane
# nikkei_yasune="日経安値:"+nikkei_yasune

# 取得できたのでこれをcsvに書き込む


#csvを追記モードで開く
#ファイルが存在しなかったら作ってくれる
f = open("nikkei_heikin.csv","a")
writer = csv.writer(f,lineterminator='\r')
#改行文字に¥nを指定

#csvに出力するレコードを作成
#出力レコードはリストで作成するようで
csv_list = []

#現在の時刻を年、月、日、時間,分,秒で取得
time_ = datetime.now().strftime("%Y/%m/%d %H:%M:%S")


#レコードに挿入データを追加 時間　平均　始値　高値　安値
csv_list.append(time_)
csv_list.append(nikkei_heikin)
csv_list.append(nikkei_hajimene)
csv_list.append(nikkei_takane)
csv_list.append(nikkei_yasune)



#念のため出力して中身を見る
print(csv_list)

#追記
writer.writerow(csv_list)

#ファイル破損防止のために閉じる
f.close()


#できた！！！！
#が、複数行挿入すると改行されない
# →改行特殊文字を入れてどうだ→ダメでした
#writerowsでどうだ→大失敗。文字列を分割してしまった
#\nでできるのだけど、改行文字が残ってしまうのがアウト
#やっとできた。lineterminatorをマシン規定の\rに合わせればよかったのだ。windowsだと\n

