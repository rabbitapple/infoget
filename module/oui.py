# oui.py
import os

def oui_data():
    """
    Oui 정보가 포함된 DB의 정보를 가공하여 List형태로 반환하는 함수
    Returns:
        list: [[Mac, 장치명, 제조사]] 형태의 리스트 반환
    """
    ouikey = {}
    with open(os.path.dirname(os.path.abspath(__file__)) + "/../db_data/oui_db", "r", encoding="UTF-8") as db:
        ouidb = db.read()
    ouili = ouidb.strip().splitlines()
    for i in ouili:
        ouiinfo = i.split(",")
        try:
            ouiinfo[1]
        except:
            ouiinfo.append("")
            ouiinfo.append("")

        try:
            ouiinfo[2]
        except:
            ouiinfo.append("")

        ouikey[ouiinfo[0]] = [ouiinfo[1],ouiinfo[2]]
    return ouikey

def ouifind(mac):
    """
    특정 Mac 주소의 Oui를 통해 장치명, 제조사를 반환
    Args:
        mac(str): Oui정보를 찾을 Mac주소 (형식 : xx:xx:xx:xx:xx:xx)
    Returns:
        list: [장치명, 제조사]형태의 List 반환
    """
    try:
        oui = mac[0:8].upper()
        ouikey = oui_data()
        ouiinfo = ouikey[oui]
        return ouiinfo
    except:
        ouiinfo = ["",""]
        return ouiinfo

if __name__ == "__main__":
    a = ouifind("00:0c:29:59:2c:c1")
    print(a)
