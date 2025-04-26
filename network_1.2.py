from socket import *
import requests
import time
from urllib.parse import urlparse
from datetime import datetime

class ProxyServerWithCache:
    def __init__(self):
        self.cache = {}  # Dictionary to store cached responses
        self.server_port = 12000


        self.blocked_domains = [
            "youtube.com",
            "facebook.com",
            "tiktok.com"
        ]

        self.start_server()

    def log_request(self, url, status):

        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {status} → {url}"
        print(log_entry)



    def start_server(self):
        server_socket = socket(AF_INET, SOCK_STREAM)
        server_socket.bind(('localhost', self.server_port))
        server_socket.listen(1)
        print(f" Proxy server with cache, firewall, and logging is running on port {self.server_port}")

        while True:
            connection_socket, addr = server_socket.accept()
            print(" Connected by:", addr)

            try:
                url = connection_socket.recv(1024).decode().strip()
                print(" Client requested:", url)


                domain = urlparse(url).netloc.lower()
                if any(domain.endswith(blocked) for blocked in self.blocked_domains):
                    print(f" BLOCKED: {domain}")
                    connection_socket.send(" Access to this domain is blocked by the firewall.".encode())
                    connection_socket.close()
                    continue

                if url in self.cache:
                    cached_data = self.cache[url]
                    age = time.time() - cached_data["timestamp"]
                    max_age = cached_data.get("max_age", 0)

                    if age <= max_age:
                        self.log_request(url, "CACHE_HIT")
                        connection_socket.send(cached_data["content"].encode())
                        connection_socket.close()
                        continue
                    else:
                        print(" Cache expired, refetching...")


                response = requests.get(url)
                content = response.text[:5000]
                headers = response.headers


                max_age = 0
                cache_control = headers.get("Cache-Control", "")
                if "max-age" in cache_control:
                    try:
                        max_age = int(cache_control.split("max-age=")[-1].split(",")[0])
                    except:
                        pass

                # Save to cache
                self.cache[url] = {
                    "content": content,
                    "timestamp": time.time(),
                    "max_age": max_age
                }

                self.log_request(url, "CACHE_MISS")
                print(f"💾 Cached {url} for {max_age} seconds")
                connection_socket.send(content.encode())

            except Exception as e:
                error_message = f" Failed to fetch {url}: {str(e)}"
                print(error_message)
                connection_socket.send(error_message.encode())

            connection_socket.close()

if __name__ == '__main__':
    ProxyServerWithCache()
