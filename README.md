Simple Movie Recommendation Engine

This project provides a simple, command-line based movie recommendation engine written in Python. It uses a user-based collaborative filtering algorithm to suggest movies to a user based on the preferences of similar users.


Features
Data-driven: Loads user, movie, and rating data from a CSV file.

Collaborative Filtering: Implements a user-based filtering algorithm from scratch using pandas.

Customizable: Easily specify the target user and the number of recommendations to generate via command-line arguments.

User-friendly: Automatically creates a sample ratings.csv file if one is not found, making it easy to run out of the box.


How It Works
The engine is based on the principle that if two users have rated movies similarly in the past, they are likely to have similar tastes in the future.

Load Data: The script reads a CSV file containing user ratings and transforms it into a user-item matrix, where rows are movies and columns are users.

Calculate Similarity: It then calculates the Pearson correlation coefficient between the target user and all other users. This creates a similarity score, where 1 means very similar tastes and -1 means opposite tastes.

Generate Recommendations: The script identifies movies that highly-rated, similar users have liked but that the target user has not yet seen. It ranks these potential recommendations and returns the top results.


Requirements
Python 3.6+

pandas


Installation
Clone the repository:

git clone https://github.com/Runasth/Reusable_Recommendation_Engine.git
cd Reusable_Recommendation_Engine



Install dependencies:
It's recommended to use a virtual environment.

python -m venv venv
source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Create a file named requirements.txt with the following content:

pandas

Then, install the requirements:

pip install -r requirements.txt

Usage
You can run the recommendation engine directly from your terminal.

1. Prepare Your Data
The script requires a CSV file (by default ratings.csv) with three columns: user, movie, and rating.

Example ratings.csv:

user,movie,rating
Alice,The Matrix,5
Alice,Inception,4
Bob,The Matrix,4
Bob,The Dark Knight,5
Charlie,The Godfather,5
Charlie,Pulp Fiction,4
...

If you run the script without a ratings.csv file, a sample one will be created for you automatically.

2. Run the Script
Use the --user flag to specify the user you want recommendations for.

To get 2 recommendations for "Alice":

python recommendation_engine.py --user Alice

To get 3 recommendations for "David":

python recommendation_engine.py --user David --num_recs 3

To use a different data file named my_data.csv:

python recommendation_engine.py --user Frank --file my_data.csv

If you specify a user who is not in the dataset, the script will print an error and a list of available users.

License
This project is licensed under the MIT License. See the LICENSE file for details.
