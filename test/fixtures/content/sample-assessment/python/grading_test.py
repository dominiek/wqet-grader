import grading
from utils import fixture_path


def test_compare_lists():
    assert grading.compare_lists({"expectedResult": [1]}, [1])["score"] == 1.0
    assert grading.compare_lists({"expectedResult": [1, 2, 3]}, [2, 3])["score"] == 0.0


def test_compare_plot():
    assert (
        grading.compare_plot(
            {"expectedImagePath": fixture_path("plot.png")}, fixture_path("plot.png")
        )["score"]
        == 1.0
    )
