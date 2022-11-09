import mysql.connector
import hashlib
import json
import getpass
import toml
import os
import dotenv

dotenv.load_dotenv()

mydb = mysql.connector.connect(
    host = os.getenv("host"),
    user = os.getenv("user"),
    password = os.getenv("password"),
    port = os.getenv("port"),
)

cursor = mydb.cursor()
try:
    dic = json.load(open('stats.json', 'r'))
except:
    dic = {}

try:
    sett = toml.load(open(os.getcwd()+'/config.toml'))
except:
    sett = {}

try:
    acct = toml.load(open(os.getcwd()+'/.account.toml'))
except:
    acct = {}

def gensalt(uid, pwd):
    alpha = "qweryuiopasdfghjklzxcvbnm"
    count = 0
    for x in uid:
        try:
            count += alpha.index(x) + 1
        except:
            count += ord(x) 
    for x in pwd:
        try:
            count += alpha.index(x) + 1
        except:
            count += ord(x)
    return hashlib.sha3_512(hex(count)[::-1].encode()).hexdigest()

def sync(user, dic, edic, con, econ):
    print("syncing database...")
    if (edic == {} and econ == {}) and (dic == {} and con == {}):
        print("you have no data to import or export. happy habit tracking!")
    elif (edic != {} or econ != {}) and (dic == {} and con == {}):
        prompt = input("you have no data saved locally but you have data on the cloud. would you like to import from the cloud? (Y/n) ")
        if prompt == "n":
            print("import aborted.")
        else:
            dic = edic
            con = econ
    elif (edic == {} and econ == {}) and (dic != {} or con != {}):
        prompt = input("you have no data on the cloud but you have data saved locally. would you like to export to the cloud? (Y/n) ")
        if prompt == "n":
            print("export aborted.")
        else:
            edic = dic
            econ = con
    else:
        if not(edic == dic and econ == con):
            while 1:
                prompt = input("you have data on the cloud and saved locally. please pick one data file to keep. (cloud/local) ")
                if prompt == "cloud":
                    dic = edic
                    con = econ
                    break
                elif prompt == "local":
                    edic = dic
                    econ = con
                    break
                else:
                    print("invalid. try again")
        else:
            print("your data on the cloud and your data saved locally are identical. happy habit tracking!")
    
    edic = json.dumps(edic)
    econ = toml.dumps(econ)
    json.dump(dic, open('stats.json', 'w'), default=str)
    toml.dump(con, open('config.toml', 'w'))
    cursor.execute(f"""
        UPDATE
            accounts
        SET
            data = '{edic}',
            config = '{econ}'
        WHERE
            username = '{user}';
    """)

    mydb.commit()
    print("data synced successfully.")

def logout():
    print("logging out...")
    acct["loggedin"] = False
    acct["username"] = ""
    toml.dump(acct, open('account.toml', 'w'))
    json.dump(dic, open('stats.json', 'w'), default=str)
    toml.dump(sett, open('config.toml', 'w'))

def login(acct):
    print("logging in...")
    if acct["loggedin"]:
        prompt = input("you are already logged in. would you like to log out? (y/N) ")
        if prompt == "y":
            logout()
        else:
            print("logout abort.")
    else:
        username = input("enter username: ")
        acct["username"] = username
        password = getpass.getpass("enter password: ")
        maindb = os.getenv("database")
        cursor.execute("use {maindb};")
        cursor.execute("select * from accounts;")
        result = cursor.fetchall()

        fuser = False
        acct = []
        for row in result:
            if row[0] == username:
                acct = row
                fuser = True
                if hashlib.sha3_512((password + row[1]).encode()).hexdigest() == row[2]:
                    print("login successful!")
                else:
                    print("invalid credentials. please try again.")
                    exit()

        if not fuser:
            prompt = input("this username is not registered. would you like to create a new account? (Y/n) ")
            if prompt == "n":
                print("signup aborted.")
            else:
                print("creating account...")
                salt = gensalt(username, password)
                hpwd = hashlib.sha3_512((password + salt).encode()).hexdigest()
                cursor.execute(f"""
                insert into
                    `accounts` (`username`, `salt`, `password`, `data`)
                values
                    ('{username}', '{salt}', '{hpwd}', '{r"{}"}');
                """)
        
        try:
            edic = acct[3]
        except:
            edic = {}

        try:
            esett = acct[5]
        except:
            esett = {}
            
        sync(username, dic, edic, sett, esett)
        mydb.commit()
    
        toml.dump(acct, open('account.toml', 'w'))
        return dic

def removeacct():
    pass
