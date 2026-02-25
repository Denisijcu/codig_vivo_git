import socket
from threading import Thread

class ConnectionMonitor:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind(('0.0.0.0', 8080))
        self.socket.listen(5) # Listen for up to 5 connections
        self.blocked_ips = {}
        self.max_attempts = 10

    def handle_connection(self, client_socket, addr):
        attempts = 0
        
        while True:
            try:
                data = client_socket.recv(1024)
                
                if not data: break
                
                # Process the received data here.
                
                attempts += 1
                if attempts > self.max_attempts:
                    print(f'Blocking IP {addr[0]} due to exceeding max attempts.')
                    self.blocked_ips[addr[0]] = True
                    client_socket.close()
                    break
            
            except Exception as e:
                print(f"Error handling connection from {addr}: {e}")
                client_socket.close()
                break
        
        print(f'Connection closed with {addr}')

    def block_ip(self, ip):
        self.blocked_ips[ip] = True

    def unblock_ip(self, ip):
        if ip in self.blocked_ips:
            del self.blocked_ips[ip]

    def run(self):
        while True:
            client_socket, addr = self.socket.accept()
            print(f'Connection from {addr}')
            
            # Check if IP is blocked
            if addr[0] in self.blocked_ips and self.blocked_ips[addr[0]]:
                print(f'Ignoring connection from blocked IP: {addr[0]}')
                client_socket.close()
                continue
            
            thread = Thread(target=self.handle_connection, args=(client_socket, addr))
            thread.start()

    def stop(self):
        self.socket.shutdown(socket.SHUT_RDWR)
        self.socket.close()

if __name__ == "__main__":
    monitor = ConnectionMonitor()
    
    try:
        print("Starting connection monitor...")
        monitor.run()
    except KeyboardInterrupt:
        print("\nStopping connection monitor...")
        monitor.stop()