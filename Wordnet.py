import sqlite3
import pprint
import argparse

# 類似単語を検索する関数(未完成)
def search_similar_words(conn, query):
    # lemmaがqueryと一致した行のidのカーソルオブジェを取得
    cur = conn.execute("select wordid, pos from word where lemma='%s'" % query)
    # 一致結果の行を取得
    result = cur.fetchall()
    # 
    return result

# 上位語リストを入手する関数
def get_hypernym(conn, query):
    # lemmaがqueryと一致した行のidのカーソルオブジェを取得
    cur = conn.execute("select wordid, pos from word where lemma='%s'" % query)
    # 一致結果の行を取得 (複数ヒットする可能性がある)
    result = cur.fetchall()
    # ヒット件数を表示
    print(str(len(result)) + 'hit')
    for t in result:
        # 検索結果（品詞と検索ワード）を表示
        print('%s:%s of "%s"' % (t[0], t[1], query))
        # 概念IDを取得 (複数ヒットする可能性がある)
        cur = conn.execute("select synset from sense where wordid='%s'" % word_id)
        sense_result = cur.fetchall()
        # ヒット件数を表示
        print("%s hit" % len(sense_result))
        for synset in sense_result:
            print("synset:%s" % synset)
            # 単語IDを取得
            word_id = t[0]
            # 概念IDを取得
            cur = conn.execute("select pos, name from synset where synset='%s'" % synset)
            synset_result = cur.fetchall()
            print('pos="%s", name="%s"' % (synset_result[0][0], synset_result[0][1]))
            # 概念リンクを取得
            cur = conn.execute("select synset2, link from synlink where synset1='%s'" % synset)
            
        print("\n")


# 単語の情報を検索する関数
def search_word_info(conn, query):
    # lemmaがqueryと一致した行のidのカーソルオブジェを取得
    cur = conn.execute("select wordid, pos from word where lemma='%s'" % query)
    # 一致結果の行を取得 (複数ヒットする可能性がある)
    result = cur.fetchall()
    # ヒット件数を表示
    print(str(len(result)) + 'hit')
    for t in result:
        # 検索結果（品詞と検索ワード）を表示
        print('%s:%s" of "%s"' % (t[0], t[1], query))
        # 単語IDを取得
        word_id = t[0]
        # 概念IDを取得 (複数ヒットする可能性がある)
        cur = conn.execute("select synset from sense where wordid='%s'" % word_id)
        sense_result = cur.fetchall()
        # ヒット件数を表示
        print("%s hit" % len(sense_result))
        for synset in sense_result:
            print("synset:%s" % synset)
            # 概念を表示
            cur = conn.execute("select pos, name from synset where synset='%s'" % synset)
            synset_result = cur.fetchall()
            print('pos="%s", name="%s"' % (synset_result[0][0], synset_result[0][1]))
            # 概念定義を取得
            cur = conn.execute("select def from synset_def where synset='%s'" % synset)
            synset_def_result = cur.fetchall()
            print('def:%s\n' % synset_def_result[0][0])
        print('\n')

# 概念IDから上位概念IDリストを返す関数 # return:link
def get_hypernym_list(conn, synset_id):
    # 概念リンクを取得 (arg_ex:synset_id = 10023039-n)
    cur = conn.execute("select synset2, link from synlink where synset1='%s'" % synset_id)
    synlink_result = cur.fetchall()
    # 返却用の空リスト
    result = []
    # link = hypeの探索
    for synlink in synlink_result:
        if synlink[1] == 'hype':
            result.append(synlink[0])
    # リストを返却
    if len(result) == 0:
        return False
    else:
        return result

# 概念IDから下位概念IDリストを返す関数 # return:link
def get_hyponym_list(conn, synset_id):
    # 概念リンクを取得 (arg_ex:synset_id = 10023039-n)
    cur = conn.execute("select synset2, link from synlink where synset1='%s'" % synset_id)
    synlink_result = cur.fetchall()
    # 返却用の空リスト
    result = []
    # link = hypeの探索
    for synlink in synlink_result:
        if synlink[1] == 'hypo':
            result.append(synlink[0])
    # リストを返却
    if len(result) == 0:
        return False
    else:
        return result   

# 概念IDから概念情報{'pos'=xxx, 'name'=yyy}を返す関数
def get_synset(conn, synsetid):
    # 概念情報を取得
    cur = conn.execute("select pos, name from synset where synset='%s'" % synsetid)
    synset_result = cur.fetchall()
    # 返却用の空リストを作成
    result = []
    for synset in synset_result:
        dic = dict(pos=synset[0], name=synset[1])
        result.append(dic)
    # 値を返却
    return result

# queryから単語情報[(wordid,pos)]を返す関数
def get_wordid(conn, query):
    cur = conn.execute("select wordid, pos from word where lemma='%s'" % query)
    word_result = cur.fetchall()
    # 返却用の空リストを作成
    result = []
    for word in word_result:
        dic = dict(wordid=word[0], pos=word[1])
        result.append(dic)
    
    if len(result) == 0:
        return False
    else:
        return word_result

# word_idから単語[(lemma, pos)]を返す関数
def get_word(conn, wordid):
    cur = conn.execute("select lemma, pos from word where lemma='%s'" % wordid)
    word_result = cur.fetchall()
    return word_result

# 単語の属する概念IDリストを返す関数　(単語IDを使用)
def get_synsetid_list(conn, wordid):
    cur = conn.execute("select synset from sense where wordid='%s'" % wordid)
    sense_result = cur.fetchall()
    return sense_result


def main():
    # ファイルパス
    filepath = 'data/wnjpn.db'
    # データベースにコネクト
    conn = sqlite3.connect(filepath)
    # argparseのオブジェクトを作成
    parser = argparse.ArgumentParser()
    # パラメータを追加
    parser.add_argument("query")
    # 引数を取得
    args = parser.parse_args()
    # カーソルを取得
    search_word_info(conn, args.query)

if __name__ == '__main__':
    main()