import json
import sqlite3


def read_json(file_name: str) -> dict:
    with open(file_name, 'r', encoding='UTF-8') as f:
        """json.load() 讀取 JSON 檔案，轉換為 Python 的 dict"""
        pass_dict = json.load(f)
        return pass_dict


def print_json(data: dict) -> None:
    """將字典轉爲 json 字串後輸出到螢幕"""
    pass_str = json.dumps(data, ensure_ascii=False, indent=4)
    print(pass_str)


def read_txt(file_name: str) -> dict:
    """讀取txt檔"""
    try:
        with open(file_name, 'r', encoding='UTF-8') as file:
            file_contents = file.read()
            print(file_contents)
    except FileNotFoundError:
        print("找不到檔案")
    except Exception as e:
        print(f"讀取檔案時發生錯誤: {e}")


def check_pass(username: str, password: str) -> bool:
    """ 讀取 pass.json 檔案 並比對帳密"""
    try:
        with open('pass.json', 'r', encoding='UTF-8') as f:
            data = json.load(f)
            for entry in data:  # 迭代 JSON 陣列中的每個元素（字典）
                if entry.get('帳號') == username and entry.get('密碼') == password:
                    return True
            else:
                return False
    except FileNotFoundError:
        print(f'{"找不到 pass.json 檔案"}')
        return False


def menu():
    """顯示選單並選取選項"""
    print("-" * 10 + "選單" + "-" * 10)
    print("0 / Enter 離開")
    print("1 建立資料庫與資料表")
    print("2 匯入資料")
    print("3 顯示所有紀錄")
    print("4 新增記錄")
    print("5 修改記錄")
    print("6 查詢指定手機")
    print("7 刪除所有記錄")
    print("-" * 24)
    while True:
        try:
            choice = input("請輸入您的選擇 [0-7]: ").strip()
            if choice == '' or choice == '0':
                return int(0)
            elif choice in ['1', '2', '3', '4', '5', '6', '7']:
                return int(choice)
            else:
                print(f'{"=>無效的選擇"}')
                print()
        except ValueError as e:
            print(f"發生錯誤: {e}")


def create_database():
    """建立資料庫"""
    try:
        conn = sqlite3.connect('wanghong.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS members (
                iid INTEGER PRIMARY KEY AUTOINCREMENT,
                mname TEXT NOT NULL,
                msex TEXT NOT NULL,
                mphone TEXT NOT NULL
            )
        ''')

        conn.commit()
        conn.close()
        print(f'{"資料庫已建立"}')

    except sqlite3.Error as e:
        print(f"建立資料庫時發生錯誤: {e}")


def read_members_data():
    """讀取 members.txt 檔案，匯入 members 資料表"""
    try:
        conn = sqlite3.connect('wanghong.db')
        cursor = conn.cursor()
        total_changes = 0
        with open('members.txt', 'r', encoding='UTF-8') as f:
            lines = f.readlines()
            for line in lines:
                data = line.strip().split(',')
                if len(data) == 3:
                    cursor.execute('''
                        INSERT INTO members (mname, msex, mphone)
                        VALUES (?, ?, ?)
                    ''', (data[0], data[1], data[2]))
                    total_changes += cursor.rowcount
        conn.commit()
        conn.close()
        print(f"異動 {total_changes} 筆記錄")

    except (sqlite3.Error, FileNotFoundError) as e:
        print(f"匯入資料時發生錯誤: {e}")


def all_data():
    """顯示所有紀錄"""
    try:
        conn = sqlite3.connect('wanghong.db')
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM members')
        records = cursor.fetchall()

        if len(records) > 0:
            print("{:<8}{:<3}{:<6}".format("姓名", "性別", "手機"))
            for record in records:
                name = record[1]
                sex = record[2]
                phone = record[3]
                print("{:<8}{:<5}{:<10}".format(name, sex, phone))
        else:
            print(f'{"=>查無資料"}')
        conn.close()
    except sqlite3.Error as e:
        print(f"顯示紀錄時發生錯誤: {e}")


def add_data():
    """新增紀錄"""
    try:
        conn = sqlite3.connect('wanghong.db')
        cursor = conn.cursor()

        name = input("請輸入姓名: ")
        sex = input("請輸入性別: ")
        phone = input("請輸入手機: ")

        cursor.execute('''
            INSERT INTO members (mname, msex, mphone)
            VALUES (?, ?, ?)
        ''', (name, sex, phone))

        conn.commit()
        conn.close()
        print(f'{"=>異動 1 筆記錄"}')
    except sqlite3.Error as e:
        print(f"新增記錄時發生錯誤: {e}")


def modify_data():
    """修改紀錄"""
    try:
        conn = sqlite3.connect('wanghong.db')
        cursor = conn.cursor()

        name_modify = input("請輸入想修改記錄的姓名: ")
        if name_modify:
            new_gender = input("請輸入要改變的性別: ")
            new_phone = input("請輸入要改變的手機: ")

            cursor.execute('''
                SELECT * FROM members WHERE mname = ?
            ''', (name_modify,))
            data = cursor.fetchone()

            if data:
                print()
                print(f'{"原資料："}')
                print(f"姓名：{data[1]}，性別：{data[2]}，手機：{data[3]}")
                cursor.execute('''
                    UPDATE members SET msex = ?, mphone = ? WHERE mname = ?
                ''', (new_gender, new_phone, name_modify))
                conn.commit()

                print(f'{"=>異動 1 筆記錄"}')
                cursor.execute('''
                    SELECT * FROM members WHERE mname = ?
                ''', (name_modify,))
                modified_data = cursor.fetchone()
                print(f'{"修改後資料："}')
                print(f'姓名：{modified_data[1]}，'
                      f'性別：{modified_data[2]}，'
                      f'手機：{modified_data[3]}')
            else:
                print(f'{"=>找不到姓名的紀錄"}')
        else:
            print(f'{"=>必須指定姓名才可修改記錄"}')

        conn.close()
    except sqlite3.Error as e:
        print(f"修改記錄時發生錯誤: {e}")


def search_phone():
    """查詢手機紀錄"""
    try:
        conn = sqlite3.connect('wanghong.db')
        cursor = conn.cursor()

        phone_number = input("請輸入想查詢記錄的手機: ")
        cursor.execute('''
            SELECT * FROM members WHERE mphone = ?
        ''', (phone_number,))
        data = cursor.fetchall()

        if len(data) > 0:
            print("{:<8}{:<3}{:<6}".format("姓名", "性別", "手機"))
            for data in data:
                print("{:<8}{:<5}{:<10}".format(data[1], data[2], data[3]))
        else:
            print(f'{"=>查無手機號碼"}')

        conn.close()
    except sqlite3.Error as e:
        print(f"查詢時發生錯誤: {e}")


def delete_all_records():
    """刪除資料庫資料"""
    try:
        conn = sqlite3.connect('wanghong.db')
        cursor = conn.cursor()

        cursor.execute('DELETE FROM members')
        conn.commit()

        num_deleted = cursor.rowcount
        print(f"異動 {num_deleted} 筆記錄")

        conn.close()
    except sqlite3.Error as e:
        print(f"刪除記錄時發生錯誤: {e}")
