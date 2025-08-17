import random
import time
import tryy
import RPi.GPIO as GPIO
import socket 
import json 
import signal
import sys
from threading import Thread
from pythonosc import udp_client, osc_message_builder

#######################
# At the top of your file
rfid_thread_started = False

# Global variables to store RFID inputs from both secondary pis
rfid_data_pi2 = {"inputs": [], "readers": []}
rfid_data_pi3 = {"inputs": [], "readers": []}
server_socket = None


#Audio
def send_message(receiver_ip, receiver_port, address, message):
	try:
		# Create an OSC client to send messages
		client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)

		# Send an OSC message to the receiver
		client.send_message(address, message)

		print("Audio Message sent successfully.")
	except:
		print("Message not sent")
def send_message1(receiver_ip, receiver_port, address, message):
	try:
		# Create an OSC client to send messages
		client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)

		# Send an OSC message to the receiver
		client.send_message(address, message)

		print("Audio Message sent successfully.")
	except:
		print("Message not sent")
          
def send_message2(receiver_ip, receiver_port, address, message):
	try:
		# Create an OSC client to send messages
		client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)

		# Send an OSC message to the receiver
		client.send_message(address, message)

		print("Audio Message sent successfully.")
	except:
		print("Message not sent")
          
def send_message3(receiver_ip, receiver_port, address, message):
	try:
		# Create an OSC client to send messages
		client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)

		# Send an OSC message to the receiver
		client.send_message(address, message)

		print("Audio Message sent successfully.")
	except:
		print("Message not sent")
          
def send_message4(receiver_ip, receiver_port, address, message):
	try:
		# Create an OSC client to send messages
		client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)

		# Send an OSC message to the receiver
		client.send_message(address, message)

		print("Audio Message sent successfully.")
	except:
		print("Message not sent")

def send_message5(receiver_ip, receiver_port, address, message):
	try:
		# Create an OSC client to send messages
		client = udp_client.SimpleUDPClient(receiver_ip, receiver_port)

		# Send an OSC message to the receiver
		client.send_message(address, message)

		print("Audio Message sent successfully.")
	except:
		print("Message not sent")
          
   
#Audio
PI_A_ADDR = "192.168.254.12"		# wlan ip
PORT = 8000
addr = "/marker/33" # Jump to BGM2
addr1 = "/marker/37" # Jump to yellow
addr2 = "/marker/36" # Jump to wrong
addr3 = "/marker/35" # Jump to winning music
addr4 = "/marker/34" 
addr5 = "/marker/32" # Jump to BGM1
addr6 = "/marker/38" # Jump to Electricity
addr7 = "/marker/39" # Jump to OneC
addr8 = "/marker/40" # Jump to TwoC
addr9 = "/marker/41" # Jump to ThreeC
addr10 = "/marker/42" # Jump to FourC
addr11 = "/marker/43" # Jump to Marker Incorrect
addr12 = "/action/1007" # To play the track
addr13 = "/marker/45" # Jump to Marker Incorrect
addr14 = "/marker/46" # Jump to Marker Incorrect


#Lighting
GMA_IP = "192.168.254.213"  # grandMA3 laptop IP
GMA_PORT = 2000      # grandMA3 port
GMA_ADDR = "/gma3/cmd"

def send_gma3_command(command):
    try:
        client = udp_client.SimpleUDPClient(GMA_IP, GMA_PORT)
        client.send_message(GMA_ADDR, command)
        print(f"grandMA3 OSC sent: {command}")
    except Exception as e:
        print(f"grandMA3 OSC error: {e}")


msg = float(1) # Trigger TRUE Value


#bgm
send_gma3_command("Off Sequence Thru Please")
time.sleep(0.3)
send_gma3_command("Go+ Sequence 68")
time.sleep(10)
send_message5(PI_A_ADDR, PORT, addr12, msg)
send_message5(PI_A_ADDR, PORT, addr5, msg)




