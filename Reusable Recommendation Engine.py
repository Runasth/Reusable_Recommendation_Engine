import pandas as pd
import argparse
import os

def load_data(file_path='ratings.csv'):
    """
    Loads user ratings data from a CSV file and pivots it into a user-item matrix.
    The CSV should have 'user', 'movie', and 'rating' columns.

    Args:
        file_path (str): The path to the CSV file.

    Returns:
        pandas.DataFrame or None: A DataFrame in user-item matrix format, or None if an error occurs.
    """
    # Check if the file exists, and create a sample if it doesn't.
    if not os.path.exists(file_path):
        print(f"'{file_path}' not found. Creating a sample file for demonstration.")
        sample_data = {
            'user': ['Alice', 'Alice', 'Alice', 'Alice', 'Bob', 'Bob', 'Bob', 'Bob', 'Charlie', 'Charlie', 'Charlie', 'David', 'David', 'David', 'David', 'Eve', 'Eve', 'Eve', 'Frank', 'Frank', 'Frank'],
            'movie': ['The Matrix', 'Inception', 'The Godfather', 'Pulp Fiction', 'The Matrix', 'Inception', 'The Dark Knight', 'Forrest Gump', 'The Godfather', 'Pulp Fiction', 'The Dark Knight', 'Inception', 'The Dark Knight', 'Forrest Gump', 'The Matrix', 'Pulp Fiction', 'The Godfather', 'The Matrix', 'The Dark Knight', 'Forrest Gump', 'Inception'],
            'rating': [5, 4, 3, 5, 4, 5, 5, 2, 5, 4, 3, 3, 4, 5, 2, 5, 4, 4, 5, 5, 4]
        }
        pd.DataFrame(sample_data).to_csv(file_path, index=False)

    try:
        # Read the data from the CSV.
        ratings_df = pd.read_csv(file_path)
        # Check if the required columns exist.
        if not {'user', 'movie', 'rating'}.issubset(ratings_df.columns):
            print(f"Error: The CSV file must contain 'user', 'movie', and 'rating' columns.")
            return None
        # Pivot the DataFrame to create the user-item matrix.
        user_item_matrix = ratings_df.pivot(index='movie', columns='user', values='rating')
        return user_item_matrix
    except pd.errors.EmptyDataError:
        print(f"Error: The file '{file_path}' is empty.")
        return None
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return None

def recommend_movies(df, target_user, num_recommendations=2):
    """
    Generates movie recommendations for a target user using user-based collaborative filtering.

    Args:
        df (pandas.DataFrame): The user-item matrix.
        target_user (str): The user for whom to generate recommendations.
        num_recommendations (int): The number of movies to recommend.

    Returns:
        list or str: A list of recommended movie titles, or an error string.
    """
    # --- Collaborative Filtering Logic ---
    # Use Pearson correlation to find similarity between users.
    user_similarity = df.corr(method='pearson', min_periods=2)

    # Get the ratings of the target user.
    target_user_ratings = df[target_user]

    # Find users who are similar to the target user, sorted by similarity.
    similar_users = user_similarity[target_user].drop(target_user).sort_values(ascending=False)

    recommendations = {}

    # Iterate through similar users to find movie recommendations.
    for user, similarity_score in similar_users.items():
        # Only consider users with a positive similarity score.
        if similarity_score <= 0:
            continue

        other_user_ratings = df[user]

        # Find movies the similar user liked but the target user hasn't seen.
        for movie, rating in other_user_ratings.items():
            if pd.isna(target_user_ratings.get(movie)) and rating >= 4:
                # Weight the rating by the similarity score.
                if movie not in recommendations:
                    recommendations[movie] = 0
                recommendations[movie] += similarity_score * rating

    # Sort the recommendations by their calculated score.
    sorted_recommendations = sorted(recommendations.items(), key=lambda item: item[1], reverse=True)
    
    # Return the top N recommendations.
    return [movie for movie, score in sorted_recommendations[:num_recommendations]]

def main():
    """
    Main function to run the recommendation engine from the command line.
    """
    # --- Command-Line Interface ---
    parser = argparse.ArgumentParser(
        description="A simple movie recommendation engine using user-based collaborative filtering.",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('--user', type=str, required=True, help='The user ID to get recommendations for.')
    parser.add_argument('--num_recs', type=int, default=2, help='Number of recommendations to generate (default: 2).')
    parser.add_argument('--file', type=str, default='ratings.csv', help='Path to the ratings CSV file (default: ratings.csv).')
    args = parser.parse_args()

    # --- Run the Engine ---
    data_matrix = load_data(args.file)

    if data_matrix is None:
        return # Exit if data loading failed.

    if args.user not in data_matrix.columns:
        print(f"\nError: User '{args.user}' not found in the dataset.")
        print(f"Available users are: {list(data_matrix.columns)}")
        return

    recommendations = recommend_movies(data_matrix, args.user, args.num_recs)

    print(f"\n--- Generating recommendations for {args.user} ---\n")

    if isinstance(recommendations, list):
        if recommendations:
            print(f"Top {args.num_recs} recommendations for {args.user}:")
            for i, movie in enumerate(recommendations, 1):
                print(f"{i}. {movie}")
        else:
            print(f"Could not generate new recommendations for {args.user}.")
            print("This could be because they have already seen all movies liked by similar users.")
    else:
        print(recommendations) # Print error message if one occurred.

if __name__ == "__main__":
    # This block makes the script executable from the command line.
    main()