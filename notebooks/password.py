def find_strong_passwords():
    f = open('/Users/thomassong0604/Documents/GitHub/OIM3640/Data/common_passwords.txt', 'r')
    for line in f:
        password = line.strip()
        #print password



strong_passwords = find_strong_passwords()
print(len(strong_passwords))




def has_uppercase(s):
    return any(c.isupper() for c in s)

def has_lowercase(s):
    return any(c.islower() for c in s)

def has_digit(s):
    return any(c.isdigit() for c in s)

def no_consecutive_identical(s):
    return all(s[i] != s[i+1] for i in range(len(s) - 1))
