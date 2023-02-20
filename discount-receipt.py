#from escpos.printer import Network

code_to_product = {
    1: ("Złoto", 10),
    2: "Srebro"
}

receipt_header = "Zloty kolczyk\n<ulica>\nTel. <numer>\n--------------------------------\n"




purchased_products = []
print(
    "Add product - Leave empty\n"
    "Remove product - 1\n"
    "Clear - 2\n"
    "Save and print - 3"
)
# print(
#     "Dodaj produkt - puste\n"
#     "Usuń produkt - 1\n"
#     "Wyczyść - 2\n"
#     "Zapisz i drukuj - 3"
# )
option = input(">")
if option == "":
    print("Enter product code or custom name")
    # print("Wpisz kod lub niestandardową nazwę")
    while True:
        code_or_name = input(">")
        try: code = int(code_or_name)
        except ValueError:
            name = code_or_name
            if len(name) == 0:
                print("Can't be empty")
            else:
                print("Enter discount")
                discount_percentage = input(">")
                break
        else:
            name = code_to_product[code][0]
            discount_percentage = code_to_product[code][1]
            break
    while True:
        print("Enter starting price")
        # print("Wpisz cenę początkową")
        try:
            starting_price = float(input(">"))
        except ValueError:
            print("Invalid price")
        else:
            break
    final_price = round(float(starting_price*(1-(discount_percentage/100))), 2)
    output=(name, starting_price, final_price, discount_percentage)
    with open("log.svg", "a") as file:
        # TODO
        pass
    print(output)
    print("--------------------------WYDRUK------------------------")
    receipt=receipt_header
    starting_price=f"{output[1]:0.2f}"
    difference = f"{output[2] - output[1]:0.2f}"
    final_price = f"{output[2]:0.2f}"
    discount_percentage = str(output[3])
    receipt += f"{output[0]:<19}{'-' + discount_percentage:>4}%\n"
    receipt += f"         {starting_price:>7} {difference:>7} {final_price:>7}"
    print(receipt)
    
    
exit()

# Rabat 19.02.2022 11:27

# Zloto                 ~20%
#          1000.00 -100.00 1000.00
#         1000.00 1000.00 1000.00
# Srebro                ~15%
#                50.00 -0.85 49.15
# --------------------------------
# Suma:       150.00 -20.85 129.15

#       Zapraszamy ponownie"

kitchen = Network("192.168.1.100") #Printer IP Address
kitchen.text("Hello World\n")
kitchen.barcode('1324354657687', 'EAN13', 64, 2, '', '')
kitchen.cut()
