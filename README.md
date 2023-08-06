## Title 
A High Schooler's Guide to Choosing a College

## Purpose  
This application was created to assist high schooler seniors to decide on which college they would like to attend. Using this application, high school seniors can see different aspects of universities such as what research topics they specialize in, how many publications they've put out, and the number of faculty. 

## Demo  
https://mediaspace.illinois.edu/media/t/1_0x2bjtav

## Installation

1. Start Neo4j Server
2. Make sure mysql_utils.py, mongodb_utils.py, and neo4j_utils.py and app.py are all in the same directory
3. Open mysql_utils.py and neo4j_utils.py and change the pw and usernames for connections to the servers where appropriate
4. Open terminal and navigate to the directory containing the files above.
5. Run app.py and the terminal should output the following message: Dash is running on http://127.0.0.1:8053/. Copy and paste that http to a browser and enter

## Usage

The application consists of 6 widgets. Below are descriptions of each widget:  
**Research Interests by University**: The user will select a university from the dropdown menu and the app will output the top ten keywords associated with faculty affiliated with the selected university along with the number of times it occurs among the faculty members  
**Publications Filtered by Research Interes**: The user will select a keyword from the dropdown menu and the app will output a table containing all of the publications associated with the keyword along with the faculty member and university that are attached to the publication  
**Keyword Frequency By University**: The dropdown used above will also output a pie chart showing the percentage that each university occupies for the kwyword  
**KRC Score for Keyword by University**: The user will select a keyword from the dropdown menu and the app will output a bar chart containing the keyword-relevant citation scores for each university for the selected keyword 
**Number of Publications Over the Years**: The user will select a university and the app will output a line chart showing the number of publications for that university between 2000 and 2020  
**University Characteristics**: The user will select a university and the app will output a table containing characteristics of that university.  

## Design 
The application consists of 6 widgets that are organized vertically one on top of the other in order for the user to explore the widgets sequentially

## Implementation
The application was created using plotly.dash and all data manipulation was done using the Pandas library in Python.  

## Database Techniques
1. An index was created in the mongodb_utils.py file on the name column for the keywords table in order to speed up the query considering the keyword name is used as a filter
2. A view was created in the mysql_utils.py file that is queried thereafter to create a table in the application
3. A NOT NULL constraint is used in the mysql_utils.py file on university name because that field cannot be null or else the table will fail

## Contributions
I created this application alone. 
