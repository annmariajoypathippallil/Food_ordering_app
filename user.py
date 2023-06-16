import admin
from prettytable import PrettyTable as PT
from datetime import datetime
import getpass
import re

class User:
    USER_LOGIN = {}
    USER_ORDER_HISTORY = {}
    USER_PHONE_NUMBER = ""
    

    #  1. Register on the application
    def register_on_the_application(self,full_name,phone_number,email,address,passwd):
        self.full_name = full_name
        self.phone_number = phone_number
        self.email = email
        self.address = address
        self.passwd = passwd
        temp_dict ={
                        "full_name":full_name,
                        "email":email,
                        "address":address,
                        "password":passwd
                    }
        if phone_number not in self.USER_LOGIN.keys():
             self.USER_LOGIN[self.phone_number]=temp_dict
             return True
        else:
            return False
   

    # 2. Log in to the application
    def user_login(self,phone_number,passwd):
        if phone_number in self.USER_LOGIN.keys():
            if self.USER_LOGIN[phone_number]['password']==passwd:
                self.USER_PHONE_NUMBER = phone_number
                return 0    # Login Success
            else:
                return 1    # Incorrect username or passswd
        else:
            return 2        # Please create an account!
   



    # 4. Place New Order
    def place_new_order(self, user_input):
        user_food_dict = {}
        table_header=PT()
        food_id_list=[]
        invalid_food_id_list = []
        admin_object = admin.Admin()

        user_input = user_input.split(',')
        for x in user_input:
            for i,j in  admin_object.FOOD_ITEMS.items():
                if  j['index'] == int(x):
                    food_id_list.append(i)
        else:
            invalid_food_id_list.append(x)

        #Fetching user items with food id
        total_price = 0
        headers_to_be_fetched = ['name', 'quantity', 'price', 'discount', 'discounted_price']
        for food_id in food_id_list:
            user_food_list_temp = []
            for food_id_admin in admin_object.FOOD_ITEMS.keys():
                if food_id==food_id_admin:
                    total_price += int(admin_object.FOOD_ITEMS[food_id_admin]['discounted_price'])
                    for header in headers_to_be_fetched:
                        user_food_list_temp.append(admin_object.FOOD_ITEMS[food_id_admin][header])
            user_food_dict[food_id] = user_food_list_temp
        
        print(invalid_food_id_list)
        table_header.field_names = ['Name', 'Quantity', 'Price', 'Discount(%)',  'Discounted Price']
        for key,values in user_food_dict.items():
            table_header.add_row(values)
        table_header.add_row(['', '', '', '', ''])
        total_price = 'Rs '+str(total_price)
        table_header.add_row(['', '', '', 'Total Price', total_price])
        print(table_header)
        try:
            order_confirming = input("Do you Want \n1.Confirm order \n2.Cancel order\n")
            if order_confirming == '1':
                self.order_confirmation(user_food_dict, self.USER_PHONE_NUMBER, invalid_food_id_list)
            elif order_confirming == '2':
                print("Your Order has cancelled!")
            else:
                print('Invalid option!')
        except Exception as e:
            print(e)
            # print('invalid response')


