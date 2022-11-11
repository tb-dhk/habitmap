import mysql.connector
import hashlib
import json
import getpass
import toml
import os
import dotenv
import random

dotenv.load_dotenv()

mydb = mysql.connector.connect(
    host = os.getenv("host"),
    user = os.getenv("user"),
    password = os.getenv("password"),
    port = os.getenv("port"),
)
cursor = mydb.cursor(buffered=True)

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
    edic = json.dumps(edic).replace(r"\\", "").strip(r"'\\").strip('"').replace("'", "")
    print([econ])
    econ = toml.loads(econ.replace(r"\\", "").strip(r"'\\").strip('"'))
    if (edic in [{}, "null", None] and econ in [{}, "null", None]) and (dic in [{}, "null", None] and con in [{}, "null", None]):
        print("you have no data to import or export. happy habit tracking!")
    elif (edic not in [{}, "null", None] or econ not in [{}, "null", None]) and (dic in [{}, "null", None] and con in [{}, "null", None]):
        prompt = input("you have no data saved locally but you have data on the cloud. would you like to import from the cloud? (Y/n) ")
        if prompt == "n":
            print("import aborted.")
        else:
            dic = edic
            con = econ
    elif (edic in [{}, "null", None] and econ in [{},"null",  None]) and (dic not in [{}, "null", None] or con not in [{}, "null", None]):
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
    
    edic = json.loads(json.dumps(edic).replace(r"\\", ""))
    econ = toml.loads(toml.dumps(econ).replace(r"\\", ""))
    dic = json.loads(json.dumps(dic).replace(r"\\", ""))
    con = toml.loads(toml.dumps(con).replace(r"\\", ""))
    json.dump(dic, open('stats.json', 'w'), default=str)
    toml.dump(con, open('config.toml', 'w'))
    if edic == None:
        edic = {}
    if econ == None:
        econ = {}
    cursor.execute(f"""
        UPDATE
            accounts
        SET
            data = "{edic}",
            config = "{econ}"
        WHERE
            username = '{user}';
    """)

    mydb.commit()
    print("data synced successfully.")

def logout(acct, dic, sett):
    if acct["loggedin"]:
        prompt = input("are you sure you would like to log out? (y/N) ")
        if prompt == "y":
            print("logging out...")
            acct["loggedin"] = False
            acct["username"] = ""
            toml.dump(acct, open('.account.toml', 'w'))
            json.dump(dic, open('stats.json', 'w'), default=str)
            toml.dump(sett, open('config.toml', 'w'))
        else:
            print("logout abort.")
    else:
        print("you are already logged out.")

def login(acct, dic, sett):
    print("logging in...")
    if acct["loggedin"]:
        prompt = input("you are already logged in. would you like to log out? (y/N) ")
        if prompt == "y":
            logout(acct, dic, sett)
            login(acct, dic, sett)
        else:
            print("logout abort.")
    else:
        username = input("enter username: ")
        acct["username"] = username
        password = getpass.getpass("enter password: ")
        maindb = os.getenv("database")
        cursor.execute(f"use {maindb};")
        cursor.execute("select * from accounts;")
        result = cursor.fetchall()

        fuser = False
        for row in result:
            if row[0] == username:
                account = row
                fuser = True
                if hashlib.sha3_512((password + row[1]).encode()).hexdigest() == row[2]:
                    acct["loggedin"] = True
                    print("login successful!")
                else:
                    print("invalid credentials. please try again.")
                    exit()

        if not fuser:
            prompt = input("this username is not registered. would you like to create a new account? (Y/n) ")
            if prompt == "n":
                print("signup aborted.")
                exit()
            else:
                print("creating account...")
                salt = gensalt(username, password)
                hpwd = hashlib.sha3_512((password + salt).encode()).hexdigest()
                id = hashlib.sha3_512(str(random.random()).encode()).hexdigest()
                cursor.execute(f"""
                insert into
                    `accounts` (`username`, `salt`, `password`, `data`, `config`, `id`, `discord`)
                values
                    ('{username}', '{salt}', '{hpwd}', '{r"{}"}', '{r"{}"}', '{id}', '');
                """)
                acct["loggedin"] = True
        
        try:
            edic = account[3]
        except:
            edic = {}

        try:
            esett = account[4]
        except:
            esett = {}
            
        sync(username, dic, edic, sett, esett)
        mydb.commit()
    
        toml.dump(acct, open('.account.toml', 'w'))
        print()
        if dic in ["none", None]:
            dic = {}
        return dic

def editacct(acct, det, new):
    if acct["loggedin"]:
        maindb = os.getenv("database")
        cursor.execute(f"use {maindb};")
        cursor.execute("select * from accounts;")
        result = cursor.fetchall()
        fuser = False

        for row in result:
            if row[0] == acct["username"]:
                fuser = True
                account = row
                break

        if fuser:
            if det in ["username", "password"]:
                prompt = input(f"are you sure you would like to change {det}? (y/N) ")
                if prompt == "y":
                    verify = getpass.getpass(f"enter your current {det} to verify: ")
                    if det == "username":
                        if verify == acct["username"]:
                            print("username verified.")
                            acct["username"] = new
                            cursor.execute(f"""
                                UPDATE
                                    accounts
                                SET
                                    username = '{new}'
                                WHERE
                                    id = '{account[5]}';
                            """)
                            toml.dump(acct, open('.account.toml', 'w'))
                            mydb.commit()
                            print(f"your username is now {new}.")
                        else:
                            print("invalid username.")
                    elif det == "password":
                        if hashlib.sha3_512((verify + account[1]).encode()).hexdigest() == account[2]:
                            print("password verified.")
                            cursor.execute(f"""
                                UPDATE
                                    accounts
                                SET
                                    salt = '{gensalt(account[0], new)}',
                                    password = '{hashlib.sha3_512((new + gensalt(account[0], new)).encode()).hexdigest()}'
                                WHERE
                                    username = '{acct["username"]}';
                            """)
                            mydb.commit()
                            print(f"your password has been changed.")
                        else:
                            print("invalid password.")
            else:
                print("invalid credential.")
    else:
        print("please login first.")

def removeacct(acct, dic, sett):
    if acct["loggedin"]:
        prompt = input("are you sure you would like to remove your account? (y/N) ")
        if prompt == "y":
            maindb = os.getenv("database")
            cursor.execute(f"use {maindb};")
            cursor.execute("select * from accounts;")
            uname = acct["username"]
            cursor.execute(f"delete from accounts where username = '{uname}'")
            mydb.commit()
            print("account successfully deleted.")
            prompt = ("would you like to keep your data? (Y/n)")
            if prompt != "n":
                print("logging out...")
                acct["loggedin"] = False
                acct["username"] = ""
                toml.dump(acct, open('.account.toml', 'w'))
                json.dump(dic, open('stats.json', 'w'), default=str)
                toml.dump(sett, open('config.toml', 'w'))
            else:
                print("deleting local data...")
                acct["loggedin"] = False
                acct["username"] = ""
                toml.dump({}, open('.account.toml', 'w'))
                json.dump({}, open('stats.json', 'w'), default=str)
                toml.dump({}, open('config.toml', 'w'))
    else:
        print("you are not logged in.")
