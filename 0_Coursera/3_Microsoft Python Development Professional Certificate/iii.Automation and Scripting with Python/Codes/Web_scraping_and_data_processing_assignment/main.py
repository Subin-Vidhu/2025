# Step 3.1: Fetch HTML Content
# Please be careful to follow instructions on how to run the program; 
# the Run menu or right-click > Run options do not work in the simulated environment. 
# Ensure you have run the terminal command to install the correct libraries using pip.
# You must use the terminal window as directed in Step 3.
### YOUR CODE HERE ###
import requests
from bs4 import BeautifulSoup
import pandas as pd
# Fetch the webpage content
url = "http://127.0.0.1:5500/baseball_stats.html"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Print the HTML content to inspect
print(soup.prettify())
# Step 3.2: Extract the Required Data
### YOUR CODE HERE ###
table_body = soup.find('tbody')

# Find all table rows
table_rows = table_body.find_all('tr')

# Initialize an empty list to store the data
data = []

# Iterate over each table row
for row in table_rows:
    # Find all table data in the row
    table_data = row.find_all('td')
    
    # Extract the data from each table data
    game_id = table_data[0].text
    team1 = table_data[1].text
    team2 = table_data[2].text
    expected_runs_team1 = table_data[3].text
    expected_runs_team2 = table_data[4].text
    over_under = table_data[5].text
    moneyline_favorite = table_data[6].text
    
    # Store the data in a dictionary
    game_data = {
        'GameID': game_id,
        'Team 1': team1,
        'Team 2': team2,
        'Expected Runs (Team 1)': expected_runs_team1,
        'Expected Runs (Team 2)': expected_runs_team2,
        'Over/Under': over_under,
        'Moneyline Favorite': moneyline_favorite
    }
    
    # Append the dictionary to the data list
    data.append(game_data)

# Print the extracted data
for game in data:
    print(game)
# Step 4.1: Convert to a DataFrame
# Import pandas
### YOUR CODE HERE ###
# Convert the data list into a DataFrame
df = pd.DataFrame(data)

# Inspect the DataFrame
### YOUR CODE HERE ###
print(df)
# Save and print the shaped data
### YOUR CODE HERE ###
# Save and print the shaped data
print("Number of rows and columns in the DataFrame: ", df.shape)
print("Columns in the DataFrame: ", df.columns)
print("Data types of each column: ", df.dtypes)
print("Summary statistics of the DataFrame: ", df.describe())
# Step 5.1: Save to a CSV File
# Save the DataFrame to a CSV file named sports_statistics.csv
### YOUR CODE HERE ###
df.to_csv('sports_statistics.csv', index=False)