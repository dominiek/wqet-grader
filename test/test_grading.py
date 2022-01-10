from wqet_grader.grading import (
    execute_grading,
    get_assessment_definition,
    get_grader_definition,
    load_assessment_definitions,
)

def test_loading_definitions():
    definitions = load_assessment_definitions("test/fixtures/content")
    assert len(definitions) >= 1
    definition = get_assessment_definition(definitions, "Sample Assessment")
    assert definition["id"] == "Sample Assessment"
    definition, grader = get_grader_definition(definitions, "Sample Assessment", "Question 1")
    assert grader["gradingType"] == "code"


def test_execute_grading():
    definitions = load_assessment_definitions("test/fixtures/content")
    submission_object = {
        "type": "simple",
        "argument": [
            [
                "Querétaro",
                "Guanajuato",
                "Nuevo León",
                "Quintana Roo",
                "Jalisco",
                "Distrito Federal",
                "Chihuahua",
                "Guerrero",
                "Estado de México",
                "Puebla",
            ]
        ],
    }
    result = execute_grading(definitions, "Sample Assessment", "Question 1", submission_object)
    assert result["score"] == 1.0
