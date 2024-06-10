import math

def calculate_euclidean_distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

def convert_solomon_to_vrplib_with_weights(solomon_file, vrplib_file):
    with open(solomon_file, 'r') as file:
        lines = file.readlines()

    name, comment, dimension, capacity = None, None, None, None
    # get filename from solomon_file
    name = solomon_file.split('/')[-1].split('.')[0]
    comment = "SOLOMON"
    
    nodes = []
    demands = []

    for line in lines:
        if line.startswith("CAPACITY"):
            capacity = line.split()[-1]
        elif line.startswith("CUSTOMER"):
            break

    customer_section = False
    for line in lines:
        if line.startswith("CUSTOMER"):
            customer_section = True
            continue
        if customer_section:
            parts = line.split()
            if len(parts) == 7:
                cust_no, x, y, demand, *_ = parts
                nodes.append((int(cust_no), float(x), float(y)))
                demands.append((int(cust_no), int(demand)))
                
    dimension = len(nodes)

    with open(vrplib_file, 'w') as file:
        file.write(f"{name}\n")
        file.write("TYPE : CVRP\n")
        file.write(f"{comment}\n")
        file.write(f"DIMENSION : {dimension}\n")
        file.write("EDGE_WEIGHT_TYPE : EXPLICIT\n")
        file.write("EDGE_WEIGHT_FORMAT : FULL_MATRIX\n")
        file.write(f"CAPACITY : {capacity}\n")
        file.write("NODE_COORD_SECTION\n")
        for cust_no, x, y in nodes:
            file.write(f" {cust_no} {x} {y}\n")
        file.write("DEMAND_SECTION\n")
        for cust_no, demand in demands:
            file.write(f" {cust_no} {demand}\n")
        file.write("DEPOT_SECTION\n")
        file.write(" 1\n")
        file.write(" -1\n")
        file.write("EDGE_WEIGHT_SECTION\n")
        
        # Calculate and write the edge weights
        for i in range(len(nodes)):
            for j in range(len(nodes)):
                dist = calculate_euclidean_distance(nodes[i][1], nodes[i][2], nodes[j][1], nodes[j][2])
                file.write(f" {dist:.2f}")
            file.write("\n")
        
        file.write("EOF\n")

# Example usage
convert_solomon_to_vrplib_with_weights('instances/solomon/raw/r108.txt', 'instances/solomon/vrplib/r108.vrp')
