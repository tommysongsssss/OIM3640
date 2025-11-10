 #how to count rhe frequency of numbers in a list 
 
nums = [1,2,3,4,5,6,6,6,6,]

freq = {}

for num in nums:
    if num not in freq:
        freq[num] = 0 
    else:
        freq[num] += 1


print(freq)