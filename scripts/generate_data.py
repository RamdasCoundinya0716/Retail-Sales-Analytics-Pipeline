from datetime import datetime, timedelta
import random
import uuid
import pandas as pd
from faker import Faker

fake = Faker("en_IN")


def generate_customers(n=1000):
    customers = []

    genders = ["Male", "Female"]

    for i in range(1, n + 1):
        customers.append(
            {
                "customer_id": f"CUST{i:06d}",
                "customer_name": fake.name(),
                "gender": random.choice(genders),
                "city": fake.city(),
                "state": fake.state(),
            }
        )

    return pd.DataFrame(customers)


def inject_customer_issues(df):
    df = df.copy()

    n_rows = len(df)

    # ----------------------------------
    # 1% missing names
    # ----------------------------------
    missing_name_idx = df.sample(frac=0.01).index
    df.loc[missing_name_idx, "customer_name"] = None

    # ----------------------------------
    # 1% invalid genders
    # ----------------------------------
    invalid_gender_idx = df.sample(frac=0.01).index

    invalid_values = [
        "M",
        "F",
        "Unknown",
        "",
        None,
    ]

    df.loc[invalid_gender_idx, "gender"] = [
        random.choice(invalid_values)
        for _ in range(len(invalid_gender_idx))
    ]

    # ----------------------------------
    # 1% leading/trailing spaces
    # ----------------------------------
    city_space_idx = df.sample(frac=0.01).index

    df.loc[city_space_idx, "city"] = (
        " "
        + df.loc[city_space_idx, "city"]
        + " "
    )

    # ----------------------------------
    # 1% duplicate rows
    # ----------------------------------
    duplicates = df.sample(frac=0.01)

    df = pd.concat(
        [df, duplicates],
        ignore_index=True
    )

    return df

def generate_products(n=200):

    categories = {
        "Electronics": [
            "Laptop",
            "Phone",
            "Tablet",
            "Headphones",
            "Smartwatch",
        ],
        "Clothing": [
            "T-Shirt",
            "Jeans",
            "Jacket",
            "Shirt",
            "Hoodie",
        ],
        "Home": [
            "Chair",
            "Table",
            "Lamp",
            "Sofa",
            "Fan",
        ],
        "Books": [
            "Novel",
            "Textbook",
            "Biography",
            "Cookbook",
            "Dictionary",
        ],
        "Sports": [
            "Football",
            "Cricket Bat",
            "Basketball",
            "Tennis Racket",
            "Dumbbell",
        ],
    }

    brands = [
        "Nike",
        "Adidas",
        "Samsung",
        "Apple",
        "Sony",
        "HP",
        "Dell",
        "Puma",
        "Boat",
        "Generic",
    ]

    products = []

    for i in range(1, n + 1):

        category = random.choice(
            list(categories.keys())
        )

        product_name = random.choice(
            categories[category]
        )

        products.append(
            {
                "product_id": f"PROD{i:06d}",
                "product_name": product_name,
                "category": category,
                "brand": random.choice(brands),
                "price": round(
                    random.uniform(100, 100000),
                    2,
                ),
            }
        )

    return pd.DataFrame(products)
def inject_product_issues(df):

    df = df.copy()

    # Missing category
    idx = df.sample(frac=0.01).index
    df.loc[idx, "category"] = None

    # Negative price
    idx = df.sample(frac=0.01).index
    df.loc[idx, "price"] *= -1

    # Zero price
    idx = df.sample(frac=0.01).index
    df.loc[idx, "price"] = 0

    # Inconsistent categories
    idx = df.sample(frac=0.01).index

    replacements = [
        "electronics",
        "ELECTRONICS",
        "Electronic",
    ]

    df.loc[idx, "category"] = [
        random.choice(replacements)
        for _ in range(len(idx))
    ]

    return df

def generate_stores(n=20):

    stores = []

    for i in range(1, n + 1):

        stores.append(
            {
                "store_id": f"STORE{i:03d}",
                "store_name": f"{fake.city()} Retail Store",
                "city": fake.city(),
                "state": fake.state(),
            }
        )

    return pd.DataFrame(stores)

