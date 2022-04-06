import requests
import pandas as pd
import idgen

df = pd.read_excel('data.xlsx', index_col=None)

def is_exist_user(user_name, bpn):
    r = requests.get(f'http://localhost:8000/user?user_name={user_name}&back_phone_number={bpn}')

    if r.status_code==200:
        return True
    else:
        return False

def insert_user(user_name, bpn):
    data = {'user_name': user_name, 'back_phone_number': bpn}
    r = requests.post('http://localhost:8000/user', json=data,
    headers={"Content-Type": "application/json; charset=utf-8"})
    print(r.text)

def create_challange_log(challange_id, user_id, now_date, status, link=None, is_duplicate=False):
    data = {
        'challange_id': challange_id,
        'user_id': user_id,
        'now_date': now_date,
        'status': status,
        'link': link,
        'is_duplicate': is_duplicate
    }
    r = requests.post('http://localhost:8000/challange/participate', json=data,
    headers={"Content-Type": "application/json; charset=utf-8"})

if __name__=="__main__":
    now_date = input("날짜(2022-xx-xx): ")
    status = input("상태(SUCCESS/FAIL/EXCEPT): ")
    challange_id = int(input("챌린지 ID: "))

    for index, row in df.iterrows():
        user_name = row['user_name']
        user_name = user_name.replace(" ", "")

        bpn = str(row['back_phone_number'])
        bpn = bpn.replace(" ", "")
        if len(bpn) != 4:
            bpn = '0'*(4-len(bpn))+bpn
        
        user_id = idgen.id_generator(user_name, bpn)
        if not is_exist_user(user_name, bpn):
            insert_user(user_name, bpn)
        
        if status=="EXCEPT":
            create_challange_log(challange_id, user_id, now_date, status)
        else:
            link = row['link']
            create_challange_log(challange_id, user_id, now_date, status, link)
