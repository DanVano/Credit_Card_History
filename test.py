import string

from collections import defaultdict

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
            # Update the count and total amount for this word
            temp_dict[word]['count'] += 1
            temp_dict[word]['total'] += amount

    # Initialize the final dictionary
    final_dict = {}

    # Iterate over the items in the temp_dict
    for word, info in temp_dict.items():
        # If this word appears at least 3 times, add it to the final_dict
        if info['count'] >= 3:
            # If this word is already in the final_dict and the current count is greater
            # than the count in the final_dict, update the final_dict
            if word in final_dict and info['count'] > final_dict[word]['count']:
                final_dict[word] = info
            # If this word is not in the final_dict, add it
            elif word not in final_dict:
                final_dict[word] = info

    return final_dict


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


print = group_by_common_words(test_expenses)

print(print)

