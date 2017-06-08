import sqlite3
from pprint import pprint

conn = sqlite3.connect('aws_httping.db')
cursor = conn.cursor()
#執行SQL命令
#cursor.execute('select avg(latency) from aws_httping where region=?', ('Asia Pacific (Seoul)',))
cursor.execute('select region, round(avg(latency),2) from aws_httping group by region order by 2')
#cursor.execute('select * from aws_httping')
#獲得結果
values = cursor.fetchall()

pprint (values)
#關閉命令
cursor.close()
#關閉連線
conn.close()
