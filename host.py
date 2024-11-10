import subprocess
import ipaddress

def is_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False
    
def system(cmd):
    cmd_return = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return cmd_return.stdout
    

def netdiscover(ip):
    net_res = system("netdiscover -P -r" + ip)
    
    ip_addr = []
    mac_addr = []
    # print(net_res)
    for i in net_res.strip().splitlines():
        line = i.split()

        try:
            line[0]
        except:
            continue

        if is_ip(line[0]):
            ip_addr.append(line[0])
            mac_addr.append(line[1])
    return (ip_addr, mac_addr)


if __name__ == "__main__":
    ip = "172.16.20.0/24"
    print(netdiscover(ip))