def signal_handler(sig, frame):
    global server_socket
    print('\nReceived interrupt signal. Cleaning up...')
    
    if server_socket:
        try:
            server_socket.close()
        except:
            pass
    
    GPIO.cleanup()
    sys.exit(0)

# Register signal handlers
signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def read_rfid_inputs_with_timeout(timeout=0.5):
    """Capture RFID inputs from Pi2 and Pi3 within a timeout window."""
    global rfid_data_pi2, rfid_data_pi3

    print(f"🕒 Waiting up to {timeout} seconds for RFID inputs...")

    start_time = time.time()
    captured = [None, None, None, None]  # For 4 readers

    while time.time() - start_time < timeout:
        temp = combined_rfid_inputs()

        for i in range(4):
            if captured[i] is None and temp[i] is not None:
                captured[i] = temp[i]

        if all(x is not None for x in captured):
            break

        time.sleep(0.1)

    print(f"✅ Captured RFID Inputs: {captured}")
    return captured


def combined_rfid_inputs():
    """Returns all 4 RFID inputs combined from both secondary Pis in correct order"""
    combined = [None, None, None, None]

    pi2_readers = rfid_data_pi2.get("readers", [])
    pi2_inputs = rfid_data_pi2.get("inputs", {})
    for reader in pi2_readers:
        try:
            reader_index = int(reader) - 1
            if 0 <= reader_index < 4:
                combined[reader_index] = pi2_inputs.get(reader)
        except Exception as e:
            print(f"[Warning] Failed to assign Pi2 reader {reader}: {e}")

    pi3_readers = rfid_data_pi3.get("readers", [])
    pi3_inputs = rfid_data_pi3.get("inputs", {})
    for reader in pi3_readers:
        try:
            reader_index = int(reader) - 1
            if 0 <= reader_index < 4:
                combined[reader_index] = pi3_inputs.get(reader)
                time.sleep(0.1)
        except Exception as e:
            print(f"[Warning] Failed to assign Pi3 reader {reader}: {e}")

    return combined


def rfid_server():
    global rfid_data_pi2, rfid_data_pi3, server_socket
    HOST = '0.0.0.0'  # Listen on all interfaces
    PORT = 65432

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST, PORT))
        server_socket.listen(2)  # Allow 2 connections
        print("🚀 RFID Server is running and ready for connections...")
        
        def handle_client(conn, addr):
            global rfid_data_pi2, rfid_data_pi3
            print(f"✅ Connection established with {addr}")
            buffer = b""
            try:
                while True:
                    data = conn.recv(4096)
                    if not data:
                        print(f"❌ No data received from {addr}, client disconnected")
                        break
                    buffer += data
                    buffer_str = buffer.decode(errors = 'ignore')
                    while True :
                        try:
                    # Try to decode one JSON object from the start of the buffer
                            decoded_obj, index = json.JSONDecoder().raw_decode(buffer_str)
                    # Successfully decoded an object, remove it from buffer
                            buffer_str = buffer_str[index:].lstrip()
                        except json.JSONDecodeError:
                    # Not enough data to decode, wait for more
                            break
                        except Exception as e:
                            print(f"❌ Unexpected decode error from {addr}: {e}")
                            break
                        else:
                    # Process the decoded JSON object
                            rfid_data = decoded_obj
                            received_inputs = rfid_data.get("rfid_inputs", [])
                            pi_id = rfid_data.get("pi_id", "unknown")
                            readers = rfid_data.get("readers", [])
                    
                        if pi_id == "pi2":
                            rfid_data_pi2 = {"inputs": received_inputs, "readers": readers}
                            if random.randint(1, 20) == 1:
                                print(f"📡 Pi2 (Readers {readers}): {received_inputs}")
                        elif pi_id == "pi3":
                            rfid_data_pi3 = {"inputs": received_inputs, "readers": readers}
                            if random.randint(1, 20) == 1:
                                print(f"📡 Pi3 (Readers {readers}): {received_inputs}")
                        else:
                            print(f"⚠️ Unknown Pi ID: {pi_id}")

                        if random.randint(1, 50) == 1:
                            combined = combined_rfid_inputs()
                            print(f"🔄 Combined RFID data: {combined}")
                            print(f"   Pi2 readers {rfid_data_pi2['readers']}: {rfid_data_pi2['inputs']}")
                            print(f"   Pi3 readers {rfid_data_pi3['readers']}: {rfid_data_pi3['inputs']}")
                    buffer = buffer_str.encode()    
            except Exception as e:
                print(f"❌ Connection error with {addr}: {e}")
            finally:
                try:
                    conn.close()
                except:
                    pass
                print(f"🔌 Client {addr} disconnected")
        
        # Accept multiple connections
        while True:
            try:
                conn, addr = server_socket.accept()
                # Handle each client in a separate thread
                client_thread = Thread(target=handle_client, args=(conn, addr), daemon=True)
                client_thread.start()
                        
            except Exception as e:
                print(f"❌ Server error: {e}")
                break
                
    except Exception as e:
        print(f"❌ Server error: {e}")
    finally:
        if server_socket:
            server_socket.close()
        print("🛑 RFID Server stopped")

