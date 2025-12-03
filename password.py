"""
You've been hired as a cybersecurity analyst for a major e-commerce platform, and your primary task is to improve the security of user accounts by identifying strong passwords and eliminating weak ones.

Recently, your team has received reports of user accounts being compromised due to weak, easily guessable passwords. After conducting a security audit, you have identified a list of commonly used passwords stored in a file called "common_passwords.txt", which you can access and download through a link (https://bit.ly/python-quiz-3)

The passwords in the file look like this:

mm44693avl$
kdOP
2kEqMWWFi
4NyTu0
gt$YrkPwTm8!g
…

Your Task:

Write a function, find_strong_passwords, that identifies strong passwords and returns them as a list. (If you are not yet familiar with lists, you can simply print out the strong passwords instead.) A password is considered "strong" if it meets all of the following conditions:
•	The password must contain at least one uppercase letter, one lowercase letter, and one digit.
•	The password must NOT contain two consecutive identical characters.
•	The password must be at least 12 characters long.

Note:
•	You might want to create “helper” functions to keep your code organized.
•	Use meaningful function and variable names to improve readability.
•	You can use the following scaffold code to help you get started:
f = open("data/common_passwords.txt") # Open the file "common_passwords.txt" that contains all the passwords, one per line.
for line in f: # Iterate through each line, where each line contains one password. Note: you should know that each line ends with a newline character ('\n').

"""

def contains_upper_lower_digit(s):
    """Return True if s contains at least one uppercase,
       one lowercase, and one digit."""
    has_upper = False
    has_lower = False
    has_digit = False

    for c in s:
        if c.isupper():
            has_upper = True
        elif c.islower():
            has_lower = True
        elif c.isdigit():
            has_digit = True

    return has_upper and has_lower and has_digit


def no_double_characters(s):
    """Return True if s has NO two consecutive identical characters."""
    for i in range(len(s) - 1):
        if s[i] == s[i + 1]:
            return False
    return True


def find_strong_passwords():
    """Return list of strong passwords from common_passwords.txt"""
    strong_passwords = []

    with open("data/common_passwords.txt", "r") as f:
        for line in f:
            password = line.strip()

            # Rule 1: length ≥ 12
            if len(password) < 12:
                continue

            # Rule 2: must contain upper, lower, digit
            if not contains_upper_lower_digit(password):
                continue

            # Rule 3: no double characters
            if not no_double_characters(password):
                continue

            # Passed all tests
            strong_passwords.append(password)

    return strong_passwords


# Run it
strong_passwords = find_strong_passwords()
print("Number of strong passwords:", len(strong_passwords))
print(strong_passwords)