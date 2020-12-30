class SessionStore:
    """
    Store user sessions for later analysis and reporting
    """
    def __init__(self):
        self.recorded_answers = []
        
    def record_answer(self, quiz_name, question_number, selection, is_correct):
        self.recorded_answers.append( (quiz_name, question_number, selection, is_correct))

    def perfect_answers(self, quiz_name):
        return [ item for item in self.recorded_answers if item[-1] == True ]

    def incorrect_answers(self, quiz_name):
        return [ item for item in self.recorded_answers if item[-1] == False ]

    def number_of_correct_answers(self, quiz_name):
        return len(self.perfect_answers(quiz_name))

    def number_of_incorrect_answers(self, quiz_name):
        return len(self.incorrect_answers(quiz_name))
    