# if conf, minus 1 from stock of food


    # Order confirmation function
    def order_confirmation(self, user_food_dict, phone_number, invalid_food_id_list):
        admin_object = admin.Admin()
        # History table starts here
        
        temp_orders_list = []
        
        for order_list_key, order_list_value in user_food_dict.items():
            stock = admin_object.FOOD_ITEMS[order_list_key]['stock']
            stock = int(stock)-1
            admin_object.FOOD_ITEMS[order_list_key]['stock'] = stock
            # Current date is created and added here to the temp list
            current_datetime = datetime.now()
            formatted_date = current_datetime.strftime("%d-%m-%Y")
            formatted_time = current_datetime.strftime("%H:%M:%S")
            order_list_value.append(formatted_time)
            order_list_value.append(formatted_date)
            temp_orders_list.append(order_list_value)
            
        if phone_number not in self.USER_ORDER_HISTORY.keys():
            self.USER_ORDER_HISTORY[phone_number] = temp_orders_list
        else:
            value = self.USER_ORDER_HISTORY[phone_number]
            for i in temp_orders_list:
                value.append(i)
            self.USER_ORDER_HISTORY[phone_number] = value
            print(self.USER_ORDER_HISTORY[phone_number])


        return invalid_food_id_list       


        # Print order history
    def display_order_history(self):
        history_table=PT()
        history_table.field_names = ['Name', 'Quantity', 'Price', 'Discount(%)',  'Discounted Price', 'Time', 'Date']
        for phone in self.USER_ORDER_HISTORY.keys():
            if phone==self.USER_PHONE_NUMBER:
                for orders in self.USER_ORDER_HISTORY.values():
                    for order in orders:
                        history_table.add_row(order)

        print(history_table)            

    # 8. Update Profile: the user should be able to update their profile.
    def update_profile(self):
        try:
            user_update = int(input("Please select the field that you want to update: \n1. Full Name\n2. Email\n3. Address\n4. Password\n"))
            if user_update == 1:
                new_name = input("Enter new name: ")
                self.USER_LOGIN[self.USER_PHONE_NUMBER]['full_name'] = new_name
            elif user_update == 2:
                new_email = input("Enter email: ")
                validate = self.validate_email(new_email)
                if validate!=None:
                    self.USER_LOGIN[self.USER_PHONE_NUMBER]['email'] = new_email
                else:
                    print('Enter a valid email!')
            elif user_update ==3:
                new_address = input("Enter the new address: ")
                self.USER_LOGIN[self.USER_PHONE_NUMBER]['address'] = new_address
            elif user_update == 4:
                new_passwd = getpass.getpass("Enter new password: ")
                conf_password = getpass.getpass("Re-enter password: ")
                if new_passwd==conf_password:
                    validate = self.validate_password(new_passwd)
                    if validate!=None:
                        self.USER_LOGIN[self.USER_PHONE_NUMBER]['password'] = new_passwd
                    else:
                        print('Please create a password with the below criterias\n1. Minimum 8 characters\n2. Maximum 16 characters\n3. Atleast one symbol\n4. Atleast one capital letter\n5. Atleast one small letter')
                else:
                    print('Passwords are not matching')
            else :
                print("Invalid Entry")
        except:
            print('Please select a valid option!') 


    def display_profile(self):
        display_profile_table = PT()
        display_profile_table.field_names = ['Phone', 'Name', 'Email', 'Address', 'Password']
        temp_list = []
        phone_key = self.USER_PHONE_NUMBER
        temp_list.append(phone_key)
        for details in self.USER_LOGIN[self.USER_PHONE_NUMBER].keys():
            temp_list.append(self.USER_LOGIN[phone_key][details])
        display_profile_table.add_row(temp_list)
        print(display_profile_table)
                    
    
    def logout(self):
        self.USER_PHONE_NUMBER = "" 
        return True      


    def validate_email(self, email):
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if re.match(email_regex, email):
            return True
        
    def validate_password(self, passwd):
        password_regex = r"^(?=.*[A-Z])(?=.*[a-z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!%*#?&]{8,16}$"
        if re.match(password_regex, passwd):
            return True


        


if __name__=='__main__':   
    user_object = User()
    admin_object = admin.Admin()
    admin_object.adding_new_food_items("abc","100ml","1978","3","0")
    admin_object.adding_new_food_items("abghjg","100ml","1010","13","10")
    admin_object.adding_new_food_items("ghghghggjhg","100ml","1097","13","5")
    user_object.register_on_the_application("Ann","7025644086","annmariajoy199@gmail.com","32 c","Ann@2805")
    user_object.register_on_the_application("Jerin","8025694086","jerin1999@gmail.com","37 c","abc")
    user_object.register_on_the_application("Albin","9025644056","albin@gmail.com","32 c","xyz")
    user_object.update_profile()
    user_object.display_profile()

    # admin_object.display_list_of_food_items('user')
    # print('Before order')
    # admin_object.display_list_of_food_items('user')
    # user_object.place_new_order('1,2,3', '7025644056')
    # print('After order')
    # admin_object.display_list_of_food_items('user')
    # user_food_dict = {1000: ['abc', '100ml', '100', '3', 97.0], 1001: ['abghjg', '100ml', '100', '13', 87.0], 1002: ['ghghghggjhg', '100ml', '1097', '13', 954.39]}
    # user_object.order_confirmation(user_food_dict,'7025644056')

    # admin_object.display_list_of_food_items()
    # user_object.view()
    # user_object.user_login('1234567892',"xyz")
