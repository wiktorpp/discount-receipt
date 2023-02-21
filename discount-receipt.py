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
        return f"Product({name}, {discount_percentage}, {starting_price}, {final_price})"

code_to_product = {
    1: Product("Złoto", 10),
    2: Product("Srebro")
}

receipt_header = "Zloty kolczyk\n<ulica>\nTel. <numer>\n--------------------------------\n"
receipt_footer = "--------------------------------\n      Zapraszamy ponownie"



def generate_receipt(products, preview=False):
    receipt=receipt_header
    for index, product in enumerate(purchased_products):
        if preview:
            receipt += f"Nr. {index}"
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




purchased_products = []
while True:
    print(
        "Add product - 1\n"
        "Remove product - 2\n"
        "Clear - 3\n"
        "Save and print - 4"
    )
    # print(
    #     "Dodaj produkt - puste\n"
    #     "Usuń produkt - 1\n"
    #     "Wyczyść - 2\n"
    #     "Zapisz i drukuj - 3"
    # )
    option = input(">")
    if option == "1":
        print("Enter product code or custom name")
        # print("Wpisz kod lub niestandardową nazwę")
        while True:
            code_or_name = input(">")
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
        print("Enter discount")
        while True:
            value = input(f"{discount_percentage}%>")
            if value != "":
                try:
                    discount_percentage = int(value)
                except ValueError:
                    print("Invalid value")
                else:
                    break
            else:
                break
        while True:
            print("Enter starting price")
            # print("Wpisz cenę początkową")
            try:
                starting_price = input(">")
                if "." in starting_price or "," in starting_price:
                    starting_price = int(starting_price[:-3] + starting_price[-2:])
                else:
                    starting_price = int(f"{starting_price}00")
            except ValueError:
                print("Invalid price")
            else:
                break
        final_price = int(starting_price*(1-(discount_percentage/100)))
        purchased_products.append(Product(name, discount_percentage, starting_price, final_price))
    elif option == "4":
        break
    else:
        print("Invalid option")
print(purchased_products)
with open("log.svg", "a") as file:
    pass
    # TODO
print("--------------------------WYDRUK------------------------")

print(purchased_products)
print(generate_receipt(purchased_products))
