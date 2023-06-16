from prettytable import PrettyTable as PT
import user
class Admin:
    ADMIN_CREDENTIALS = {"a":"a"}
    FOOD_ITEMS = {}
    FOOD_ID = 1000
    INDEX = 1
    ADMIN_ACTIVE = False

    # item = {'food_id':[name, qua, price]}

    # Login
    def login(self,user_name,password):
        for i in self.ADMIN_CREDENTIALS.keys():
            if user_name==i and password== self.ADMIN_CREDENTIALS[i]:
                self.ADMIN_ACTIVE = True
                user_obj = user.User()
                return True
            else:
                return False



    # 1. Add new food items. 
    def adding_new_food_items(self,name,quantity,price,discount,stock):
        discounted_price = (int(price)*(1-(int(discount)/100)))
        discounted_price = round(discounted_price, 2)
        #  discounted_price = (1-(int(self.FOOD_ITEMS[key]['discount']))/100)*int(self.FOOD_ITEMS[key]['price'])
        temp_dict = {
            'index':self.INDEX,
            'name': name, 
            'quantity':quantity,
            'price':price,
            'discount':discount,
            'stock':stock,
            'discounted_price': discounted_price
            }
        self.FOOD_ITEMS[self.FOOD_ID] = temp_dict
        self.FOOD_ID += 1
        self.INDEX += 1
        return True
        # print (self.FOOD_ITEMS.keys())

    

     #  2. Edit food items using FoodID.
    def editing_food_items_with_food_id(self,id):
        if id not in self.FOOD_ITEMS.keys():
            return False
        else:
            item_to_be_edited=int(input("Which one do you want to edit?\n1. Name\n2. Quantity\n3. Price\n4. Stock\n"))
            if(item_to_be_edited==1):
                new_name = str(input("Enter the new name: "))
                self.FOOD_ITEMS[id]['name']=new_name
                return True
            elif(item_to_be_edited==2):
                new_quandity=str(input("Enter the new quandity: "))
                self.FOOD_ITEMS[id]['quantity']=new_quandity
            elif(item_to_be_edited==3):
                new_price=int(input("Enter the new price: "))
                self.FOOD_ITEMS[id]['price']=new_price
            elif(item_to_be_edited==4):
                new_stock=int(input("Enter the updated stock: "))
                self.FOOD_ITEMS[id]['stock']=new_stock
            else:
                print("Invalid entry!")



    # 3. View the list of all food items.
    def display_list_of_food_items(self, user='admin'):
        x = PT()
        if user=='admin':
            x.field_names = ['Food ID', 'Index', 'Name', 'Quantity', 'Price', 'Discount(%)', 'Stock',  'Discounted Price']
        else:
            x.field_names = ['Index', 'Name', 'Quantity', 'Price', 'Discount(%)', 'Stock',  'Discounted Price']
        
        # for  i, j in self.FOOD_ITEMS.items():
        #     print(i, j)
        for key, value in self.FOOD_ITEMS.items():
            items_temp_list = []
            if user=='user':
                if int(value['stock'])<1:
                    continue
            if user=='admin':
                items_temp_list.append(key) #Food ID
            for field_name, field_value in value.items():                    
                if field_name=='discounted_price' or field_name=='price':
                    field_value = 'Rs '+str(field_value)
                items_temp_list.append(field_value)
            x.add_row(items_temp_list)
        print(x)
            # print('Discounted Price : Rs', discounted_price)
        print('\n')



    # 4. Remove a food item from the menu using FoodID
    def removing_food_item_using_id(self,id):
        if id not in self.FOOD_ITEMS.keys():
            return False
        else:
            del self.FOOD_ITEMS[id]
            return True
        


if __name__=='__main__':
    admin_object = Admin()
    # admin.login('Ann','Ann@2805')
    admin_object.adding_new_food_items("abc","100ml","100","3","0")
    admin_object.adding_new_food_items("abghjg","100ml","100","13","5")
    admin_object.adding_new_food_items("ghghghggjhg","100ml","1097","13","5")
    # admin_object.display_list_of_food_items()
    # # admin_object.editing_food_items_with_food_id(1000)
    admin_object.display_list_of_food_items()
    # admin_object.removing_food_item_using_id(1000)
    # admin_object.display_list_of_food_items()
