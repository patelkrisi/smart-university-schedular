import pandas as pd
import json

def load_data(courses_path="data/synthetic/courses.csv", historical_path="data/synthetic/historical_instances.csv"):
    courses = pd.read_csv(courses_path)
    hist = pd.read_csv(historical_path)
    return courses, hist

def featurize(courses_df, hist_df):
    def hist_mean(arr_str):
        try:
            arr = json.loads(arr_str)
            return float(sum(arr) / len(arr)) if len(arr) > 0 else 0.0
        except Exception:
            return 0.0

    courses = courses_df.copy()
    courses["hist_mean"] = courses["historical_enrollment"].apply(hist_mean)
    courses["hist_len"] = courses["historical_enrollment"].apply(
        lambda s: len(json.loads(s)) if pd.notnull(s) else 0
    )
    courses["level_num"] = courses["course_level"].map({"UG": 0, "PG": 1}).fillna(0)

    feature_cols = ["hist_mean", "hist_len", "level_num", "duration"]
    X = courses[feature_cols].fillna(0)

    y = courses["expected_students"].fillna(courses["hist_mean"])

    return X, y, courses
