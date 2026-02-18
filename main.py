import configparser as confp
import psycopg as db
from pathlib import Path

## Main Global vars
openMenu = True

#config vars
CONFIG_NAME='config.ini'
config = confp.ConfigParser()
configPath = Path(CONFIG_NAME)

#DB vars
conn = None
cursor = None

def config_init() -> bool:
    global openMenu
    global config
    if configPath.exists():
        print("Loading config")
        config.read(CONFIG_NAME)
        return True
    else:
        print("Config not found, Creating default config")
        config["DATABASE"] = {
            "Hostname": "localhost",
            "Port": "5432",
            "Database_Name": "changeme to database name",
            "Username": "postgres",
            "Password": "changeme"
            }
        with open(CONFIG_NAME, 'w') as f:
            config.write(f)
        print('Config created successfully. Please input data into "config.ini" and restart program')
        openMenu = False
        return False
    
def db_init() -> bool:
    global conn
    global cursor
    global config

    try:
        conn = db.connect(
            f'''host={config["DATABASE"]["Hostname"]},
            port={config["DATABASE"]["Port"]},
            dbname={config["DATABASE"]["Database_Name"]},
            user={config["DATABASE"]["Username"]},
            pass={config["DATABASE"]["Password"]}
            '''
        )
        cursor = conn.cursor()
        print('Database connected successfully')
        return True
    except Exception as e:
        print('Error: {e}')
        return False

def flag_checker(f:function) -> bool:
    try:
        if f() == True:
            return True
    except Exception as e:
        print(f'Error: {e}')
        return False

def init() -> bool:
    INIT_LIST = [config_init, db_init]
    for i in INIT_LIST:
        if flag_checker(i):
            continue
        else:
            return False
    return True

def main():

    #globals
    global openMenu
    global conn
    global cursor

    

    if init():
        print('Initialization successfull')
    else:
        openMenu = False

    while openMenu:
        print('''
    DB manager
    1. 
    ''')
        
    if openMenu is not True:
        print('Shutting down')
        conn.close()
        input('Press any key to continue')
        exit()

if __name__ == '__main__':
    main()