import random

random_no_gen = [random.randint(0,10)* 10 for i in range (4)] #generate 4 random heights ranging from 0 to 100 in multiples of 10
colors = ['green','yellow','red']

def validation(userinput):
    try:
        user_no = [int(num) for num in userinput.split()] #converts each number to an integer
        if len(user_no) != 4 or not all(num % 10 == 0 for num in user_no) or not all(0 <= num <= 100 for num in user_no): #checks that user has entered exactly 4 numbers that are multiples of 10 and that the numbers are from 0-100
            raise ValueError #if validation fails , return ValueError and run line 12
        return user_no #if validation succeeds returns the values keyed by user
    except ValueError:
        print("Invalid input. Please enter exactly 4 numbers ranging from 0 to 100") 
        return None #return none to signify input is invalid

def matching_numbers(user_no,random_no_gen): 
    result = []
    for i, num in enumerate(user_no): #enumerate  = counter for items in user_no (i,num) num = random number in random_no_gen / used to match with user location of numbers in user input
        if num == random_no_gen[i]:
            result.append('green')  # Correct number, correct position
        elif num in random_no_gen:
            result.append('yellow')  # Correct number, wrong position
        else:
            result.append('red')  # Incorrect number
    return result

print('4 random numbers have been generated , guess them')
print('Hint : multiples of 10')
print(random_no_gen)
attempts = 0
max_attempts = 5    

while attempts < max_attempts:
    userinput = input(f"Attempt {attempts + 1}/{max_attempts}: Enter your numbers of choice (HR-SC04 INPUT HERE): ")
    user_no = validation(userinput)
    if user_no is None or len(userinput)< 4 :
        # print("Random Numbers (for debugging):", random_no_gen)
        continue #reprompt , allowing users to try again

    results =  matching_numbers(user_no,random_no_gen)
    print(results)
    

    #check for the win 
    if all(colors=='green' for colors in results):
        print("Congratulations u win , thx for playing")
        break # keeps looping unless player wins 

    attempts += 1
    if attempts < max_attempts:
        print("Try Again!")
    
    if attempts == max_attempts and not all(colors == 'green' for colors in results):
        print("Out of attempts bye")
        print("The correct numbers are: " , random_no_gen)
