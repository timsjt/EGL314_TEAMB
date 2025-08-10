from Phidget22.Phidget import *
from Phidget22.Devices.RFID import *
from Phidget22.PhidgetException import *
from Phidget22.Devices.Manager import Manager

connected_readers = {}
tag_states = {}  # {serial: tag_id}

def on_tag_handler(rfid, tag, protocol):
    serial = rfid.getDeviceSerialNumber()
    tag_states[serial] = tag
    print(f"Tag Detected on Reader #{serial}: {tag} (Protocol: {protocol})")

def on_tag_lost_handler(rfid, tag, protocol):
    serial = rfid.getDeviceSerialNumber()
    if serial in tag_states and tag_states[serial] == tag:
        del tag_states[serial]
    print(f"Tag Lost on Reader #{serial}: {tag} (Protocol: {protocol})")

def on_attach_handler(manager, phidget):
    serial = phidget.getDeviceSerialNumber()
    if serial not in connected_readers:
        try:
            rfid = RFID()
            rfid.setDeviceSerialNumber(serial)
            rfid.setOnTagHandler(on_tag_handler)
            rfid.setOnTagLostHandler(on_tag_lost_handler)
            rfid.openWaitForAttachment(5000)
            rfid.setAntennaEnabled(True)
            connected_readers[serial] = rfid
            print(f"RFID Reader Connected: Serial #{serial}")
        except PhidgetException as e:
            print(f"Failed to open RFID #{serial}: {e.details}")

def on_detach_handler(manager, phidget):
    serial = phidget.getDeviceSerialNumber()
    if serial in connected_readers:
        try:
            connected_readers[serial].close()
        except:
            pass
        del connected_readers[serial]
        if serial in tag_states:
            del tag_states[serial]
        print(f"RFID Reader Disconnected: Serial #{serial}")

def start_rfid_manager():
    try:
        manager = Manager()
        manager.setOnAttachHandler(on_attach_handler)
        manager.setOnDetachHandler(on_detach_handler)
        manager.open()
        return manager
    except PhidgetException as e:
        print("Phidget Exception:", e.details)
        return None

def get_rfid_inputs():
    return dict(tag_states)  # Copy for thread safety

def get_connected_readers():
    return list(connected_readers.keys())

def close_all_readers(manager=None):
    if manager:
        try:
            manager.close()
        except:
            pass
    for reader in connected_readers.values():
        try:
            reader.close()
        except:
            pass
    connected_readers.clear()
    tag_states.clear()
