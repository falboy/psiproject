import sqlite3
import pprint

# 類似単語を検索する関数
def search_similar_words(conn, query):
    # lemmaがqueryと一致した行のidのカーソルオブジェを取得
    cur = conn.execute("select wordid, pos from word where lemma='%s'" % query)
    # 一致結果の行を取得
    result = cur.fetchall()
    # 
    return result

def main():
    # ファイルパス
    filepath = 'data/wnjpn.db'
    # データベースにコネクト
    conn = sqlite3.connect(filepath)
    # カーソルを取得

    x = search_similar_words(conn, '選挙')
    print(x)

if __name__ == '__main__':
    main()