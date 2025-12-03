import csv


def write_data(data, filepath):
    """
    Write stock data to a CSV file.
    data = [["AAPL", 200, 250], ...]
    """
    with open(filepath, "w", encoding="utf8", newline="") as file:
        writer = csv.writer(file)
        header = ["name", "shares", "price"]
        writer.writerow(header)
        writer.writerows(data)


def read_csv(filepath):

    data = []
    with open(filepath, "r", encoding="utf8") as file:
        reader = csv.reader(file)

        # Read header row
        header = next(reader)

        # Convert rows into dictionaries
        for row in reader:
            item = {
                header[0]: row[0],
                header[1]: int(row[1]),
                header[2]: float(row[2]),
            }
            data.append(item)
    return data


def find_expensive_stocks(filepath):

    with open(filepath, "r", encoding="utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            price = float(row["price"])
            if price > 250:
                print({
                    "name": row["name"],
                    "shares": int(row["shares"]),
                    "price": price
                })


def calculate_total_value(filepath):

    total = 0.0
    with open(filepath, "r", encoding="utf8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            shares = int(row["shares"])
            price = float(row["price"])
            total += shares * price
    return total


def main():
    stocks = [
        ["AAPL", 200, 250],
        ["NVDA", 100, 500],
        ["META", 150, 200],
    ]

    file = "data/stocks.csv"

    write_data(stocks, file)

    # Read CSV as list of dicts
    data = read_csv(file)
    print("CSV DATA:", data)

    # Find expensive stocks
    print("\nExpensive stocks (>250):")
    find_expensive_stocks(file)

    # Calculate total portfolio value
    total_val = calculate_total_value(file)
    print("\nTotal Portfolio Value:", total_val)


main()