# RFID server will only be started during Expert level

# --- Button setup centralized here ---
button_pin = 26  # your chosen GPIO pin
GPIO.setmode(GPIO.BCM)
GPIO.setup(button_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

lock_in = False

def button_callback(channel):
    global lock_in
    # send_message5(PI_A_ADDR, PORT, addr5, msg)
    lock_in = True
    print("Button pressed! Inputs locked in.")

GPIO.add_event_detect(button_pin, GPIO.FALLING, callback=button_callback, bouncetime=300)

# --- Game logic ---
def start_game(level, random_no_gen):
    global lock_in
    print(f"Random Numbers (for debugging): {random_no_gen}")
    time.sleep(0.3)
    print("Press the button to start the game!")
    while not lock_in:
        time.sleep(0.1)

    lock_in = False
    print(f"Game started! Level: {level}")
    send_gma3_command("Go+ Sequence 68 Cue 6")
    time.sleep(3)
    send_gma3_command("Off Sequence Thru Please")
    time.sleep(0.3)
    send_gma3_command("Go+ Sequence 69")
    time.sleep(0.3)

    attempts = 0
    max_attempts = 500

    while attempts < max_attempts:
        print("Updating sensor inputs. Press the button to lock in your answer...")

        sensor_input = [0, 0, 0, 0]
        while not lock_in:
            sensor_input[0] = tryy.get_dist_sensor1()
            sensor_input[1] = tryy.get_dist_sensor2()
            sensor_input[2] = tryy.get_dist_sensor3()
            sensor_input[3] = tryy.get_dist_sensor4()
            print(f"🔄 Live Sensor Inputs: {sensor_input}", flush=True)
            # print(f"Current Sensor Inputs: {sensor_input}", end="\r", flush=True)
            time.sleep(1)
       


        lock_in = False
        print("\nInputs locked in!")
        send_gma3_command("Off Sequence 69")
        time.sleep(0.3)

        if tryy.validation(sensor_input) is None:
            print("Invalid sensor input. Retrying...")
            continue

        results = tryy.matching_numbers(sensor_input, random_no_gen)
        print(f"Results: {results}")
        correct_all = ['green','green','green','green']

        for i in range(4):
            if i == 0:
                if results[i] == 'green' :
                    send_gma3_command("Go+ Sequence 70 Cue 5")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr, msg)
                    time.sleep(2)
                    send_gma3_command("Off Sequence 70")
                    time.sleep(0.3)
                elif results[i] == 'yellow' :
                    send_gma3_command("Go+ Sequence 70 Cue 3")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr1, msg)
                    time.sleep(2)
                    send_gma3_command("Off Sequence 70")
                    time.sleep(0.3)
                elif results[i] == 'red':
                    send_gma3_command("Go+ Sequence 70 Cue 1")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr2, msg)
                    time.sleep(2)
                    send_gma3_command("Off Sequence 70")
                    time.sleep(0.3)
            elif i == 1:
                if results[i] == 'green' :
                    send_gma3_command("Go+ Sequence 71 Cue 5")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr, msg)                    
                    time.sleep(2)
                    send_gma3_command("Off Sequence 71")
                    time.sleep(0.3)
                elif results[i] == 'yellow' :
                    send_gma3_command("Go+ Sequence 71 Cue 3")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr1, msg)                   
                    time.sleep(2)
                    send_gma3_command("Off Sequence 71")
                    time.sleep(0.3)
                elif results[i] == 'red':
                    send_gma3_command("Go+ Sequence 71 Cue 1")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr2, msg)                      
                    time.sleep(2)
                    send_gma3_command("Off Sequence 71")
                    time.sleep(0.3)
            elif i == 2:
                if results[i] == 'green' :
                    send_gma3_command("Go+ Sequence 72 Cue 5")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr, msg)                     
                    time.sleep(2)
                    send_gma3_command("Off Sequence 72")
                    time.sleep(0.3)
                elif results[i] == 'yellow' :
                    send_gma3_command("Go+ Sequence 72 Cue 3")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr1, msg)                      
                    time.sleep(2)
                    send_gma3_command("Off Sequence 72")
                    time.sleep(0.3)
                elif results[i] == 'red':
                    send_gma3_command("Go+ Sequence 72 Cue 1")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr2, msg)                      
                    time.sleep(2)
                    send_gma3_command("Off Sequence 72")
                    time.sleep(0.3)
            elif i == 3:
                if results[i] == 'green' :
                    send_gma3_command("Go+ Sequence 73 Cue 5")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr, msg)                      
                    time.sleep(2)
                    send_gma3_command("Off Sequence 73")
                    time.sleep(0.3)
                    break
                elif results[i] == 'yellow' :
                    send_gma3_command("Go+ Sequence 73 Cue 3")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr1, msg)                      
                    time.sleep(2)
                    send_gma3_command("Off Sequence 73")
                    time.sleep(0.3)
                    break
                elif results[i] == 'red':
                    send_gma3_command("Go+ Sequence 73 Cue 1")
                    time.sleep(0.8)
                    send_message(PI_A_ADDR, PORT, addr12, msg)
                    send_message(PI_A_ADDR, PORT, addr2, msg)                      
                    time.sleep(2)
                    send_gma3_command("Off Sequence 73")
                    time.sleep(0.3)
                    break
            else:
                break
                 


        if all(color == 'green' for color in results):
            print(f"Congratulations! You completed the {level} level!") # stage 1 win
            send_message(PI_A_ADDR, PORT, addr12, msg)
            send_message(PI_A_ADDR, PORT, addr3, msg)
            send_gma3_command("Off Sequence Thru Please")
            time.sleep(0.3)
            send_gma3_command("Go+ Sequence 75") # win
            time.sleep(8)
            send_gma3_command("Off Sequence 75")
            time.sleep(3)
            send_message(PI_A_ADDR, PORT, addr12, msg)
            send_message(PI_A_ADDR, PORT, addr6, msg)
            send_gma3_command("Off Sequence Thru Please")      
            send_gma3_command("Go+ Sequence 78") # buzzing
            time.sleep(4.5)
            send_gma3_command("Off Sequence 78")     
            send_gma3_command("Go+ Sequence 77") # warning
            time.sleep(6)
            send_gma3_command("Off Sequence 77")
            time.sleep(0.3)
            send_message(PI_A_ADDR, PORT, addr5, msg)
            send_gma3_command("Off Sequence Thru Please")     
            send_gma3_command("Go+ Sequence 69")
            time.sleep(0.3)
            return True
        else:
            send_gma3_command("Off Sequence Thru Please")     
            time.sleep(0.3)   
            send_gma3_command("Go+ Sequence 69")
            time.sleep(0.3)
        

        attempts += 1
        if attempts < max_attempts:
            print(f"Try again! Attempts left: {max_attempts - attempts}")
        else:
            print(f"Out of attempts! The correct numbers were: {random_no_gen}")
            return False
        

