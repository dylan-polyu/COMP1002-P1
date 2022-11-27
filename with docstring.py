tracking = {"income": {}, "expense": {}, "saving/investment": {}, "charity": {}}
# Opening
"""
The opening() function is responsible to prompt user to input what record they wish to append, followed by several purposes available.
"""
def opening():
    print("\nWelcome back, user! What do you want to track today?")
    purpose = input(f"Type 'i' for income.\nType 'e' for expense.\nType 's' for saving/investment.\nType 'c' for charity.\n>> ")
    while purpose not in ["i", "e", "s", "c"]:
        purpose = input("Invalid input! Please type one of the above.\n>> ")
    if purpose == "i":
        purpose = "income"
    elif purpose == "e":
        purpose = "expense"
    elif purpose == "s":
        purpose = "saving/investment"
    else:
        purpose = "charity"
    print(f"\nThank you for choosing {purpose}. What do you want to do?")
    status = input(f"Type 's' to store {purpose}.\nType 'u' to update {purpose}.\nType 'r' to retrieve {purpose}.\nType 'd' to delete {purpose}.\nNew feature! Type 'n' to display the total {purpose} of last year.\nNew feature! Type 'p' to display the top 3 {purpose} of the past 30 days.\n>> ")
    while status not in ["s", "u", "r", "d", "n", "p"]:
        status = input("Invalid input! Please type one of the above.\n>> ")
    return purpose, status

# Input Validation
"""
The validate_date() function is responsible to ensure that the inputted date is according to the format.
"""
def validate_date(destination, function):
    print(f"\nPlease input the date according to YYYY-MM-DD format. When was the {destination} happened?")
    def validate_date_details(text, start, end, length):
        result = input(f"Input the {text}\n>> ")
        while not result.isdigit():
            result = input(f"'{result}' is invalid. Please re-input\n>> ")
        # Specificity
        while int(result) not in range(start, end) or len(result) != length:
            result = input(f"{result} is out of range. Please re-input\n>> ")
        return result
    result = 0
    while result not in tracking[destination]:        
        year = validate_date_details("year", 1000, 10000, 4)
        if function == "n":
            result = year
            break
        month = validate_date_details("month", 1, 13, 2)
        date = validate_date_details("date", 1, 32, 2)
        result = year + "-" + month + "-" + date
        if function in ["s", "p"] or result in tracking[destination]:
            break
        print(f"\n{destination} in {result} not found. Please input another date.")
    return result
"""
The validate_category() function is responsible to ensure that the inputted category does not contain digits and does not exist in the ledger.
"""
def validate_category(destination, date, condition):
    category = input("\nPlease input the category\n>> ")
    while category.isdigit():
        category = input(f"Category can't be integers. Please input a string\n>> ")
    while (category in tracking[destination][date]) == condition:
        category = input("Category not found. Please input another category\n>> ")
    return category
"""
The validate_amount() function is responsible to ensure that the inputted amount does not contain characters and above 0.
"""
def validate_amount():
    amount = input("\nPlease input the amount greater than 0\n>> ")
    while True:
        try:
            amount = float(amount)
        except ValueError:
            amount = input("\nAmount can't be strings. Please input the amount again\n>> ")
        if float(amount) < 0:
            amount = input("\nAmount must be greater than 0. Please input the amount again\n>> ")
        else:
            break
    return amount

# Helper Functions
def sort_date(goal):
    x, y = [], {}
    for i in tracking[goal]:
        x.append(i)
        x.sort(reverse=True)
    for j in x:
        for k in tracking[goal]:
            if j == k:
                y[j] = tracking[goal][j]
    tracking[goal] = y

# Functions
"""
The store() function is responsible to store either i/e/s/c to the ledger with the date, category, and amount inputted by the user.
"""
def store(goal):
    date = validate_date(goal, "s")
    if date not in tracking[goal]:
        tracking[goal][date] = {}
    category = validate_category(goal, date, True)
    amount = validate_amount()
    tracking[goal][date][category] = amount
    sort_date(goal)
    print("\nSTORE SUCCESSFUL")
"""
The update() function is responsible to update either i/e/s/c in the ledger with the date, category, and amount inputted by the user.
"""
def update(goal):
    if len(tracking[goal]) != 0:
        date = validate_date(goal, "u")
        category = validate_category(goal, date, False)
        amount = validate_amount()
        tracking[goal][date][category] = amount
        sort_date(goal)
        print("\nUPDATE SUCCESSFUL")
    else:
        print("\nNothing to update.")
"""
The retrieve() function is responsible to retrieve either i/e/s/c from the ledger with the category and amount based on the date inputted by the user.
"""
def retrieve(goal):
    if len(tracking[goal]) != 0:
        date = validate_date(goal, "r")
        if len(tracking[goal][date]) == 0:
            return "No record found."
        print("\nRETRIEVE SUCCESSFUL")
        return tracking[goal][date]
    return "\nNothing to retrieve."
"""
The delete() function is responsible to delete either i/e/s/c record from the ledger according to the date, category, and amount inputted by the user.
"""
def delete(goal):
    if len(tracking[goal]) != 0:
        date = validate_date(goal, "d")
        print("\nWhich record do you wish to delete?\n" + str(tracking[goal][date]))
        category = validate_category(goal, date, False)
        del tracking[goal][date][category]
        sort_date(goal)
        print("\nDELETE SUCCESSFUL")
        return category
    else:
        print("\nNothing to delete.")
"""
The new1() function is responsible to display either i/e/s/c of last year from the ledger according to the year inputted by the user.
"""
def new1(goal):
    if len(tracking[goal]) != 0:
        year = validate_date(goal, "n")
        dates = tracking[goal]
        total = 0
        for date in dates:
            if date[:4] == year:
                print(date, dates[date])
                for key in dates[date]:
                    total += dates[date][key]
        print(f"----------\nTotal: {total}")
    else:
        print("\nNothing to display.")
"""
The new2() function is responsible to display the top 3 of either i/e/s/c in the past 30 days from the ledger according to the date inputted by the user.
"""
def new2(goal):
    if len(tracking[goal]) != 0:
        result = validate_date(goal, "p")
        dates = tracking[goal]
        year, month, date = [int(x) for x in result.split("-")]
        for i in range(30):
            date -= 1
            if date < 1:
                month -= 1
                if month < 1:
                    month = 12
                    year -= 1
                if month == 2:
                    date = 28
                elif month in [1, 3, 5, 7, 8, 10, 12]:
                    date = 31
                else:
                    date = 30
            for key in dates:
                if [year, month, date] == [int(x) for x in key.split("-")]: 
                    print(key, dates[key])
    else:
        print("\nNothing to display.")

# Main
def main():
    status = "s"
    while status != "y":
        purpose, status = opening()
        if status == "s":
            store(purpose)
        elif status == "u":
            update(purpose)     
        elif status == "r":
            result = retrieve(purpose)
            print(result)
        elif status == "d":
            delete(purpose)
        elif status == "n":
            new1(purpose)
        else:
            new2(purpose)
        status = input("\nThank you for tracking. Do you want to end the session?\nType 'y' to proceed.\nType 'n' to reject.\n>> ")
main()
