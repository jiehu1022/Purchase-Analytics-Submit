#!/usr/bin/python3
"""
    author: Jie Hu
    email: tojiehu@gmail.com
    date: 2019-07-06
"""

import sys

def read_products(products_file):
    products_data = {}
    with open(products_file) as products:
        # pass the first row
        products.readline()
        for line in products:
            # Remove whitepsace
            line = line.strip()
            fields = line.split(',')
            # only process the valid record
            if len(fields) == 4:
                product_id = fields[0].strip()
                department_id = fields[3].strip()
                products_data[product_id] = department_id
    return products_data


def process_orders(products_data, order_products_file):
    department_data = {}
    with open(order_products_file) as orders:
        # pass the first row
        orders.readline()
        for line in orders:
            line = line.strip()
            fields = line.split(',')
            if len(fields) != 4:
                continue
            current_order_id = fields[0].strip()
            d_id = fields[1].strip()
            if d_id not in products_data:
                # in case we can not find the department id
                continue;
            current_department_id = products_data[d_id]
            current_reorderd = int(fields[3].strip())
            if current_department_id not in department_data:
                department_data[current_department_id] = {}
                department_data[current_department_id]['total'] = 0
                department_data[current_department_id]['first'] = 0
            department_data[current_department_id]['total'] += 1
            if current_reorderd == 0:
                department_data[current_department_id]['first'] += 1
    return department_data

def output_result(department_data, output_file):
    data = []
    for department, value in department_data.items():
        data.append([int(department), value['total'], value['first']])
    data = sorted(data, key=lambda d: d[0])
    # open file and with write
    with open(output_file, "w") as output:
        # write the first line
        output.writelines("department_id,number_of_orders,number_of_first_orders,percentage\n")
        for item in data:
            department_id = item[0]
            number_of_orders = item[1]
            number_of_first_orders = item[2]
            percentage = item[2] / item[1]
            str_price = '{0},{1},{2},{3:.2f}\n'.format(
                department_id,
                number_of_orders,
                number_of_first_orders,
                percentage
            )
            output.writelines(str_price)

def main():
    # check input parameters
    if len(sys.argv) < 4:
        print("please input: purchase_analytics.py input_file1 input_file2 output_file")
        # there is a error
        exit(1)
    # read command line parameters
    order_products_file = sys.argv[1]
    products_file = sys.argv[2]
    output_file = sys.argv[3]
    # read products data to get product_id => department id mapping
    product_department_map = read_products(products_file)
    # process the data order by order.
    department_data = process_orders(product_department_map, order_products_file)

    output_result(department_data, output_file)

if __name__ == "__main__":
    main()
