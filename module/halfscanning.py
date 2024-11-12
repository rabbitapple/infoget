from scapy.all import *
import os
import socket
import trace

class Halfscan:
    """
    하프 스캐닝 및 다른 IP/Port 스캐닝에 필요한 메서드가 포함된 class
    """
    def __init__(self) -> None:
        """
        local network 정보 정의
        """
        self.path = os.path.dirname(os.path.abspath(__file__))
        self.gateway = self.getgateway()
        if self.gateway != "0.0.0.0":
            self.gateway_mac = self.getmac(self.gateway)
        else:
            self.gateway_mac = "FF:FF:FF:FF:FF:FF"

        self.my_ip = socket.gethostbyname(socket.gethostname())
        
    

    def getmyip(self) -> str:
        """
        local ip 주소 획득 메서드        
        Returns:
            str: local ip address
        """

        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:
            # Google의 공개 DNS 서버(8.8.8.8)와 임의 연결 시도
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
        finally:
            s.close()
            print(ip)
        return ip   

    
    def getmac(self, dip):
        """
        ARP를 통한 Mac Address 획득 메서드

        ARP 요청을 통해 주어진 Destination IP Address(dip)에 해당하는 MAC 주소를 얻는다.
        만약 ARP 응답이 없거나 호스트가 다른 네트워크에 있을 경우, Gateway의 MAC 주소를 반환하며 
        ARP 수신에 문제가 발생할 경우, 0을 반환.

        Args:
            dip(str): ARP Destination IP Address (형식 : xxx.xxx.xxx.xxx)
        Returuns:
            str: Destination IP Address의 Mac Address. ARP Response가 있을 경우에 반환
            str: Gateway의 Mac Address. 호스트가 없거나 다른 네트워크일경우 반환
            int: Gateway Mac Address Searching 중 ARP 수신에 문제가 발생할경우 반환
        """
         # Mac 주소 획득
        ether = Ether(dst = "ff:ff:ff:ff:ff:ff")
        arp = ARP(pdst = dip)
        arppk  = srp(ether/arp, timeout = 0.1, verbose = 0)

        if not arppk[0]:
            print("ARP 패킷이 도달하지 않는 호스트입니다.")
            # os.system("tput rmcup")
            try:
                return self.gateway_mac
            except:
                return 0
        
        else:
            dmac = arppk[0][0][1][ARP].hwsrc
            return dmac
            
    def getgateway(self):
        """
        Local에 설정된 Default Gateway를 /proc/net/route 파일을 읽어 16진수로 획득 후 10진수로 변환하여 반환
        Returns:
            str: Local Default Gateway Decimal IP Addres
        """
        with open("/proc/net/route", "r", encoding="UTF=8") as router:
            router_read = router.read()
        router_li = router_read.strip().splitlines()
        router_info = router_li[1].split("\t")

        if router_info[1] == "00000000":
            gateway_hexa = router_info[2]
        else:
            gateway_hexa = router_info[1]

        gateway = "%s.%s.%s.%s"%(str(int(gateway_hexa[6:8],16)), str(int(gateway_hexa[4:6],16)), str(int(gateway_hexa[2:4],16)), str(int(gateway_hexa[0:2],16)))

        return gateway

            

    def scanstart(self, dip):
        """
        특정 IP에 대하여 Half Port Scanning(TCP)

        이 메서드는 지정된 IP 주소에 대해 미리 정의된 포트 리스트를 이용해 TCP 연결을 시도하고, 열린 포트를 찾아 출력. 
        또한, 해당 IP 주소의 MAC 주소를 확인하고, 연결할 수 없는 경우에는 스캔을 중단.
        Args:
            dip(str): Port Scanning할 IP Address (형식 : xxx.xxx.xxx.xxx)
        """
        try:
            os.system("tput smcup")
            clearcmd = "clear"
            os.system(clearcmd)
            
            # Mac 주소 획득
            dmac = self.getmac(dip)

            if dmac == 0:
                return

            # 2,3 Layer 패킷빌딩
            ether = Ether(dst = dmac)
            ip = IP(dst = dip)

            # 포트 정보 가져오기 / 가공
            with open(self.path + "/../db_data/port_db", "r", encoding="UTF-8") as dbfile:
                port_db = dbfile.read()
            print(self.path + "/../db_data/port_db")

            port_list = port_db.strip().splitlines()
            
            # wellkown포트 TCP 패킷 전송/결과출력
            print("%s : "%dip)
            print("%-5s%-25s"%("Port", "Discription"))
            open_port = []
            for i in port_list:
                p_list = i.split(",")
                tcp = TCP(dport = int(p_list[0]))

                res = srp1(ether/ip/tcp, verbose = 0, timeout = 1)

                if res[TCP].flags in ["SA", "A"]:
                    open_port.append(p_list)
                    print("%-5s%-25s"%(p_list[0], p_list[1]))
            input("End")
            os.system("tput rmcup")
        except TypeError:
            os.system("tput rmcup")
            print("TypeError: 호스트가 존재하지 않을 수 있습니다.")

        except:
            os.system("tput rmcup")
            print(traceback.format_exc())
            pass


if __name__ == "__main__":
    scan = Halfscan()
    scan.scanstart("172.16.20.15")
