from scapy.all import *
from halfscanning import Halfscan



class Pingscan(Halfscan):
    """
    Pingscanning과 관련된 메서드들이 포함된 Class. halfscanning.Halfscan으로부터 상속받음.
    """
    def binip(self, ip):
        """
        Decimal 형식의 IP를 Binary 형식으로 변환하여 반환하는 메서드.
        Args:
            ip(str): Decimal 형식의 IP (형식 : xxx.xxx.xxx.xxx)
        Returns:
            str: Binary 형식의 IP (형식: xxxxxxxx.xxxxxxxx.xxxxxxxx.xxxxxxxx)
        """
        ipli = ip.split(".")
        binip = ["","","",""]
        for i in range(len(ipli)):
            int_ipli = int(ipli[i])
            for j in range(8):
                if (int_ipli-(2**(7-j))) >= 0:
                    binip[i] = binip[i] + "1"
                    int_ipli = int_ipli - (2**(7-j)) 
                else:
                    binip[i] = binip[i] + "0"
                
        return_bin_ip = ".".join(binip)
        return return_bin_ip
    
    def get_ni(self, bin_ip, bin_subnet):
        """
        Binary 형식의 IP와 Subnetmask를 통해 Network ID를 획득하여 반환하는 메서드
        And 연산을 통해 Decimal 형식의 NI를 획득한다.
        Args:
            bin_ip(str): Binary 형식의 IP (형식: xxxxxxxx.xxxxxxxx.xxxxxxxx.xxxxxxxx)
            bin_subnet(str): Binary 형식의 Subnetmask (형식: xxxxxxxx.xxxxxxxx.xxxxxxxx.xxxxxxxx)
        Returns:
            str: Deciaml 형식의 Network ID (형식: xxx.xxx.xxx.xxx)
        """
        ip_li = bin_ip.split(".")
        subnet_li = bin_subnet.split(".")

        ni_dic_li = []
        for i in range(4):
            ni_dec = int(ip_li[i],2) &  int(subnet_li[i],2)
            ni_dic_li.append(str(ni_dec))
        ni = ".".join(ni_dic_li)

        return ni
        
                

    def iplist(self, ni, subnet):
        """
        NI 및 Subnetmask를 이용하여 범위내의 IP를 List형식으로 반환
        Args:
            ni(str): Decimal 형태의 NI (형식: xxx.xxx.xxx.xxx)
            subnet(str): Decimal 형태의 Subnetmask (형식: xxx.xxx.xxx.xxx)
        Returns:
            list: NI의 Subnetmask에 포함된 IP List. Decimal 형태의 String 형식 IP (형식: xxx.xxx.xxx.xxx)
        """
        ni_li = ni.split(".")
        subnet_li = subnet.split(".")      
        wildmask = []
        ip_len_li = []
        for i in range(4):
            wildmask.append(255 - int(subnet_li[i]))
            ni_li[i] = int(ni_li[i])
            
            ip_len_li.append([])
            for j in range(wildmask[i]+1):
                ip_len_li[i].append(str(ni_li[i]+j))

        ip_li = []
        for k in ip_len_li[0]:
            for l in ip_len_li[1]:
                for m in ip_len_li[2]:
                    for n in ip_len_li[3]:
                        ip_li.append("%s.%s.%s.%s"%(k,l,m,n))
        
        return ip_li
    
    def prifix_to_subnet(self, prifix):
        """
        Prifix를 Subnetmask 형태로 변환하여 반환하는 메서드
        Args:
            prifix(int): int 포멧의 Prifix
        Returns:
            str: Prifix의 Decimal 형식 Subnetmask. (형식: xxx.xxx.xxx.xxx)
        """

        bin_subnet_li = [] 
        subnet_li = []
        for i in range(4):
            bin_subnet_li.append("")
            for j in range(8):                
                if int(prifix) > 0:
                    bin_subnet_li[i] = bin_subnet_li[i] + "1"
                else:
                    bin_subnet_li[i] = bin_subnet_li[i] + "0"
                prifix -= 1
            subnet_li.append(str(int(bin_subnet_li[i],2)))
        bin_subnet = ".".join(bin_subnet_li)
        subnet = ".".join(subnet_li)
        return (subnet,bin_subnet)
    

    
    def ping(self, dip):
        """
        Scapy를 통해 ICMP패킷을 전송하고, Response패킷의 ICMP 코드값이 0인지 확인하는 메서드
        0일경우 True를, 이외의 코드이거나 Response패킷이 없을경우 0을 반환
        Destination Mac 주소는 FF:FF:FF:FF:FF:FF를 사용.

        Args:
            dip(str): Destination IP Addres (형식: xxx.xxx.xxx.xxx)
        Returns:
            bool:
                - True: Response Packet의 ICMP Coad가 0일경우
                - False:  Response Packet의 ICMP Coad가 0이 아니거나 Response Packet이 없을 경우
        """
        ether = Ether(dst = "ff:ff:ff:ff:ff:ff")
        ip = IP(dst = dip, src = self.my_ip)
        icmp = ICMP()

        req_pkt = ether/ip/icmp


        res = srp1(req_pkt, verbose = 0, timeout = 0.1)

        try:
            if res[ICMP].code == 0:
                return True
            else:
                return False
        except:
            return False



                    
    def scanstart(self, iprange):
        """
        입력한 범위에 대하여 Ping Scanning을 하는 메서드. 
        Args:
            iprange(str): IP/Prifix 형식의 스캔 범위. (형식: xxx.xxx.xxx.xxx/xx)
        Returns:
            list: String 포멧의 Host가 존재하는 IP가 포함된 List
        """
        iprange_li = iprange.split("/")
        ip = iprange_li[0]
        prifix = int(iprange_li[1])
        
        subnet, bin_subnet = self.prifix_to_subnet(prifix)

        bin_ip = self.binip(ip)

        ni = self.get_ni(bin_ip,bin_subnet)

        find_ip_list = self.iplist(ni, subnet)


        findhost_list = []

        print("Host Finding.....")

        for i in find_ip_list:
            run = True
            cnt = 0
            while run and (cnt < 5):
                cnt += 1
                if self.ping(i):
                    run = False
                    findhost_list.append(i)
                    print("%s:\n\tHost is Up"%i)
        return findhost_list



if __name__ == "__main__" :
    a = Pingscan()
    b = a.scanstart("172.16.20.0/24")