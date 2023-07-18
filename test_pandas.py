import pandas as pd

df = pd.read_json("data.json")

def calc_product_quantity(products):

    quantity_list = []

    for instance in products:
        quantity = 0
        for dictionary in instance:
            quantity += dictionary['quantity']
        quantity_list.append(quantity)
        quantity = 0
    
    return quantity_list

df_task_1 = df

df_task_1["highway_rate"] = abs(df_task_1["highway_cost"]) / calc_product_quantity(df_task_1['products'])

task_1 = df_task_1.drop_duplicates(subset=["warehouse_name"])
task_1_result = task_1[["warehouse_name", "highway_rate"]]
print('Ответ на задание 1:\n\n', task_1_result)

def calcuate_task_2(df):
    dataframe = {'product':[],'warehouse_name':[], 'quantity':[], 'income':[], 'expenses': [], 'profit':[]}

    for index, row in df_task_1.iterrows():
        for dictionary in row['products']:

            dataframe['product'].append(dictionary['product'])

            dataframe['warehouse_name'].append(row['warehouse_name'])

            dataframe['quantity'].append(dictionary['quantity'])

            income = dictionary['quantity'] * dictionary['price']
            dataframe['income'].append(income)

            expenses = row['highway_rate'] * dictionary['quantity']               
            dataframe['expenses'].append(expenses)

            profit = income - expenses                
            dataframe['profit'].append(profit)

    result = pd.DataFrame(data=dataframe)
    result = result[['quantity', 'income','expenses', 'profit']].sum()

    return result

task_2_result = calcuate_task_2(df_task_1)
print('Ответ на задание 2:\n\n', task_2_result)

def calcuate_task_3(df):
    dataframe = {'order_id':[],'order_profit':[]}

    for index, row in df_task_1.iterrows():
        
        dataframe['order_id'].append(row['order_id'])
                
        order_income = 0
        order_expense = 0
        
        for dictionary in row['products']:                        

            order_income += dictionary['price'] * dictionary['quantity']
            
            order_expense += dictionary['quantity'] * row['highway_rate']
            
        order_profit = order_income - order_expense
        
        dataframe['order_profit'].append(order_profit)

    result = pd.DataFrame(data=dataframe)

    return result

task_3_result = calcuate_task_3(df_task_1)


print('Ответ на задание 3 часть 1:\n\n', task_3_result)     
task_3_result


print('Ответ на задание 3 часть 2 (средняя прибыль с заказа): ', task_3_result['order_profit'].mean())


def calcuate_task_4(df):
    
    dataframe = {'warehouse_name':[], 'product':[], 'quantity':[], 'profit':[], 'percent_profit_product_of_warehouse':[]}

    grouped_by_warehouse = df.groupby(['warehouse_name'])

    group_names = grouped_by_warehouse.groups.keys()

    for group in group_names:

        group_data = grouped_by_warehouse.get_group(group)

        group_products = {}

        for index, row in group_data.iterrows():
            for dictionary in row['products']:
                if dictionary['product'] not in group_products:
                    group_products[dictionary['product']] = {'quantity': dictionary['quantity'], 
                                                             'rate': row['highway_rate'],
                                                             'price': dictionary['price'] }

                elif dictionary['product'] in group_products:
                    group_products[dictionary['product']]['quantity'] += dictionary['quantity']



        product_income = 0
        product_expense = 0

        for product in group_products:
            rate = group_products[product]['rate']
            price = group_products[product]['price']
            quantity = group_products[product]['quantity']

            product_income += price * quantity

            product_expense += quantity * rate

        warehouse_profit = product_income - product_expense

        product_income = 0
        product_expense = 0


        for product in group_products:

            dataframe['warehouse_name'].append(group)
            dataframe['product'].append(product)

            quantity = group_products[product]['quantity']
            price = group_products[product]['price']
            rate = group_products[product]['rate']

            dataframe['quantity'].append(quantity)

            profit = quantity * price - quantity * rate

            dataframe['profit'].append(profit)

            profit_percentage = profit / warehouse_profit

            dataframe['percent_profit_product_of_warehouse'].append(profit_percentage)
            
    result = pd.DataFrame(data=dataframe)
    
    return result


task_4_result = calcuate_task_4(df_task_1)

print('Ответ на задание 4:\n\n', task_4_result)

df_task_5 =  task_4_result.sort_values(['warehouse_name','percent_profit_product_of_warehouse'],ascending=False).groupby('warehouse_name')

def calcuate_task_5(df):
    dataframe = {'warehouse_name':[], 'product':[], 'quantity':[], 'profit':[], 
                 'percent_profit_product_of_warehouse':[], 'accumulated_percent_profit_product_of_warehouse':[]}

    group_names = df.groups.keys()

    for group in group_names: 

        group_data = df.get_group(group)

        accumulated_percentage = 0

        for index, row in group_data.iterrows():
            dataframe['warehouse_name'].append(row['warehouse_name'])
            dataframe['product'].append(row['product'])
            dataframe['quantity'].append(row['quantity'])
            dataframe['profit'].append(row['profit'])
            dataframe['percent_profit_product_of_warehouse'].append(row['percent_profit_product_of_warehouse'])

            accumulated_percentage += row['percent_profit_product_of_warehouse']

            dataframe['accumulated_percent_profit_product_of_warehouse'].append(accumulated_percentage)


    result = pd.DataFrame(data=dataframe)   

    return result

result_task_5 = calcuate_task_5(df_task_5)

print('Ответ на задание 5:\n\n', result_task_5)


df_task_6 = result_task_5

def ranger(number):
    if number <= 0.7:
        return 'A'        
    elif 0.7 < number <= 0.9:
        return 'B'
    elif number > 0.9:
        return 'C'

df_task_6['category'] = df_task_6['accumulated_percent_profit_product_of_warehouse'].apply(ranger)
result_task_6 = df_task_6

print('Ответ на задание 6:')
result_task_6


