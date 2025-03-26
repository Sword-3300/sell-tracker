import json
import datetime
import statistics
import os

import rich.style
from rich.table import Table
from rich.panel import Panel
from rich.console import Console
from rich.style import Style as rstyle

# COLORS
# RED - #e06c75
# GREEN - #7bb85a
# CYAN - #56b6c2
#YELLOW - #e5c07b

sells = [] # [[name, price, quantity, category], [name, price, quantity, category], ...]
data = {}
console = Console()
rprint = console.print

rprint(Panel(
        "[#e5c07b]Welcome to the sell tracker![/]",
        title="[#e5c07b]Hello![/]",
        width=console.width
    ), justify="center")
rprint(Panel(
        """Write all today's sells [underline]one by one[/] in the format [#56b6c2]name:price_per_unit:quantity:category[/]
        Then write a number of customers
        If you want to stop writing sells, type [#56b6c2]stop[/]
        In you want to exit the program, type [#56b6c2]exit[/]""",
        title="[#e5c07b]Instructions[/]",
        width=console.width
    ), justify="center")

# Main input
while True:
    user_input = input("— ").lower()
    splited_input = user_input.split(":")

    if user_input == "stop":
        if not sells: rprint(f"[#e06c75]You have not written any sell yet[/]", justify="center") # If sells list is empty
        else: break
    elif user_input == "exit": break
    elif len(splited_input) == 4 and all(splited_input): # Check if input is valid
        if splited_input[1].isnumeric() and float(splited_input[1]) > 0 and splited_input[2].isnumeric() and float(splited_input[2]) > 0: # Check if price and quantity is a valid number
            rprint(f"[#7bb85a]Sell submitted ({splited_input[0]})[/]", justify="center")
            sells.append(splited_input)
        else:
            rprint(f"[#e06c75]Your price or quantity is not a valid number. Your sell will not be submitted[/]", justify="center")
    else:
        rprint(f"[#e06c75]Invalid format. Your sell will not be submitted[/]", justify="center")
        continue
while True:
    try:
        customers_number = int(input("Write the number of customers\n— "))
        break
    except ValueError:
        rprint("[red]Invalid number of customers[/]")

most_popular_products = [sell[0] for sell in sells if int(sell[2]) == max(int(sell[2]) for sell in sells)]
least_popular_products = [sell[0] for sell in sells if int(sell[2]) == min(int(sell[2]) for sell in sells)]


data["DATE"] = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
data["CUSTOMERS_NUMBER"] = customers_number
data["OVERALL"] = {
    "products": [sell[0] for sell in sells],
    "overall_price": sum([float(sell[1]) * int(sell[2]) for sell in sells]),
    "average_price": round(statistics.mean([float(sell[1]) * int(sell[2]) for sell in sells]), 2)
}
data["BY_CATEGORIES"] = {}
data["POPULARITY"] = {
    "MOST_POPULAR_PRODUCT(S)": ', '.join(most_popular_products) + f" ({next(quantity for name, _, quantity, _ in sells for product in most_popular_products if name == product)})",
    "LEAST_POPULAR_PRODUCT(S)": ', '.join(least_popular_products) + f" ({next(quantity for name, _, quantity, _ in sells for product in least_popular_products if name == product)})"
}
data["AVERAGE_RECEIPT"] = round(data["OVERALL"]["overall_price"] / customers_number, 2)


print(f"\nAverage receipt price: {data['AVERAGE_RECEIPT']}\n")

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
categories_table.add_column("[#7bb85a]Category[/]", justify="center")
categories_table.add_column("[#7bb85a]Products[/]", justify="center")
categories_table.add_column("[#7bb85a]Overall price[/]", justify="center")
categories_table.add_column("[#7bb85a]Average price[/]", justify="center")

for category in data["BY_CATEGORIES"].keys():
    data["BY_CATEGORIES"][category]["average_price"] = round(data["BY_CATEGORIES"][category]["overall_price"] / sum([int(sell[2]) for sell in sells if sell[3] == category]), 2)

    categories_table.add_row(category.upper(),
                             ', '.join(data["BY_CATEGORIES"][category]["products"]),
                             str(data["BY_CATEGORIES"][category]["overall_price"]),
                             str(data["BY_CATEGORIES"][category]["average_price"]))
rprint(categories_table)

popularity_table = Table(title="[bold magenta]POPULARITY ANALYSIS[/]")
popularity_table.add_column("[#7bb85a]The most popular products(s)[/]", justify="center")
popularity_table.add_column("[#7bb85a]The least popular products(s)[/]", justify="center")
popularity_table.add_row(', '.join(most_popular_products) + f" ({next(quantity for name, _, quantity, _ in sells for product in most_popular_products if name == product)})",
                         ', '.join(least_popular_products) + f" ({next(quantity for name, _, quantity, _ in sells for product in least_popular_products if name == product)})")
rprint(popularity_table)

with open("report.json", "a+") as file:
    json.dump(data, file, indent=4)
    report_path = f"file:///{os.path.abspath(file.name)}"
rprint(Panel(f"""[#e5c07b]Report saved at {datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")}
[link={report_path} #e5c07b]Open report file[/]""", width=console.width), justify="center")
