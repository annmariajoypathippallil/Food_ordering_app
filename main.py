import admin
import user
import re
import getpass
import pyttsx3
import threading

user_object = user.User()
admin_object=admin.Admin()
user_input = ""
admin_object.adding_new_food_items("abc","100ml","100","3","1")
admin_object.adding_new_food_items("abghjg","100ml","100","13","5")
admin_object.adding_new_food_items("ghghghggjhg","100ml","1097","13","5")


def play_string(text):
    engine = pyttsx3.init()
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate - 30)
    engine.say(text)
    engine.runAndWait()


# *************************************************************************User Starts**************************************************************************
def validate_email(email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, email):
            return True
        
def validate_password(passwd):
    password_regex = r'^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$'
    if re.match(password_regex, passwd):
        return True
    
def validate_phone(phone):
    phone_regex = r'^(\+91[\-\s]?)?[0]?(91)?[789]\d{9}$'
    if re.match(phone_regex, phone):
        return True

def validate_user_input(user_input):
    user_input_regex = r'^\d+(,\d+)*$'
    if re.match(user_input_regex, user_input):
        return True

def register():
    full_name = input('Enter your full name: ')
    phone_number = input('Enter your phone number: ')
    phone_validate = validate_phone(phone_number)
    if phone_validate==None:
        print('Invalid phone number!')
        return
    email = input('Enter your email: ')
    email_validate = validate_email(email)
    if email_validate==None:
        print('Invalid email!')
        return
    address = input('Enter your address: ')
    password = getpass.getpass('Enter your password: ')
    conf_password = getpass.getpass('Re-enter your password: ')
    if password==conf_password:
        password_validate = validate_password(password)
        if password_validate==None:
            print('Please create a password with the below criterias\n1. Minimum 8 characters\n2. Maximum 16 characters\n3. Atleast one symbol\n4. Atleast one capital letter\n5. Atleast one small letter')
            return
    else:
        print('Passwords are not matching!')
        return
    
    # full_name = 'Ann'
    # phone_number = '90'
    # email = 'e'
    # address = 'ASD'
    # password = 'as'
    res = user_object.register_on_the_application(full_name, phone_number, email, address, password)
    if res:
        print('\nYour account has been successfully created')
        play_string('Your account has been successfully created')
    else:
        print('\nExisting user, Please login!')
        play_string('Existing user, Please login!')


def login_user():
    if user_object.USER_PHONE_NUMBER=="":
        phone_number = input('Enter your phone number: ')
        password = getpass.getpass('Enter your password: ')

        # phone_number = '90'
        # password = 'as'
        res = user_object.user_login(phone_number, password)
        if res==0:
            print('\nYou have successfully logged in to Zomato')
            play_string('You have successfully logged in to Zomato')
        elif res==1:
            print('\nIncorrect username or password')
            play_string('Incorrect username or password')
        elif res==2:
            print('\nPlease register to Zomato')
            play_string('Please register to Zomato')
    else:
        print('\nYou are already logged in to Zomato')
        play_string('You are already logged in to Zomato')


def new_order():
    admin_object.display_list_of_food_items('user')
    if user_object.USER_PHONE_NUMBER!="":
        def task1():
            play_string('Please select the index of food items seperated by comma')
        def task2():
            global user_input 
            user_input = input('Please select the index of food items seperated by comma: ')
        thread1 = threading.Thread(target=task1)
        thread2 = threading.Thread(target=task2)
        thread1.start()
        thread2.start()

        thread1.join()
        thread2.join()
        user_input_validate = validate_user_input(user_input)
        if user_input_validate==None:
            print('\nPlease select a valid food index')
            play_string('Please select a valid food index')
            return
        res = user_object.place_new_order(user_input)
        if res==None:
            print('Your order has been confirmed, You can view it in order history')
            play_string('Your order has been confirmed, You can view it in order history')
        else:
            print('Your valid selected orders have been confirmed')
            print('Some orders have been rejected as it is invalid! -->', res)
            play_string('Your valid selected orders have been confirmed but Some orders have been rejected as it is invalid!')
    else:
        print('\nPlease login to place order!')
        play_string('Please login to place order!')


def order_history():
    if user_object.USER_PHONE_NUMBER!="":
        user_object.display_order_history()
    else:
        print('\nPlease login to view your order history!')
    

def update_profile():
    if user_object.USER_PHONE_NUMBER!="":
        user_object.update_profile()
    else:
        print('\nPlease login to view profile!')


def view_profile():
    if user_object.USER_PHONE_NUMBER!="":
        user_object.display_profile()
    else:
        print('\nPlease login to view profile!')


