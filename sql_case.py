import sqlite3
import random

def setup_database():
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # Create Table 'ads_performance' to match the user's query schema
    cursor.execute('''
        CREATE TABLE ads_performance (
            campaign_name TEXT,
            cost REAL,
            revenue REAL
        )
    ''')
    
    return conn

def generate_mock_data(conn):
    cursor = conn.cursor()
    
    data_points = []
    
    # 1. Contributing Campaigns (Good)
    for _ in range(10):
        data_points.append(('Brand_Search_USA', 100.0, 400.0))
        data_points.append(('Generic_Shoes_Global', 50.0, 80.0))
        data_points.append(('Competitor_Conquesting', 120.0, 150.0))

    # 2. Leaking Campaign (Bad)
    # High Cost, Zero Revenue entries
    for _ in range(5):
        data_points.append(('Retargeting_Leaking_Campaign', 200.0, 0.0))

    cursor.executemany('INSERT INTO ads_performance VALUES (?,?,?)', data_points)
    conn.commit()

def run_analysis(conn):
    try:
        with open('revenue_analysis.sql', 'r') as f:
            query = f.read()
            
        cursor = conn.cursor()
        cursor.execute(query)
        
        columns = [description[0] for description in cursor.description]
        rows = cursor.fetchall()
        
        # Pretty Print
        header = " | ".join([f"{col:<20}" for col in columns])
        print(header)
        print("-" * len(header))
        
        for row in rows:
            # Format row
            formatted = []
            for item in row:
                if isinstance(item, float):
                    formatted.append(f"${item:<19.2f}")
                else:
                    formatted.append(f"{str(item):<20}")
            print(" | ".join(formatted))

    except Exception as e:
        print(f"SQL Execution Error: {e}")

if __name__ == "__main__":
    conn = setup_database()
    generate_mock_data(conn)
    print("Running SQL Revenue Leakage Analyzer...\n")
    run_analysis(conn)
    conn.close()
