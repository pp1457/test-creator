import csv

def write_to_csv(filename: str, fields, rows):
    with open(filename, 'w') as csvFile:
        csvWriter = csv.writer(csvFile)
        csvWriter.writerow(fields)
        csvWriter.writerows(rows)

if __name__ == "__main__":
    fields = ["Name", "Hobit", "Friend"]
    rows = [
            ["Paul", "Play", "Vivian"],
            ["Vivian", "Play", "Paul"],
            ["Who", "What", "None"]
           ]
    write_to_csv("write.csv", fields, rows)


