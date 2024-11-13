import requests
from requests.adapters import HTTPAdapter, Retry
import os
import inspect


class Finddir:
    def __init__(self):    
        self.path = os.path.dirname(os.path.abspath(__file__))
        print(self.path)  
        with open(self.path + "/../db_data/dir_db", "r", encoding="UTF-8") as dir_db:
            dir_data = dir_db.read()
        self.dir_li = dir_data.strip().splitlines()
        self.cnt = 1

    def reqdir(self, url):
        session = requests.Session()

        # 재시도 설정
        retries =Retry(
            total=0
        )

        # HTTPAdapter를 통해 세션에 재시도 설정 추가
        session.mount('http://', HTTPAdapter(max_retries=retries))

        response = session.get(url)
        issit_url = []
        if response.status_code in [200, 403]:  
            issit_url.append([response.url])
            cnt = 1         
            issit_url.append([])
            for i in self.dir_li:
                response = session.get(url + "/" + i)
                if response.status_code in [200, 403]:
                    try:
                        issit_url[cnt+1]
                    except:
                        issit_url.append([])
                    print(response.url)
                    issit_url[1].append(response.url)
            while len(issit_url) > cnt:
                for j in issit_url[cnt]:
                    if j[len(j) - 1] == "/":
                        try:
                            issit_url[cnt+1]
                        except:
                            issit_url.append([])
                                                
                        for k in self.dir_li:
                            response = session.get(j + k)
                            if response.status_code in [200, 403]:
                                print(response.url)
                                issit_url[cnt+1].append(response.url)
                cnt += 1

    def scanstart(self, url):
        session = requests.Session()

        # 재시도 설정
        retries =Retry(
            total=0
        )

        # HTTPAdapter를 통해 세션에 재시도 설정 추가
        session.mount('http://', HTTPAdapter(max_retries=retries))
        
        self.issit_url = []
        if self.cnt == 1 :
            self.cnt += 1
            response = session.get(url)
            if response.status_code in [200, 403]:
                print(response.url)
                self.issit_url.append(response.url)
                self.scanstart(response.url)
            else:
                print("%s로의 접속이 불가능 합니다."%url)
        else:
            for i in self.dir_li:
                response = session.get(url + i)
                if response.status_code in [200, 403]:
                    print(" " * (self.cnt - 1), end = "")
                    print("ㄴ" + response.url)
                    self.issit_url.append(response.url)

                    if response.url[len(response.url)-1] == "/":
                        self.cnt += 1
                        self.scanstart(response.url)
                        self.cnt -= 1
        if self.cnt == 1:
            return self.issit_url

                    

if __name__ == "__main__":
    a = Finddir()
    b = a.scanstart("http://nk.iqsp.com")
    