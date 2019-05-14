from pyknp import KNP
import sys
import pprint
import sqlite3
import category_settings

# 連体形にする必要のある単語を特定
def get_attribute_mrph(mrph_list):
    # 複合名詞作成に利用する単語用の変数を用意
    attribute = {'原形': None, '品詞':None, '活用1':None, '活用2':None}
    # 形態素の構成数別で処理をする
    mrph_count = len(mrph_list)
    if 2 < mrph_count:
        print("mrph_count:%i" % mrph_count)
        for mrph in mrph_list:
            print("原形:%s 品詞:%s" % (mrph.genkei, mrph.hinsi))
            # 名詞、動詞、形容詞以外のカウント変数を用意
            josi_count = 0

            # attributeの値を埋める
    elif mrph_count == 1:
        mrph = mrph_list[0]
        attribute['原形'] = mrph.genkei
        attribute['品詞'] = mrph.hinsi
        attribute['活用1'] = mrph.katuyou1
        attribute['活用2'] = mrph.katuyou2
    else:
        print("error 属性単語の長さ部分")

    return attribute

# 複合名詞を作成する関数(letter)
def get_compound_noun(word):
    # 形態素解析
    knp = KNP()
    result = knp.parse(word)
    # 解析結果の形態素部分を取得 (len > 2 の可能性あり)
    mrph_list = result.mrph_list()

    # 変形対象の単語(形態素)を取得
    attribute = get_attribute_mrph(mrph_list)

    # 品詞判定をして連体名詞に変形
    X = None
    if attribute['品詞'] == '形容詞':
        X = adjective_function(attribute)
    elif attribute['品詞'] == '動詞':
        X = verb_function(attribute)
    elif attribute['品詞'] == '名詞':
        X = noun_function(attribute)
    else:
        print("error 品詞判定部分")

    # 人や物を表す要素部分の名詞を取得
    Y = None
    # 複合名詞を出力
    compound_noun = X + Y
    # 値を返却
    return compound_noun

# 形容詞の語尾変形処理関数
def adjective_function(dic):
    # 引数から原形を取得
    genkei = dic['原形']
    # 返却変数を用意
    X = None
    # イ活用、ナ活用か判定
    if dic['活用1'] == 'イ形容詞':
        if genkei[-1:] == 'い':
            X = genkei
        else:
            X = genkei + 'い'
    
    if dic['活用1'] == 'ナ形容詞':
        if genkei[-1:] == 'な':
            X = genkei
        else:
            X = genkei + 'な'
    # 変換結果を返す
    return X

# 動詞の語尾変形処理関数
def verb_function(dic):
    X = None
    return X

# 名詞の語尾変形処理関数
def noun_function(dic):
    X = None
    return X

# 様々な解析結果(文字列)を辞書形式に変換する関数
def get_dic(str):
    pass

# str形式のimisをlist[dic{'xxx'=yyy}]形式に変換する関数
def convert_imis2dic(str):
    str_list = str.split(" ")
    result = []
    for s in str_list:
        i = s.find(":")
        key = s[:i]
        value = s[i+1:]
        dic = {key: value}
        result.append(dic)
    return result

# 辞書形式imis内に特定カテゴリが含まれるかチェック
def is_human_category(_list):
    flag = False
    for d in _list:
        if 'カテゴリ' in d:
            if d['カテゴリ'] in category_settings.CATEGORY:
                flag = True
    return flag

# 品詞が名詞か判定
def is_noun(str):
    if str == '名詞':
        return True
    else:
        return False

# データベースに登録する関数

# main method
def main():
    # データベース定義
    db_filename = 'data/noun.db'
    # データベースに接続
    conn = sqlite3.connect(db_filename)
    # knp
    knp = KNP()
    # 入力文字列
    input_sentence = 'ヤクザ乙'
    # 解析
    result = knp.parse(input_sentence)

    print("文節")
    for bnst in result.bnst_list():
        print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親文節ID:%d, 素性:%s" 
            % (bnst.bnst_id, "".join(mrph.midasi for mrph in bnst.mrph_list()), bnst.dpndtype, bnst.parent_id, bnst.fstring))

    print("基本句")
    for tag in result.tag_list(): # 各基本句へのアクセス
        print("\tID:%d, 見出し:%s, 係り受けタイプ:%s, 親基本句ID:%d, 素性:%s" 
            % (tag.tag_id, "".join(mrph.midasi for mrph in tag.mrph_list()), tag.dpndtype, tag.parent_id, tag.fstring))

    print("形態素")
    for mrph in result.mrph_list(): # 各形態素へのアクセス
        print("見出し:%s\n 読み:%s\n 原形:%s \n 品詞:%s \n 品詞細分類:%s \n 活用型:%s \n 活用形:%s \n 意味情報:%s \n 代表表記:%s" 
        % (mrph.midasi, mrph.yomi, mrph.genkei, mrph.hinsi, mrph.bunrui, mrph.katuyou1, mrph.katuyou2, mrph.imis, mrph.repname))

    for mrph in result.mrph_list():
        # mrph.imisを変換(str -> dic)
        imis = convert_imis2dic(mrph.imis)
        # 品詞チェック (人、動物)
        if is_noun(mrph.hinsi) is True:
            # カテゴリチェック
            if is_human_category(imis) is True:
                # 対象単語
                word = mrph.genkei
                # 単語が登録されているか検索(IDを取得)
                search_command = conn.execute("select wordid from word where word='%s'" % word)
                result = search_command.fetchall()
                # 登録されていない場合の処理
                if len(result) == 0:
                    # レコード数を取得
                    count_command = conn.execute('select count (wordid) from word')
                    count_result = count_command.fetchall()
                    # wordid = レコード数 + 1
                    wordid = (int(count_result[0][0]) + 1)
                    # wordテーブルにデータ登録
                    innsert_command_word = 'insert into word (wordid, word, category) values (?, ?, ?)'
                    # カテゴリを取得
                    category = ''
                    for d in imis:
                        if 'カテゴリ' in d:
                            category = d['カテゴリ']
                    # 挿入データ
                    tuple_word = (wordid, word, category)
                    # SQL文の実行
                    conn.execute(innsert_command_word, tuple_word)
                    
                    # linkテーブルにデータ登録
                    insert_command_link = 'insert into link (wordid, sentence) values (?, ?)'
                    # 挿入データ
                    tuple_link = (wordid, input_sentence)
                    # SQL文の実行
                    conn.execute(insert_command_link, tuple_link)
                else:
                    # 単語ID
                    wordid = result[0][0]
                    # linkテーブルにデータ登録
                    insert_command_link = 'insert into link (wordid, sentence) values (?, ?)'
                    # 挿入データ
                    tuple_link = (wordid, input_sentence)
                    # SQL文の実行
                    conn.execute(insert_command_link, tuple_link)

                # 挿入データを保存
                conn.commit()
        pprint.pprint(imis)
        print("\n")

if __name__ == '__main__':
    main()