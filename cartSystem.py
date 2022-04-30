#!/usr/bin/env python
# coding: utf-8



import sys
import warnings
import os
warnings.filterwarnings("ignore")



def ReadFileAndCreateCart():
    """
    READS Values from a Test files
    """
    #create a list to hold cart
    # the cart will have other sublist inside it that will contain details for the items selected
    cart = []
    with open("Product and price lists.txt" , "r") as f:
        for line in f.readlines():
            line = line.strip().split("=")
            if len(line)==1:
                pass
            else:
                try:
                    #read the first line
                    iten_list = [item.split("\'")[1].strip() for item in line[1].split(",")]
                except:
                    #read the second line
                    price_list = []
                    for item in line[1].split(","):
                        #ensure that the data is is the needed format
                        item = item.split("\'")[0]
                        item = item.split("]")[0].split()[0]
                        if len(item.split("["))>1:   
                            item = item.split("[")[1].strip()
                        price_list.append(float(item))
    f.close()
    #return the price , item and cart
    return iten_list , price_list , cart



# adding to cart
# ask for code , quantity , shipping method
# code and quantity must be int where 0<=code <=40  and   0 < quantity <=99
# if code = END|end  exit the program

def isValidCode(code):
    """
    @INPUT - > code  which is the product code to be selected
    @RETURN -> Bool whether the code meets some criteria
    returns false if code is not END or code<0 or code>39
    """
    #check first if it is end
    if code.upper() == "END":
        return True
    else:
        #use try-catch block in order to avoid program breaking because of int conversion
        try:
            #change to integer
            code = int(code)
        except ValueError:
            return False
        else:
            #check the criteria
            if int(code)>=0 and int(code) <= 39:
                return True
            else:
                return False
            

def isValidQuantity(quantity):
    """
    @INPUT -> quantity   which is the item amaount selected
    @RETURNS -> Bool 
    returns true if quantity is between 1 and 99
    """
    #convert to int
    try:
        quantity = int(quantity)
    except Exception as e:
        return False
    else:
        # check the condition
        if int(quantity) >0 and int(quantity)<=99:
            return True
        else:
            return False

def isValidShipping(ship_method):
    """
    @INPUT -> ship_method which is type of shipping
    @RETURNS -> Bool
    returns true if the method is either Pick-up or Delivery else false
    """
    #check if it is among the two
    if ship_method !="Pick-up" and ship_method != "Delivery":
        return False
    else:
        return True
    




def addRecord():
    """
    @INPUT -- > None as it is a function that alters cat.
    Main functionalities like adding to cart are here.
    Checks validity of the inputs first
    Follow up steps are perfomed depending on the input validity
    """
    # ask user for input always until the program is exited
    while True:
        #get inputs from the user
        code = input("Please enter the product code:  ")
        #exit if code is end
        if code.upper() == "END":
            #show the current cart
            showRecords(cart_items)
            print("\n\n")
            
            #call controller function again
            Controller()
            #exit
            break;
        
        else:
            quantity = input("Enter the Quantity:  ")
            #ask for delivery
            delivery_method = input("Enter Delivery Method (Delivery or Pick-Up):   ")
        
            #add to cart only when all are good
            if isValidCode(code) and isValidQuantity(quantity) and isValidShipping(delivery_method):
                print("All are good")
                code = int(code)
                quantity = int(quantity)
                #add to cart
                current_item = [code ,productList[code] , priceList[code] , quantity , delivery_method]
                cart_items.append(current_item)
                #add the current product to the main list
                print(f"Item with {code}  added to cart")

            #none of the input is correct    
            elif not isValidCode(code) and not isValidQuantity(quantity) and not isValidShipping(delivery_method) :
                print("Code , Shipping  and Quantity are not valid Valid")
            #only shipping is correct
            elif not isValidCode(code) and not isValidQuantity(quantity):
                print("Code and Quantity are not correct")
            #only code is correct
            elif not isValidQuantity(quantity) and not isValidShipping(delivery_method):
                print("Shipping and Quaantity are not correct")
            #only quantity is correct
            elif not isValidCode(code) and not isValidShipping(delivery_method):
                print("Shipping and code are not correct")
            #shipping not correct
            elif not isValidShipping(delivery_method):
                print("Shipping Method not corrected")
            #code ot correct
            elif not isValidCode(code):
                print("Code  not valid")
            #quantity not correct
            else:
                print("Quantity not valid")
            print("Items not Added to the Cart")
            print("\n\n")



