import sqlite3


class HandleData:
    # -- コンストラクタ　引数ファイル名
    def __init__(self, input_filename):
        self.con = sqlite3.connect(input_filename)
        self.cur = self.con.cursor()
        self.list = []
        self.__table_name = "data_set"

    # -- テーブル名のセッター --
    def set_table_name(self, _table_name):
        self.__table_name = _table_name

    # -- テーブル名のゲッター --
    def get_table_name(self):
        return self.__table_name

    # -- テーブル作成 (要素の文字列リストからSQL文を実行)---
    def create_table(self, column_list):
        command = ','.join(column_list)
        command = 'CREATE TABLE IF NOT EXISTS ' + self.__table_name + '(' + command + ');'
        self.cur.execute(command)

    # --- データ取得 ---
    # 引数 str_list[] = ["取得したいカラム名１","取得したいカラム名１", ........]
    # 戻り値　取得したデータのタプルが格納されたリストが返される
    # ex. [('1', '2'), ('3', '4')]
    def get_data(self, column_list):
        command = ','.join(column_list)
        command = 'SELECT ' + command + ' FROM ' + self.__table_name
        self.cur.execute(command)
        text_list = self.cur.fetchall()
        return text_list

    # --- データを登録 ---
    def add_data(self, column_list, data_list):
        command = ','.join(column_list)
        que_str = '?,' * len(data_list)[:-1]
        command = 'INSERT INTO ' + self.__table_name + '(' + command + ') VALUES(' + que_str
        self.cur.execute(command)

    # デストラクタでデータベースを終了
    def __del__(self):
        self.con.close()
