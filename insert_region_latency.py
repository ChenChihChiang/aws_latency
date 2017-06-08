import os
import sys
import json
import sqlite3

#檢查資料檔案是否存在，存在就刪除
if os.path.exists("./aws_httping.db"):
   os.remove("./aws_httping.db")

conn = sqlite3.connect('aws_httping.db')
# 創建一個Cursor:
cursor = conn.cursor()
# 執行一個SQL命令，建立aws_httping表:
cursor.execute('create table aws_httping (region varchar(100), latency integer)')


#把log目錄下的檔案資料都匯入資料庫中
DATA_DIR = "log/"

#建立dictionary
aws_latency = {}

#以檔案數量做迴圈
for filename in os.listdir(DATA_DIR):
   print ("Loading: %s" % filename)

#讀json檔到json_data
   with open('log/'+filename,'r') as f:
      json_data = json.load(f)

#用key value 跑迴圈      
      for (i,j) in json_data.items():

#拿掉不需要的字串，讓value可以為integer   
         m = j.split()[0]

         aws_region = i
         aws_latnecy = m
#把每一筆資料匯入資料庫
         cursor.execute('insert into aws_httping (region, latency) values (?,?)',(aws_region,aws_latnecy))

#關閉SQL命令
cursor.close()
#送出commit
conn.commit()
# 關閉Connection
conn.close()
