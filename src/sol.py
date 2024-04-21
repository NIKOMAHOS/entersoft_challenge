import configparser
config = configparser.RawConfigParser()
config.read("../api_key.ini")

import cohere
#API_KEY = config[config.sections()[0]]['api_key']

co = cohere.Client('t8wpSMYmR1lntY7RrsMKblq2kKKbAzo60E7EPxDP')

import pandas as pd
# Load data to pandas dataframes:
sales_by_day = pd.read_csv('../data/raw/LastWeekSalesByDay.csv', delimiter=';')
top_customers = pd.read_csv('../data/raw/LastWeekTopCustomers.csv', delimiter=';')
top_products = pd.read_csv('../data/raw/LastWeekTopProducts.csv', delimiter=';')
order_statistics = pd.read_csv('../data/raw/LastWeekOrderStatistics.csv', delimiter=';')
cash_flow_report = pd.read_csv('../data/raw/CashFlowReport.csv', delimiter=';')
understocked_products = pd.read_csv('../data/raw/UnderstockedProducts.csv', delimiter=';')

import csv

# Initialize an empty dictionary to store the data
product_revenue = {}

# Read the CSV file and populate the dictionary
with open('../data/raw/LastWeekTopProducts.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        product_description = row['Product Description']
        revenue = int(row['Revenue'])
        product_revenue[product_description] = revenue

# Print the dictionary to verify
print(product_revenue)

# Initialize an empty dictionary to store the data
customer_revenue = {}

# Read the CSV file and populate the dictionary
with open('../data/raw/LastWeekTopCustomers.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        customer_name = row['Customer Name']
        revenue = int(row['Revenue'])
        customer_revenue[customer_name] = revenue

# Print the dictionary to verify
print(customer_revenue)


revenue_data = {}

# Read the CSV file and populate the dictionary
with open('../data/raw/LastWeekSalesByDay.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        date = row['Date']
        product_category = row['Product category']
        revenue = int(row['Revenue'])
        
        # If the product category already exists in the dictionary, update its revenue
        if product_category in revenue_data:
            revenue_data[product_category][date] = revenue
        # If the product category is new, add it to the dictionary with its revenue for the current date
        else:
            revenue_data[product_category] = {date: revenue}

channel_orders = {}

# Read the CSV file and populate the dictionary
with open('../data/raw/LastWeekOrderStatistics.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        channel = row['Channel']
        orders_count = int(row['Orders Count'])
        order_lines = int(row['Order Lines'])
        quantity_pieces = int(row['Quantity in pieces'])
        quantity_boxes = int(row['Quantity in boxes'])
        amount = int(row['Amount'])
        fulfillment_percentage = int(row['Percentage of fulfillment'])
        
        # Store the data in the dictionary
        channel_orders[channel] = {
            'Orders Count': orders_count,
            'Order Lines': order_lines,
            'Quantity in pieces': quantity_pieces,
            'Quantity in boxes': quantity_boxes,
            'Amount': amount,
            'Percentage of fulfillment': fulfillment_percentage
        }

financial_data = {}

# Read the CSV file and populate the dictionary
with open('../data/raw/CashFlowReport.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        debit = int(row['Debit'])
        credit = int(row['Credit'])
        balance = int(row['Balance'])
        inflows_forecast = int(row['Inflows Forecast'])
        outflows_forecast = int(row['Outflows Forecast'])
        projected_balance = int(row['Projected Balance'])
        
        # Store the data in the dictionary
        financial_data['Debit'] = debit
        financial_data['Credit'] = credit
        financial_data['Balance'] = balance
        financial_data['Inflows Forecast'] = inflows_forecast
        financial_data['Outflows Forecast'] = outflows_forecast
        financial_data['Projected Balance'] = projected_balance

understocked_product_data = {}

# Read the CSV file and populate the dictionary
with open('../data/raw/UnderstockedProducts.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile, delimiter=';')
    for row in reader:
        product_description = row['Product Description']
        minimum_stock = int(row['Minimum stock'])
        current_stock = int(row['Current stock'])
        expected_qty = int(row['Expected Qty'])
        required_stock = int(row['Required stock'])
        
        # Store the data in the dictionary
        understocked_product_data[product_description] = {
            'Minimum stock': minimum_stock,
            'Current stock': current_stock,
            'Expected Qty': expected_qty,
            'Required stock': required_stock
        }


def calculate_total_product_revenue():
    total_revenue = sum(product_revenue.values())
    return {
        'revenue': total_revenue,
        'summary': f"The total revenue from the top products is {total_revenue} euros."
    }   


def get_total_revenue_for_category(category):
    category_revenue = format(sum(revenue_data[category].values()), '.2f')
    return {'revenue_for_category': category_revenue, 
            'summary': f"The total revenue for the category {category} is {category_revenue}."
    }

def calculate_average_product_revenue():
    total_revenue = sum(product_revenue.values())
    num_products = len(product_revenue)
    average_revenue = total_revenue / num_products
    return {
        'average_revenue': round(average_revenue, 2),
        'summary': f"The average revenue per product is {average_revenue} euros."
    }

def retrieve_top_k_products(k):
    # Sort product_revenue dictionary by values (revenue) in descending order
    sorted_products = sorted(product_revenue.items(), key=lambda x: x[1], reverse=True)
    
    # Extract the top k products
    top_k_products = [product for product, revenue in sorted_products[:k]]
    
    return {
        'top_products': top_k_products,
        'summary': f"The top {k} products based on revenue are: {', '.join(top_k_products)}."
    }

def retrieve_least_k_products(k):
    # Sort product_revenue dictionary by values (revenue) in ascending order
    sorted_products = sorted(product_revenue.items(), key=lambda x: x[1])
    
    # Extract the least k products
    least_k_products = [product for product, revenue in sorted_products[:k]]
    
    return {
        'least_products': least_k_products,
        'summary': f"The least {k} products based on revenue are: {', '.join(least_k_products)}."
    }

def calculate_total_customer_revenue():
    total_revenue = sum(customer_revenue.values())
    return {
        'revenue': total_revenue,
        'summary': f"The total revenue from the top customers is {total_revenue} euros."
    }  

def get_total_revenue_for_customer(customer_name):
    revenue = customer_revenue.get(customer_name, 0)
    return {
        'revenue': revenue,
        'summary': f"The revenue from customer {customer_name} is {revenue} euros."
    }

def calculate_average_customer_revenue():
    total_revenue = sum(customer_revenue.values())
    num_customers = len(customer_revenue)
    average_revenue = total_revenue / num_customers
    return {
        'average_revenue': round(average_revenue, 2),
        'summary': f"The average revenue per customer is {average_revenue} euros."
    }

def retrieve_top_k_customers(k):
    # Sort customer_revenue dictionary by values (revenue) in descending order
    sorted_customers = sorted(customer_revenue.items(), key=lambda x: x[1], reverse=True)
    
    # Extract the top k customers
    top_k_customers = [customer for customer, revenue in sorted_customers[:k]]
    
    return {
        'top_customers': top_k_customers,
        'summary': f"The top {k} customers based on revenue are: {', '.join(top_k_customers)}."
    }

def retrieve_least_k_customers(k):
    # Sort customer_revenue dictionary by values (revenue) in ascending order
    sorted_customers = sorted(customer_revenue.items(), key=lambda x: x[1])
    
    # Extract the least k customers
    least_k_customers = [customer for customer, revenue in sorted_customers[:k]]
    
    return {
        'least_customers': least_k_customers,
        'summary': f"The least {k} customers based on revenue are: {', '.join(least_k_customers)}."
    }


def get_balance():
    return {'balance': financial_data['Balance'], 'summary': f"The balance is {balance}."}

def get_projected_balance():
    return {'projected_balance': financial_data['Projected Balance'], 'summary': f"The projected balance is {projected_balance}."}

def get_total_inflows():
    return {'total_inflows': financial_data['Inflows Forecast'], 'summary': f"The total inflows are {inflows_forecast}."}

def get_total_outflows():
    return {'total_outflows': financial_data['Outflows Forecast'], 'summary': f"The total outflows are {outflows_forecast}."}

def get_flows_difference():
    return {'flows_difference': financial_data['Inflows Forecast'] - financial_data['Outflows Forecast'], 'summary': f"The difference between inflows and outflows is {inflows_forecast - outflows_forecast}."}

def get_credit():
    return {'credit': financial_data['Credit'], 'summary': f"The credit is {credit}."}

def get_debit():
    return {'debit': financial_data['Debit'], 'summary': f"The debit is {debit}."}

def get_balance_loss():
    return {'balance_loss': financial_data['Debit'] - financial_data['Credit'], 'summary': f"The balance loss is {debit - credit}."}

def get_projected_balance_loss():
    diff = financial_data['Projected Balance'] - financial_data['Balance']
    if diff > 0:
        return {'projected_balance_loss': diff, 'summary': f"The projected balance is {diff} euros higher than the current balance."}
    elif diff < 0:
        return {'projected_balance_loss': diff, 'summary': f"The projected balance is {diff} euros lower than the current balance."}
    else:
        return {'projected_balance_loss': diff, 'summary': f"The projected balance is the same as the current balance."}

def get_channel_orders(channel):
    return {'channel_orders': channel_orders[channel], 'summary': f"The order statistics for the channel {channel} are {channel_orders[channel]}."}

def percentage_fulfilled(channel):
    return {'percentage_fulfilled': channel_orders[channel]['Percentage of fulfillment'], 'summary': f"The percentage of fulfillment for the channel {channel} is {channel_orders[channel]['Percentage of fulfillment']}."}

def get_orders_count(channel):
    return {'orders_count': channel_orders[channel]['Orders Count'], 'summary': f"The number of orders for the channel {channel} is {channel_orders[channel]['Orders Count']}."}

def highest_amount_channel():
    max_amount = 0
    max_channel = None
    for channel, data in channel_orders.items():
        if data['Amount'] > max_amount:
            max_amount = data['Amount']
            max_channel = channel
    return {'highest_amount_channel': max_channel, 'summary': f"The channel with the highest amount is {max_channel}."}

def calculate_average_order_values():
    total_revenue = channel_orders.get('Online Retailers')['Amount'] + channel_orders.get('Web Site')['Amount']
    total_orders = channel_orders.get('Online Retailers')['Orders Count'] + channel_orders.get('Web Site')['Orders Count']
    
    aov = total_revenue / total_orders
    return {
        'average_order_value': aov,
        'summary': f"The average order value is {aov:.2f}"}

# get most understocked products
def get_understocked_products():
    return {'understocked_products': understocked_product_data, 'summary': f"The understocked products are {understocked_product_data}."}

functions_map = {
    # Product functions
    "calculate_total_product_revenue": calculate_total_product_revenue,
    "get_total_revenue_for_category": get_total_revenue_for_category,
    "calculate_average_product_revenue" : calculate_average_product_revenue,
    "retrieve_top_k_products": retrieve_top_k_products,
    "retrieve_least_k_products": retrieve_least_k_products,

    # Customer functions
    "calculate_total_customer_revenue": calculate_total_customer_revenue,
    "get_total_revenue_for_customer": get_total_revenue_for_customer,
    "calculate_average_customer_revenue": calculate_average_customer_revenue,
    "retrieve_top_k_customers": retrieve_top_k_customers,
    "retrieve_least_k_customers": retrieve_least_k_customers,

    # Cash flow functions
    "get_total_inflows": get_total_inflows,
    "get_total_outflows": get_total_outflows,
    "get_flows_difference": get_flows_difference,
    "get_credit": get_credit,
    "get_debit": get_debit,
    "get_balance_loss": get_balance_loss,
    "get_projected_balance_loss": get_projected_balance_loss,
    "get_balance": get_balance,
    "get_projected_balance": get_projected_balance,

    # Order statistics functions
    "get_channel_orders": get_channel_orders,
    "percentage_fulfilled": percentage_fulfilled,
    "get_orders_count": get_orders_count,
    "highest_amount_channel": highest_amount_channel,
    "calculate_average_order_values":calculate_average_order_values,

    # Understocked products functions
    "get_understocked_products": get_understocked_products,
}

tools = [
    # Product tools
    {
        "name": "calculate_total_product_revenue",
        "description": "Calculate the total revenue from the top products.",
        "parameter_definitions": {}
    },
    {
        "name": "get_total_revenue_for_category",
        "description": "Get the revenue data for a specific product category.",
        "parameter_definitions": {
            "category": {
                "description": "The product category for which to get the revenue data.",
                "type": "str",
                "required": True
            }
        }
    },
    {
        "name": "calculate_average_product_revenue",
        "description": "Calculate the average revenue per product.",
        "parameter_definitions": {}
    },
    {
        "name": "retrieve_top_k_products",
        "description": "Retrieve the top products based on revenue.",
        "parameter_definitions": {
            "k": {
                "type": "int",
                "description": "Number of top products to retrieve."
            }
        }
    },
    {
        "name": "retrieve_least_k_products",
        "description": "Retrieve the least products based on revenue.",
        "parameter_definitions": {
            "k": {
                "type": "int",
                "description": "Number of least products to retrieve."
            }
        }
    },

    # Customer tools
    {
        "name": "calculate_total_customer_revenue",
        "description": "Calculate the total revenue from the top customers.",
        "parameter_definitions": {}
    },
    {
        "name": "get_total_revenue_for_category",
        "description": "Get the revenue data for a specific product category.",
        "parameter_definitions": {
            "category": {
                "description": "The product category for which to get the revenue data.",
                "type": "str",
                "required": True
            }
        }
    },
    {
        "name": "calculate_average_customer_revenue",
        "description": "Calculate the average revenue per customer.",
        "parameter_definitions": {}
    },
    {
        "name": "retrieve_top_k_customers",
        "description": "Retrieve the top customers based on revenue.",
        "parameter_definitions": {
            "k": {
                "type": "int",
                "description": "Number of top customers to retrieve."
            }
        }
    },
    {
        "name": "retrieve_least_k_customers",
        "description": "Retrieve the least customers based on revenue.",
        "parameter_definitions": {
            "k": {
                "type": "int",
                "description": "Number of least customers to retrieve."
            }
        }
    },

    # Cash flow tools
    {
        "name": "get_balance",
        "description": "Get the current balance.",
        "parameter_definitions": {}
    },
    {
        "name": "get_projected_balance",
        "description": "Get the projected balance.",
        "parameter_definitions": {}
    },
    {
        "name": "get_total_inflows",
        "description": "Get the total inflows forecast.",
        "parameter_definitions": {}
    },
    {
        "name": "get_total_outflows",
        "description": "Get the total outflows forecast.",
        "parameter_definitions": {}
    },
    {
        "name": "get_flows_difference",
        "description": "Get the difference between inflows and outflows.",
        "parameter_definitions": {}
    },
    {
        "name": "get_credit",
        "description": "Get the credit.",
        "parameter_definitions": {}
    },
    {
        "name": "get_debit",
        "description": "Get the debit.",
        "parameter_definitions": {}
    },
    {
        "name": "get_balance_loss",
        "description": "Get the balance loss.",
        "parameter_definitions": {}
    },
    {
        "name": "get_projected_balance_loss",
        "description": "Get the projected balance loss.",
        "parameter_definitions": {}
    },

    # Understocked products tools
        {
        "name": "get_understocked_products",
        "description": "Get the most understocked products.",
        "parameter_definitions": {}
    },

    # Order statistics tools
    {
        "name": "percentage_fulfilled",
        "description": "Get the percentage of fulfillment for a specific channel.",
        "parameter_definitions": {
            "channel": {
                "description": "The channel for which to get the percentage of fulfillment.",
                "type": "str",
                "required": True
            }
        }
    },
    {
        "name": "get_orders_count",
        "description": "Get the number of orders for a specific channel.",
        "parameter_definitions": {
            "channel": {
                "description": "The channel for which to get the number of orders.",
                "type": "str",
                "required": True
            }
        }
    },
        {
        "name": "get_channel_orders",
        "description": "Get the order statistics for a specific channel.",
        "parameter_definitions": {
            "channel": {
                "description": "The channel for which to get the order statistics.",
                "type": "str",
                "required": True
            }
        }
    },
    {
        "name": "highest_amount_channel",
        "description": "Get the channel with the highest amount.",
        "parameter_definitions": {}
    },
    {
        "name": "calculate_average_order_values",
        "description": "Calculate the average order values.",
        "parameter_definitions": {}
    }
]

preamble = """
##Task & Context: You are an AI assistant integrated with the company's Enterprise Resource Planning (ERP) system containing data from the last week only.
Your role is to help employees access and understand data from the ERP system through natural language interactions.
Employees will ask you questions or make requests related to various business operations like inventory, sales, accounting, manufacturing, etc. 
Your task is to query the relevant data from the ERP databases, analyze and synthesize it as needed, and provide helpful responses to the employees.

##Style Guide:
Use clear, professional language tailored for a workplace context.
Respond succinctly when possible, but provide detailed explanations when the query requires it.
Maintain objectivity and avoid injecting personal opinions unless explicitly asked.
Speak in the first-person from the perspective of an AI assistant (e.g. "I retrieved the latest inventory data from the system.")
Use proper formatting like bulleted lists, tables, and code snippets where appropriate to make responses easier to parse.
Do not include non-requested data, but do provide relevant additional context if it can enhance the usefulness of your response.
Be polite and constructive. If you cannot fulfill a request, explain why in a respectful manner.
"""
query = "Who were our top five customers by sales volume last week ?"

from cohere import ChatMessage
def create_chat(q):
    chat = co.chat(
        message=q, 
        model="command-r",
        preamble=preamble,
        tools=tools,
    )
    return chat

chat = create_chat(query)
print(chat.tool_calls)

print("The model recommends doing the following tool calls:")
print("\n".join(str(tool_call) for tool_call in chat.tool_calls))

import json

def tool_res(cha):
    tool_results = []
    for tool_call in cha.tool_calls:
        # print(f"=== Running tool: {tool_call.tool_name}, with parameters {tool_call.parameters}")
        if not tool_call.parameters:
            output = functions_map[tool_call.name]()
        else:
            output = functions_map[tool_call.name](**tool_call.parameters)
        outputs = [output]
        print(f"== tool results: {outputs}")
        tool_results.append({"call": tool_call, "outputs": outputs})

    return tool_results

print("The tool results that will be fed back to the model are:")
# print(json.dumps(tool_results, indent=4))

tool_results = tool_res(chat)

def get_responce(q):
    chat = create_chat(q)
    tool = tool_res(chat)
    return co.chat(message=q, tools=tools, tool_results=tool, preamble=preamble, model="command-r",temperature=0.3)

print('Final response:', get_responce(query).text)

