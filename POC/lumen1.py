import random
import time
import sonic

def start_game(level, random_no_gen):
    print(f"Random Numbers (for debugging): {random_no_gen}")
    
    # Wait for button press to start the game
    print("Press the button to start the game!")
    while not sonic.lock_in:
        time.sleep(0.1)

    # Reset the flag after button press
    sonic.lock_in = False
    print(f"Game started! Level: {level}")

    # Main game logic
    attempts = 0
    max_attempts = 5

    while attempts < max_attempts:
        print("Updating sensor inputs. Press the button to lock in your answer...") 

        # Continuously update sensor inputs until the button is pressed
        sensor_input = [0, 0, 0, 0]
        while not sonic.lock_in:
            sensor_input[0] = sonic.get_dist_sensor1()
            sensor_input[1] = sonic.get_dist_sensor2()
            sensor_input[2] = sonic.get_dist_sensor3()
            sensor_input[3] = sonic.get_dist_sensor4()
            print(f"Current Sensor Inputs: {sensor_input}", end="\r", flush=True)
            time.sleep(0.1)

        # Reset the flag after button press
        sonic.lock_in = False
        print("\nInputs locked in!")

        # Validate sensor inputs
        if sonic.validation(sensor_input) is None:
            print("Invalid sensor input. Retrying...")
            continue

        # Compute and display results
        results = sonic.matching_numbers(sensor_input, random_no_gen)
        print(f"Results: {results}")

        # Check for win condition
        if all(color == 'green' for color in results):
            print(f"Congratulations! You completed the {level} level!")
            return True

        attempts += 1
        if attempts < max_attempts:
            print(f"Try again! Attempts left: {max_attempts - attempts}")
        else:
            print(f"Out of attempts! The correct numbers were: {random_no_gen}")
            return False

def main():
    # Start with the basic level
    basic_level_numbers = [10, 20, 30, 40]
    print("Starting Basic Level...")
    if start_game("Basic", basic_level_numbers):
        print("\nMoving to Hard Level...")
        hard_level_numbers = [random.choice([10, 20, 30, 40]) for _ in range(4)]
        start_game("Hard", hard_level_numbers)
    else:
        print("\nGame Over. Try again from the Basic Level.")

if name == "main":
    main()