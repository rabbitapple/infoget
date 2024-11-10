import host
import tkinter


class Application(tkinter.Tk):
    def __init__(self):
        super().__init__()
        self.title("IQSP")
        self.geometry("600x400")

        self.frames = []
        self.current_page = 0
        self.buttons_per_page = 5  # 페이지당 버튼 수
        self.create_widgets()

    def create_widgets(self):
        self.ip_label = tkinter.Label(self, text="IP 범위:")
        self.ip_label.pack(pady=10)

        self.ip_entry = tkinter.Entry(self, width=50)
        self.ip_entry.pack(pady=10)

        self.run_button = tkinter.Button(self, text="실행", command=self.host_find)
        self.run_button.pack(pady=10)

        self.page_frame = tkinter.Frame(self)
        self.page_frame.pack(pady=10)

    def host_find(self):
        ip = self.ip_entry.get()
        g_ip, g_mac = host.netdiscover(ip)

        # 기존 프레임을 지웁니다.
        for frame in self.frames:
            frame.destroy()
        self.frames.clear()

        # 버튼을 페이지로 나누기
        num_buttons = len(g_ip)
        total_pages = (num_buttons + self.buttons_per_page - 1) // self.buttons_per_page  # 총 페이지 수

        for page in range(total_pages):
            frame = tkinter.Frame(self)
            self.frames.append(frame)

            # 각 페이지에 버튼 추가
            start_index = page * self.buttons_per_page
            end_index = min(start_index + self.buttons_per_page, num_buttons)
    
            for i in range(start_index, end_index):
                txt = "[%s] [%s]" % (g_ip[i], g_mac[i])
                ip_btn = tkinter.Button(frame, text=txt, command=lambda ip=g_ip[i]: print(ip))
                ip_btn.pack(pady=5)

            frame.pack(fill="both", expand=True)

        self.show_page(0)  # 처음 페이지 표시

        # 페이지 전환 버튼 추가
        self.page_buttons = []
        for page in range(total_pages):
            page_button = tkinter.Button(self.page_frame, text=f"{page + 1}",
                                         command=lambda p=page: self.show_page(p))
            page_button.pack(side="left", padx=5)
            self.page_buttons.append(page_button)

    def show_page(self, page):
        """지정된 페이지를 보여줍니다."""
        for index, frame in enumerate(self.frames):
            if index == page:
                frame.pack(fill="both", expand=True)
            else:
                frame.pack_forget()


if __name__ == "__main__":
    app = Application()
    app.mainloop()
