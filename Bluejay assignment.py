import pandas as pd

# Load the CSV file into a DataFrame
file_path = r"C:\Users\Mohammad Sharique\Downloads\Assignment_Timecard.csv"
df = pd.read_csv(file_path, parse_dates=['Time', 'Time Out'])

# Function to check consecutive days
def has_consecutive_days(entries, threshold_days):
    return (entries['Time'].diff().dt.days.abs() >= threshold_days - 1).any()

# Function to check time between shifts
def has_valid_shift_times(entries, min_hours, max_hours):
    time_between = entries['Time'].shift(-1) - entries['Time Out']
    return ((min_hours < time_between.dt.total_seconds() / 3600) & (time_between.dt.total_seconds() / 3600 < max_hours)).any()

# Function to check total hours in a single shift
def has_long_shift(entries, threshold_hours):
    return ((entries['Time Out'] - entries['Time']).dt.total_seconds() / 3600 > threshold_hours).any()

# Analyzing the data
for employee, entries in df.groupby('Employee Name'):
    if has_consecutive_days(entries, 7):
        print(f"{employee} has worked for 7 consecutive days.")
    
    if has_valid_shift_times(entries, 1, 10):
        print(f"{employee} has less than 10 hours between shifts but greater than 1 hour.")
    
    if has_long_shift(entries, 14):
        print(f"{employee} has worked for more than 14 hours in a single shift.")
