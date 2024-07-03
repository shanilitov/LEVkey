import requests

# פונקציה לבדיקת חיבור
def test_connect():
    url = 'http://localhost:5000/connect'
    response = requests.post(url)
    assert response.status_code == 200
    print("Connect:", response.json())

# פונקציה לבדיקת ניתוק
def test_disconnect():
    url = 'http://localhost:5000/disconnect'
    response = requests.post(url)
    assert response.status_code == 200
    print("Disconnect:", response.json())

# פונקציה לשליחת הודעה
def test_send_message():
    url = 'http://localhost:5000/send_message'
    data = {'message': 'Hello, Mesh!'}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    print("Send Message:", response.json())

# פונקציה לקבלת הודעות
def test_get_messages():
    url = 'http://localhost:5000/get_messages'
    response = requests.get(url)
    assert response.status_code == 200
    print("Get Messages:", response.json())

# פונקציה לשליחת הודעת מיקום
def test_send_location():
    url = 'http://localhost:5000/send_message'
    data = {'message': 'LOC:32.12345,34.56789'}
    response = requests.post(url, json=data)
    assert response.status_code == 200
    print("Send Location:", response.json())

# פונקציה לקבלת מיקומים
def test_get_locations():
    url = 'http://localhost:5000/get_locations'
    response = requests.get(url)
    assert response.status_code == 200
    print("Get Locations:", response.json())

# ביצוע כל הבדיקות
if __name__ == '__main__':
    test_connect()
    test_send_message()
    test_get_messages()
    test_send_location()
    test_get_locations()
    test_disconnect()
