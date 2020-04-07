import tweepy
import urllib.request
import change #change.py を参照

# OAuthHandler
CK = '*********************************' # Consumer Key
CS = '*********************************' # Consumer Secret
AT = '*********************************' # Access Token
AS = '*********************************' # Accesss Token Secert

# log.txt の取得
with open('log.txt') as logs:
    log = (logs.read())
usephoto,usevar = map(int,log.split()) # usephoto:写真の番号 usevar:車両型式配列のキー

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

f = open('log.txt','w') # log.txtの書き換え
f.write(str(nextphoto)+' '+str(nextvar))
f.close


