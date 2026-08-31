def show_menu():
    print("1. Add stock")
    print("2. Remove stock")
    print("3. Show stock")
    print("4. Exit")






def show_stock(stock_dictionary):
    number = 1
    for name, amount in stock_dictionary.items():
        print(f"{number}. {name}: {amount}\n")
        number += 1







def add_stock(stock_dictionary):
    show_stock(stock_dictionary)   
    stock_input_modification = input("Enter the stock name or ID: \n")
    stock_input_modification = stock_input_modification.lower()
         
    if stock_input_modification.isdigit():
        stock_id= int(stock_input_modification)
        
        if stock_id not in range(1, len(stock_dictionary) + 1):
            print("no such Id exists\n")
            return

        for i, name in enumerate(stock_dictionary, 1):
            if stock_id == i:
                stock_input_modification = name
                break

    amount_to_add = int(input("enter how much stock to add: \n"))
    if amount_to_add < 0:
        print("number can't be negative.\n")
        return
    if stock_input_modification in stock_dictionary:
        stock_dictionary[stock_input_modification] += amount_to_add
    else:
        stock_dictionary[stock_input_modification] = amount_to_add







def remove_stock(stock_dictionary):
    show_stock(stock_dictionary)

    stock_input_modification = input("Enter the stock name or Id to remove: \n")
    stock_input_modification = stock_input_modification.lower()

    if stock_input_modification.isdigit():
        stock_id = int(stock_input_modification)

        if stock_id not in range(1, len(stock_dictionary) + 1):
            print("Invalid stock ID.\n")
            return

        for i, name in enumerate(stock_dictionary, 1):
            if stock_id == i:
                stock_input_modification = name
                break        
    if stock_input_modification not in stock_dictionary:
        print("Stock does not exist.\n")
        return
    amount_to_remove = int(input("Enter how much stock to remove: \n"))

    if amount_to_remove < 0:
        print("Number can't be negative.\n")
        return

    if stock_dictionary[stock_input_modification] - amount_to_remove < 0:
        print("Not enough stock.\n")
        return
    stock_dictionary[stock_input_modification] -= amount_to_remove











try:
    file = open("stock.txt", "r")
    stock = file.read()
    file.close()
    lines = stock.splitlines()
    
    stock_dictionary = {}
    for line in lines:
        item = line.split(",")
        if len(item) != 2:
            raise ValueError
        item_name = item[0]
        amount = int(item[1])
        stock_dictionary[item_name] = amount

    
except FileNotFoundError:
    print("Error: stock was not found.\n")

except ValueError:
    print("Error: stock file has an invalid format (name,comma,number) requried format.\n")



while True:
    show_menu()
    operation_number = int(input("choose which operation: \n"))

    if operation_number not in range(1, 5):
        print("wrong number entered, try another\n")
        continue

    if operation_number == 1:
        add_stock(stock_dictionary)
    
    elif operation_number == 2:
        remove_stock(stock_dictionary)
        
    elif operation_number == 3:
        show_stock(stock_dictionary)
    
    elif operation_number == 4:
        file = open("stock.txt", "w")

        for name, amount in stock_dictionary.items():
            file.write(f"{name},{amount}\n")

        file.close()
        break