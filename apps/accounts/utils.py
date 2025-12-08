import random
import string


def generate_activation_code():
    """Function for generating 6-digit code for activating the user's account"""
    return ''.join(random.choices(string.digits, k=6))