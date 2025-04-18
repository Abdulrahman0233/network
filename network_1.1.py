from socket import *
import time

class ProxyClient:
    def __init__(self):
        self.server_name = 'localhost'
        self.server_port = 12000

    def run(self):
        client_socket = socket(AF_INET, SOCK_STREAM)

        try:
            client_socket.connect((self.server_name, self.server_port))
            url = input("🌐 Enter a URL to request (e.g. https://www.wikipedia.org): ").strip()

            # Send the URL to the proxy
            client_socket.send(url.encode())

            # ⏱ Start timing the response
            start_time = time.time()

            response = client_socket.recv(8192).decode()

            # ⏱ End timing
            end_time = time.time()
            duration = round(end_time - start_time, 4)

            print("\n📥 Response from proxy (first 1000 characters):\n")
            print(response[:1000])  # Limit print size

            print(f"\n⏱️ Time taken to receive response: {duration} seconds")

            client_socket.close()

        except ConnectionRefusedError:
            print("❌ Could not connect to the proxy server. Is it running?")
        except Exception as e:
            print("❌ Error occurred:", e)

if __name__ == '__main__':
    client = ProxyClient()
    client.run()
