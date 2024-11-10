# with open("./oui_db.txt", "r", encoding="utf-8") as txt:
#     a = txt.read()

# b = a.replace('\t', ',')


# with open("./oui_db", "w", encoding="utf-8") as db:
#     db.write(b)


from scapy.all import *

def a(pkt):
    if "ARP" in pkt:
        print(pkt["ARP"].hwsrc)

sniff(prn = a)
