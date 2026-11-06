"""Windows desktop entry; work runs away from the Tk event loop."""
import queue
import threading
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from pathlib import Path
from .core import compress_item


def main(paths=(), smoke=False):
    root=tk.Tk();root.title('Allzip');root.geometry('660x420')
    try: root.iconbitmap(str(Path(__file__).resolve().parents[1]/'assets/app.ico'))
    except tk.TclError: pass
    items=list(paths);events=queue.Queue();busy=False
    ttk.Label(root,text='เลือกไฟล์หรือโฟลเดอร์เพื่อสร้าง ZIP ข้างต้นฉบับ').pack(pady=12)
    listing=tk.Listbox(root,selectmode='extended');listing.pack(fill='both',expand=True,padx=12)
    status=tk.StringVar(value='ไฟล์ชื่อซ้ำจะบันทึกเป็นชื่อใหม่');ttk.Label(root,textvariable=status,wraplength=620).pack(pady=8)
    buttons=ttk.Frame(root);buttons.pack(pady=10)
    def refresh():
        listing.delete(0,'end')
        for item in items:listing.insert('end',item)
    def add(folder=False):
        selected=[filedialog.askdirectory(parent=root)] if folder else filedialog.askopenfilenames(parent=root)
        for item in selected:
            if item and item not in items: items.append(item)
        refresh()
    def work(targets):
        try:
            results=[compress_item(item,auto_rename=True) for item in targets]
            events.put(results)
        except Exception as error: events.put([(False,str(error))])
    def start():
        nonlocal busy
        if not items or busy:return
        busy=True;status.set('กำลังสร้าง ZIP กรุณารอ...')
        for button in controls:button.state(['disabled'])
        threading.Thread(target=work,args=(list(items),),daemon=True).start()
    controls=[]
    for text,command in [('เพิ่มไฟล์',lambda:add()),('เพิ่มโฟลเดอร์',lambda:add(True)),('ล้างรายการ',lambda:(items.clear(),refresh())),('สร้าง ZIP',start)]:
        button=ttk.Button(buttons,text=text,command=command);button.pack(side='left',padx=4);controls.append(button)
    def poll():
        nonlocal busy
        try:results=events.get_nowait()
        except queue.Empty:pass
        else:
            busy=False
            for button in controls:button.state(['!disabled'])
            errors=[str(info) for ok,info in results if not ok]
            status.set('สร้าง ZIP สำเร็จ '+str(sum(ok for ok,_ in results))+' รายการ')
            if errors:messagebox.showerror('Allzip','\n'.join(errors),parent=root)
        root.after(100,poll)
    def close():
        if busy:messagebox.showinfo('Allzip','กรุณารอให้สร้าง ZIP เสร็จก่อนปิด',parent=root)
        else:root.destroy()
    root.protocol('WM_DELETE_WINDOW',close);refresh();poll()
    if smoke:root.after(300,root.destroy)
    root.mainloop()
