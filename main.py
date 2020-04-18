import tweepy
import urllib.request
import os
import change #change.py を参照
import psycopg2

# OAuthHandler（環境変数）
CK = os.environ["CONSUMER_KEY"] # Consumer Key
CS = os.environ["CONSUMER_SECRET"] # Consumer Secret
AT = os.environ["ACCESS_TOKEN"] # Access Token
AS = os.environ["ACCESS_TOKEN_SECRET"] # Accesss Token Secert

# Database Credentials（環境変数）
host = os.environ["host"]
database = os.environ["database"]
user = os.environ["user"]
password = os.environ["password"]

# connect postgreSQL
dsn = "host="+host+" port=5432 dbname="+database+" user="+user+" password="+password
conn = psycopg2.connect(dsn)

# excexute sql
cur = conn.cursor()
cur.execute('SELECT * FROM use;')
use = cur.fetchall()
usephoto = use[0][0] # usephoto:写真の番号
usevar = use[0][1] # usevar:車両型式配列のキー

# URLの生成
with open('url.txt') as urls:
    l = urls.readlines()
a = l[usevar] # usevarによって指定された車両形式の情報
semiurl,num = a.strip().split() # semiurl:指定された車両の写真が格納されているディレクトリのURL num:写真の数
num = int(num)

# 画像の取得
url = semiurl + '/'+str(usephoto)+'.jpg' # 指定した番号の写真を含めたURLを生成
savename = "tweet.jpg"
urllib.request.urlretrieve(url, savename) # 写真の保存（上書き）

# 情報の生成
url_litter = semiurl.split('/') # URLの分割
com = change.com(url_litter[3]) # 鉄道会社名の取得・変換
var = change.var(url_litter[4]) # 車両型式の取得・変換

# Twitterオブジェクトの生成
auth = tweepy.OAuthHandler(CK, CS)
auth.set_access_token(AT, AS)
api = tweepy.API(auth)

# 画像付きツイート
api.update_with_media(status = '#おはようトレイン #おはようトレインbot おはようございます。今日の車両は'+com+'の'+var+'系です。', filename = './tweet.jpg')

# logの更新
nextvar = usevar
nextphoto = usephoto + 1
if nextphoto == num : # 写真の番号が写真の数と等しくなったとき次の形式に変更される。
    nextphoto = 0
    nextvar = nextvar + 1

# DBの内容を変更する
cur.execute('UPDATE use SET photo = %s;' % nextphoto)
cur.execute('UPDATE use SET var = %s;' % nextvar)
conn.commit()

cur.close()
conn.close()


