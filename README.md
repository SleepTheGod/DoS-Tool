# Amp NTP DoS Tool using Flask and Scapy

This project demonstrates an NTP amplification attack using Flask for the interface and Scapy for sending crafted NTP packets. This script allows you to simulate the attack by sending NTP requests to a target using randomly selected NTP servers from a provided list.

Important: This project is intended for educational purposes only. Do not use this tool for malicious activities. Always ensure you have permission from any target you are testing against.

Features
Simulates an NTP amplification attack by sending crafted NTP requests.
Uses a list of NTP servers to randomly choose from when sending packets.
Flask-powered web interface for user input and attack execution.
Supports multi-threading for sending requests concurrently.
Requirements
Python 3.x
Scapy library for crafting and sending packets
Flask for web interface

```bash
git clone https://github.com/SleepTheGod/DoS-Tool
cd DoS-Tool
pip install -r requirements.txt
python app.py
```
Open your web browser and navigate to http://127.0.0.1:5000/ to access the web interface.

Enter the target IP/hostname and the number of threads to execute the attack.

Press Submit to start the attack. The backend will send NTP requests to the target using multiple threads.

Sample Request
If you prefer to use a tool like curl or Postman to send the attack request, you can do so by making a POST request to the /attack endpoint.
```bash
curl -X POST -d "target=example.com&threads=50" http://127.0.0.1:5000/attack
```
This will trigger an attack with 50 threads targeting example.com.

Code Explanation
Core Components
Flask Web Interface: The Flask framework provides a simple web interface for entering the target IP/hostname and the number of threads for the attack.

NTP Packet Crafting: The NTP attack leverages Scapy to craft and send NTP requests. The payload is constructed to simulate a valid NTP request

```python
packet = IP(dst=self.tgt) / UDP(dport=123) / Raw(load=b"\x1b" + 47 * b"\0")
```
Multi-threading: Multiple threads are used to send requests concurrently, increasing the intensity of the attack
```python
threading.Thread(target=self.send_ntp_request, args=(ntp_server,))
```

File Descriptions
app.py: The main Flask application containing the logic for the attack simulation.
ntp.txt: A text file containing a list of NTP server IP addresses. This file is read to select random servers for each request.
Security and Ethical Considerations
This tool is for educational purposes only. Misusing this tool to perform actual NTP amplification attacks without permission is illegal and unethical. Always ensure you have proper authorization before running security tests on any system.
