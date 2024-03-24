
import pandas as pd
import pymongo
from cryptography.fernet import Fernet

# MongoDB connection
client = pymongo.MongoClient("mongodb+srv://ravi:ravi123@cluster0.1egcrvd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client["test"]
collection = db["policies"]

# Encryption/Decryption key
key = b'Qy8JNTlaEjyDcEvNinW1Zbur1tIbLXvydv93k1QhE8k='
cipher_suite = Fernet(key)

# Encryption function
def encrypt(data):
    if data:
        return cipher_suite.encrypt(data.encode()).decode()
    return None

# Masking function
def mask(data):
    if data:
        return '*' * len(data)
    return None

# Access the MongoDB collection, create DataFrame with policy information
policies_cursor = collection.find({})
policies = pd.DataFrame(list(policies_cursor))

# Calculate total number of open and closed policies for each policy
claims_data = {
    'Policy ID': policies['id'],
    'Claim Status': ['Open'] * len(policies)  # Assume all policies have open status initially
}
claims_df = pd.DataFrame(claims_data)
policy_claims_summary = claims_df.groupby('Policy ID')['Claim Status'].value_counts().unstack(fill_value=0)
policy_claims_summary.columns = ['Total Open Policies']
policy_claims_summary.reset_index(inplace=True)

# Merge policy data with claims summary to get total number of open policies
policies = pd.merge(policies, policy_claims_summary, left_on='id', right_on='Policy ID', how='left')

# Calculate total number of closed policies
policies['Total Closed Policies'] = len(claims_df) - policies['Total Open Policies']

# Encrypt and mask PII data
policies['Encrypted Name'] = policies['name'].apply(encrypt)
policies['Encrypted Address'] = policies['address'].apply(encrypt)
policies['Masked Name'] = policies['name'].apply(mask)
policies['Masked Address'] = policies['address'].apply(mask)

# Print the resulting dataset
print("Dataset with policy information:")
print(policies)

# Print encrypted and masked PII data
print("\nEncrypted and Masked PII data:")
print(policies[['id', 'Encrypted Name', 'Masked Name', 'Encrypted Address', 'Masked Address', 'amount', 'status', 'Total Open Policies', 'Total Closed Policies']])
