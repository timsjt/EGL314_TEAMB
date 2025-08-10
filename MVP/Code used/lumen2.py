import socket
import json
import time
from Phidget22.PhidgetException import PhidgetException
from rfid import get_rfid_inputs, start_rfid_manager, close_all_readers, get_connected_readers

# Reader and tag mappings
READER_NAMES = {
    78725: "1",
    77943: "2",
    78639: "3",
    77946: "4",
}

TAG_NAMES = {
    "01068de1e7": "A", "01068dc193": "A", "01068df314": "A", "01068de7f6": "A",
    "01068dc1ac": "B", "01068db98f": "B", "01068dd202": "B", "01068dc4f5": "B",
    "01068defca": "C", "01068de125": "C", "01068deaaf": "C", "01068dc357": "C",
    "01068dead9": "D", "01068dedb8": "D", "01068dbdae": "D", "01068dc5c1": "D",
}

def resolve_tag_data(raw_data):
    resolved = {}
    for serial, tag in raw_data.items():
        reader_name = READER_NAMES.get(int(serial), f"Unknown Reader ({serial})")
        tag_name = TAG_NAMES.get(tag, f"Unknown Tag ({tag})")
        resolved[reader_name] = tag_name
    return resolved

def send_rfid_data():
    manager = None
    client_socket = None

    try:
        manager = start_rfid_manager()

        if manager is None:
            print("❌ Failed to start RFID manager. Check hardware connections.")
            return

        print("Waiting for RFID readers to initialize...")
        time.sleep(5)

        connected = get_connected_readers()
        if not connected:
            print("❌ No RFID readers detected. Waiting...")
            while True:
                time.sleep(10)
                connected = get_connected_readers()
                if connected:
                    print(f"✅ RFID readers now detected: {connected}")
                    break

        print(f"✅ Detected RFID readers: {connected}")

        PRIMARY_PI_IP = "192.168.254.133"
        PORT = 65432

        retry_delay = 3
        connected_to_server = False

        while True:
            try:
                client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
                client_socket.connect((PRIMARY_PI_IP, PORT))

                if not connected_to_server:
                    print("✅ Connected to Primary Raspberry Pi!")
                    print(f"📡 This Pi handles RFID readers: {get_connected_readers()}")
                    connected_to_server = True

                while True:
                    rfid_inputs = get_rfid_inputs()  # {serial: tag}
                    connected = get_connected_readers()

                    if not connected:
                        print("⚠️  No connected readers, waiting...")
                        time.sleep(5)
                        continue

                    resolved_data = resolve_tag_data(rfid_inputs)

                    data = {
                        "rfid_inputs": resolved_data,
                        "pi_id": "pi2",
                        "readers": [READER_NAMES.get(int(r), str(r)) for r in connected]
                    }

                    message = json.dumps(data).encode()
                    client_socket.sendall(message)

                    print(f"📤 Sent RFID data: {resolved_data}")
                    time.sleep(1)

            except (ConnectionResetError, BrokenPipeError):
                if connected_to_server:
                    print("🔌 Disconnected from Primary Raspberry Pi.")
                    connected_to_server = False
                time.sleep(retry_delay)

            except ConnectionRefusedError:
                print(f"❌ Unable to connect. Retrying in {retry_delay} seconds...")
                connected_to_server = False
                time.sleep(retry_delay)

            except Exception as e:
                print(f"❌ Unexpected error: {e}")
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
        close_all_readers(manager)

if __name__ == "__main__":
    send_rfid_data()
