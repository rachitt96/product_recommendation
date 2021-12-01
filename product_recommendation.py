import json
import sys
import heapq
import os
import time

import pandas as pd

class Recommendations:
    def __init__(self):
        """ Constructor to initialize two variables as soon as instance is created
        """

        self.transactions_items_lst = []
        self.products_df = None

    def get_co_occurance_dict(self, product_id):
        """ A function to calculate co-purchase frequency, the number of times each product is purchased with a specific product id.

        Arguments:
            product_id: (str) id of product, for which we need to count the number of time other products bought with in a same transaction

        Returns:
            co_occurance_dict: (dict) {key:value} pair where 
                                        key = product_id 
                                        value = the co-purchase frequency with input product_id
        """

        co_occurance_dict = {}

        for item_list in self.transactions_items_lst:
            if(product_id in item_list):
                for item in item_list:
                    if(item != product_id):
                        if(item not in co_occurance_dict):
                            co_occurance_dict[item] = 1
                        else:
                            co_occurance_dict[item] += 1
        
        return co_occurance_dict

    def get_top_recommendations(self, product_id, file_path='./transactions.txt', get_latency=False):
        """ A function to get top 5 recommended product names of a specific product id. 

        Arguments:
            product_id: (str) id of a product, for which we want to get top recommendations
            file_path: (str)(optional) location of text file having transactions in json format
            get_latency: (bool)(optional) get execution time of a function
        
        Returns:
            recommended_products_name_lst: (list[str]) list of 5 recommended products for input product id
        """

        start_time = time.time()

        if(not self.transactions_items_lst):
            self.transactions_items_lst = self.read_transactions_from_file(file_path)
        
        product_co_occurance_dict = self.get_co_occurance_dict(product_id)
        recommended_product_ids_lst = heapq.nlargest(5, product_co_occurance_dict, key=product_co_occurance_dict.get)

        recommended_products_name_lst = self.get_product_names_by_ids(recommended_product_ids_lst)

        if(get_latency):
            print(time.time() - start_time)

        return recommended_products_name_lst

    def get_product_names_by_ids(self, product_ids_lst, products_file_path = './products.txt'):
        """ A function to get name of products based on their associated ids.

        Arguments:
            product_ids_lst: (list[str]) list of product ids for which we want to get the name.
            products_file_path: (str) location of text file having product id and associated name in tsv format 
        
        Returns:
            product_name_lst: (list[str]) list of product names 
        """

        if(self.products_df is None):
            self.products_df = pd.read_csv(products_file_path, sep='\t', header=None, names=['product_id', 'mch_code', 'product_name'])

        filtered_df = self.products_df[self.products_df['product_id'].isin(product_ids_lst)]
        return filtered_df['product_name'].values.tolist()

    def read_transactions_from_file(self, file_path):
        """ A function to read transaction files and extract list of items purchased in each transaction by customers.

        Arguments:
            file_path: (str) location of transactions json file
        
        Returns:
            transaction_item_name_lst: (list[list[str]]) A list storing list of purchased items in each transaction
        """

        transaction_item_name_lst = []

        with open(file_path, encoding='utf-8') as f:
            for transaction in f.readlines():
                transaction_json = json.loads(transaction)
                item_name_lst = [item['item'] for item in transaction_json['itemList']]
                transaction_item_name_lst.append(item_name_lst)

        return transaction_item_name_lst      