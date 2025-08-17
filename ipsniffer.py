import  re
import subprocess
predict =  r"Failed password.*?(\d{1,3}(?:\.\d{1,3}){3})"
store = {}
with open("aut.log","r") as file:
    for line in file:
        match = re.search(predict,line)
        if match:
            ip = match.group(1)
            store[ip] = store.get(ip,0)+1

def block_ip(ip,test_mode = True):
    command = ["sudo", "ufw", "deny", "from", ip]
    if test_mode:
        print("TEST MODE — Would run:", " ".join(command))
    else:
        subprocess.run(command)
        print(f"This ip {ip} has been blocked")

threshold = 2
for ip,count in sorted(store.items(), key = lambda x:x[1], reverse=True):
    if count >= threshold:
        print(f"This ip address {ip} has made {count} failed attempts")
        block_ip(ip,test_mode = True)