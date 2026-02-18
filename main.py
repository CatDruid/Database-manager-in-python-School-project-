import configparser as cfp
import psycopg as db
from pathlib import Path

## Main Global vars
openMenu = True

#config vars
CONFIG_NAME='config.ini'
config = cfp.ConfigParser()
configPath = Path(CONFIG_NAME)

#DB vars
conn = None

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
            "Database_Name": "changemetodatabasename",
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
        print('Database connected successfully')
        return True
    except Exception as e:
        print(f'Error: {e}')
        return False
    
def db_sqlexec(sql:str) -> bool:
    global conn
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
    except BaseException:
        conn.rollback()
        return False
    else:
        conn.commit()
        return True
    
def db_sqlread(sql:str) -> bool:
    global conn
    cursor = conn.cursor()
    try:
        record = cursor.execute(sql).fetchone()

        for record in cursor.execute(sql):
            print(record)

    except Exception as e:
        print(f'Error: {e}')
        return False

def db_sqlgen(table:str ,type:str, argtype:list, args:list ) -> tuple[str, bool]:

    argstr = ''
    valuestr = ''

    if len(argtype) != len(args):
        print('Debug Error: Uneven length of argtype && args')
        return "", False
    

    for i in range(len(argtype)):
        if i == len(argtype):
            argstr += f'{argtype[i]}'
        else:
            argstr += f'{argtype[i]}, '

    
    
    match type:
        case "insert":
            sql = f"insert intro {table}({argstr}) values ({valuestr})"
            return sql, True
        case _:
            print('Debug Error: Unmatching type in sqlgen')

def handle(f:function) -> bool:
    try:
        if f() == True:
            return True
    except Exception as e:
        print(f'Error: {e}')
        return False

def init() -> bool:
    INIT_LIST = [config_init, db_init]
    for i in INIT_LIST:
        if handle(i):
            continue
        else:
            return False
    return True

def customer_menu() -> bool:
    menu = True
    while menu:
        print(
            "Customer menu: \n" +
            "1. See current customers \n" +
            "2. Add a customer \n" +
            "3. Remove a customer \n" +
            "4. Edit a customer" 
        )
        inp = input()
        match inp.lower():
            case "1":
                print('Multiple input options will now appear\n' + 'Only input a single entry on each line\n' + "Only enter the asked datatype\n")
                customer_args = ['address', 'birth_date', 'city', 'first_name', 'last_name', 'postal_code']
                adress = input('Customers adress: ')
                birth_date = input('Birth date[****-**-**]: ')
                city = input('City: ')
                first_name = input('First name: ')
                last_name = input('Last name: ')
                postcode = input('Postal code[***-**]: ')
                sql = db_sqlgen('customer','insert',customer_args, [adress,birth_date,city,first_name,last_name,postcode])
                if db_sqlexec(sql):
                    print('successfully added the customer')

            case "2":
                pass
            case "3":
                pass
            case "4":
                pass
            case "q":
                menu = False
                break
            case _:
                print('Unrecognized command')



def main():

    #globals
    global openMenu
    global conn

    if init():
        print('Initialization successfull')
    else:
        openMenu = False

    while openMenu:
        print(
    "DB manager \n" +
    "1. Customer Management \n" +
    "2. Employee Management \n" +
    "3. Inventory Management \n" +
    "4. Order Managemant \n" +
    "q. quit"
    )
        inp = input('Enter your choice: ')
        match inp.lower().strip('.'):
            case "1":
                handle(customer_menu)
            case "q":
                openMenu = False
                break
            case _:
                print('Unrecognized command')
        
    if openMenu is not True:
        print('Shutting down')
        if conn:
            conn.close()
        _ = input('Press any key to continue')
        exit()

if __name__ == '__main__':
    main()