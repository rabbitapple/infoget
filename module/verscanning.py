from scapy.all import *
import os
from halfscanning import Halfscan
import traceback
import socket
import random




class Verscan(Halfscan):
    """
    버전 스캐닝에 필요한 메서드들이 포함된 클래스
    """
    def tcpack(self,pkt:object) -> str:
        """
        TCP Syn/Ack 패킷을 받아 Ack 패킷을 전송하며 Ack의 응답을 받을 경우 
        Args:
            pkt(object): Syn/Ack 패킷을 Scapy 객체 형식으로 전달받는 요소.
        Returns:
            str: TCP Ack의 respons로 받은 패킷의 응용프로토콜 Layer(Raw)의 Data(load)를 문자열로 인코딩하여 반환
            None: TCP Ack의 response가 없을 경우 반환
        """
        try: 
            rawdata = None  
            ether = Ether(dst = pkt[Ether].src, src = pkt[Ether].dst)
            ip = IP(dst = pkt[IP].src, src = pkt[IP].dst)
            # tcp = TCP(dport = pkt[TCP].dport, sport = pkt[TCP].sport, flags = "A", seq = pkt[TCP].ack , ack = pkt[TCP].seq+1)
            tcp = TCP(dport = pkt[TCP].sport, sport = pkt[TCP].dport, flags = "A", seq = pkt.ack , ack = pkt.seq+1)
        
            res = srp1(ether/ip/tcp,verbose = 0, timeout = 1)

            if res != None:
                loaddata = res[3].load
                try:
                    # UTF-8 디코딩
                    rawdata = loaddata.decode('utf-8', errors='ignore').strip()
                except UnicodeDecodeError:
                    # ASCII로 디코딩 
                    rawdata = loaddata.decode('ascii', errors='ignore').strip()


            # info = str(res[Raw].load)
            return rawdata
        except:
            print(traceback.format_exc())
            return
        
    def sendrst(self, dmac:str, dip:str, dport:str) -> None:

        """
        TCP Rst 패킷을 전송하는 메서드. Syn/Ack를 계속해서 전송하는 상태를 중지하기 위해서 사용. 현제 사용안함.
        Args:
            dmac(str): Destination Mac Addres. (형식: xx:xx:xx:xx:xx:xx)
            dip(str): Destination IP Addres. (형식: xxx.xxx.xxx.xxx)
            dport(str): Destination Port. 
        """
        #R패킷
        ether = Ether(dst = dmac)
        ip = IP(dst = dip)

        p_list = dport.split(",")
        tcp = TCP(dport = int(p_list[0]), sport = 50000 + int(p_list[0]), flags = "R")
        srp1(ether/ip/tcp,verbose = 0, timeout = 0) 

    def osdeco(func):
        """
        Os가 자동으로 보내지 않은 Syn 패킷에 대하여 Rst 패킷을 전송하는것을 iptables를 통해서 차단,
        tput을 이용하여 terminal의 화면을 저장 후 함수를 실행 한 뒤 iptable rule 및 화면 복구를 하는 데코레이터
        """
        def indeco(self, *args, **kwargs):
            # 방화벽 해제
            os.system( "iptables -A OUTPUT -p tcp --tcp-flags RST RST -s " + self.getmyip() + " -j DROP"  )
            # iptables -A OUTPUT -p tcp --tcp-flags RST RST -s 172.16.20.15 -j DROP

            os.system("tput smcup")
            clearcmd = "clear"
            os.system(clearcmd)

            returnlist = func(self, *args, **kwargs)

            os.system( "iptables -D OUTPUT -p tcp --tcp-flags RST RST -s " + self.getmyip() + " -j DROP"  )
            os.system("tput rmcup")                     
            return returnlist
        return indeco
    
      

    @osdeco
    def scanstart(self, dip:str):
        """
        Version Scanning을 하는 메서드. Osdeco를 통해 꾸며준다.
        TCP 3 Way Handshake 과정 후의 Psh/Ack 패킷의 응용 프로토콜 레이어 데이터를 받아와서
        열린 포트 및 열린 포트의 정보를 출력 및 반환한다.
        Args:
            dip(str): Destination IP Address. (형식: xxx.xxx.xxx.xxx)
        Returns:
            list: [[str,str,str]] 형태의 list. 열린 포트의 번호, 열린 포트 정보, 열린 포트 세부정보가 포함된 List. 
        """
        try:

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

            port_list = port_db.strip().splitlines()

            # wellkown포트 TCP 패킷 전송/결과출력

            print("%-5s%-25s"%("Port", "Discription"))

            open_port = []
         
            for i in port_list:
                p_list = i.split(",")
                rport = random.randrange(50000, 65000)
                if str(p_list[0]) == "21":
                    rport = 20

                tcp = TCP(dport = int(p_list[0]), sport = rport)

                
                res = srp1(ether/ip/tcp, verbose = 0)
                # (ether/ip/tcp).show()
                # res.show()
                # break


                if res[TCP].flags in ["SA", "A"]:
                    #재전송
                    
                    if rport != 20:
                        res1 = srp1(ether/ip/tcp, verbose = 0)
                        #ACK
                        adddis = self.tcpack(res1)   
                    if rport == 20:
                        print(1)
                        #ACK
                        adddis = self.tcpack(res)          
                    #출력/저장    
                    open_port.append([p_list[0], p_list[1],adddis])
                    print("%-5s%-25s"%(p_list[0], p_list[1]))
                    print("%5s%-25s"%(":", adddis))
            input("End")
            return open_port
        except TypeError:
            # os.system("tput rmcup")
            print("TypeError: 호스트가 존재하지 않을 수 있습니다.")

        except:
            # os.system("tput rmcup")
            print(traceback.format_exc())





if __name__ == "__main__":
    scan = Verscan()
    scan.scanstart("172.16.20.15")
    
