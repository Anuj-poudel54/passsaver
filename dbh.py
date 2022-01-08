# Here i handeled and defined the logic and functions behind the database.


from enc_and_dec import enc, dec
import sqlite3
from os import getcwd

def does_label_exist(label):
    """ RETURNS TRUE IF THE LABEL ALREADY EXISTS IN DB. """
    with conn:
        c.execute("SELECT * FROM Savepass WHERE label=:checkLabel", {'checkLabel':label}) #### GIVES THE ALL DATA OF THE SELECTED DATA FROM ITS FIELD NAME.
        if len(c.fetchall()) == 0:
            return False
    return True             


def add(label):

    """ Add the new password """

    if not does_label_exist(label):

        if label == "gatePassword":
            password = "gatekey"
        else:            
            password = input(f"Enter your password for {label}: ")

        enc_pass = enc(password)

        with conn:
            c.execute("SELECT MAX(id) FROM Savepass")   ### THIS COMMAND GIVES THE LAST ID THAT WAS CREATED IN DB.
            lastId = c.fetchone()[0]                     #### THIS COMMAND GIVES THE THAT ID VALUE.
            try:
                newId = lastId + 1
            except TypeError:
                newId = 0


            c.execute("INSERT INTO Savepass VALUES (:id, :label, :password)", {'id':newId, 'label':label, 'password':enc_pass})

    else:
         print(f"label '{label}' already exist please try another!")         


def edit_label(oldlabel):
    """ Edits the label """

    if does_label_exist(oldlabel):
        newlabel = input(f"Enter your new label replacing '{oldlabel}': ")

        if does_label_exist(newlabel):
            print(f"Label {newlabel} already existed please try another!")

        else:
            with conn:
                c.execute("SELECT * FROM Savepass WHERE label = :label", {'label': oldlabel})
                id = c.fetchall()[0][0]

                c.execute("UPDATE Savepass SET label = :newLabel WHERE id = :id", {'newLabel':newlabel ,'id':id}) #### CHANGES THE SELECTED LABEL OF SELETED DATA.

            print("Label change successful!")
    else:
        print(f"No any label named {oldlabel} found!")
        


def edit_password(label):   #  Edits saved password. 

    if does_label_exist(label):
        if label == "gatePassword":
            while True:
                newpassword = input("Set your new gate password: ")
                if len(newpassword) > 0:
                    done = input("do you wana set this your gate password [y/n]: ").lower()
                    if done == "y":
                        break

        else:            
            newpassword = input("Enter your new password: ")
        enc_newpass = enc(newpassword)

        with conn:
            c.execute("UPDATE Savepass SET password = :newPass WHERE label = :label", {'newPass': enc_newpass, 'label': label})

    else:
        print(f"There is no any label called {label} is saved.")  


def get_pwd(label):
    """ HERE TRUE MEANS YES THERE IS PASSWORD SAVED YOU WANTED. """

    if does_label_exist(label):

        with conn:
            c.execute("SELECT * FROM Savepass WHERE label = :label", {'label': label})
            enc_pwd = c.fetchall()[0][2]
            dec_pwd = dec(enc_pwd)

        return dec_pwd, True

    else:
        return '', False


def delete(label):
    if does_label_exist(label):
            a = input("Do you really want todelete it permanently yes or no[y\n]:")
            if a == "y":
                with conn:
                    c.execute("DELETE from Savepass WHERE label = :label", {'label': label})
                    print("Deleted successfully!")

    else:
        print(f"Not found! check your spelling!")


def showAllLabel():
    """ Returns the sorted saved label """

    with conn:
        c.execute("SELECT label FROM Savepass")
        labelList = c.fetchall()
        
        return sorted(labelList)

############### CREATING CONNECTION TO THE DATABASE.

db_path = getcwd()+'\\pwd.db'
conn = sqlite3.connect(db_path)
c = conn.cursor()

####### Creating new database and saving initial gate password as 'gatekey' if the program is running for first time or db not found.
try:
    with conn:
        c.execute(""" CREATE TABLE Savepass (
            id integer AUTO_INCREMENT,
            label text,
            password text
        )""")
        pwd = enc("gatekey")
        c.execute("INSERT INTO Savepass VALUES(:id, :label, :pwd)", {'id': 0, 'label': 'gatePassword', 'pwd': pwd})
        
except sqlite3.OperationalError:
    pass
