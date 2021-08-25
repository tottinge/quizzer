import unittest

from hamcrest import assert_that, is_, contains_exactly, contains_string, not_, \
    all_of

from quizzes.quiz_store import filename_for


class TestFilenameGeneration(unittest.TestCase):
    def test_adds_json_extension(self):
        assert_that(filename_for("poo"), is_("poo.json"))

    def test_translates_spaces(self):
        actual = filename_for('pooh bear and tigger')
        assert_that(actual, not_(contains_string(' ')))

    def test_handles_path_characters(self):
        actual = filename_for('~/c:x/y/blah\this\\')
        for unwanted in '/', '\\', ':', '~':
            assert_that(actual, not_(contains_string(unwanted)))

    def test_handles_scary_bash_characters(self):
        actual = filename_for('\'\" bite me; rm * && rm -rf || format & ')
        for bad_thing in '"\'&|;':
            assert_that(actual, not_(contains_string(bad_thing)))


if __name__ == '__main__':
    unittest.main()
