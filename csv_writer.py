import csv

with open('names.csv', 'a', newline='') as csvfile:
    fieldnames= ['first_name', 'last_name']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

    writer.writeheader()
    writer.writerow({'first_name':'Baked','last_name':'Beans'})
    writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
    writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

#ここからわかること
#まずheaderにheaderを与える
#次にkeyとvalueが全て一対一対応した文字列を一行ずつ作成する。
#{国内: 首相演説 野党から激しいやじ, 国内: 安田さん 情報収集部隊の働き ... } こんなイメージ
#そのあとは辞書として keyを指定し、valueも指定する
#→すなわちkeyとvalueを個別に取得する必要がある

