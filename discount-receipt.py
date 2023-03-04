import socket
from datetime import datetime
from os import getcwd, listdir, mkdir

receipt_header = "Zloty kolczyk\nUl. Henryka Sienkiewicza 30\nTel. 41-343-78-69\n--------------------------------\n"
receipt_footer = "       Zapraszamy ponownie\n"

printer_ip = ("localhost", 9100)

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

code_to_product = dict()
svg = open(f"{getcwd()}/products.csv").read()
for product in svg.splitlines():
    try:
        code, name, discount_percentage = product.split(",")
        try:
            code_to_product[int(code)] = Product(
                name,
                int(discount_percentage)
            )
        except ValueError:
            code_to_product[int(code)] = Product(
                name
            )
    except ValueError:
        pass

def generate_receipt(products, date="", preview=False):
    receipt=receipt_header
    starting_price_sum = 0
    difference_sum = 0
    final_price_sum = 0
    receipt += f"Rabat {date}\n"
    for index, product in enumerate(products):
        if preview:
            receipt += f"Nr. {index}\n"
        starting_price=f"{str(product.starting_price)[:-2]}.{str(product.starting_price)[-2:]}"
        starting_price_sum += product.starting_price
        discount_percentage = str(product.discount_percentage)
        if discount_percentage == "0":
            difference = "-0.00"
        else:
            difference = product.starting_price - product.final_price
            difference_sum += difference
            difference = f"-{str(difference)[:-2]}.{str(difference)[-2:]}"
        final_price = f"{str(product.final_price)[:-2]}.{str(product.final_price)[-2:]}"
        final_price_sum += product.final_price
        receipt += f"{product.name:<19}{'~' + discount_percentage:>4}%\n"
        receipt += f"         {starting_price:>7} {difference:>7} {'~' + final_price:>7}\n"
    receipt += "--------------------------------\n"
    starting_price_sum = f"{str(starting_price_sum)[:-2]}.{str(starting_price_sum)[-2:]}"
    difference_sum = f"{str(difference_sum)[:-2]}.{str(difference_sum)[-2:]}"
    final_price_sum = f"{str(final_price_sum)[:-2]}.{str(final_price_sum)[-2:]}"
    receipt += f"Suma:    {starting_price_sum:>7} {'-' + difference_sum:>7} {final_price_sum:>7}\n"
    receipt += receipt_footer
    return receipt

def save_receipt_as_txt(receipt, filename):
    try:
        mkdir(f"{getcwd()}/printed/")
    except:
        pass
    with open(f"{getcwd()}/printed/{filename}", "w+") as file:
        file.write(receipt)

def print_receipt_network_printer(receipt):
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect(printer_ip)
        s.send(receipt.encode() + bytes(16))
        s.close()
    except:
        print("\033[31mPrinting error\033[39m")
        # print("\033[31mBłąd drukowania\033[39m")
    else:
        print("Printing...")
        # print("Drukowanie...")

def save_logs(products, filename):
    out = ""
    for product in products:
        out += product.to_csv() + "\n"
    try:
        mkdir(f"{getcwd()}/logs/")
    except:
        pass
    with open(f"{getcwd()}/logs/{filename}", "w+") as file:
        file.write(out)

