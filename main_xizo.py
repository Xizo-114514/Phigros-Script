import configparser
import ctypes
import inspect
import json
import os
import subprocess
from threading import Thread
from tkinter import ttk, messagebox, Tk, X, IntVar, StringVar
from typing import Iterator

from rich.console import Console

from algo.algo_base import TouchEvent
from algo.algo_base import load_from_json, export_to_json
from chart import Chart
from control import DeviceController


def agreement():
    if os.path.exists('./cache'):
        return
    if not messagebox.askyesno(title='用户协定', message='您因使用或修改本程序发生的一切后果将由您自己承担而与程序原作者无关。\n' '您是否同意？'):
        exit(1)

class App(ttk.Frame):

    cache: configparser.ConfigParser | None
    serials: list[str]
    running: bool
    start_time: float
    controller: DeviceController | None
    player_worker_thread: Thread | None
    console: Console

    def __init__(self, master: Tk):
        super().__init__(master)
        self.console = Console()
        self.controller = None
        self.player_worker_thread = None
        self.cache_path = None
        self.running = True
        self.start_time = 0.0
        self.cache = None
        self.pack()

        ttk.Separator(orient='horizontal').pack(fill=X)

        frm = ttk.Frame()
        frm.pack()

        ttk.Label(frm, text='选择设备: ').grid(column=0, row=0)
        self.serial = StringVar()
        self.serial_select = ttk.Combobox(frm, width=18, state='readonly', values=[], textvariable=self.serial)
        self.serial_select.grid(column=1, row=0)
        self.serial_select.bind('<<ComboboxSelected>>', self.adb_serial_selected)
        self.serial_refresh_btn = ttk.Button(frm, width=14, text='刷新', command=self.detect_adb_devices)
        self.serial_refresh_btn.grid(column=2, row=0)

        ttk.Separator(orient='horizontal').pack(fill=X)

        frm = ttk.Frame()
        frm.pack()

        ttk.Label(frm, text='手动连接: 127.0.0.1:').grid(column=0, row=0)
        self.port_bar = ttk.Entry(frm, width=8)
        self.port_bar.grid(column=1, row=0)
        self.adb_connect_btn = ttk.Button(frm, width=7, text='连接', command=self.adb_connect_devices)
        self.adb_connect_btn.grid(column=2, row=0)
        self.adb_rest_btn = ttk.Button(frm, width=10, text='重置adb', command=self.adb_rest)
        self.adb_rest_btn.grid(column=3, row=0)

        ttk.Separator(orient='horizontal').pack(fill=X)

        self.song_select = IntVar()
        self.song_select.set(0)

        frm = ttk.Frame()
        frm.pack()

        ttk.Label(frm, text='曲目选择：').grid(column=0, row=0)

        self.song_select1 = ttk.Radiobutton(
            frm, text='Better Graphic Animation       |刷Data最快| ', variable=self.song_select, value=0
        )
        self.song_select2 = ttk.Radiobutton(
            frm, text='Engine x Start!! (melody mix)  |更易解锁| ', variable=self.song_select, value=1
        )
        self.song_select1.grid(column=0, row=1, sticky='W')
        self.song_select2.grid(column=0, row=2, sticky='W')

        ttk.Separator(orient='horizontal').pack(fill=X)

        self.xizobtn = ttk.Button(text='准备自动打歌', command=self.xizorun)
        self.xizobtn.pack(anchor='center', expand=1)

        ttk.Separator(orient='horizontal').pack(fill=X)

        self.info_label = ttk.Label()
        self.info_label.pack()

        ttk.Separator(orient='horizontal').pack(fill=X)

        self.round_log_label = ttk.Label()
        self.round_log_label.pack()

        ttk.Separator(orient='horizontal').pack(fill=X)

        self.log_label = ttk.Label()
        self.log_label.pack()

        ttk.Separator(orient='horizontal').pack(fill=X)

        self.log_label['text'] = '| 已运行：---- | ---- 次 | 预估Data：---- MB |'
        self.round_log_label['text'] = '| 本次用时：---- s | 平均速度：---- KB/s |'
        self.update()

        agreement()

    def adb_connect_devices(self):
        subprocess.run(['adb', 'connect', '127.0.0.1:'+self.port_bar.get()])
        return self

    def adb_rest(self):
        subprocess.run(['adb', 'kill-server'])
        subprocess.run(['adb', 'start-server'])
        return self

    def detect_adb_devices(self):
        self.serial_select['values'] = DeviceController.get_devices()
        return self

    def adb_serial_selected(self, event):
        serial = event.widget.get()
        print(serial)

    def xizorun(self):
        try:
            import time

            self.times = 0
            self.lasttime = 0
            self.mainstarttime = time.time()

            def logall():
                while True:
                    nowtime = time.time()
                    runtimes = nowtime - self.mainstarttime
                    m, s = divmod(runtimes, 60)
                    h, m = divmod(m, 60)
                    rantime = "%02d:%02d:%02d" % (h, m, s)
                    if self.song_select.get() == 0:
                        datas = str(self.times * 1.25)
                    else:
                        datas = str(self.times)
                    self.log_label['text'] = '| 已运行：'+rantime+' | '+str(self.times)+' 次 | 预估Data：'+datas+' MB |'
                    self.update()
                    time.sleep(1)

            self.logall = Thread(target=logall, daemon=True)
            self.logall.start()

            if self.controller is None:
                self.controller = DeviceController()
                print('[client]', '正在确认设备尺寸，请稍候')
                time.sleep(1)
                print('[client]', f'设备尺寸: {self.controller.device_width}x{self.controller.device_height}')

            device_width = self.controller.device_width
            device_height = self.controller.device_height

            height = device_height
            width = height * 16 // 9
            xoffset = (device_width - width) >> 1
            yoffset = (device_height - height) >> 1
            scale_factor = height / 720

            self.info_label['text'] = '准备就绪\nTip: 请开一首曲子，再暂停，然后再点击开始\n或者在歌曲结算界面点击开始'
            self.xizobtn['text'] = '开始'
            self.round_log_label['text'] = '| 本次用时：---- s | 平均速度：---- KB/s |'
            self.update()

            self.running = True

            def go_now():
                def stop():
                    self.running = False

                self.running = True

                # BetterGraphicAnimation.ルゼ.0
                # EnginexStartmelodymix.CrossingSound.0
                if self.song_select.get() == 0:
                    chart_path = f'./Assets/Tracks/BetterGraphicAnimation.ルゼ.0/Chart_IN.json'
                else:
                    chart_path = f'./Assets/Tracks/EnginexStartmelodymix.CrossingSound.0/Chart_IN.json'

                ans: dict
                ans_file = chart_path + '.ans.json'
                try:
                    ans = load_from_json(open(ans_file))
                except:
                    import algo.algo1
                    chart = Chart.from_dict(json.load(open(chart_path)))
                    ans = algo.algo1.solve(chart, self.console)
                    export_to_json(ans, open(ans_file, 'w'))
                    ans = load_from_json(open(ans_file))

                adapted_ans = [
                    (timestamp, [ev.map_to(xoffset, yoffset, scale_factor, scale_factor) for ev in ans[timestamp]])
                    for timestamp in sorted(ans.keys())
                ]

                ans_iter = iter(adapted_ans)

                self.player_worker_thread = Thread(target=player_worker, args=(ans_iter,), daemon=True)

                def gogogo():
                    def stop():
                        def stop_thread(t):
                            def _async_raise(tid, exctype):
                                """raises the exception, performs cleanup if needed"""
                                tid = ctypes.c_long(tid)
                                if not inspect.isclass(exctype):
                                    exctype = type(exctype)
                                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
                                if res == 0:
                                    raise ValueError("invalid thread id")
                                elif res != 1:
                                    # """if it returns a number greater than one, you're in trouble,
                                    # and you should call it again with exc=NULL to revert the effect"""
                                    ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                                    raise SystemError("PyThreadState_SetAsyncExc failed")
                            _async_raise(t.ident, SystemExit)
                        stop_thread(self.go_thread)
                        self.xizobtn['command'] = go_now
                        self.xizobtn['text'] = '开始'
                        self.info_label['text'] = '准备就绪\nTip: 请开一首曲子，再暂停，然后再点击开始\n或者在歌曲结算界面点击开始'
                        self.running = False

                    self.xizobtn['command'] = stop
                    self.info_label['text'] = '正在等待第一个Note出现'
                    self.update()

                    self.controller.tap(30, 30)
                    time.sleep(0.83)
                    self.controller.tap(device_width >> 1, device_height >> 1) # (480, 268)

                    if self.song_select.get() == 0:
                        time.sleep(13.16) # Better Graphic Animation
                    else:
                        time.sleep(3.3) # Engine x Start!!

                    self.player_worker_thread.start()

                    #print("Started！")

                    def stop():
                        self.running = False
                    self.xizobtn['command'] = stop
                    self.info_label['text'] = '正在打歌中......'
                    self.update()

                self.go_thread = Thread(target=gogogo, daemon=True)
                self.go_thread.start()
                self.xizobtn['command'] = stop
                self.xizobtn['text'] = '停止'

                self.update()

            def player_worker(ans_iter: Iterator[tuple[int, list[TouchEvent]]]) -> None:
                """打歌线程"""
                if self.controller:
                    timestamp, events = next(ans_iter)
                    self.start_time = time.time() - timestamp / 1000 - 0.01  # 0.01 for the delay time

                    try:
                        while self.running:
                            now = round((time.time() - self.start_time) * 1000)
                            if now >= timestamp:
                                for event in events:
                                    self.controller.touch(*event.pos, event.action, pointer_id=event.pointer)
                                timestamp, events = next(ans_iter)
                    except StopIteration:
                        pass
                else:
                    self.console.print('self.controller == None')

                if self.running == True:
                    self.info_label['text'] = '即将自动开始循环'
                    self.update()

                    def rego():
                        if self.song_select.get() == 0:
                            time.sleep(7.5)  # Better Graphic Animation
                        else:
                            time.sleep(6)  # Engine x Start!!
                        go_now()

                    self.re_go_thread = Thread(target=rego, daemon=True)
                    self.re_go_thread.start()

                    def stop():
                        def stop_thread(t):
                            def _async_raise(tid, exctype):
                                """raises the exception, performs cleanup if needed"""
                                tid = ctypes.c_long(tid)
                                if not inspect.isclass(exctype):
                                    exctype = type(exctype)
                                res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
                                if res == 0:
                                    raise ValueError("invalid thread id")
                                elif res != 1:
                                    # """if it returns a number greater than one, you're in trouble,
                                    # and you should call it again with exc=NULL to revert the effect"""
                                    ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
                                    raise SystemError("PyThreadState_SetAsyncExc failed")
                            _async_raise(t.ident, SystemExit)
                        stop_thread(self.re_go_thread)
                        self.xizobtn['command'] = go_now
                        self.xizobtn['text'] = '开始'
                        self.info_label['text'] = '准备就绪\nTip: 请开一首曲子，再暂停，然后再点击开始\n或者在歌曲结算界面点击开始'
                        self.running = False

                    self.xizobtn['command'] = stop
                    self.update()
                    endtime = time.time()
                    self.times = self.times + 1

                    if self.lasttime != 0:
                        parttime = endtime - self.lasttime
                        if self.song_select.get() == 0:
                            datakbps = str('%.2f' % (1280 / parttime))
                        else:
                            datakbps = str('%.2f' % (1024 / parttime))
                        usedtime = str('%.1f' % parttime)
                        self.lasttime = endtime
                        self.round_log_label['text'] = '| 本次用时：'+usedtime+' s | 平均速度：'+datakbps+' KB/s |'
                        self.update()
                    else:
                        self.lasttime = endtime
                        self.round_log_label['text'] = '| 本次用时：---- s | 平均速度：---- KB/s |'
                        self.update()

                else:
                    self.xizobtn['command'] = go_now
                    self.xizobtn['text'] = '开始'
                    self.info_label['text'] = '准备就绪\nTip: 请开一首曲子，再暂停，然后再点击开始\n或者在歌曲结算界面点击开始'
                    self.update()

            self.xizobtn['command'] = go_now
            self.update()
        except Exception:
            self.console.print_exception(show_locals=True)

if __name__ == '__main__':
    tk = Tk()
    tk.title('Phisap - Revision by Xizo')
    tk.iconbitmap('icon.ico')
    App(tk).detect_adb_devices().mainloop()