def inject_store_issues(df):

    df = df.copy()

    # Missing city
    idx = df.sample(frac=0.05).index
    df.loc[idx, "city"] = None

    # Duplicate stores
    duplicates = df.sample(frac=0.10)

    df = pd.concat(
        [df, duplicates],
        ignore_index=True
    )

    return df
def random_date():
    start = datetime(2024, 1, 1)
    end = datetime(2025, 12, 31)

    delta = end - start

    return start + timedelta(
        days=random.randint(0, delta.days)
    )


def generate_sales(
    customers_df,
    products_df,
    stores_df,
    n=100_000
):

    sales = []

    customer_ids = (
        customers_df["customer_id"]
        .dropna()
        .unique()
        .tolist()
    )

    store_ids = (
        stores_df["store_id"]
        .dropna()
        .unique()
        .tolist()
    )

    products = (
        products_df[
            ["product_id", "price"]
        ]
        .dropna()
        .to_dict("records")
    )

    order_number = 1

    while len(sales) < n:

        order_id = f"ORD-{order_number:08d}"

        customer_id = random.choice(customer_ids)

        store_id = random.choice(store_ids)

        order_date = random_date()

        # Each order contains 1-5 products
        num_items = random.randint(1, 5)

        selected_products = random.sample(
            products,
            min(num_items, len(products))
        )

        for product in selected_products:

            if len(sales) >= n:
                break

            quantity = random.randint(1, 10)

            unit_price = round(
                float(product["price"]),
                2
            )

            sales_amount = round(
                quantity * unit_price,
                2
            )

            sales.append(
                {
                    "sale_id": str(uuid.uuid4()),
                    "order_id": order_id,
                    "date_id": int(
                        order_date.strftime("%Y%m%d")
                    ),
                    "customer_id": customer_id,
                    "product_id": product["product_id"],
                    "store_id": store_id,
                    "quantity": quantity,
                    "unit_price": unit_price,
                    "sales_amount": sales_amount,
                }
            )

        order_number += 1

    return pd.DataFrame(sales)
def inject_sales_issues(df):

    df = df.copy()

    n_rows = len(df)

    # ---------------------------
    # 1% Null Customer IDs
    # ---------------------------
    idx = df.sample(frac=0.01).index
    df.loc[idx, "customer_id"] = None

    # ---------------------------
    # 1% Invalid Product IDs
    # ---------------------------
    idx = df.sample(frac=0.01).index
    df.loc[idx, "product_id"] = "PROD999999"

    # ---------------------------
    # 1% Negative Quantities
    # ---------------------------
    idx = df.sample(frac=0.01).index
    df.loc[idx, "quantity"] = (
        df.loc[idx, "quantity"] * -1
    )

    # ---------------------------
    # 1% Future Dates
    # ---------------------------
    idx = df.sample(frac=0.01).index
    df.loc[idx, "date_id"] = 20350101

    # ---------------------------
    # 1% Wrong Sales Amounts
    # ---------------------------
    idx = df.sample(frac=0.01).index

    df.loc[idx, "sales_amount"] = (
        df.loc[idx, "sales_amount"] *
        random.uniform(1.5, 5.0)
    ).round(2)

    # ---------------------------
    # 1% Duplicate Rows
    # ---------------------------
    duplicates = df.sample(frac=0.01)

    df = pd.concat(
        [df, duplicates],
        ignore_index=True
    )

    return df

def main():

    customers = generate_customers(1000)

    customers = inject_customer_issues(customers)

    customers.to_csv(
        "data/raw/customers.csv",
        index=False
    )

    products = generate_products(200)

    products = inject_product_issues(products)

    products.to_csv(
        "data/raw/products.csv",
        index=False
    )

    stores = generate_stores(20)

    stores = inject_store_issues(stores)

    stores.to_csv(
        "data/raw/stores.csv",
        index=False
    )
    sales = generate_sales(
    customers,
    products,
    stores,
    n=100000
)

    sales = inject_sales_issues(sales)

    sales.to_csv(
        "data/raw/sales.csv",
        index=False
    )
    
if __name__ == "__main__":
    main()