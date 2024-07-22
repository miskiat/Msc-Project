import csv
from flask_login import UserMixin
from datetime import datetime

# Define file paths
USER_CSV = 'data/users.csv'
DATAFILE_CSV = 'data/data_files.csv'
SENSORDATA_CSV = 'data/sensor_data.csv'


class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def get(user_id):
        with open(USER_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['id'] == user_id:
                    return User(row['id'], row['username'], row['password'])
        return None

    @staticmethod
    def authenticate(username, password):
        with open(USER_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row['username'] == username and row['password'] == password:
                    return User(row['id'], row['username'], row['password'])
        return None


class DataFile:
    def __init__(self, id, location, timestamp, user_id):
        self.id = id
        self.location = location
        self.timestamp = timestamp
        self.user_id = user_id

    @staticmethod
    def load_datafiles():
        datafiles = []
        with open(DATAFILE_CSV, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                datafiles.append(DataFile(**row))
        return datafiles


class SensorData:
    @staticmethod
    def load_sensordata(location=None):
        sensor_data = []
        with open(SENSORDATA_CSV, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                if location is None or row.get('location') == location:
                    sensor_data.append(row)
        return sensor_data

    @staticmethod
    def get_statistics():
        sensor_data = SensorData.load_sensordata()
        num_locations = len(set(row.get('location', '') for row in sensor_data))
        num_users = len(set(row.get('user_id', '') for row in sensor_data))
        num_records = len(sensor_data)
        return num_locations, num_users, num_records
