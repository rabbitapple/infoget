from scapy.all import *
import os
import traceback
import oui

class NDS:
    """
    ARP 패킷 스니핑을 통하여 현제 네트워크에 존재하는 Host를 탐색하는 class
    """
    def __init__(self) -> None:
        self.addr = []
        self.cnt = 1


    def chackhost(self, pkt):
        """
        Host가 이미 탐지되었는지를 확인하는 메서드. 이미 탐지되었을경우 탐지 수를 증가.
        Args:
            pkt(object): scapy 패킷
        Returns:
            bool: 
                - `True`: Host가 새로 탐지된 경우
                - `False`: Host가 이미 탐지되어 탐지 횟수가 증가된 경우
            
        Note:
            self.addr은 MAC 주소와 해당 Host의 탐지 횟수 등을 저장하는 리스트이다.
        """
        for i in range(len(self.addr)):
            if pkt["ARP"].hwsrc in self.addr[i][1]:
                self.addr[i][4] += 1
                return False
        return True
    
    def clearwindow(self):
        """
        Commend Window를 삭제하는 명령어를 운영체제에 맞춰서 입력하는 메서드

        Note:
            `window`: cls
            `Linux`: clear
        """
        if os.name == 'nt':  # Windows인 경우
            os.system('cls')
            pass
        else:  # Linux 및 macOS인 경우
            os.system('clear')
            pass
            
    def scanstart(self, pkt):
        """
        ARP 패킷을 Sniff하여 현제 네트워크의 Host및 해당 Host의 Oui를 이용하여 IP, Mac, 장치명, 제조사 등을 획득, 출력하는 메서드
        Args:
            object: scapy 패킷 Object        
        """
        # try:
        if "ARP" in pkt:
            print(pkt)
            # HOST 존재여부 확인
            host_not_isset = self.chackhost(pkt)

            if host_not_isset:
                # 탐지된 HOST 추가
                ouiinfo = oui.ouifind(pkt["ARP"].hwsrc)
                self.addr.append([pkt["ARP"].psrc, pkt["ARP"].hwsrc, ouiinfo[0], ouiinfo[1], 1])

            # 탐지된 HOST 정렬
            self.addr.sort(key=lambda x: [int(y) for y in x[0].split('.')])

            # 화면 초기화
            self.clearwindow()
                
            # 탐지된 HOST 출력
            print("%-15s%-25s%-15s%-35s%-15s"%("IP", "MAC","Hardware", "Manufactur" , "Count"))

            for j in self.addr:
                # 탐지된 HOST OUI검색
                print("%-15s%-25s%-15s%-35s%-15s"%(j[0],j[1], j[2], j[3], j[4]))
                                   
        # except :
        #     pass


if __name__ == "__main__":
    netdis = NDS()
    sniff(prn = netdis.scanstart)