def enter_product_menu():
        products = list(code_to_product.items())
        for i in range(0, len(products), 2):
            key, product = products[i]
            print(f"{key:>3} {product.name:<19}", end="")
            try:
                key, product = products[i+1]
                print(f"{key:>3} {product.name:<19}")
            except:
                print()
        print("Enter product code or custom name (0 - Cancel)")
        # print("Wpisz kod lub niestandardową nazwę (0 - Anuluj)")
        while True:
            code_or_name = input("@> ")
            if code_or_name == "0":
                raise RuntimeError
            try:
                code = int(code_or_name)
                product = code_to_product[code]
            except ValueError:
                name = code_or_name
                discount_percentage = 0
                if len(name) == 0:
                    print("\033[31mCan't be empty\033[39m")
                    # print("\033[31mNie może być puste\033[39m")
                else:
                    break
            except KeyError:
                print("\033[31mInvalid code\033[39m")
                # print("\033[31mNiepoprawny kod\033[39m")
            else:
                name = product.name
                discount_percentage = product.discount_percentage
                break
        while True:
            print("Enter starting price (0 - Cancel)")
            # print("Wpisz cenę początkową (0 - Anuluj)")
            try:
                starting_price = input("zł> ")
                if starting_price == "0":
                    raise RuntimeError
                if "." in starting_price or "," in starting_price or "-" in starting_price:
                    starting_price = int(starting_price[:-3] + starting_price[-2:])
                else:
                    starting_price = int(f"{int(starting_price)}00")
            except ValueError:
                print("\033[31mInvalid price\033[39m")
                # print("\033[31mNiepoprawna cena\033[39m")
            else:
                break
        while True:
            print("Enter discount (0 - Cancel)")
            # Print("Wpisz zniszkę (0 - Anuluj)")
            value = input(f"{discount_percentage}%> ")
            if value == "0":
                raise RuntimeError
            if value != "":
                try:
                    discount_percentage = int(value)
                except ValueError:
                    print("\033[31mInvalid value\033[39m")
                    # print("\033[31mNiepoprawna wartość\033[39m")
                else:
                    break
            else:
                break
        final_price = int(starting_price*(1-(discount_percentage/100)))
        while True:
            print("Enter final price (0 - Cancel)")
            # print("Wpisz cenę końcową (0 - Anuluj)")
            value = input(f"{str(final_price)[:-2]}.{str(final_price)[-2:]}zł> ")
            if value == "0":
                raise RuntimeError
            if value != "":
                try:
                    if "." in value or "," in value:
                        final_price = int(value[:-3] + value[-2:])
                    else:
                        final_price = int(f"{value}00")
                except ValueError:
                    print("\033[31mInvalid value\033[39m")
                    # print("\033[31mNiepoprawna wartość\033[39m")
                else:
                    break
            else:
                break
        return Product(
            name,
            discount_percentage,
            starting_price,
            final_price
        )


if __name__ == "__main__":
    purchased_products = []
    while True:
        print(
            "1. Add product\n"
            "2. Remove product\n"
            "3. Clear\n"
            "4. Save and print\n"
            "5. Print file\n"
            "6. Print text"
        )
        # print(
        #     "1. Dodaj produkt\n"
        #     "2. Usuń produkt\n"
        #     "3. Wyczyść\n"
        #     "4. Zapisz i drukuj\n"
        #     "5. Drukuj plik\n"
        #     "6. Drukuj tekst"
        # )
        option = input("#> ")
        if option == "1":
            try:
                product = enter_product_menu()
            except RuntimeError:
                print("Cancelled")
                # print("Anulowano")
            else:
                purchased_products.append(product)
        elif option == "2":
            print(generate_receipt(purchased_products, preview=True))
            try:
                index=int(input("@> "))
            except ValueError:
                print("\033[31mInvalid index\033[39m")
                # print("N\033[31miepoprawna wartość\033[39m")
            else:
                if index == 0:
                    print("Cancelled")
                    # print("Anulowano")
                else:
                    purchased_products.pop(index)

        elif option == "3":
            print("Confirm")
            # print("Potwierdź")
            if input("1> ") == "1":
                purchased_products = []
            else:
                print("Cancelled")
                # print("Anulowano")

        elif option == "4":
            now = datetime.now()
            receipt = generate_receipt(
                purchased_products, 
                now.strftime("%d.%m.%Y %H:%M")
            )
            print(receipt)
            print("Confirm")
            # print("Potwierdź")
            if input("1> ") == "1":
                print_receipt_network_printer(receipt)
                filename = now.strftime("%d_%m_%Y__%H_%M_%S")
                save_receipt_as_txt(receipt, filename + ".txt")
                save_logs(purchased_products, filename + ".csv")
                purchased_products = []
            else:
                print("Cancelled")
                # print("Anulowano")

        elif option == "5":
            try:
                dir = f"{getcwd()}/receipts/"
                files = listdir(dir)
            except FileNotFoundError:
                print(f"Directory doesn't exist: {dir}")
                # print(f"Folder nie istnieje: {dir}")
            else:
                for index, file in enumerate(files):
                    print(f"{index}. {file}")
                try:
                    index = int(input("@>"))
                except ValueError:
                    print("Invalid value")
                    # print("Niepoprawna wartość")
                else:
                    receipt = open(dir + files[index]).read()
                    print(receipt)
                    print_receipt_network_printer(receipt)

        elif option == "6":
            receipt = ""
            while True:
                line = input()
                if line == "":
                    break
                else:
                    receipt += f"{line}\n"
            print_receipt_network_printer(receipt)

        else:
            print("\033[31mInvalid option\033[39m")
            # print("\033[31mNiepoprawna opcja\033[39m")