def totalCost(cart):
    """
    @INPUT -> cart which is a list of items 
    Returns the total cost of the items in the list
    """
    total_cost = 0
    for item in cart:
        #check if the shipping is delievery
        if item[4] == "Delivery":
            #shipping fees is 10%
            total_item_price = 1.1*(item[2]*item[3])
        else:
            total_item_price = item[2]*item[3]
            
        total_cost =total_cost +  total_item_price
    return round(total_cost , 2)



# show all products function
def showRecords(cart):
    """
    @Input -> cart which is a list of items
    Prints all items in formatted method
    Returns none
    """
    #define format characters
    myspace = " "
    mydash = "-"
    #print the header
    #HERE column for Code has 10 space , Product=41 , Price =15 ,Qunatity=17 and Shipping method the rest.
    print(f"Code{myspace*6}Product{myspace*34}Price ${myspace*8}Quantity{myspace*9}Shipping Method")
    print(f"{mydash*5}{myspace*5}{mydash*36}{myspace*5}{mydash*10}{myspace*5}{mydash*12}{myspace*5}{mydash*15}")
    
    for each_item in cart:
        #In order to display the columns well formatted
        #WE will take the following formular to get the space remaining
        #TOTAL_SPACE  - len(current_string) as showing below
        print(f"{each_item[0]}{myspace*(10-(len(str(each_item[0]))))}{each_item[1]}{myspace*(41-(len(str(each_item[1]))))}{each_item[2]}{myspace*(15-(len(str(each_item[2]))))}{each_item[3]}{myspace*(17-(len(str(each_item[3]))))}{each_item[4]}")
        
    
    print("\n")
    #display cost
    print(f"Total Cost is  ${totalCost(cart)}")



def sortRecords(cart):
    """
    Uses Lambda function to sort the cart 
    We are only sorted depending on the first values of each sublist which is code
    Return sorted list
    """
    cart = sorted(cart, key=lambda item: item[0])
    showRecords(cart)




# search record
def searchRecord(cart):
    """
    Return a sorted cart with the Items that had keyword searched for
    """
    print("Search Results are ...")
    found_items = []
    #ask for the keyword
    keyword = input("Enter the keyword for the search:   ")
    for item in cart:
        #check if their is any element with the keyword
        if len([a for a in item if keyword in str(a)])>0:
            found_items.append(item)
    else:
        pass
    
    return sortRecords(found_items)




def Controller():
    """
    This is the controller function for the system
    """
    print("""
    1. Add Items to Cart  
    2. ShowRecords  
    3. Sort You Cart  
    4. Search for Items   
    Any Character to  Exit
    """)
    
    choice = input("Enter Choice:  ")
    
    if choice == "1":
        addRecord()
    elif choice == "2":
        showRecords(cart_items)
        #call the controller function after display
        print("\n\n")
        Controller()
    elif choice == "3":
        sortRecords(cart_items)
        #call the controller
        print("\n\n")
        Controller()
    elif choice == "4":
        searchRecord(cart_items)
        print("\n\n")
        Controller()
    else:
        print("\nEXITING...........\n")
        


# call the function to create cart and product information
#create the shooping items and empty cart from the list
# This variables are created globally
productList , priceList , cart_items =  ReadFileAndCreateCart()
# main function
def main():
    """
    These function is used to call all other functions
    """
    print("Welcome to Toowoomba Shopping Site")
    print("Please  select what you want to view\n")
    Controller()



#### run the whole program
main()






# In[ ]:





# In[ ]:




