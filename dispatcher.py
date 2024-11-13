import os
from dotenv import load_dotenv
import json
import pandas as pd
import requests # Import requests to fetch data from URL
from sqlalchemy import create_engine, Integer, String, Float, JSON, text
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

def parse_scoreboard_json(json_data):
    """
    Parse the scoreboard JSON and convert it into DataFrame format suitable for PostgreSQL
    """
    # Extract the base data
    tick = json_data['tick']
    current_time = datetime.now()
    
    # Create teams DataFrame
    teams_data = []
    for team in json_data['teams']:
        team_base = {
            'team_id': team['id'],
            'name': team['name'],
            'rank': team['rank'],
            'total_offense': team['offense'],
            'total_defense': team['defense'],
            'total_sla': team['sla'],
            'total_score': team['total'],
            'image_path': team.get('image', '/uploads/team-images/default.png'),
            'thumbnail_path': team.get('thumbnail', '/uploads/team-images/thumbnails/default.png'),
            'tick': tick,
            'recorded_at': current_time
        }
        teams_data.append(team_base)
    
    teams_df = pd.DataFrame(teams_data)
    
    # Create services DataFrame with status descriptions
    services_data = []
    status_descriptions = json_data['status-descriptions']
    
    for team in json_data['teams']:
        for service_idx, service in enumerate(team['services']):
            service_data = {
                'team_id': team['id'],
                'service_index': service_idx,
                'status': service['status'],
                'status_description': status_descriptions[str(service['status'])],
                'offense': service['offense'],
                'defense': service['defense'],
                'sla': service['sla'],
                'tick': tick,
                'recorded_at': current_time
            }
            services_data.append(service_data)
    
    services_df = pd.DataFrame(services_data)
    
    return teams_df, services_df

def create_tables(engine):
    """
    Create the necessary PostgreSQL tables if they don't exist
    """
    # Teams table with unique constraint on team_id
    teams_sql = text("""
    CREATE TABLE IF NOT EXISTS teams (
        id SERIAL PRIMARY KEY,
        team_id INTEGER NOT NULL UNIQUE,
        name VARCHAR(255) NOT NULL,
        rank INTEGER NOT NULL,
        total_offense FLOAT NOT NULL,
        total_defense FLOAT NOT NULL,
        total_sla FLOAT NOT NULL,
        total_score FLOAT NOT NULL,
        image_path VARCHAR(255) NOT NULL,
        thumbnail_path VARCHAR(255) NOT NULL,
        tick INTEGER NOT NULL,
        recorded_at TIMESTAMP NOT NULL
    );
    """)
    
    # Services table with foreign key reference to teams table
    services_sql = text("""
    CREATE TABLE IF NOT EXISTS services (
        id SERIAL PRIMARY KEY,
        team_id INTEGER NOT NULL,
        service_index INTEGER NOT NULL,
        status INTEGER NOT NULL,
        status_description VARCHAR(50) NOT NULL,
        offense FLOAT NOT NULL,
        defense FLOAT NOT NULL,
        sla FLOAT NOT NULL,
        tick INTEGER NOT NULL,
        recorded_at TIMESTAMP NOT NULL,
        FOREIGN KEY (team_id) REFERENCES teams(team_id)
    );
    """)
    
    with engine.connect() as conn:
        conn.execute(teams_sql)
        conn.execute(services_sql)
        conn.commit()

def load_data_to_postgres(json_url, db_connection_string):
    """
    Main function to load JSON data into PostgreSQL
    """
     # Fetch JSON data from the URL
    response = requests.get(json_url)
    response.raise_for_status()  # Check if the request was successful
    json_data = response.json()  # Parse the response JSON
    
    # Create database engine
    engine = create_engine(db_connection_string)
    
    # Create tables
    create_tables(engine)
    
    # Parse JSON into DataFrames
    teams_df, services_df = parse_scoreboard_json(json_data)
    
    # Load data into PostgreSQL
    teams_df.to_sql('teams', engine, if_exists='append', index=False)
    services_df.to_sql('services', engine, if_exists='append', index=False)

if __name__ == "__main__":
    # Load environment variables from .env file
    load_dotenv()
    
    # Get the database connection details from environment variables
    db_host = os.environ.get('DB_HOST')
    db_port = os.environ.get('DB_PORT')
    db_name = os.environ.get('DB_NAME')
    db_user = os.environ.get('DB_USER')
    db_password = os.environ.get('DB_PASSWORD')
    json_link = os.environ.get('JSON_LINK')
    
    # Construct the database connection string
    db_connection_string = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
    
    # URL to the JSON file
    json_url = f"{json_link}"  # Replace with actual URL
    
    # Call the main function
    load_data_to_postgres(json_url, db_connection_string)