def start_expert_level(sonic_target, rfid_target):
    global lock_in, expert_mode

    print("Starting Expert Level!")
    print(f"Ultrasonic target sequence: {sonic_target}")
    print(f"RFID target sequence: {rfid_target}")

    expert_mode = True  # enable debug prints

    # Start RFID reader thread
    global rfid_thread_started
    if not rfid_thread_started:
        rfid_thread = Thread(target=rfid_server, daemon=True)
        rfid_thread.start()
        rfid_thread_started = True        

    attempts = 0
    max_attempts = 500

    while attempts < max_attempts:
        print(f"🔄 Attempt {attempts + 1}/{max_attempts} — Monitoring live inputs. Press the button to lock in your answer...")

        sonic_input = [0, 0, 0, 0]
        rfid_input = [None, None, None, None]

        # Wait for button press and show live data
        last_print_time = 0
        while not lock_in:
            try:
                sonic_input = [
                    tryy.get_dist_sensor1(),
                    tryy.get_dist_sensor2(),
                    tryy.get_dist_sensor3(),
                    tryy.get_dist_sensor4()
                ]
                temp_rfid = combined_rfid_inputs()

                current_time = time.time()
                if current_time - last_print_time > 2:
                    print(f"   Live Sonic: {sonic_input} | RFID: {temp_rfid}")
                    last_print_time = current_time
                time.sleep(7)
            except Exception as e:
                print(f"⚠️ Error reading inputs: {e}")
                time.sleep(1)

        print("✅ Inputs locked in!")
        lock_in = False

        try:
            rfid_input = read_rfid_inputs_with_timeout(timeout=1.5)
        except Exception as e:
            import traceback
            print("⚠️ Full input error:")
            traceback.print_exc()
            continue

        if tryy.validation(sonic_input) is None:
            print("Invalid ultrasonic input. Retrying...")
            continue

        if any(r is None for r in rfid_input):
            print("Invalid RFID input detected. Retrying...")
            continue

        sonic_results = tryy.matching_numbers(sonic_input, sonic_target)
        rfid_results = ['green' if inp == tgt else 'red' for inp, tgt in zip(rfid_input, rfid_target)]
        green_count_rfid_check = rfid_results.count('green')
        green_count_ultras_check = sonic_results.count('green')
        if green_count_rfid_check == 1 :
            send_message(PI_A_ADDR, PORT, addr12, msg)
            send_message(PI_A_ADDR, PORT, addr7, msg)
            send_gma3_command("Off Sequence Thru Please")     
            time.sleep(0.3)   
            send_gma3_command("Go+ Sequence 79")
            time.sleep(2)
            send_gma3_command("Off Sequence 79")   
            send_gma3_command("Go+ Sequence 69")
            time.sleep(0.3)
        elif green_count_rfid_check == 2:
            send_message(PI_A_ADDR, PORT, addr12, msg)
            send_message(PI_A_ADDR, PORT, addr8, msg)
            send_gma3_command("Off Sequence Thru Please")     
            time.sleep(0.3)   
            send_gma3_command("Go+ Sequence 79")
            time.sleep(1)
            send_gma3_command("Go+ Sequence 79 Cue 1")
            time.sleep(1)
            send_gma3_command("Off Sequence 79")   
            send_gma3_command("Go+ Sequence 69")
            time.sleep(0.3)
        # elif green_count_rfid_check == 3:
        #     send_message(PI_A_ADDR, PORT, addr12, msg)
        #     send_message(PI_A_ADDR, PORT, addr9, msg)
        #     send_gma3_command("Off Sequence Thru Please")     
        #     time.sleep(0.3)   
        #     send_gma3_command("Go+ Sequence 79")
        #     time.sleep(1)
        #     send_gma3_command("Go+ Sequence 79 Cue 1")
        #     time.sleep(1)
        #     send_gma3_command("Go+ Sequence 79 Cue 1")
        #     time.sleep(1)
        #     send_gma3_command("Off Sequence 79")   
        #     send_gma3_command("Go+ Sequence 69")
        #     time.sleep(0.3)
        elif green_count_rfid_check == 4:
            send_message(PI_A_ADDR, PORT, addr12, msg)
            send_message(PI_A_ADDR, PORT, addr10, msg)
            time.sleep(1)
            send_gma3_command("Off Sequence Thru Please")       
            send_gma3_command("Go+ Sequence 79")
            time.sleep(1)
            send_gma3_command("Go+ Sequence 79 Cue 1")
            time.sleep(1)
            send_gma3_command("Go+ Sequence 79 Cue 1")
            time.sleep(1)
            send_gma3_command("Go+ Sequence 79 Cue 1")
            time.sleep(1)
            send_gma3_command("Off Sequence 79")
        else:
            send_message(PI_A_ADDR, PORT, addr12, msg)
            send_message(PI_A_ADDR, PORT, addr11, msg)
            send_gma3_command("Off Sequence Thru Please")
            send_gma3_command("Go+ Sequence 74")
            time.sleep(9)
            send_gma3_command("Off Sequence 74")  
            send_gma3_command("Go+ Sequence 69")
            time.sleep(0.3)
        print(f"Ultrasonic Results: {sonic_results}")
        print(f"RFID Results: {rfid_results}")
    
        if all(c == 'green' for c in sonic_results) and all(c == 'green' for c in rfid_results):
            print("🎉 Congratulations! You completed the Expert Level!")
            send_message5(PI_A_ADDR, PORT, addr12, msg)
            send_gma3_command("Off Sequence Thru Please")
            send_gma3_command("Go+ Sequence 75")
            time.sleep(0.3)
            send_message5(PI_A_ADDR, PORT, addr3, msg)
            time.sleep(8)
            send_gma3_command("Off Sequence 75")
            send_gma3_command("Off Sequence Thru Please")
            time.sleep(0.3)
            send_gma3_command("Go+ Sequence 76")
            send_message5(PI_A_ADDR, PORT, addr13, msg)
            time.sleep(4)
            send_message5(PI_A_ADDR, PORT, addr14, msg)                       
            expert_mode = False
            return True
        # else:
        #     send_gma3_command("Off Sequence Thru Please")     
        #     time.sleep(0.3)   
        #     send_gma3_command("Go+ Sequence 69")
        #     time.sleep(0.3)

        attempts += 1
        time.sleep(1)

    print("❌ Out of attempts.")
    expert_mode = False
    return False

def main():
    print("🎮 Starting game system...")

    time.sleep(3)  # Wait for network connections to establish

    while True:
        try:
            hard_numbers = [random.choice([10, 20, 30, 40]) for _ in range(4)]
            print("🟡 Starting Hard Level...")

            if start_game("Hard", hard_numbers):
                print("\n🔴 Moving to Expert Level...")
                rfid_sequence = random.sample(['A', 'B', 'C', 'D'], k=4)
                expert_sonic_sequence = hard_numbers
                if start_expert_level(expert_sonic_sequence, rfid_sequence):
                    print("🏁 Game Completed!")
                    time.sleep(40)
                    continue  # Restart the game
                else:
                    send_message(PI_A_ADDR, PORT, addr4, msg)
                    print("\n💀 Game Over at Expert Level. Restarting from Hard Level...")
            else:
                send_message(PI_A_ADDR, PORT, addr4, msg)
                print("\n💀 Game Over at Hard Level. Restarting from Hard Level...")

        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"💥 Fatal error: {e}")
            break
        finally:
            GPIO.cleanup()

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"💥 Fatal error: {e}")
        GPIO.cleanup()


