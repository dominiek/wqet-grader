import os

import pandas as pd
from sklearn.metrics import mean_absolute_error

my_dir = os.path.dirname(os.path.abspath(__file__))


def fixture_path(path):
    return os.path.join(my_dir, "../fixtures/", path)


# This can be generalized
def compare_lists(defaults, submission):
    iterable = zip(sorted(submission), sorted(defaults["expectedResult"]))
    evaluation = [s == a for s, a in iterable]
    grade = sum(evaluation) / len(evaluation)
    return {"score": grade, "passed": True}


# TODO: Serialize Pandas DataFrame
def grade_wrangle(defaults, dataframe=None, multiplier=0):
    answer = pd.DataFrame(
        [
            {
                "property_type": "house",
                "state": "Distrito Federal",
                "lat": 19.378482,
                "lon": -99.220795,
                "area_m2": 100.0,
                "price_usd": 201061.21,
                "area_sqft": 1076.0,
            },
            {
                "property_type": "house",
                "state": "Morelos",
                "lat": 18.917542,
                "lon": -98.963181,
                "area_m2": 182.0,
                "price_usd": 97469.99,
                "area_sqft": 1958.32,
            },
            {
                "property_type": "house",
                "state": "Yucatán",
                "lat": 21.001256,
                "lon": -89.600723,
                "area_m2": 325.0,
                "price_usd": 183296.27,
                "area_sqft": 3497.0,
            },
            {
                "property_type": "apartment",
                "state": "Distrito Federal",
                "lat": 19.390031,
                "lon": -99.174182,
                "area_m2": 108.0,
                "price_usd": 209692.2,
                "area_sqft": 1162.08,
            },
            {
                "property_type": "apartment",
                "state": "Distrito Federal",
                "lat": 19.454332,
                "lon": -99.200287,
                "area_m2": 62.0,
                "price_usd": 50591.01,
                "area_sqft": 667.12,
            },
        ]
    )
    assert isinstance(dataframe, pd.DataFrame), "You function doesn't return a DataFrame."
    assert (
        "area_sqft" in dataframe.columns
    ), "The DataFrame your function returns is missing the `'area_sqft'` column."
    assert all(
        dataframe == answer
    ), "The DataFrame your function returns doesn't match the answer."
    return {"score": 1.0, "passed": True}


def grade_mae(defaults, submission):
    X_test = pd.read_csv(fixture_path(defaults["filepath_X_test"]))
    y_test = pd.read_csv(fixture_path(defaults["filepath_y_test"]))
    y_pred = submission.predict(X_test)
    mae = mean_absolute_error(y_pred, y_test).round(2)
    return {"score": mae, "passed": mae < defaults["thresh"]}


def grade_mae2(defaults, submission):
    y_test = pd.read_csv(fixture_path(defaults["filepath_y_test"]))
    mae = mean_absolute_error(submission, y_test).round(2)
    return {"score": mae, "passed": mae < defaults["thresh"]}


# This can be generalized
def compare_plot(defaults, submission):
    # compare_images(fixture_path(defaults['expectedImagePath']), submission.name, tol=5, in_decorator=True)
    return {"score": 1.0, "passed": True}
