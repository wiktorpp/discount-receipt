from os.path import dirname
from datetime import datetime
from os import mkdir

class Product:
    def __init__(
        self, 
        name = None, 
        discount_percentage = 0,
        starting_price = None, 
        final_price = None
    ):
        self.name = name
        self.starting_price = starting_price
        self.final_price = final_price
        self.discount_percentage = discount_percentage
    
    def __repr__(self) -> str:
        starting_price = f"{str(self.starting_price)[:-2]}_{str(self.starting_price)[-2:]}"
        final_price = f"{str(self.final_price)[:-2]}_{str(self.final_price)[-2:]}"
        return f"Product({self.name}, {self.discount_percentage}, {starting_price}, {final_price})"
    
    def to_csv(self):
        starting_price = f"{str(self.starting_price)[:-2]}_{str(self.starting_price)[-2:]}"
        final_price = f"{str(self.final_price)[:-2]}_{str(self.final_price)[-2:]}"
        return f"{self.name};{self.discount_percentage};{self.starting_price};{final_price}"

code_to_product = {
    1: Product("Złoto", 10),
    2: Product("Srebro")
}

receipt_header = "Zloty kolczyk\n<ulica>\nTel. <numer>\n--------------------------------\n"
receipt_footer = "--------------------------------\n      Zapraszamy ponownie\n"



def generate_receipt(products, date="", preview=False):
    receipt=receipt_header
    for index, product in enumerate(purchased_products):
        receipt += f"Rabat {date}\n"
        if preview:
            receipt += f"Nr. {index}\n"
        starting_price=f"{str(product.starting_price)[:-2]}.{str(product.starting_price)[-2:]}"
        discount_percentage = str(product.discount_percentage)
        if discount_percentage == "0":
            difference = "-0.00"
        else:
            difference = str(product.final_price - product.starting_price)
            difference = f"{difference[:-2]}.{difference[-2:]}"
        final_price = f"{str(product.final_price)[:-2]}.{str(product.final_price)[-2:]}"
        receipt += f"{product.name:<19}{'-' + discount_percentage:>4}%\n"
        receipt += f"         {starting_price:>7} {difference:>7} {final_price:>7}\n"
    receipt += receipt_footer
    return receipt

def print_receipt(receipt, date):
    filename = date.replace(" ", "_") + ".txt"
    try:
        mkdir(f"{dirname(__file__)}/autoprint/")
    except:
        pass
    with open(f"{dirname(__file__)}/autoprint/{filename}", "w+") as file:
        file.write(receipt)

def save_logs(products, date):
    out = ""
    for product in products:
        out += product.to_csv() + "\n"
    filename = date.replace(" ", "_") + ".csv"
    try:
        mkdir(f"{dirname(__file__)}/logs/")
    except:
        pass
    with open(f"{dirname(__file__)}/logs/{filename}", "w+") as file:
        file.write(out)

purchased_products = []
while True:
    print(
        "1. Add product - 1\n"
        "2. Remove product - 2\n"
        "3. Clear - 3\n"
        "4. Save and print - 4"
    )
    # print(
    #     "1. Dodaj produkt\n"
    #     "2. Usuń produkt\n"
    #     "3. Wyczyść\n"
    #     "4. Zapisz i drukuj"
    # )
    option = input("#> ")
    if option == "1":
        print("Enter product code or custom name")
        # print("Wpisz kod lub niestandardową nazwę")
        while True:
            code_or_name = input("@> ")
            try: 
                code = int(code_or_name)
                product = code_to_product[code]
            except ValueError:
                name = code_or_name
                discount_percentage = 0
                if len(name) == 0:
                    print("Can't be empty")
                else:
                    break
            except KeyError:
                print("Invalid code")
            else:
                name = product.name
                discount_percentage = product.discount_percentage
                break
        while True:
            print("Enter starting price")
            # print("Wpisz cenę początkową")
            try:
                starting_price = input("zł> ")
                if "." in starting_price or "," in starting_price or "-" in starting_price:
                    starting_price = int(starting_price[:-3] + starting_price[-2:])
                else:
                    starting_price = int(f"{starting_price}00")
            except ValueError:
                print("Invalid price")
            else:
                break
        while True:
            print("Enter discount")
            value = input(f"{discount_percentage}%> ")
            if value != "":
                try:
                    discount_percentage = int(value)
                except ValueError:
                    print("Invalid value")
                else:
                    break
            else:
                break
        final_price = int(starting_price*(1-(discount_percentage/100)))
        while True:
            print("Enter final price")
            value = input(f"{str(final_price)[:-2]}.{str(final_price)[-2:]}zł> ")
            if value != "":
                try:
                    if "." in value or "," in value:
                        final_price = int(value[:-3] + value[-2:])
                    else:
                        final_price = int(f"{value}00")
                except ValueError:
                    print("Invalid value")
                else:
                    break
            else:
                break
        purchased_products.append(Product(name, discount_percentage, starting_price, final_price))
        print(purchased_products)
    elif option == "2":
        print(generate_receipt(purchased_products, preview=True))
        try:
            index=int(input("@> "))
        except ValueError:
            print("Invalid index")
        else:
            purchased_products.pop(index)
    elif option == "3":
        print("Confirm")
        if input("1> ") == "1":
            purchased_products = []
        else:
            print("Cancelled")
    elif option == "4":
        now = datetime.now()
        receipt = generate_receipt(purchased_products, now.strftime("%d.%m.%Y %H:%M"))
        print(receipt)
        print("Confirm")
        if input("1> ") == "1":
            print_receipt(receipt, now.strftime("%d.%m.%Y %H:%M:%S"))
            print("Printing...")
            save_logs(purchased_products, now.strftime("%d.%m.%Y %H:%M:%S"))
            purchased_products = []
        else:
            print("Cancelled")
    else:
        print("Invalid option")
