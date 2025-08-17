# Explanation For Lighting Code

## Introduction
Explanation of lighting codes used in lumen1.py  



---

## Python OSC client code for grandMA3 control
```
GMA_IP = "192.168.254.213"  # grandMA3 laptop IP
GMA_PORT = 2000      # grandMA3 port
GMA_ADDR = "/gma3/cmd" # OSC address pattern

def send_gma3_command(command):
    try:
        client = udp_client.SimpleUDPClient(GMA_IP, GMA_PORT) # Creates a network client to send OSC messages
        client.send_message(GMA_ADDR, command) # Sends command to grandMA3
        print(f"grandMA3 OSC sent: {command}")
    except Exception as e:
        print(f"grandMA3 OSC error: {e}")
```
## Python function call that sends an OSC command to grandMA3
```
send_gma3_command("Off Sequence Thru Please")
```
This command clears all existing sequences and cues. This should be used at the start of each exhibition to ensure that there are no clashes with the previous sequences and cues.
```
time.sleep(0.3)
```
This code provides a delay so the the cues in the sequence can be played through without cutting off. This code could also be added after each command to prevent clashing.
```
send_gma3_command("Go+ Sequence 68")
time.sleep(5)
send_gma3_command("Off Sequence 68")
time.sleep(0.3)
```
For example Sequence 68 takes 5 seconds to play so a 5 second delay is added so the lights do not cut off suddenly.