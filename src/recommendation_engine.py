import pandas as pd


def top_five_restaurants():
    """
    Suggest the top 5 restaurants based on overall rating.

    Returns:
        pd.DataFrame: A DataFrame of the top 5 highest-rated restaurants.
    """
    try:
        # Load the combined cleaned dataset
        data = pd.read_csv("../data/final_combined_cleaned_data.csv")

        # Return the top 5 highest-rated restaurants
        return data.nlargest(5, "rating")[["name", "address", "cuisine_type", "rating"]]
    except FileNotFoundError:
        print("Error: The file 'data/final_combined_cleaned_data.csv' was not found.")
        return pd.DataFrame()  # Return an empty DataFrame if the file is missing
    except KeyError as e:
        print(f"Error: Missing required column in the dataset - {e}")
        return pd.DataFrame()  # Return an empty DataFrame if columns are missing


if __name__ == "__main__":
    print("Top 5 Restaurants Based on Overall Rating:\n")
    recommendations = top_five_restaurants()

    if not recommendations.empty:
        print(recommendations)
    else:
        print("No recommendations available.")
