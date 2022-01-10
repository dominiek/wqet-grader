import os

import pandas as pd
import requests_mock

from wqet_grader.transport import encode_submission

my_dir = os.path.dirname(os.path.abspath(__file__))

def test_grade(http_client):
    df = pd.read_csv(my_dir + "/../fixtures/mexico-real-estate-train-sample.csv")
    df["area_sqft"] = df["area_m2"] * 10.76
    submission = {"type": "object", "object": {"dataframe": df, "multiplier": 10.76}}
    encoded_submission = encode_submission(submission)
    with requests_mock.Mocker() as m:
        response = http_client.post(
            "/1/grade",
            json={
                "assessment": "Sample Assessment",
                "question": "Question 2",
                "submission": encoded_submission
            },
        )
        assert response.status_code == 200
        body = response.get_json()
        assert body["data"]["result"]["score"] == 1.0
