from scapy.all import *
from module.halfscanning import Halfscan

class Finddns(Halfscan):
    def __init__(self):
        """
        아래 변수에 대한 값을 DB 및 현제 시스템으로부터 획득하여 정의
        -   self.name_li: /etc/resolv.conf의 nameserver IP
        -   self.sub_dns_list: sub dns 사전
        -   self.gateway_mac: gateway의 Mac Address
        -   self.gateway: gateway IP
        -   self.my_ip: Local IP
        """
        self.path = os.path.dirname(os.path.abspath(__file__))
        with open( self.path + "/../db_data/sub_dns_db", "r", encoding = "UTF-8") as sub_dns_db:
            self.sub_dns_list = sub_dns_db.read().strip().splitlines()
        with open("/etc/resolv.conf") as resolv:
            name_data = resolv.read().strip().splitlines()
        self.name_li = []
        for i in name_data:
            if "nameserver" in i:
                self.name_li.append(i.replace("nameserver", "").strip())
        self.gateway = self.getgateway()
        if self.gateway != "0.0.0.0":
            self.gateway_mac = self.getmac(self.gateway)
        else:
            self.gateway_mac = "FF:FF:FF:FF:FF:FF"

        self.my_ip = socket.gethostbyname(socket.gethostname())
        
        for j in self.name_li:
            self.gateway
    
    def reqdns(self, root_domain):
        """
        사전에 준비한 Sub Domain에 대하여 Root 도메인과 합쳐 DNS 쿼리를 전송하여 
        Response 패킷의 DNS Layer에서 IP가 포함되어있을 경우에 해당 Domain과 IP주소를 출력/반환
        Args:
            root_domain(str): 사전대입을 진행할 루트 도메인 주소를 입력 (형식 : example.com)
        Returns:
            list: [[str, str]] 형식. 전체 도메인과 IP주소가 포함되어있다.
        """
        ether = Ether(dst = self.gateway_mac)
        udp = UDP()
        dns = DNS()        
        issit_domain = []
        for i in self.name_li:
            ip = IP(dst = i )
            # self.sub_dns_list = ["nk", "asdfasdf"]
            for j in self.sub_dns_list:
                dns.qd = DNSQR(
                    qtype = "A",
                    qclass = "IN",
                    qname = j+ "." + root_domain)
                pkt = ether/ip/udp/dns

                res = srp1(pkt, verbose = 0)
                try:
                    # if res[DNS].qd.rname:
                    if res[DNS].an.rdata != None:
                        issit_domain.append([ j+ "." + root_domain , res[DNS].an.rdata])
                        print("%-20s%-20s"%(j+ "." + root_domain , res[DNS].an.rdata))
                    
                    # res[domain]
                except:
                    pass

        return issit_domain





if __name__ == "__main__":

    a = Finddns()
    a.reqdns("iqsp.com")
            
