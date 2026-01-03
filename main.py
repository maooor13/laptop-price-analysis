import pandas as pd
import matplotlib.pyplot as plt


def plot_laptop_prices(laptop_data: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(laptop_data["Price (Euro)"], bins=40, edgecolor="black")
    ax.set_title("Distribution of Laptop Prices")
    ax.set_xlabel("Price (Euro)")
    ax.set_ylabel("Number of Laptops")
    return fig


def plot_avg_laptop_prices_by_company(laptop_data: pd.DataFrame):
    fig, ax = plt.subplots(figsize=(10, 5))
    companies_avg = (
        laptop_data.groupby("Company")["Price (Euro)"]
        .mean()
        .sort_values(ascending=True)
    )
    companies_avg.plot(ax=ax, kind="barh", edgecolor="black")
    ax.set_title("Distribution of Average Laptop Prices (By Company)")
    ax.set_xlabel("Average Price (Euro)")
    ax.set_ylabel("Company")
    return fig


def plot_os_distribution_price(laptop_data: pd.DataFrame, os_name: str):
    """
    Plot for each of the operating system types the distribution of the prices, so that
    the number of plots equals to the number of unique operating systems.
    """
    fig, ax = plt.subplots(figsize=(10, 5))
    os_data = laptop_data[laptop_data["OpSys"] == os_name]
    ax.hist(os_data["Price (Euro)"], edgecolor="black")
    ax.set_title(f"Distribution of Price for Operation System {os_name}")
    ax.set_xlabel("Average Price (Euro)")
    ax.set_ylabel("Operating System")
    return fig


def plot_ram_and_price(laptop_data: pd.DataFrame):
    copy_data = laptop_data.copy()
    data_cleaned = remove_outliers(copy_data, "RAM (GB)")
    data_cleaned = remove_outliers(data_cleaned, "Price (Euro)")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(data_cleaned["RAM (GB)"], data_cleaned["Price (Euro)"], "x")
    return fig


def correlate_two_numeric_columns(data, column1, column2):
    return data[column1].corr(data[column2])


def list_all_unique_opsys(laptop_data: pd.DataFrame):
    unfiltered_opsys = pd.Series(laptop_data["OpSys"].unique())
    return unfiltered_opsys


def list_all_opsys(laptop_data: pd.DataFrame):
    unique_opsys = list_all_unique_opsys(laptop_data)
    return generalize_opsys(unique_opsys)


def generalize_opsys(specific_opsys: pd.Series):
    return specific_opsys.apply(simplify_os).unique()


def simplify_os(name: str):
    lowered_name = name.lower()
    if "windows" in lowered_name:
        return "Windows"
    if "mac" in lowered_name:
        return "macOS"
    return name


def generalize_column_opsys(laptop_data: pd.DataFrame):
    data_copy = laptop_data.copy()
    data_copy["OpSys"] = data_copy["OpSys"].apply(simplify_os)
    return data_copy


def remove_outliers(df, column):
    """
    Removes outliers from a specific column using the IQR method.
    """
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]


def load_laptop_data(datafile="laptop_price - dataset.csv") -> pd.DataFrame:
    try:
        laptop_data = pd.read_csv(datafile)
        return laptop_data
    except FileNotFoundError as e:
        print(f"No such file '{datafile}' in this directory.")
        exit(e)
    except (pd.errors.ParserError, pd.errors.EmptyDataError) as e:
        print("There is some data error.")
        exit(e)


def main():
    laptop_data = load_laptop_data()
    new_laptop_data = generalize_column_opsys(laptop_data)
    # print(laptop_data)
    # plot_laptop_prices(laptop_data)
    # plot_avg_laptop_prices_by_company(laptop_data)
    # plt.show()
    # for os_name in list_all_unique_opsys(new_laptop_data):
    # print(plot_os_distribution_price(new_laptop_data, os_name))
    plot_ram_and_price(new_laptop_data)
    plt.show()
    print(correlate_two_numeric_columns(new_laptop_data, "RAM (GB)", "Price (Euro)"))


if __name__ == "__main__":
    main()
