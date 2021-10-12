
# Hello `Ivan`! :)

## Task 1 - Palindromes

# Write a small function that finds `p` the smallest palindrome number such as `p > 20` and the square of `p` is a palindrome number.

# Your code here

def smallest_palindrome(i=21):
    while(true):
        if(isPalindrome(i)):
            square=i**2
            if(isPalindrome(square)):
                return i
        i+=1


def isPalindrome(i):
    return(str(i)==str(i)[::-1])



## Task 2 - Estimate Pi
#We want to estimate the number Pi using only a random generator.
# Hint: unit circle in a square ;)

# ![this](https://loresayer.com/wp-content/uploads/2012/03/pi-circle-inscribed-square.png)
# See also https://en.wikipedia.org/wiki/Monte_Carlo_method#Monte_Carlo_and_random_numbers


# you have this function at your disposal
# def uniform() -> float:
    # returns a number x such as 0 <= x < 1

# Your code here
inside_points=0
number_of_points=1000
r = 1

A_c = PI* r**2
A_s = r**2


for in range(0,number_of_points):
    x=uniform()
    y=uniform()
    if((x**2)+(b**2)<=1):
        inside_points+=1
pi=4*inside_points/number_of_points
return pi



N = 1000000
pi = 4 * sum([1 if uniform()**2 + uniform()**2 < 1]) / N 



