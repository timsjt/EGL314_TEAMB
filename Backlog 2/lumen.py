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
    

# # SENSORS

# import board
# import busio
# import adafruit_ads1x15.ads1115 as ADS
# from adafruit_ads1x15.analog_in import AnalogIn
# import time

# # Initialize I2C
# i2c = busio.I2C(board.SCL, board.SDA)
# ads = ADS.ADS1115(i2c)

# # Configure sensor channels
# sensor1 = AnalogIn(ads, ADS.P0)  # A0
# sensor2 = AnalogIn(ads, ADS.P1)  # A1
# sensor3 = AnalogIn(ads, ADS.P2)  # A2

# # Calibration (adjust based on your sensor)
# VOLTAGE_PER_CM = 0.0049  # 4.9mV per cm (example)

# def read_distance(voltage):
#     return voltage / VOLTAGE_PER_CM

# try:
#     while True:
#         # Read voltages
#         v1 = sensor1.voltage
#         v2 = sensor2.voltage
#         v3 = sensor3.voltage

#         # Calculate distances
#         d1 = read_distance(v1)
#         d2 = read_distance(v2)
#         d3 = read_distance(v3)

#         print(f"Sensor 1: {d1:.1f} cm | Sensor 2: {d2:.1f} cm | Sensor 3: {d3:.1f} cm")
#         time.sleep(0.5)

# except KeyboardInterrupt:
#     print("Stopped.")
