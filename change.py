def com(com): # 会社名の変換
    code = {'jr-central':'JR東海','jr-east':'JR東日本','jr-west':'JR西日本','jr-shikoku':'JR四国'}
    name = code[com]
    return name 

def var(var): # 気動車の場合
    trainid = var
    if trainid[:5]=='kiha-':
        trainid = 'キハ'+trainid[5:]
    return trainid