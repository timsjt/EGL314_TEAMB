import socket

import json

import time

from rfid import get_rfid_inputs, start_rfid_manager, close_all_readers, get_connected_readers



def send_rfid_data():

    manager = None
    client_socket = None

    try:

        # Start RFID manager and let it auto-detect connected readers
        manager = start_rfid_manager()
        if manager is None:
            print("❌ Failed to start RFID manager. Check hardware connections.")
            return

        print("Waiting for RFID readers to initialize...")
        time.sleep(5)

        # Check which readers are actually connected
        connected = get_connected_readers()
        if not connected:
            print("❌ No RFID readers detected on this Pi. Check connections.")
            print("This Pi will continue running but won't send any data.")
            # Keep the program running in case readers are connected later
            while True:
                time.sleep(10)
                connected = get_connected_readers()
                if connected:
                    print(f"✅ RFID readers now detected: {connected}")
                    break

        print(f"✅ Detected RFID readers: {connected}")

        PRIMARY_PI_IP = "192.168.254.137"  # Update if needed

        PORT = 65432

        retry_delay = 3

        connected_to_server = False



        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.connect((PRIMARY_PI_IP, PORT))

                if not connected_to_server:
                    print("✅ Connected to Primary Raspberry Pi!")
                    current_readers = get_connected_readers()
                    print(f"📡 This Pi handles RFID readers: {current_readers}")
                    connected_to_server = True

                while True:
                    # Get inputs from connected readers only
                    rfid_inputs = get_rfid_inputs()
                    current_readers = get_connected_readers()

                    

                    # Only send data if we have connected readers

                    if not current_readers:

                        print("⚠️  No connected readers, waiting...")

                        time.sleep(5)

                        continue

                    

                    # Create data packet with dynamic reader information

                    data = {

                        "rfid_inputs": rfid_inputs,

                        "pi_id": "pi2",  # Identify which Pi this is

                        "readers": current_readers  # Dynamic list of connected readers

                    }

                    message = json.dumps(data).encode()

                    client_socket.sendall(message)



                    print(f"📤 Sent RFID data (Readers {current_readers}): {rfid_inputs}")

                    time.sleep(1)



            except (ConnectionResetError, BrokenPipeError):

                if connected_to_server:

                    print("🔌 Disconnected from Primary Raspberry Pi.")

                    connected_to_server = False

                time.sleep(retry_delay)



            except ConnectionRefusedError:

                if connected_to_server:

                    print("🔌 Connection refused. Primary Raspberry Pi may be down.")

                    connected_to_server = False

                else:

                    print(f"❌ Unable to connect. Retrying in {retry_delay} seconds...")

                time.sleep(retry_delay)



            except Exception as e:

                print(f"❌ Unexpected error: {e}")

                if connected_to_server:

                    connected_to_server = False

                time.sleep(retry_delay)



            finally:

                if client_socket:

                    try:

                        client_socket.close()

                    except:

                        pass

                    client_socket = None



    except KeyboardInterrupt:

        print("\nShutdown requested...")

    except Exception as e:

        print(f"Fatal error: {e}")

    finally:

        print("Cleaning up...")

        if client_socket:

            try:

                client_socket.close()

            except:

                pass

        

        # This will now handle None values gracefully

        close_all_readers(manager)



if __name__ == "__main__":

    send_rfid_data()

##