def user_logout():
    if user_object.USER_PHONE_NUMBER=="":
        print('\nYou are not logged in to Zomato!')
    else:
        res = user_object.logout()
        if res:
            print('\nYou have been successfully logged out of Zomato')
            print('\nThank you for using Zomato')

def user_activity():
    while(True):
        print('\n')
        print('-----------------------------------------------')
        print('|              Welcome to Zomato              |')
        print('-----------------------------------------------')
        print('| 1. Register                                 |')
        print('| 2. Login                                    |')
        print('| 3. Place Order                              |')
        print('| 4. View Order History                       |')
        print('| 5. Update Profile                           |')
        print('| 6. View Profile                             |')
        print('| 7. Logout                                   |')
        print('| 8. Exit                                     |')
        print('-----------------------------------------------')
        option = input('Please select an option to continue: ')
        if option=='1':
            register()
        elif option=='2':
            login_user()
        elif option=='3':
            new_order()
        elif option=='4':
            order_history()
        elif option=='5':
            update_profile()
        elif option=='6':
            view_profile()
        elif option=='7':
            user_logout()
        elif option=='8':
            break
        else:
            print('Invalid Entry!\n\n')

# *************************************************************************User Ends**************************************************************************



# *************************************************************************Admin Starts**************************************************************************
def admin_login():
    #Entering the crediantians for login
    username=input("Enter the username: ")
    password=input("Enter the password: ")
    res = admin_object.login(username,password)
    if res :
        print("You are succesfully logged in as admin!\n")
    else:
        print("Incorrect Username or Password!\n")

def add_food():
    if admin_object.ADMIN_ACTIVE:
        name = input('Enter food name: ')

        temp_quantity_type = input('Enter the amount of quantity \n1. ml\n2. gm\n3. pieces\n')
        if temp_quantity_type == '1':
            quantity_type = 'ml' 
        elif temp_quantity_type == '2':
            quantity_type = 'gm' 
        elif temp_quantity_type == '3':
            quantity_type = 'pieces'
        else:
            print('Invalid Entry!')
            return False

        try:
            quantity = int(input("Enter the quantity: "))
            quantity = str(quantity)+" "+quantity_type
        except:
            print('Invalid Entry')
            return False
        
        try:
            price = float(input('Enter food price: '))
        except:
            print("Incorrect Entry!")
            return False
           
        try:
            discount = int(input('Enter food discount (in %): '))
        except:
            print("Incorrect Entry!")
            return False
        
        try:
            stock = int(input('Enter food stock: '))
        except:
            print("Incorrect Entry!")
            return False  

        res = admin_object.adding_new_food_items(name, quantity, price, discount, stock)
        if res:
            print('New Food has been added successfully')
    else:
        print('Please login to add food!\n')

def view_food():
    if admin_object.ADMIN_ACTIVE:
        admin_object.display_list_of_food_items()
    else:
        print('Please login to view food!\n')


def edit_food():
    if admin_object.ADMIN_ACTIVE:
        id=int(input("Enter th Food ID:"))
        admin_object.editing_food_items_with_food_id(id)
    else:
        print('Please login to edit food!\n')


def delete_food():
    if admin_object.ADMIN_ACTIVE:
        id=int(input("Enter th Food ID:"))
        admin_object.removing_food_item_using_id(id)
    else:
        print('Please login to delete food!\n')
    

        


def admin_activity():
    while(True):
        print('\n')
        print('-----------------------------------------------')
        print('|              Welcome to Admin               |')
        print('-----------------------------------------------')
        print('| 1. Login                                    |')
        print('| 2. Add Food                                 |')
        print('| 3. Edit Food                                |')
        print('| 4. View Food                                |')
        print('| 5. Delete Food                              |')
        print('| 6. Exit                                     |')
        print('-----------------------------------------------')
        option = input('Please select an option to continue: ')
        if option=='1':
            admin_login()
        elif option=='2':
            add_food()
        elif option=='3':
            edit_food()
        elif option=='4':
            view_food()
        elif option=='5':
            delete_food()
        elif option=='6':
            break
        else:
            print('Invalid Entry!\n\n')


# *************************************************************************Admin Ends**************************************************************************

while(True):
    print('-----------------------------------------------')
    print('|              Welcome to Zomato              |')
    print('-----------------------------------------------')
    print('| 1. Admin                                    |')
    print('| 2. User                                     |')
    print('| 3. Exit                                     |')
    print('-----------------------------------------------')
    option = input('Please select an option to continue: ')
    if option=='1':
        admin_activity()
    elif option=='2':
        user_activity()
    elif option=='3':
        break
    else:
        print('Invalid Entry!\n\n')



if '__name__' == '__main__':
    pass