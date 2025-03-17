import json
from colorama import Fore, Style
import datetime
import statistics

sells = [] # [[name, price, category], [name, price, category], ...]
data = {}

print(f"{Fore.YELLOW}Welcome to the sell tracker!{Fore.RESET}")
print("Write a sell in the format" + Fore.CYAN + " name:price:category" + Fore.RESET, end='. ')
print("If you want to stop writing sells, type '" + Fore.CYAN + "stop" + Fore.RESET + "'.")

# Main input
while True:
    user_input = input("— ").lower()
    splited_input = user_input.split(":")

    if user_input == "stop":
        if not sells: print(Fore.RED + "You have not written any sell yet" + Fore.RESET) # If sells list is empty
        else: break
    elif len(splited_input) == 3 and all(splited_input): # Check if input is valid
        if splited_input[1].isnumeric() and float(splited_input[1]) > 0: # Check if price is a valid number
            print(Fore.GREEN + f"Sell submitted ({splited_input[0]})" + Fore.RESET)
            sells.append(splited_input)
        else:
            print(Fore.RED + "Your price is not a valid number. Your sell will not be submitted" + Fore.RESET)
    else:
        print(Fore.RED + "Invalid format. Your sell will not be submitted" + Fore.RESET)
        continue

# Overall sells
print(Style.BRIGHT + Fore.MAGENTA + f"\nOVERALL SELLS" + Style.RESET_ALL, end="")
print(f"""
    ● Products: {', '.join([sell[0] for sell in sells])}
    ● Overall price: {sum([float(sell[1]) for sell in sells])}
    ● Average price: {round(statistics.mean([float(sell[1]) for sell in sells]), 2)}""" + Style.RESET_ALL)

data["DATE"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
data["OVERALL"] = {
    "products": [sell[0] for sell in sells],
    "overall_price": sum([float(sell[1]) for sell in sells]),
    "average_price": round(statistics.mean([float(sell[1]) for sell in sells]), 2)
}
data["BY_CATEGORIES"] = {}

# Sells by categories
print(Style.BRIGHT + Fore.MAGENTA + "\nSELLS BY CATEGORIES" + Style.RESET_ALL)


for product, price, category in sells:
    price = float(price)
    if category not in data["BY_CATEGORIES"].keys():
        data["BY_CATEGORIES"][category.lower()] = {
            "products": [],
            "overall_price": None,
            "average_price": None
        }
    data["BY_CATEGORIES"][category]["products"].append(product)
    if data["BY_CATEGORIES"][category]["overall_price"]: data["BY_CATEGORIES"][category]["overall_price"] += price
    else: data["BY_CATEGORIES"][category]["overall_price"] = price

for category in data["BY_CATEGORIES"].keys():
    prices = [float(sell[1]) for sell in sells if sell[2] == category]
    data["BY_CATEGORIES"][category]["average_price"] = round(statistics.mean(prices), 2)
    print(f"""Category: {Fore.YELLOW + category.upper() + Fore.RESET}
        ● Products: {', '.join(data["BY_CATEGORIES"][category]["products"])}
        ● Overall price: {sum(prices)}
        ● Average price: {round(statistics.mean(prices), 2)}""")


date_time = datetime.datetime.now()
print(Style.DIM + Fore.CYAN + "\nReport generated at " + date_time.strftime("%d.%m.%Y %H:%M:%S") + Style.RESET_ALL)

with open("report.json", "a+") as file:
    json.dump(data, file, indent=4)