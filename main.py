import json
from colorama import Fore, Style
import datetime
import statistics

sells = [] # [[name, price, quantity, category], [name, price, quantity, category], ...]
data = {}

print(f"{Fore.YELLOW}Welcome to the sell tracker!{Fore.RESET}")
print("Write a sell in the format" + Fore.CYAN + " name:price_for_one_unit:quantity:category" + Fore.RESET, end='. ')
print("If you want to stop writing sells, type '" + Fore.CYAN + "stop" + Fore.RESET + "'.")

# Main input
while True:
    user_input = input("— ").lower()
    splited_input = user_input.split(":")

    if user_input == "stop":
        if not sells: print(Fore.RED + "You have not written any sell yet" + Fore.RESET) # If sells list is empty
        else: break
    elif len(splited_input) == 4 and all(splited_input): # Check if input is valid
        if splited_input[1].isnumeric() and float(splited_input[1]) > 0 and splited_input[2].isnumeric() and float(splited_input[2]) > 0: # Check if price is a valid number
            print(Fore.GREEN + f"Sell submitted ({splited_input[0]})" + Fore.RESET)
            sells.append(splited_input)
        else:
            print(Fore.RED + "Your price or quantity is not a valid number. Your sell will not be submitted" + Fore.RESET)
    else:
        print(Fore.RED + "Invalid format. Your sell will not be submitted" + Fore.RESET)
        continue


data["DATE"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
data["OVERALL"] = {
    "products": [sell[0] for sell in sells],
    "overall_price": sum([float(sell[1]) for sell in sells]),
    "average_price": round(statistics.mean([float(sell[1]) for sell in sells]), 2)
}
data["BY_CATEGORIES"] = {}

# Overall sells
print(f"""Style.BRIGHT + Fore.MAGENTA + "\nOVERALL SELLS" + Style.RESET_ALL
● Products: {', '.join(data["OVERALL"]["products"])}
● Overall price: {data["OVERALL"]["overall_price"]}
● Average price: {data["OVERALL"]["average_price"]}
""")

# Sells by categories
for product, price, quantity, category in sells:
    price = float(price); quantity = int(quantity)
    if category not in data["BY_CATEGORIES"].keys():
        data["BY_CATEGORIES"][category] = {
            "products": [],
            "overall_price": 0,
            "average_price": 0
        }
    data["BY_CATEGORIES"][category]["products"].append(product)
    data["BY_CATEGORIES"][category]["overall_price"] += price * quantity

print(Style.BRIGHT + Fore.MAGENTA + "\nSELLS BY CATEGORIES" + Style.RESET_ALL)
for category in data["BY_CATEGORIES"].keys():
    data["BY_CATEGORIES"][category]["average_price"] = round(data["BY_CATEGORIES"][category]["overall_price"] / sum([int(sell[2]) for sell in sells if sell[3] == category]), 2)
    print(f"""Category: {Fore.YELLOW + category.upper() + Fore.RESET}
        ● Products: {', '.join(data["BY_CATEGORIES"][category]["products"])}
        ● Overall price: {data["BY_CATEGORIES"][category]["overall_price"]}
        ● Average price: {round(data["BY_CATEGORIES"][category]["overall_price"] / sum([int(sell[2]) for sell in sells if sell[3] == category]), 2)}""")


date_time = datetime.datetime.now()
print(Style.DIM + Fore.CYAN + "\nReport generated at " + date_time.strftime("%d.%m.%Y %H:%M:%S") + Style.RESET_ALL)

with open("report.json", "a+") as file:
    json.dump(data, file, indent=4)