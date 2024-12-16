import pandas as pd


def load_json_to_dataframe(file_path, nrows=1000):
    """
    Load a JSON file into a pandas DataFrame and take the first n rows.

    Args:
        file_path (str): Path to the JSON file.
        nrows (int): Number of rows to extract.

    Returns:
        pd.DataFrame: DataFrame containing the first n rows.
    """
    chunks = []
    with open(file_path, "r") as f:
        for i, line in enumerate(f):
            if i == nrows:
                break
            chunks.append(pd.read_json(line, lines=True))
    return pd.concat(chunks, ignore_index=True)


def load_and_merge_yelp_data(
    business_file, review_file, checkin_file, tip_file, nrows=1000
):
    """
    Load and merge Yelp JSON datasets on 'business_id'.

    Args:
        business_file (str): Path to the business JSON file.
        review_file (str): Path to the review JSON file.
        checkin_file (str): Path to the checkin JSON file.
        tip_file (str): Path to the tip JSON file.
        nrows (int): Number of rows to extract from each JSON.

    Returns:
        pd.DataFrame: Combined DataFrame with relevant columns from Yelp datasets.
    """
    business = load_json_to_dataframe(business_file, nrows)
    review = load_json_to_dataframe(review_file, nrows)
    checkin = load_json_to_dataframe(checkin_file, nrows)
    tip = load_json_to_dataframe(tip_file, nrows)

    # Merge datasets step-by-step
    business_review = pd.merge(business, review, on="business_id", how="inner")
    business_review_checkin = pd.merge(
        business_review, checkin, on="business_id", how="inner"
    )
    final_data = pd.merge(business_review_checkin, tip, on="business_id", how="inner")

    return final_data


def load_restaurant_data(restaurant_file):
    """
    Load and clean the restaurant.csv dataset.

    Args:
        restaurant_file (str): Path to the restaurant CSV file.

    Returns:
        pd.DataFrame: Cleaned DataFrame with relevant columns.
    """
    restaurants = pd.read_csv(restaurant_file)
    restaurants_filtered = restaurants[
        [
            "Restaurant ID",
            "Restaurant Name",
            "City",
            "Address",
            "Latitude",
            "Longitude",
            "cuisine_type",
            "rating",
            "Votes",
        ]
    ].rename(
        columns={
            "Restaurant ID": "restaurant_id",
            "Restaurant Name": "name",
            "City": "city",
            "Address": "address",
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Votes": "review_count",
        }
    )
    return restaurants_filtered


def load_fast_food_data(fast_food_file):
    """
    Load and clean the fast food dataset.

    Args:
        fast_food_file (str): Path to the fast food CSV file.

    Returns:
        pd.DataFrame: Cleaned DataFrame with relevant columns.
    """
    # Load the dataset
    fast_food_df = pd.read_csv(fast_food_file)

    # Check available columns
    print("Available columns in fast_food_df:", fast_food_df.columns)

    # Substitute or skip missing columns
    fast_food_df["state"] = fast_food_df.get(
        "province", "Unknown"
    )  # Replace 'state' with 'province' if present
    fast_food_df["rating"] = fast_food_df.get(
        "rating", 0
    )  # Set default rating to 0 if missing

    # Select relevant columns
    relevant_columns = [
        "name",
        "categories",
        "address",
        "city",
        "state",
        "latitude",
        "longitude",
        "rating",
    ]
    fast_food_df = fast_food_df[
        [col for col in relevant_columns if col in fast_food_df.columns]
    ]

    # Rename columns for consistency
    fast_food_df.rename(
        columns={
            "name": "restaurant_name",
            "categories": "cuisine_type",
            "address": "location",
        },
        inplace=True,
    )

    return fast_food_df


def save_combined_and_cleaned_data(
    yelp_data, restaurant_data, fast_food_data, output_path
):
    """
    Save the combined Yelp, restaurant, and fast food data to a CSV file.

    Args:
        yelp_data (pd.DataFrame): Combined Yelp data.
        restaurant_data (pd.DataFrame): Cleaned restaurant.csv data.
        fast_food_data (pd.DataFrame): Cleaned fast food data.
        output_path (str): Path to save the final dataset.
    """
    combined_data = pd.concat(
        [yelp_data, restaurant_data, fast_food_data], ignore_index=True
    )
    combined_data.to_csv(output_path, index=False)
    print(f"Final combined dataset saved to {output_path}")


if __name__ == "__main__":
    # File paths
    business_file = "../data/yelp_academic_dataset_business.json"
    review_file = "../data/yelp_academic_dataset_review.json"
    checkin_file = "../data/yelp_academic_dataset_checkin.json"
    tip_file = "../data/yelp_academic_dataset_tip.json"
    restaurant_file = "../data/restaurants.csv"
    fast_food_file = "../data/american_fast_food.csv"
    output_path = "../data/final_combined_cleaned_data.csv"

    # Load and process Yelp data
    print("Processing Yelp datasets...")
    yelp_data = load_and_merge_yelp_data(
        business_file, review_file, checkin_file, tip_file
    )

    # Load and process restaurant.csv data
    print("Processing restaurant.csv dataset...")
    restaurant_data = load_restaurant_data(restaurant_file)

    # Load and process fast food data
    print("Processing fast food dataset...")
    fast_food_data = load_fast_food_data(fast_food_file)

    # Combine and save the final dataset
    print("Combining datasets and saving final data...")
    save_combined_and_cleaned_data(
        yelp_data, restaurant_data, fast_food_data, output_path
    )
