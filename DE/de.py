import pymongo
import time
import pandas as pd
from datetime import datetime, timedelta
import threading
import os  # Import the os module for accessing file paths

# MongoDB connection string
connection_string = "mongodb+srv://ravi:ravi123@cluster0.1egcrvd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Connect to the MongoDB cluster
client = pymongo.MongoClient(connection_string)

# Database name
db_name = "test"

# Collection name
collection_name = "users"

csv_file_path = "users_Data.csv"
parquet_file_path = "users_Data.parquet"

def incremental_update():
    # Connect to the database
    db = client[db_name]
    collection = db[collection_name]

    # Query for all entries in the collection
    all_entries = collection.find({})

    # Convert MongoDB cursor to a DataFrame
    df = pd.DataFrame(list(all_entries))

    # Drop the '_id' column
    df = df.drop('_id', axis=1)

    # Add time column with current timestamp
    df['time'] = pd.Timestamp.now()

    # Print the DataFrame
    print("DataFrame:")
    print(df)

    # Save data to CSV
    df.to_csv(csv_file_path, index=False)

    # Save data to Parquet
    df.to_parquet(parquet_file_path, engine='pyarrow')

    print("Data saved to CSV and Parquet files on the desktop.")

def job():
    while True:
        print("Running incremental update...")
        incremental_update()
        time.sleep(60)  # Wait for 60 seconds before next execution

# Start the initial job
job()
