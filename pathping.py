import pandas as pd
import subprocess
import re
from pyvis.network import Network
dfip=pd.read_csv(r"C:\Users\DANIEL\Downloads\endpoints_to_graph.csv")
net = Network(notebook=True, directed=True) 
added_nodes = set()
added_edges = set()
for index, row in dfip.iterrows():
    previous_address=None
    # Run the command adjust the -q value based on the amount of ICMP you want to send
    command = f"pathping {str(row['ip'])} -q 10"
    result = subprocess.run(command, stdout=subprocess.PIPE, shell=True)
    output = result.stdout.decode()
    lines = output.split('\n')

    # Define a regular expression that matches the lines we're interested in
    regex = r"\s*(\d+)\s+(\d+)ms\s+([0-9]|\d\d)/\s\s(\d\d)\s=\s\s(100|[1-9]?\d\s*%)\s\s\s\s\s([0-9]|\d\d)/\s\s(\d\d)\s=\s\s(100|[1-9]?\d\s*%)\s\s(([\w\.-]+)\s*\[([\d\.]+)\]|([\d\.]+))"
    data = []

    for line in lines:
        match = re.match(regex, line)
        if match:

            hop = match.group(1)
            rtt = match.group(2)
            lost_1 = match.group(3)
            sent_1 = match.group(4)
            pct_1= match.group(5)
            lost_2 = match.group(6)
            sent_2= match.group(7)
            pct_2 = match.group(8)
            address1 = match.group(9)
            data.append({'hop': hop, 'rtt': rtt, 'lost_sent_1': f"{lost_1}/{sent_1}", 'pct_1': pct_1, 
                        'lost_sent_2': f"{lost_2}/{sent_2}", 'pct_2': pct_2, 'address1': address1})
    df = pd.DataFrame(data)
    print(df)

    # Create a directed network
    for index2, row2 in df.iterrows():
        address = str(row2['address1'])

        # Only add node if it's not added yet
        if address not in added_nodes:
            net.add_node(address)
            added_nodes.add(address)

        if previous_address is not None:
            # Only add edge if it's not added yet
            edge = (previous_address, address)
            if edge not in added_edges:
                net.add_edge(*edge,label=str(row2['rtt']))
                added_edges.add(edge)

        previous_address = address

# Show the graph
net.show('cloudflare.html')
net.save_graph('cloudflare.html')





