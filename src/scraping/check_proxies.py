import requests
import threading
import queue

q = queue.Queue()
valid_proxies = []

with open("proxy_list.txt", "r") as f:
    proxies = f.read().splitlines()
    for proxy in proxies:
        q.put(proxy)

def check_proxy():
    while not q.empty():
        proxy = q.get()
        try:
            response = requests.get(
                "http://httpbin.org/ip",
                proxies={"http": f"http://{proxy}", "https": f"http://{proxy}"},
                timeout=5
            )
            if response.status_code == 200:
                print(f"Proxy válido: {proxy}")
                valid_proxies.append(proxy)
        except:
            pass

threads = []
for _ in range(10): 
    thread = threading.Thread(target=check_proxy)
    threads.append(thread)
    thread.start()

for thread in threads:
    thread.join()

with open("valid_proxies.txt", "w") as f:
    f.write("\n".join(valid_proxies))
print("Proxies válidos guardados en valid_proxies.txt")
