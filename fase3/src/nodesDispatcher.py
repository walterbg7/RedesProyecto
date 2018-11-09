import csv
import utilities

with open('nodes.csv', 'rt',  encoding="utf8") as csvfile:
    nodesReader = csv.DictReader(csvfile)
    for row in nodesReader:
        try:
            print(row['IP'], row['Mask'], row['Port'])
            # I need to check if the parameter in the csv file are valid
            # I need to create a new terminal and run the 'node.py' program with the row parameters on that terminal
        except Exception as e:
            print("Error: Invalid csv file format!")
