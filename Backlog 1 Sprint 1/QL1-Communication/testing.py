import subprocess
import time

def run_command(command):
    text = 'python3 command.py '
    config = text + command
    print(config)
    try:
        output = subprocess.check_output(config, shell=True)
        print(output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.returncode}, {e.output.decode('utf-8')}")

def run_recall(command):
    text = 'python3 recall.py '
    config = text + command
    print(config)
    try:
        output = subprocess.check_output(config, shell=True)
        print(output.decode('utf-8'))
    except subprocess.CalledProcessError as e:
        print(f"Error: {e.returncode}, {e.output.decode('utf-8')}")


# Define another function to store the channel and level values n run the command using them

channel_max = 32
channel_min = 1
level_max =1001
level_min = -7001

def adjust_fader(channel, level):
    command = f'set MIXER:Current/InCh/Fader/Level {channel} 0 {level}'
    run_command(command)


if __name__ == "__main__":
    
    try: #takes in the inputs (channel no / fader level) given by the user > checks for error 
        channel_input = input("Enter which channel/s you want to adjust (separate channel no. by comma if mulitple): ").strip()
        channels = [int(ch.strip()) for ch in channel_input.split(",")]
        level = int(input("Enter the level you want the fader/s to be adjusted by: ").strip())
        
        if any(channel_input < channel_min or channel_input >= channel_max for channel_input in channels):
            print("Invalid channel number , please try again")
            exit()
        if level < level_min  or level >= level_max:
            print("Invalid level number , please try again")
            exit()

    except ValueError: #if have error > displays error msg n program stops
        print("Invalid Input. Please enter a valid integer for the level adjustment and channel selection.")
        exit()
        
        
    #if no error > runs the adjust_fader function , setting the channel/s that user wants to control 
    for channel in channels:
        adjust_fader(channel, level)
        time.sleep(1)
