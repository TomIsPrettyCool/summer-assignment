import num2words
from random import randint
from namesfornumbers import Question, db
from flask_login import current_user

def generate_question():
    number = randint(1, 1000)
    number_words = num2words.num2words(number)

    return number, number_words

def generate_and_add_question():
    number, words = generate_question()

    next_question = Question(words, number)
    next_question.student = current_user
    db.session.add(next_question)

    return next_question