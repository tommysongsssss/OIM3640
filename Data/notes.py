import os 
print(os.getcwd())

f= open ('/Users/thomassong0604/Documents/GitHub/OIM3640/Data/words.txt')

number_of_words = 0 

for line in f:
    word = line.strip()
    number_of_words += 1

print(number_of_words)



