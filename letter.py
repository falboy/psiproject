from pyknp import KNP
import sys
import pprint

# creat compound noun(letter)
def compound_noun(word, _knp):
    # 形態素解析
    result = _knp.parse(word)
    # 品詞判定

    # 原型取得

    # 名詞に接続可能な形にする

    # 複合名詞作成

    # 複合名詞を出力

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
            if d['カテゴリ'] == '人' or d['カテゴリ'] == '動物':
                flag = True
    return flag

# main method
def main():
    # knp
    knp = KNP()
    # 解析
    result = knp.parse("このバカ野郎が！")

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
        imis = convert_imis2dic(mrph.imis)
        print(is_human_category(imis))
        pprint.pprint(imis)
        print("\n")


if __name__ == '__main__':
    main()