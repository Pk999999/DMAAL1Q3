import pandas as pd
from itertools import combinations

def load_transactions(file_path):
    df = pd.read_csv(file_path)
    transactions = df['Items'].apply(lambda x: set(x.split(';'))).tolist()
    return transactions

def apriori(transactions, min_support):
    def get_itemsets(transactions, size):
        itemsets = set()
        for transaction in transactions:
            for itemset in combinations(sorted(transaction), size):
                itemsets.add(itemset)
        return itemsets

    def get_frequent_itemsets(itemsets, transactions, min_support):
        itemset_count = {itemset: 0 for itemset in itemsets}
        for transaction in transactions:
            for itemset in itemsets:
                if set(itemset).issubset(transaction):
                    itemset_count[itemset] += 1
        return {itemset: count for itemset, count in itemset_count.items() if count >= min_support}

    itemsets = get_itemsets(transactions, 1)
    frequent_itemsets = {}
    size = 1

    while itemsets:
        current_itemsets = get_frequent_itemsets(itemsets, transactions, min_support)
        frequent_itemsets.update(current_itemsets)
        size += 1
        itemsets = get_itemsets(transactions, size)
        itemsets = set([itemset for itemset in itemsets if itemset in frequent_itemsets])

    return frequent_itemsets

file_path = 'retail_data.csv'
min_support = 3 

transactions = load_transactions(file_path)
frequent_itemsets = apriori(transactions, min_support)
print("Frequent Itemsets:")
for itemset, count in frequent_itemsets.items():
    print(f"Itemset: {itemset}, Count: {count}")