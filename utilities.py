# Read the credit card csv file and seperate the data into credit purchases and payments. Collect dates of credit purchases
#fix the json files. do all manipulation here so the html files just needs to read the data

import csv
import json
import string

from collections import defaultdict

def read_data():
    payment_info, credit_info, credit_dates = {}, {}, {}

    # Read the credit card monthly csv file
    with open('cc_data.csv', 'r') as file:
        reader = csv.reader(file, delimiter='\t')
        for row in reader:
            #unpack the list from reader
            date, description, credit, debit, _ = row

            # Seperate the credit charges and the payments
            # check if debit is not empty
            if debit:
                payment_info[date] = float(debit)
            # check if credit is not empty
            elif credit:
                credit_info[description] = credit_info.get(description, 0) + float(credit)
                # collect dates
                if description in credit_dates:
                    credit_dates[description].append(date)
                else:
                    credit_dates[description] = [date]
    return payment_info, credit_info, credit_dates

#Categorize expenses into groups
def categorize_expenses(credit_info, categories):
    categorized_expenses = {}
    # Use this later in a table
    other_expenses = {}

    # Iterate over each item in credit_info
    for description, amount in credit_info.items():
        found = False

        # Iterate over each category
        for category_name, keywords in categories.items():
            # Check if any keyword is in the description
            if any(keyword.lower() in description.lower() for keyword in keywords):
                categorized_expenses[category_name] = categorized_expenses.get(category_name, 0) + amount
                found = True

        # If no keyword was found in the description, add to "Other"
        if not found:
            other_expenses["Other"] = other_expenses.get("Other", 0) + amount

    # Combine categorized and other expenses
    # Unpack the dict with keys and values with **
    categorized_expenses = {**categorized_expenses, **other_expenses}

    return categorized_expenses, other_expenses

#Save data to json for javascript
def save_info(payment_info, credit_info, credit_dates, categorized_expenses):
    with open('payment_info.json', 'w') as f:
        json.dump(payment_info, f)
    with open('credit_info.json', 'w') as f:
        json.dump(credit_info, f)
    with open('credit_dates.json', 'w') as f:
        json.dump(credit_dates, f)
    with open('categorized_expenses.json', 'w') as f:
        json.dump(categorized_expenses, f)

#Try to Group expeneses from the Other dictionary using 'Like' words
def group_by_common_words(test_expenses):
    # Initialize a nested dictionary to store the words, counts, and total amounts
    temp_dict = defaultdict(lambda: defaultdict(float))

    # Iterate over the keys and values in other_expenses
    for company, amount in test_expenses.items():
        # Convert the company name to lowercase and remove punctuation
        company = company.lower().translate(str.maketrans('', '', string.punctuation))

        # Split the company name into words
        words = company.split()

        # Iterate over the words
        for word in words:
            # Only process words that are not digits
            if word.isalpha():
                # Update the count and total amount for this word
                temp_dict[word]['count'] += 1
                temp_dict[word]['total'] += amount

    # Initialize the final dictionary
    final_dict = {}

    # Sort temp_dict by count in descending order
    sorted_temp_dict = dict(sorted(temp_dict.items(), key=lambda item: item[1]['count'], reverse=True))

    # Iterate over the items in the sorted_temp_dict
    for word, info in sorted_temp_dict.items():
        # If this word appears at least 3 times, add it to the final_dict
        if info['count'] >= 3:
            # If this word is not in the final_dict, add it
            if word not in final_dict:
                final_dict[word] = info

    return final_dict

#Print data for testing.
def print_info(payment_info, credit_info, credit_dates, categorized_expenses, other_expenses, final_dict):
    print("\nDebit Info:", payment_info)
    print("Credit Info:", credit_info)
    print("Purchases dates:", credit_dates)
    print("\nCategories", categorized_expenses)
    print("\nOther", other_expenses)
    print("\nOther Grouped", final_dict)


#Test dict
test_expenses = {
    "Liquor Store 1": 5,
    "Liquor Store 2": 4,
    "Liquor Store 3": 8,
    "Liquor Store 4": 9,
    "Liquor Store 5": 10,
    "Weed Shop 1": 2,
    "Weed Shop 2": 5,
    "Weed Shop 3": 3,
    "Gas Station 1": 9,
    "Gas Station 2": 7,
    "Gas Station 3": 6,
    "Grocery Store 1": 4,
    "Grocery Store 2": 2,
    "Grocery Store 3": 3,
    "Grocery Store 4": 7,
    "Grocery Store 5": 6,
    "Clothing Store 1": 3,
    "Clothing Store 2": 3,
    "Electronics Store": 2,
    "Bookstore": 1
}

def print_grouped_expenses(final_dict):
    for word, info in final_dict.items():
        print(f"{word}: {info['total']}")

def main():
    #define the categories
    categories = {
        "Liquor": ["liquor", "lcbo", "beer", "wine"],
        "Weed": ["bud", "weed"],
        "Groceries": ["superstore", "loblaws", "t&t", "oceans", "no frills", "food basics", "metro"],
        "Gas": ["shell", "esso", "costco", "pioneer", "mobil", "petro"]
    }

    payment_info, credit_info, credit_dates = read_data()
    categorized_expenses, other_expenses = categorize_expenses(credit_info, categories)
    final_dict = group_by_common_words(other_expenses)
    save_info(payment_info, credit_info, credit_dates, categorized_expenses)
    print_info(payment_info, credit_info, credit_dates, categorized_expenses, other_expenses, final_dict)

    #Test group_by_common_words
    test_final_dict = group_by_common_words(test_expenses)
    print("\nTest Grouped")
    print_grouped_expenses(test_final_dict)

if __name__ == "__main__":
    main()

