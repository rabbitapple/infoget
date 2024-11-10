import host
import tkinter


def host_find():
    ip = ip_entry.get()
    g_ip, g_mac = host.netdiscover(ip)
    for i in range(len(g_ip)):
        txt = "[%s] [%s]"%(g_ip[i], g_mac[i])
        ip_btn = tkinter.Button(window, text=txt, command=print)
        ip_btn.pack(pady=10)



if __name__ == "__main__":
        

    window = tkinter.Tk()
    window.title("IQSP")
    window.geometry("600x400")

    ip_label = tkinter.Label(window, text="IP 범위:")
    ip_label.pack(pady=10)

    ip_entry = tkinter.Entry(window, width=50)
    ip_entry.pack(pady=10)

    run_button = tkinter.Button(window, text="실행", command=host_find)
    run_button.pack(pady=10)

    window.mainloop()