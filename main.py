import re
import pandas as pd
import matplotlib.pyplot as plt


def plot_laptop_prices(laptop_data: pd.DataFrame):
    # TODO change all magicstrings here to consts
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.hist(laptop_data["Price (Euro)"], bins=40, edgecolor="black")
    ax.set_title("Distribution of Laptop Prices")
    ax.set_xlabel("Price (Euro)")
    ax.set_ylabel("Number of Laptops")
    return fig


def plot_avg_laptop_prices_by_company(laptop_data: pd.DataFrame):
    # TODO change all magicstrings here to consts
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
    # TODO change all magicstrings here to consts
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
    # TODO change all magicstrings here to consts
    copy_data = laptop_data.copy()
    data_cleaned = remove_outliers(copy_data, "RAM (GB)")
    data_cleaned = remove_outliers(data_cleaned, "Price (Euro)")
    avg_price_by_ram = (
        data_cleaned.groupby("RAM (GB)")["Price (Euro)"].mean().reset_index()
    )
    avg_price_by_ram = avg_price_by_ram.sort_values("RAM (GB)")
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(
        avg_price_by_ram["RAM (GB)"],
        avg_price_by_ram["Price (Euro)"],
        marker="o",
        linestyle="-",
    )
    ax.set_title("Average Price by RAM Capacity")
    ax.set_xlabel("RAM (GB)")
    ax.set_ylabel("Average Price (Euro)")
    ax.grid(True, linestyle="--", alpha=0.7)
    return fig


def correlate_two_numeric_columns(data, column1, column2):
    return data[column1].corr(data[column2])


def list_all_unique_opsys(laptop_data: pd.DataFrame):
    # TODO change Opsys to a const
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
    # TODO change OpSys to a const
    data_copy["OpSys"] = data_copy["OpSys"].apply(simplify_os)
    return data_copy


def clean_memory_string(memory_column_name="Memory"):
    # TODO change Memory to a const
    cleaned = re.sub(r"[0-9.]+|GB|TB|MB", "", memory_column_name, flags=re.IGNORECASE)
    # Clean up whitespace (strip and collapse multiple spaces)
    return " ".join(cleaned.split())


def create_storage_column(laptop_data: pd.DataFrame):
    # TODO change Memory and Storage Type to a const
    """
    Takes a DataFrame, extracts the storage technology from 'Memory'
    by removing capacities (GB/TB) and numbers with regex, and adds a 'Storage Type' column.
    Regex breakdown:
    [0-9.]+ -> Matches digits and decimals (e.g., 128, 1.0)
    GB|TB|MB -> Matches the units (case insensitive)
    \\s+ -> Matches extra whitespace
    """
    new_laptop_data = laptop_data.copy()
    # Apply the cleaning logic to the Memory column
    new_laptop_data["Storage Type"] = new_laptop_data["Memory"].apply(
        clean_memory_string
    )

    return new_laptop_data


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
    plot_laptop_prices(laptop_data)
    plot_avg_laptop_prices_by_company(laptop_data)
    new_laptop_data = generalize_column_opsys(laptop_data)
    print(f"Operating Systems: {new_laptop_data["OpSys"].unique()}")
    for os_name in list_all_unique_opsys(new_laptop_data):
        plot_os_distribution_price(new_laptop_data, os_name)
    print(
        f"Correlation between RAM and price without Outliers:{correlate_two_numeric_columns(new_laptop_data, "RAM (GB)", "Price (Euro)")}"
    )
    plot_ram_and_price(new_laptop_data)
    print(create_storage_column(new_laptop_data))
    plt.show()


if __name__ == "__main__":
    main()
