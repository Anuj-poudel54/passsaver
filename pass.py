"""
This is the starting point of this pass saver program.

"""


from getpass import getpass
import dbh  # dbh = db handling.
from os import name, system, getcwd
from clipboard import copy

print(getcwd())

def clear_scr():
    """ Clears the screen """
    if name == 'nt':

        system('cls')
    else:

        system('clear')


def password(function):
    """ This runs the main function in it and also do gatepass check """

    tries = 3
    GATEKEY_LABEL = "gatePassword"
    gateKey, _ = dbh.get_pwd(GATEKEY_LABEL)

    if gateKey == "gatekey":
        print("\nYou must set the password for this app.")
        dbh.edit_password(GATEKEY_LABEL)

    changedGateKey, _ = dbh.get_pwd(GATEKEY_LABEL)
    while tries > 0:
        clear_scr()

        print(f"You got {tries} attemp left")

        if tries <= 0:
            print("You cannot try anymore!!")

        gatepass = getpass("Enter your gate password: ")
        if gatepass == changedGateKey:
            clear_scr()
            function()

        else:
            tries -= 1


def show_pass(pwd):
    """ Shows the password if 'show' is choosen for retrieving password """
    pwd = pwd.strip("'")
    a = str(input('Copy password??[y/n/(show)]: ')).lower()
    if a == 'y':
        copy(pwd)
        print("Copy successful!")

    elif a == 'show':
        print(f"Your password is '{pwd}'")
        copy(pwd)
        input()


# Main Function starts here

def main_func():
    """ Save, get, delete and changes password """

    while True:
        try:

            choose = input(
                "1--Save password\n2--Retrieve password:\n3--Change password\n4--Change label\n5--Show Labels\nd--DELETE saved password\n'e' To exit:\n#").strip().lower()

            if choose == '1':  # SAVE PASSWORD.
                addLabel = input("Enter label: ").lower()
                if len(addLabel) == 0:
                    print("You must enter the name of label.")
                    input()

                else:
                    dbh.add(addLabel)
                    input("Done!")

            elif choose == '2':  # RETRIEVE PASSWORD.
                label = input("Enter the label of password: ").lower().strip()
                if len(label) == 0:
                    print("you must enter the label of password you want to access.")

                else:
                    got_pwd, check = dbh.get_pwd(label)

                    if check:
                        show_pass(f"{got_pwd}")

                    else:
                        print(f"No password saved for {label}!")
                        save = input(
                            f"Do you want to save password for '{label}'[y/n]: ").lower()
                        if save == 'y':
                            dbh.add(label)

            elif choose == '3':  # Change the existing password
                label = input(
                    "Enter the label that you want to change password: ").lower()
                dbh.edit_password(label)
                print("Password Change successful!")

            elif choose == '4':  # Change the existing label
                label = input("Enter the old label you want to change: ")
                dbh.edit_label(label)

            elif choose == '5':  # Displays the saved labels
                labelList = dbh.showAllLabel()

                if len(labelList) > 1:
                    print("You have saved passwords of:")

                    index = 1
                    for label in labelList:
                        if label[0] != "gatePassword":
                            prLabel = f"{index}. {label[0]}"
                            index += 1
                            print(prLabel)
                else:
                    print("No passwords saved yet.")

                input()

            elif choose == 'd':  # Delete the password
                label = input("Enter the label: ").lower()
                dbh.delete(label)
                input()

            elif choose == 'e':
                clear_scr()
                exit()

            elif choose == 'cp' or choose == 'sp':
                dbh.edit_password("gatePassword")

            clear_scr()
        except ValueError as e:
            print(e)
            input()


if __name__ == '__main__':
    password(main_func)
