from flask import Blueprint, jsonify
import pandas as pd
from surprise import Reader, Dataset
from surprise.model_selection import KFold, GridSearchCV
from surprise import SVD
from datetime import datetime
from db.database import db
import json

from cache_lib.cache import cache

popularBP = Blueprint("popular", __name__)


@popularBP.route("/", methods=["GET"])
def popular():
    if cache.exists("popular"):
        return jsonify({"data": json.loads(cache.get("popular"))})

    event_table = pd.DataFrame(
        list(db.events.find({"start_time": {"$gte": datetime.now()}}))
    )
    event_table["event_id"] = event_table["_id"].astype(str)
    event_table = event_table.drop(["_id"], axis=1)

    sentiment_analysis = pd.DataFrame(list(db.reviews.find({})))

    category_table = pd.DataFrame(list(db.categories.find({})))

    # Merge data for collaborative filtering
    merged_data = pd.merge(
        sentiment_analysis[["event_id", "user_id", "rating"]],
        event_table[["event_id", "name", "category"]],
        on="event_id",
    )
    category_table["category"] = category_table["_id"].astype(str)
    category_table["category_name"] = category_table["name"]
    category_table = category_table.drop(["_id", "name"], axis=1)
    merged_data = pd.merge(merged_data, category_table, on="category")

    # Create Surprise dataset
    reader = Reader(rating_scale=(1, 5))
    data = Dataset.load_from_df(merged_data[["user_id", "name", "rating"]], reader)

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
            merged_data.groupby(["event_id", "name", "category_name"])["rating"]
            .agg(["mean", "count"])
            .sort_values(by="mean", ascending=False)
        )
        top_events = event_popularity.head(n)
        return top_events

    popularity_recommendations = generate_popularity_recommendations()

    res = {
        "data": [
            data[0] for data in popularity_recommendations.index.tolist()
        ],  # data[0] is the event_id
    }

    cache.set("popular", json.dumps(res["data"]), ex=60 * 60 * 24)  # 1 day

    """Infer a prediction from a trained model."""
    return jsonify(res)
