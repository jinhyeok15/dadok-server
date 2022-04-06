import pandas as pd

df = pd.read_excel('data.xlsx', index_col=None)

def id_generator(user_name, back_phone_number):
    user_name_id = "".join([str(ord(s)) for s in user_name])
    return user_name_id + back_phone_number


def remove_duplicated_row(df):
    return df.drop_duplicates(subset=['id'], keep='last')


if __name__=="__main__":
    for index, row in df.iterrows():
        user_name = row['user_name']
        user_name = user_name.replace(" ", "")
        df.loc[index, 'user_name'] = user_name
        bpn = str(row['back_phone_number'])
        bpn = bpn.replace(" ", "")
        if len(bpn) != 4:
            bpn = '0'*(4-len(bpn))+bpn
        df.loc[index, 'back_phone_number'] = bpn
        df.loc[index, 'id'] = id_generator(user_name, bpn)

    df = remove_duplicated_row(df)

    df.to_excel('save.xlsx')
