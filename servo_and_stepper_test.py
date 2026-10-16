import serial
import time
import sys

# --- Configuration ---
SERIAL_PORT = 'COM5' # Change if your port is different
BAUD_RATE = 115200

def send_gcode(arduino, command):
    """Sends a G-code command and waits for the 'ok' response."""
    print(f"  Command -> {command.strip()}")
    arduino.write(command.encode('utf-8'))
    
    while True:
        response = arduino.readline().decode('utf-8', errors='ignore').strip()
        if response == 'ok':
            break
        elif response != "":
            print(f"  Arduino: {response}")

def main():
    print("Connecting to Smart Typewriter...")
    try:
        arduino = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=2)
    except Exception as e:
        print(f"Error connecting: {e}")
        return

    time.sleep(2)
    arduino.flushInput()
    
    print("Unlocking GRBL Alarm...")
    arduino.write(b"$X\n")
    time.sleep(1)
    
    # Setup positioning and speed
    send_gcode(arduino, "G92 X0 Y0 Z0\n") # Set current physical position as absolute Zero
    send_gcode(arduino, "G90\n")          # Absolute positioning mode
    send_gcode(arduino, "G21\n")          # Millimeters mode
    
    print("\n=========================================")
    print(" STARTING CONTINUOUS HARDWARE TEST ")
    print(" *** PRESS 'CTRL + C' TO STOP *** ")
    print("=========================================\n")
    
    try:
        loop_count = 1
        # The 'while True' loop replaces the Arduino loop() function
        while True:
            print(f"\n--- Starting Loop #{loop_count} ---")
            
            # 1. Drop Pen to start drawing
            print("Dropping Pen...")
            send_gcode(arduino, "G0 Z0\n")
            time.sleep(0.5)

            # 2. Draw a 20x20mm Square (SPEED LOWERED TO F300)
            print("Drawing Bottom Line (X+)...")
            send_gcode(arduino, "G1 X20 Y0 F300\n")
            
            print("Drawing Right Line (Y+)...")
            send_gcode(arduino, "G1 X20 Y20 F300\n")
            
            print("Drawing Top Line (X-)...")
            send_gcode(arduino, "G1 X0 Y20 F300\n")
            
            print("Drawing Left Line (Y-)...")
            send_gcode(arduino, "G1 X0 Y0 F300\n")

            # 3. Lift Pen to finish the shape
            print("Finished shape. Lifting Pen...")
            send_gcode(arduino, "G0 Z5\n")
            time.sleep(0.5)

            # 4. Wait for the interval before repeating
            print("Waiting 2 seconds before repeating...")
            time.sleep(2)
            
            loop_count += 1

    except KeyboardInterrupt:
        # This safely catches when you press Ctrl+C to abort the script
        print("\n\nTest Stopped by User.")
        send_gcode(arduino, "G0 Z5\n") # Ensure pen lifts if you abort
        print("Returning to Home (0,0)...")
        send_gcode(arduino, "G0 X0 Y0 F300\n") # Bring the head back to the start smoothly
        
    arduino.close()
    print("\nTest complete. Connection closed.")

if __name__ == "__main__":
    main()