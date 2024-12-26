import requests
import json
import pandas as pd

# Load api key
with open('api_key.txt') as f:
    api_key = f.read()

# Start and end years
start_year = 2023
start_month = 6
end_year = 2024
end_month = 8

# List to store the results
date_strings = []

# Loop through years and months
current_year = start_year
current_month = start_month

while current_year < end_year or (current_year == end_year and current_month < end_month):
    # Calculate the next month and year
    next_year = current_year
    next_month = current_month + 1
    if next_month > 12:
        next_month = 1
        next_year += 1
    
    # Format the string and append to the list
    date_strings.append(f"{current_year:04d}-{current_month:02d}-01+{next_year:04d}-{next_month:02d}-01")
    
    # Increment the month and adjust the year if needed
    current_month += 1
    if current_month > 12:
        current_month = 1
        current_year += 1


related_topics_trump = []
related_topics_biden = []
related_queries_trump = []
related_queries_biden = []
queries = ["trump", "biden"]
types = ["RELATED_TOPICS","RELATED_QUERIES"]

for q in queries:
    print(q)
    for t in types:
        print(t)
        for date in date_strings:
            print(date)
            uri = f"https://serpapi.com/search.json?engine=google_trends&q={q}&data_type={t}&date={date}&api_key={api_key}"

            response = requests.get(uri)

            # Parse the JSON response
            data = response.json()

            # Collect rising topics for each candidate
            if q == "trump":
                if t == "RELATED_TOPICS":
                    related_topics_trump.append([item['topic']['title'] for item in data['related_topics']['rising']])
                else:
                    related_queries_trump.append([item['query'] for item in data['related_queries']['rising']])
            else:
                if t == "RELATED_TOPICS":
                    related_topics_biden.append([item['topic']['title'] for item in data['related_topics']['rising']])
                else:
                    related_queries_biden.append([item['query'] for item in data['related_queries']['rising']])

# Create dataframes for Trump and Biden
trump = pd.DataFrame({"date": date_strings, "topics": related_topics_trump, "queries": related_queries_trump})
trump = pd.concat([trump['date'].str.split('+', expand=True),trump.drop(columns=['date'])], axis=1)
trump.columns = ["start_date","end_date","topics","queries"]

biden = pd.DataFrame({"date": date_strings, "topics": related_topics_biden, "queries": related_queries_biden})
biden = pd.concat([biden['date'].str.split('+', expand=True),biden.drop(columns=['date'])], axis=1)
biden.columns = ["start_date","end_date","topics","queries"]

trump.to_csv("../data/csv/trump_trends.csv", index=False)
biden.to_csv("../data/csv/biden_trends.csv", index=False)