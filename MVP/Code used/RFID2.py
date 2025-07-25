from Phidget22.Phidget import *
from Phidget22.Devices.RFID import *
from Phidget22.Devices.Manager import Manager
import random
import time

# All 4 readers - both Pis can detect any of these
reader_custom_ids = {
    78725: "1",
    77943: "2", 
    78639: "3",
    77946: "4",
}

tag_mapping = {
    "01068de1e7": "A", 
    "01068dc193": "A", 
    "01068df314": "A",
    "01068de7f6": "A",
    "01068dc1ac": "B", 
    "01068db98f": "B", 
    "01068dd202": "B", 
    "01068dc4f5": "B",
    "01068defca": "C", 
    "01068de125": "C", 
    "01068deaaf": "C", 
    "01068dc357": "C",
    "01068dead9": "D", 
    "01068dedb8": "D", 
    "01068dbdae": "D",
    "01068dc5c1": "D",
}

rfid_readers = {}
# Track all 4 readers, regardless of which Pi detects them
current_rfid_inputs = {"1": None, "2": None, "3": None, "4": None}

# Track which readers are actually connected to this Pi
connected_readers = set()

# Configuration: Which readers should this Pi report?
# This will be dynamically determined based on connected readers
PI_READERS = []

# Global manager instance
manager_instance = None

def on_tag_handler(reader_id, tag):
    custom_tag_id = tag_mapping.get(tag, None)
    if custom_tag_id is None:
        print(f"Unknown tag detected by Artifact {reader_id}.")
        current_rfid_inputs[reader_id] = None
    else:
        current_rfid_inputs[reader_id] = custom_tag_id
        print(f"Artifact {reader_id} placed on Pedestal {custom_tag_id}.")

def on_tag_lost_handler(reader_id, tag, reason):
    print(f"Tag Lost by Artifact {reader_id}: {tag}")
    current_rfid_inputs[reader_id] = None

def on_attach_handler(manager_instance, attached_device):
    global connected_readers, PI_READERS
    try:
        if attached_device.getDeviceClass() == DeviceClass.PHIDCLASS_RFID:
            serial_number = attached_device.getDeviceSerialNumber()
            reader_id = reader_custom_ids.get(serial_number, None)
            if not reader_id:
                print(f"Attached unknown RFID reader: {serial_number}")
                return
            if serial_number in rfid_readers:
                return

            print(f"RFID Reader (Artifact {reader_id}) Attached.")
            
            # Add to connected readers and update PI_READERS
            connected_readers.add(reader_id)
            PI_READERS = sorted(list(connected_readers))  # Keep sorted for consistency
            print(f"Connected readers updated: {PI_READERS}")

            rfid = RFID()
            rfid.setDeviceSerialNumber(serial_number)

            def tag_handler(self, tag, protocol):
                on_tag_handler(reader_id, tag)

            def tag_lost_handler(self, tag, reason):
                on_tag_lost_handler(reader_id, tag, reason)

            rfid.setOnTagHandler(tag_handler)
            rfid.setOnTagLostHandler(tag_lost_handler)

            rfid.openWaitForAttachment(10000)
            rfid.setAntennaEnabled(True)

            rfid_readers[serial_number] = rfid
    except PhidgetException as e:
        print(f"Phidget Exception during attach: {e.details}")

def on_detach_handler(manager_instance, detached_device):
    global connected_readers, PI_READERS
    try:
        serial_number = detached_device.getDeviceSerialNumber()
        reader_id = reader_custom_ids.get(serial_number, None)
        print(f"RFID Reader (Artifact {reader_id}) Detached.")
        if serial_number in rfid_readers:
            rfid_readers[serial_number].close()
            del rfid_readers[serial_number]
            # Clear the input when reader is detached
            if reader_id:
                current_rfid_inputs[reader_id] = None
                # Remove from connected readers and update PI_READERS
                connected_readers.discard(reader_id)
                PI_READERS = sorted(list(connected_readers))
                print(f"Connected readers updated: {PI_READERS}")
    except PhidgetException as e:
        print(f"Phidget Exception during detach: {e.details}")

def get_rfid_inputs():
    """Return only the inputs for the readers that are physically connected to this Pi"""
    if not PI_READERS:
        print("Warning: No RFID readers connected to this Pi")
    
    return [
        current_rfid_inputs[reader_id]
        for reader_id in ["1", "2", "3", "4"]
        if reader_id in connected_readers
    ]
    # result = [current_rfid_inputs.get(reader_id, None) for reader_id in PI_READERS]
    # return result

def get_all_rfid_inputs():
    """Return all 4 RFID inputs (for debugging)"""
    return [current_rfid_inputs.get(str(i), None) for i in range(1, 5)]

def get_connected_readers():
    """Return list of reader IDs that are connected to this Pi"""
    return list(connected_readers)

def set_pi_readers(reader_list):
    """Configure which readers this Pi should report (manual override - not recommended)"""
    global PI_READERS
    PI_READERS = reader_list
    print(f"Manual override: This Pi will report readers: {PI_READERS}")
    print("Warning: This overrides automatic detection. Use get_connected_readers() to see actual connections.")

def start_rfid_manager():
    global manager_instance
    try:
        manager_instance = Manager()
        manager_instance.setOnAttachHandler(on_attach_handler)
        manager_instance.setOnDetachHandler(on_detach_handler)
        manager_instance.open()
        print("RFID Manager started successfully")
        return manager_instance
    except Exception as e:
        print(f"Error starting RFID manager: {e}")
        manager_instance = None
        return None

def close_all_readers(manager=None):
    """Close all RFID readers and the manager. Handles None values gracefully."""
    global manager_instance
    
    # Close all individual readers first
    for serial_number, rfid in list(rfid_readers.items()):
        try:
            print(f"Closing RFID reader {serial_number}")
            rfid.close()
        except Exception as e:
            print(f"Error closing RFID reader {serial_number}: {e}")
    
    # Clear the readers dictionary
    rfid_readers.clear()
    
    # Close the manager
    # Use the passed manager parameter, or fall back to the global instance
    manager_to_close = manager if manager is not None else manager_instance
    
    if manager_to_close is not None:
        try:
            print("Closing RFID manager")
            manager_to_close.close()
        except Exception as e:
            print(f"Error closing RFID manager: {e}")
    else:
        print("No RFID manager to close (was None)")
    
    # Reset global state
    manager_instance = None
    connected_readers.clear()
    global PI_READERS
    PI_READERS = []
    
    print("RFID cleanup completed")


#