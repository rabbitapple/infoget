import requests

class Finddir:
    def __init__(self):
        with open("./dir_db", "r", encoding="UTF-8") as dir_db:
            dir_data = dir_db.read()
        self.dir_li = dir_data.strip().splitlines()
    def reqdir(self, url):
        response = requests.get(url)

        if response.status_code in [200, 403]:
            
            

            print(response.status_code)


if __name__ == "__main__":
    a = Finddir()
    b = a.reqdir("http://172.16.20.7")
    