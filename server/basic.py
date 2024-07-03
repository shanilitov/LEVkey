import serial
import time

# הגדרות חיבור סיריאלי
serial_port = 'COM3'  # יש לשנות לפורט המתאים למכשיר שלך
baud_rate = 115200

try:
    # פתיחת חיבור סיריאלי
    ser = serial.Serial(serial_port, baud_rate, timeout=1)
    print(f"Connected to {ser.name}.")

    # שליחת הודעה למכשיר
    message = "Hello, TTGO T-Beam!"
    ser.write(message.encode('utf-8'))
    print(f"Sent: {message}")

    # קריאה מהמכשיר
    while True:
        line = ser.readline().decode('utf-8').strip()
        if line:
            print(f"Received: {line}")
            # כאן תוכל לעבד את ההודעה המתקבלת כראוי

except serial.SerialException as e:
    print(f"Error: {e}")

finally:
    if ser.isOpen():
        ser.close()
        print("Serial connection closed.")
