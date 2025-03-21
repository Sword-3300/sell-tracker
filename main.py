import json
import datetime
import statistics
import os

import rich.style
from colorama import Fore, Style
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.style import Style as rstyle

sells = [] # [[name, price, quantity, category], [name, price, quantity, category], ...]
data = {}
console = Console()
rprint = console.print

rprint(Panel(
        "[#e5c07b]Welcome to the sell tracker![/]",
        title="[#e5c07b]Hello![/]",
        width=console.width
    ), justify="center")
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
while True:
    try:
        customers_number = int(input("Number of customers: "))
        break
    except ValueError:
        rprint("[red]Invalid number of customers[/]")

data["DATE"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
data["OVERALL"] = {
    "products": [sell[0] for sell in sells],
    "overall_price": sum([float(sell[1]) * int(sell[2]) for sell in sells]),
    "average_price": round(statistics.mean([float(sell[1]) * int(sell[2]) for sell in sells]), 2)
}
data["BY_CATEGORIES"] = {}


overall_table = Table(title="[bold magenta]OVERALL SELLS[/]")
overall_table.add_column("[#7bb85a]Products[/]", justify="center")
overall_table.add_column("[#7bb85a]Overall price[/]", justify="center")
overall_table.add_column("[#7bb85a]Average price[/]", justify="center")
overall_table.add_row(', '.join(data["OVERALL"]["products"]),
                      str(data["OVERALL"]["overall_price"]),
                      str(data["OVERALL"]["average_price"]))
rprint(overall_table)

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

categories_table = Table(title="[bold magenta]SELLS BY CATEGORIES[/]")
categories_table.add_column("Category", justify="center")
categories_table.add_column("Products", justify="center")
categories_table.add_column("Overall price", justify="center")
categories_table.add_column("Average price", justify="center")

for category in data["BY_CATEGORIES"].keys():
    data["BY_CATEGORIES"][category]["average_price"] = round(data["BY_CATEGORIES"][category]["overall_price"] / sum([int(sell[2]) for sell in sells if sell[3] == category]), 2)

    categories_table.add_row(category.upper(),
                             ', '.join(data["BY_CATEGORIES"][category]["products"]),
                             str(data["BY_CATEGORIES"][category]["overall_price"]),
                             str(data["BY_CATEGORIES"][category]["average_price"]))

rprint(categories_table)

most_popular_products = [sell[0] for sell in sells if int(sell[2]) == max(int(sell[2]) for sell in sells)]
least_popular_products = [sell[0] for sell in sells if int(sell[2]) == min(int(sell[2]) for sell in sells)]
popularity_table = Table(title="[bold magenta]POPULARITY ANALYSIS[/]")
popularity_table.add_column("The most popular products(s)", justify="center")
popularity_table.add_column("The least popular products(s)", justify="center")
popularity_table.add_row(', '.join(most_popular_products), ', '.join(least_popular_products))
rprint(popularity_table)

print(f"Average receipt price: {data["OVERALL"]["overall_price"] / customers_number}")

print(Style.DIM + Fore.CYAN + "\nReport saved at " + datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S") + Style.RESET_ALL)
with open("report.json", "a+") as file:
    json.dump(data, file, indent=4)
    report_path = f"file:///{os.path.abspath(file.name)}"
rprint(f"[link={report_path}]Open report file[/]")