from flask import Blueprint, jsonify, request
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import pandas as pd
import numpy as np
import re
import gensim.downloader
import os

from db.database import db

inferBP = Blueprint("other", __name__)

MODEL_FILE = "glove-wiki-gigaword-100.model"


@inferBP.route("/", methods=["POST"])
def other():
    data = request.get_json(force=True)
    user_id_to_check = data["user_id"]
    threshold = data.get("threshold", 0.5)

    df_user = pd.DataFrame(list(db.users.find({})))
    df_user["user_id"] = df_user["_id"].astype(str)
    df_user = df_user.set_index("user_id")
    df_user = df_user.drop(["_id", "username"], axis=1)

    if user_id_to_check not in df_user.index:
        print("User not found")
        return jsonify({"Recommend Event": []})

    df_user_expanded = df_user.explode("user_interest_category").explode("user_past_event_category")
    df_user_expanded["row_number"] = range(1, len(df_user_expanded) + 1)

    df_event = pd.DataFrame(list(db.events.find({})))
    df_event["event_id"] = df_event["_id"].astype(str)
    df_event = df_event.drop(["_id"], axis=1)
    df_event = df_event.set_index("event_id")
    df_event = df_event[["category_id", "name", "event_description"]]

    df_event["combined"] = df_event["name"] + " " + df_event["event_description"]

    df_event["combined"] = df_event["combined"].str.lower()

    def tokenize_text(x):
        if pd.isna(x):
            return []
        x = re.sub(r"\d+", "", x)
        return word_tokenize(x.lower())

    df_event["tokenized"] = df_event["combined"].apply(tokenize_text)

    df_event["clean_tokenized"] = df_event["tokenized"].apply(
        lambda tokens: [
            word
            for word in tokens
            if word.isalpha() and word not in stopwords.words("english")
        ]
    )
    df_event.drop(columns=["combined", "tokenized"], inplace=True)

    if not os.path.exists(MODEL_FILE):
        raise ValueError("Download the model first.")

    glove = gensim.models.KeyedVectors.load(MODEL_FILE)

    def get_embedding(list_of_tokens):
        embeddings = np.zeros(100)
        for token in list_of_tokens:
            if token in glove:
                embeddings += glove[token]
        return embeddings

    df_event["embedding"] = df_event["clean_tokenized"].apply(
        lambda x: get_embedding(x)
    )

    u = user_id_to_check
    user_data = df_user.loc[u]
    
    # Combine user interests and past events
    items_of_user_1 = user_data["user_interest_category"]

    embedding_of_events_of_user = df_event.loc[
        df_event.category_id.isin(items_of_user_1), "embedding"
    ]
    profile_user = np.sum(embedding_of_events_of_user.values)

    df_event["cosine"] = df_event.embedding.apply(
        lambda x: cosine_similarity(profile_user.reshape(1, 100), x.reshape(1, 100))
    ).apply(lambda x: x[0][0])
    df_event_top50 = df_event.sort_values("cosine", ascending=False).head(50)

    relevant_items_above_threshold = df_event_top50[
        df_event_top50["cosine"] > threshold
    ].index.values
    return jsonify({"Recommend Event": relevant_items_above_threshold.tolist()})
