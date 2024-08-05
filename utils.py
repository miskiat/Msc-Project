import pandas as pd

DATA_CSV_PATH = 'data/data.csv'

def process_csv(df, location, user_id):
    try:
        df['timestamp'] = pd.to_datetime(df['Time'], format='%Y/%m/%d %H:%M:%S')
        df['location'] = location
        df['user_id'] = user_id

        try:
            existing_df = pd.read_csv(DATA_CSV_PATH)
        except FileNotFoundError:
            existing_df = pd.DataFrame()

        df_to_save = pd.concat([existing_df, df], ignore_index=True)
        df_to_save.to_csv(DATA_CSV_PATH, index=False)
        return True
    except Exception as e:
        print(f"Error processing CSV: {e}")
        return False

def get_data():
    try:
        df = pd.read_csv(DATA_CSV_PATH)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        return df
    except FileNotFoundError:
        return pd.DataFrame()
