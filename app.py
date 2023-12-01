from lib import check_pass
from lib import menu, create_database, read_members_data, all_data, add_data
from lib import modify_data, search_phone, delete_all_records

username = input("請輸入帳號：")
password = input("請輸入密碼：")

while True:
    if check_pass(username, password):
        print()
        n = menu()
        if n == 0:
            break
        elif n == 1:
            create_database()
        elif n == 2:
            read_members_data()
        elif n == 3:
            all_data()
        elif n == 4:
            add_data()
        elif n == 5:
            modify_data()
        elif n == 6:
            search_phone()
        elif n == 7:
            delete_all_records()

    else:
        print(f'{"=>帳密錯誤，程式結束"}')
        break
