import json
import random
import time
from datetime import datetime, timedelta
import csv
import psycopg2

# Database connection details
DB_NAME = 'finalproject'
DB_USER = 'postgres'
DB_PASSWORD = 'boaz0099'
DB_HOST = 'project2.czq46i0iwlfj.us-east-1.rds.amazonaws.com'
DB_PORT = '5432'

# Connect to PostgreSQL
try:
    conn = psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )
    cur = conn.cursor()
    print("Connection to the database established successfully.")
except psycopg2.Error as err:
    print(f"Error: {err}")
    exit(1)

# Function to create tables
def create_tables():
    create_orders_table = """
    CREATE TABLE IF NOT EXISTS orders (
        order_id INT PRIMARY KEY,
        user_id INT,
        product_id INT,
        quantity INT,
        price DECIMAL(10, 2),
        order_date TIMESTAMP,
        city VARCHAR(100),
        latitude DECIMAL(9, 6),
        longitude DECIMAL(9, 6),
        description TEXT
    );
    """
    create_user_interactions_table = """
    CREATE TABLE IF NOT EXISTS user_interactions (
        interaction_id INT PRIMARY KEY,
        user_id INT,
        product_id INT,
        interaction_type VARCHAR(50),
        interaction_date TIMESTAMP,
        city VARCHAR(100),
        latitude DECIMAL(9, 6),
        longitude DECIMAL(9, 6),
        description TEXT
    );
    """
    create_inventory_updates_table = """
    CREATE TABLE IF NOT EXISTS inventory_updates (
        update_id INT PRIMARY KEY,
        product_id INT,
        inventory_change INT,
        update_date TIMESTAMP,
        city VARCHAR(100),
        latitude DECIMAL(9, 6),
        longitude DECIMAL(9, 6),
        air_quality_index INT
    );
    """
    cur.execute(create_orders_table)
    cur.execute(create_user_interactions_table)
    cur.execute(create_inventory_updates_table)
    conn.commit()

# List of 15 fixed cities in Andhra Pradesh with their coordinates
cities = [
    {"city": "Visakhapatnam", "latitude": 17.6868, "longitude": 83.2185},
    {"city": "Vijayawada", "latitude": 16.5062, "longitude": 80.6480},
    {"city": "Guntur", "latitude": 16.3067, "longitude": 80.4365},
    {"city": "Nellore", "latitude": 14.4426, "longitude": 79.9865},
    {"city": "Kurnool", "latitude": 15.8281, "longitude": 78.0373},
    {"city": "Rajahmundry", "latitude": 17.0005, "longitude": 81.8040},
    {"city": "Tirupati", "latitude": 13.6288, "longitude": 79.4192},
    {"city": "Kakinada", "latitude": 16.9891, "longitude": 82.2475},
    {"city": "Eluru", "latitude": 16.7107, "longitude": 81.0952},
    {"city": "Kadapa", "latitude": 14.4673, "longitude": 78.8242},
    {"city": "Anantapur", "latitude": 14.6819, "longitude": 77.6006},
    {"city": "Vizianagaram", "latitude": 18.1067, "longitude": 83.3955},
    {"city": "Ongole", "latitude": 15.5057, "longitude": 80.0499},
    {"city": "Nandyal", "latitude": 15.477, "longitude": 78.4836},
    {"city": "Machilipatnam", "latitude": 16.1875, "longitude": 81.1389}
]

# Function to generate random date not greater than the current date
def generate_random_date():
    current_time = datetime.now()
    random_date = current_time - timedelta(days=random.randint(0, 365))
    return random_date

# Function to generate random order
def generate_order():
    city = random.choice(cities)
    order = {
        "order_id": random.randint(1000, 9999),
        "user_id": random.randint(1, 100),
        "product_id": random.randint(1, 50),
        "quantity": random.randint(1, 5),
        "price": round(random.uniform(10.0, 500.0), 2),
        "order_date": generate_random_date(),
        "city": city['city'],
        "latitude": city['latitude'],
        "longitude": city['longitude'],
        "description": "Order description for visualization"
    }
    return order

# Function to generate random user interaction
def generate_user_interaction():
    city = random.choice(cities)
    interaction = {
        "interaction_id": random.randint(1000, 9999),
        "user_id": random.randint(1, 100),
        "product_id": random.randint(1, 50),
        "interaction_type": random.choice(["view", "click", "add_to_cart"]),
        "interaction_date": generate_random_date(),
        "city": city['city'],
        "latitude": city['latitude'],
        "longitude": city['longitude'],
        "description": "Interaction description for visualization"
    }
    return interaction

# Function to generate random inventory update
def generate_inventory_update():
    city = random.choice(cities)
    update = {
        "update_id": random.randint(1000, 9999),
        "product_id": random.randint(1, 50),
        "inventory_change": random.randint(-20, 20),
        "update_date": generate_random_date(),
        "city": city['city'],
        "latitude": city['latitude'],
        "longitude": city['longitude'],
        "air_quality_index": random.randint(0, 500)
    }
    return update

# Function to send data to PostgreSQL
def send_data_to_rds(data, table_name):
    if table_name == 'orders':
        query = """
        INSERT INTO orders (order_id, user_id, product_id, quantity, price, order_date, city, latitude, longitude, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            data['order_id'],
            data['user_id'],
            data['product_id'],
            data['quantity'],
            data['price'],
            data['order_date'],
            data['city'],
            data['latitude'],
            data['longitude'],
            data['description']
        ))
    elif table_name == 'user_interactions':
        query = """
        INSERT INTO user_interactions (interaction_id, user_id, product_id, interaction_type, interaction_date, city, latitude, longitude, description)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            data['interaction_id'],
            data['user_id'],
            data['product_id'],
            data['interaction_type'],
            data['interaction_date'],
            data['city'],
            data['latitude'],
            data['longitude'],
            data['description']
        ))
    elif table_name == 'inventory_updates':
        query = """
        INSERT INTO inventory_updates (update_id, product_id, inventory_change, update_date, city, latitude, longitude, air_quality_index)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cur.execute(query, (
            data['update_id'],
            data['product_id'],
            data['inventory_change'],
            data['update_date'],
            data['city'],
            data['latitude'],
            data['longitude'],
            data['air_quality_index']
        ))
    conn.commit()

# Function to write data to CSV files
def write_data_to_csv(data, table_name):
    file_name = f"{table_name}.csv"
    fieldnames = data.keys()
    with open(file_name, mode='a', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(data)

# Function to simulate real-time data generation and ingestion
def simulate_real_time_data():
    while True:
        data_type = "order"
        if data_type == "order":
            data = generate_order()
            send_data_to_rds(data, 'orders')
            write_data_to_csv(data, 'orders')
        elif data_type == "interaction":
            data = generate_user_interaction()
            send_data_to_rds(data, 'user_interactions')
            write_data_to_csv(data, 'user_interactions')
        else:
            data = generate_inventory_update()
            send_data_to_rds(data, 'inventory_updates')
            write_data_to_csv(data, 'inventory_updates')

        print(json.dumps(data, default=str))  # Log the data for debugging
        time.sleep(random.uniform(0.5, 2))  # Simulate real-time by waiting a random interval

if __name__ == "__main__":
    try:
        create_tables()
        simulate_real_time_data()
    except KeyboardInterrupt:
        cur.close()
