from module.all import *
from scapy.all import *


def main():
    run = True
    while run:
        print("실행시킬 모듈의 번호를 입력해주세요.")
        print("%-30s%-30s%-30s\n%-30s%-30s%-30s"%("1. Host Finding","2. Ping Scanning", "3. Half Scanning", "4. Version Scanning", "5. SubDNS Enummulation", "6. Directory Enummulation"))
        use_module = input()
        if use_module == "exit":
            run = False
        elif use_module == "1":
            module_cls = NDS()
            sniff(prn = module_cls.scanstart)
        elif use_module == "2":
            module_cls = Pingscan()
            module_args = input("IP 대역을 입력해주세요.(EX: 172.16.20.10/16)\n")
            module_cls.scanstart(module_args)
        elif use_module == "3":
            module_cls = Halfscan()
            module_args = input("스캔할 IP를 입력해주세요.(EX: 172.16.20.10)\n")
            module_cls.scanstart(module_args)
        elif use_module == "4":
            module_cls = Verscan()
            module_args = input("스캔할 IP를 입력해주세요.(EX: 172.16.20.10)\n")
            module_cls.scanstart(module_args)
        elif use_module == "5":
            module_cls = Finddns()
            module_args = input("Root Domain을 입력해주세요.(EX: iqsp.com)\n")
            module_cls.reqdns(module_args)
        elif use_module == "6":
            module_cls = Finddir()
            module_args = input("Domain Address를 입력해주세요.(EX: http://www.iqsp.com)\n")
            module_cls.reqdir(module_args)
        else:
            print("올바른 값을 입력해주세요.\n")
        print("\n")


if __name__ == "__main__":
    main()