import pymongo
import pandas as pd
import datetime
import pickle
import numpy as np

# Load the trained ML model
model_path = "model.pkl"  # Replace with your actual path
with open(model_path, 'rb') as file:
    model = pickle.load(file)

# MongoDB connection
def connect_to_mongodb():
    client = pymongo.MongoClient("mongodb://localhost:27017/")  # Replace with your MongoDB URI
    db = client["poultry_database"]  # Replace with your database name
    return db

# Function to fetch sensor data for a specific device from MongoDB
def fetch_sensor_data(db, device_name):
    collection = db["device_data"]  # Replace with your collection name
    current_time = datetime.datetime.now()
    last_24_hours = current_time - datetime.timedelta(hours=24)

    # Query to fetch last 24 hours of data for the given device
    query = {"device_name": device_name, "timestamp": {"$gte": last_24_hours, "$lte": current_time}}
    data = list(collection.find(query))

    if not data:
        raise ValueError(f"No data found for device '{device_name}' in the last 24 hours.")

    # Convert to a Pandas DataFrame for easier processing
    df = pd.DataFrame(data)

    # Ensure relevant columns are present
    required_columns = ['Temp', 'Humd', 'Nh3', 'Co2', 'Dust']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Column '{col}' missing in device data.")

    return df

# Calculate min and max values for each parameter
def calculate_min_max(df):
    min_max_values = {
        'Temp_Min': df['Temp'].min(),
        'Temp_Max': df['Temp'].max(),
        'Humd_Min': df['Humd'].min(),
        'Humd_Max': df['Humd'].max(),
        'Nh3_Min': df['Nh3'].min(),
        'Nh3_Max': df['Nh3'].max(),
        'Co2_Min': df['Co2'].min(),
        'Co2_Max': df['Co2'].max(),
        'Dust_Min': df['Dust'].min(),
        'Dust_Max': df['Dust'].max()
    }
    return min_max_values

# Function to make a prediction
def predict_poultry_weight(min_max_values, week, feed_intake):
    # Prepare the input features in the required order
    input_features = [
        week,
        min_max_values['Temp_Max'], min_max_values['Temp_Min'],
        min_max_values['Humd_Max'], min_max_values['Humd_Min'],
        min_max_values['Nh3_Max'], min_max_values['Nh3_Min'],
        min_max_values['Co2_Max'], min_max_values['Co2_Min'],
        min_max_values['Dust_Max'], min_max_values['Dust_Min'],
        feed_intake
    ]

    # Convert to a 2D array for model prediction
    input_features = np.array(input_features).reshape(1, -1)

    # Make prediction
    predicted_weight = model.predict(input_features)[0]
    return predicted_weight

# Main function
def main():
    db = connect_to_mongodb()

    # User inputs
    device_name = input("Enter the device name: ")
    Current_week = int(input("Enter the week number: "))
    week = int(input("Enter the Predicted week: "))
    feed_intake = float(input("Enter the feed intake value: "))

    # Fetch and process sensor data
    try:
        df = fetch_sensor_data(db, device_name)
        min_max_values = calculate_min_max(df)
    except Exception as e:
        print(f"Error: {e}")
        return

    # Predict poultry weight
    try:
        predicted_weight = predict_poultry_weight(min_max_values, week, feed_intake)
        print(f"Predicted Poultry Weight: {predicted_weight:.2f} gm")
    except Exception as e:
        print(f"Prediction Error: {e}")

if __name__ == "__main__":
    main()
