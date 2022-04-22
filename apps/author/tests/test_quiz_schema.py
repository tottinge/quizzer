import json
import unittest


class SchemaValidator(unittest.TestCase):
    def test_schema_can_parse(self):
        # loads throws exception on failure
        with open("static/quiz_schema.json") as schema_file :
            json.load(schema_file)


if __name__ == '__main__':
    unittest.main()
