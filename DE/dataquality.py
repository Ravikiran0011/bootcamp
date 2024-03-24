import pandas as pd
import os
import re
import logging
from logging.handlers import RotatingFileHandler

# Function to count lines in a file
def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r') as file:
            line_count = sum(1 for line in file)
        return line_count
    except FileNotFoundError:
        return None  # Log file not found

# File paths
csv_file_path = "users_Data.csv"
log_file_path = 'Data_Quality_Issues.log'
csv_quality_path = 'quality_percent_v2.csv'

# Remove existing log file
if os.path.exists(log_file_path):
    os.remove(log_file_path)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    handlers=[
        RotatingFileHandler(log_file_path, maxBytes=1048576, backupCount=5)  # 1 MB max size, keep 5 backups
    ]
)

# Load CSV data into a DataFrame
df = pd.read_csv(csv_file_path)

# Define a regular expression pattern for validating email format
email_pattern = r'^[\w\.-]+@[a-zA-Z\d\.-]+\.[a-zA-Z]{2,}$'

# Data quality checks for each row
for index, row in df.iterrows():
    for column, value in row.items():
        if column == 'name':
            # Check if the 'name' value is a string
            if not isinstance(value, str):
                logging.error(f"Row {index + 1}: Name should be a string.")
        elif column == 'email':
            # Check if the 'email' value matches the email format pattern
            if not re.match(email_pattern, value):
                logging.error(f"Row {index + 1}: Invalid email format.")

# Calculate quality percentage
df_size = df.size
line_count = count_lines_in_file(log_file_path)
Qualitypercent = round((df_size - line_count) / df_size * 100, 2)

# Save quality percentage to a CSV file
df_quality = pd.DataFrame({'Quality Percent': [Qualitypercent]})
df_quality.to_csv(csv_quality_path, index=False)

# Print status messages
print("Quality percentage data saved to CSV file:", csv_quality_path)
if line_count != 0:
    print("Some data Customers is not in good quality")
else:
    print("All the Customers data is in good quality")
