import pandas as pd
import matplotlib.pyplot as plt

def plot_laptop_prices(laptop_data):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(laptop_data["Price (Euro)"], bins=40, edgecolor='black')
    ax.set_title('Distribution of Laptop Prices')
    ax.set_xlabel('Price (Euro)')
    ax.set_ylabel('Number of Laptops')
    return fig


def load_laptop_data(datafile='laptop_price - dataset.csv') -> pd.DataFrame:
    try:
        laptop_data = pd.read_csv(datafile)
        return laptop_data
    except FileNotFoundError as e:
        print(f"No such file '{datafile}' in this directory.") 
        exit(e)
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as e:
        print(f"There is some data error.")
        exit(e)


def main():
    laptop_data = load_laptop_data()
    
    print(laptop_data)
    plot_laptop_prices(laptop_data)
    plt.show()

if __name__ == "__main__":
    main()