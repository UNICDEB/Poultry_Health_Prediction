Install Library: <br>
pip install pymongo pandas numpy scikit-learn <br>
pip install pickle <br><br>


Poultry Weight Prediction System <br>
This project is a Poultry Weight Prediction System that uses a pre-trained Machine Learning model to predict poultry weight based on real-time sensor data collected from IoT devices. 
The project integrates sensor data stored in MongoDB, processes it, and predicts the poultry weight using the given user inputs (Week and Feed Intake) combined with the computed min 
and max values for the last 24 hours. <br><br>

Features
Real-time data fetching from MongoDB for selected devices. <br>
Min/Max computation of sensor parameters (Temperature, Humidity, NH3, CO2, and Dust) for the last 24 hours. <br>
Integration with a pre-trained .pkl Machine Learning model to predict poultry weight. <br>
Customizable inputs: Week and Feed Intake. <br>
Device selection based on a unique device name.<br>

Table of Contents
Technologies Used
Installation
Database Schema
How It Works
Usage
Directory Structure
Contributing
License
Technologies Used
Programming Language: Python
Database: MongoDB
Libraries:
pymongo: For database interaction.
pandas: For data manipulation.
numpy: For numerical operations.
scikit-learn: For loading and using the .pkl Machine Learning model.
Installation
1. Clone the Repository
2. Set Up the Environment
3. MongoDB Configuration
Ensure you have a MongoDB server running.
Create a database named poultry_database and a collection named device_data (or update the code to reflect your database/collection names).
Insert your device data into the collection. See the Database Schema section for the required format.
4. Add Your Model
Place your pre-trained .pkl file in the project directory and update the model_path in the Python code.

Database Schema
Collection Name: device_data
Each document in the collection should follow this structure:

json <br>

{
  "device_name": "Device_1", <br>
  "timestamp": "2024-11-20T15:00:00", <br>
  "Temp": 30.5, <br>
  "Humd": 60.2, <br>
  "Nh3": 0.5, <br>
  "Co2": 400, <br>
  "Dust": 0.02 <br>
} <br> <br>

Explanation of Fields: <br>
device_name: Unique identifier for the IoT device. <br>
timestamp: Date and time of the data collection.<br>
Temp: Temperature recorded by the device.<br>
Humd: Humidity recorded by the device.<br>
Nh3: Ammonia levels recorded by the device.<br>
Co2: Carbon dioxide levels recorded by the device. <br>
Dust: Dust concentration recorded by the device.<br><br>

How It Works <br>
Sensor Data Retrieval:<br>
Sensor data is fetched for the selected device from MongoDB for the past 24 hours. <br>

Min/Max Computation:<br>

The minimum and maximum values are calculated for Temp, Humd, Nh3, Co2, and Dust.<br>
User Input:<br>
The user provides:<br>

Week: Week number (e.g., 1, 2, 3, etc.).<br>
Feed Intake: Feed consumption in kilograms.<br>
Feature Preparation:<br>
The computed min/max values, along with the user-provided inputs, are combined into a feature vector.<br>

Prediction:<br>
The feature vector is passed into the pre-trained .pkl model, which outputs the predicted poultry weight.<br>
