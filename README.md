# CTF Analytics

## About

The goal of the project is to extract data from a JSON source, parse it and ingest into a Postgres database. Model the data and finally create a dashboard to review the results.

## Purpose Of The Project

Develop the following skills:

1. Source: Familiarize with JSON structures and the information available
2. Data Modelling: Design the database, it's tables, relationships, implement constraints and indexes
3. Python: script to parse the JSON file and break it into the different tables
4. Analytics: Visualize the results using Python libraries i.e. Numpy, Pandas, Matplotlib, Seaborn

## About The Data

The data comes from [Faust CTF 2024](https://2024.faustctf.net/competition/scoreboard.json)

- [ ] Add table or summary of the JSON data

### Analyst List

1. Leaderboard

> Summarize teams performance

2. Services

> Display services status

3. Time Series

> Performance & Services evolution on time

## Approach Used

1. **Data Wrangling:** This is the first step where inspection of data is done to make sure **NULL** values and missing values are detected and data replacement methods are used to replace, missing or **NULL** values.

WIP - Specific calculations for the dashboard

> 1. Build a database
> 2. Create table and insert the data.
> 3. Select columns with null values in them. There are no null values in our database as in creating the tables, we set **NOT NULL** for each field, hence null values are filtered out.

2. **Feature Engineering:** This will help use generate some new columns from existing ones.

WIP - Specific calculations for the dashboard

3. **Exploratory Data Analysis (EDA):** Exploratory data analysis is done to answer the listed questions and aims of this project.

JSON Key Observations

Root-Level Fields: The JSON has a root-level tick and teams array. This aligns well with the parse_scoreboard_json() function, which expects these fields to extract tick and teams data.

Teams Array: Each entry within the teams array includes fields like rank, id, name, services, offense, defense, sla, total, image, and thumbnail. This structure matches the code’s expectation for team data processing:

Team details (such as team_id, rank, and name) go into the teams_df DataFrame.
Service details are parsed into a services_df DataFrame with additional information on each service's status, offense, defense, and sla.
Status Descriptions: To use status-descriptions, ensure it is either directly provided within the JSON, or the code will need adjustments if these descriptions are obtained from another source.

## Game Questions To Answer

### Generic Question

1. Which team consistently ranks the highest in overall score, and what factors contribute most to their success (offense, defense, or SLA)?

2. What are the top-performing services across all teams based on their offense, defense, and SLA scores, and how do these services affect team rankings?

3. How do service statuses (e.g., active, inactive, error) vary across teams, and which teams have the highest number of active or error-prone services?

4. Is there a trend in team performance over time (e.g., improving offense scores or maintaining SLA) across multiple ticks?

5. Which teams have the most balanced performance between offense and defense, and how does this balance affect their SLA and overall ranking?

6. What impact does a high or low SLA score have on team rankings, and are there correlations between SLA and team performance metrics (offense, defense)?

7. Which teams have the most frequent status changes in their services, and how do these changes correlate with their overall ranking trends?

8. How do images (if available) and descriptions contribute to team identity or brand, and is there a visual distinction between higher and lower-ranking teams?

9. Which teams are most improved or most declined in rank across multiple ticks, and what metrics (offense, defense, SLA) have influenced these changes?

10. What patterns emerge when comparing high and low-ranking teams’ service performance, particularly in how they prioritize offense, defense, and SLA?


### Calculations

WIP - Specific calculations for the dashboard

## Development

For the rest of the code, check the [Code](https://github.com/link to the file) file

1. Python dispatcher
2. PostgreSQL
3. Jupyter Notebook with Graphs (Pandas, Seaborn, Matplotlib)
