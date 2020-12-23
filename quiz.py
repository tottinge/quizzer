import os
import json

from box import Box

QUIZ_DIR = 'quizzes'

def doomed_filescan(filename):
    try:
        target = os.path.join(QUIZ_DIR, filename)
        with open(target) as quizfile:
            doc = json.load(quizfile)
            return doc.get('title', 'no-title-found')
    except Exception as err:
        return f"Error: {err}"

def doomed_quiz_collector():
    for (dir,_,files) in os.walk(QUIZ_DIR):
        for filename in files:
            if not filename.endswith('json'):
                continue
            os.path.join(dir, filename)
            yield filename, title(filename)

if __name__ == "__main__":
    print(list(get_quizzes()))


class Quiz(Box):
    def next_question_number(self, number):
        if number+1 >= len(self.questions):
            return None
        return number+1