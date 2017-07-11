import num2words
from random import randint
from namesfornumbers import Question


def generate_question():
    number = randint(1, 1000)
    number_words = num2words(number)

    return number, number_words
