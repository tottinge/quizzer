import json
import unittest


class SchemaValidator(unittest.TestCase):
    def test_schema_can_parse(self):
        # loads throws exception on failure
        from apps.author.author import FORM_SCHEMA
        json.loads(FORM_SCHEMA)


if __name__ == '__main__':
    unittest.main()
