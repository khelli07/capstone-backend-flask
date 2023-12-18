from flask import Blueprint, jsonify, request
import pandas as pd
from surprise import Reader, Dataset
from surprise.model_selection import KFold, GridSearchCV
from surprise import SVD

popularBP = Blueprint("popular", __name__)


@popularBP.route("/", methods=["GET"])
def infer():
    event_table = pd.read_csv("event_table.csv")
    sentiment_analysis = pd.read_csv("sentiment_analysis.csv")
    category_table = pd.read_csv("category_table.csv")

    # Merge data for collaborative filtering
    merged_data = pd.merge(
        sentiment_analysis[["event_id", "user_id", "rating"]],
        event_table[["event_id", "event_name", "category_id"]],
        on="event_id",
    )
    merged_data = pd.merge(merged_data, category_table, on="category_id")

    # Create Surprise dataset
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(
        merged_data[["user_id", "event_name", "rating"]], reader
    )

    # Define a cross-validation iterator
    kf = KFold(n_splits=5)

    # Train models with GridSearchCV to find the best parameters
    param_grid = {"n_epochs": [5, 10], "lr_all": [0.002, 0.005], "reg_all": [0.4, 0.6]}
    gs = GridSearchCV(SVD, param_grid, measures=["rmse", "mae"], cv=kf)

    gs.fit(data)

    # We can now use the algorithm that yields the best rmse:
    algo = gs.best_estimator["rmse"]
    algo.fit(data.build_full_trainset())

    # Function to generate event recommendations based on popularity

    def generate_popularity_recommendations(n=10):
        event_popularity = (
            merged_data.groupby(["event_id", "event_name", "category_name"])["rating"]
            .agg(["mean", "count"])
            .sort_values(by="mean", ascending=False)
        )
        top_events = event_popularity.head(n)
        return top_events

    popularity_recommendations = generate_popularity_recommendations()

    """Infer a prediction from a trained model."""
    return jsonify(
        {
            "data": [data[0] for data in popularity_recommendations.index.tolist()], # data[0] is the event_id
        }
    )