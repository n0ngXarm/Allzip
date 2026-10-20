# 📦 Allzip

<p align="center">
  <b>เครื่องมือบีบอัดไฟล์และโฟลเดอร์เป็น ZIP ความเร็วสูงในคลิกเดียวสำหรับ Linux (GNOME Nautilus)</b><br>
  <i>Ultra-fast 1-click ZIP compressor for files and folders natively integrated into Linux desktop.</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/License-MIT-blue.svg" alt="License: MIT">
  <img src="https://img.shields.io/badge/Python-3.8+-yellow.svg" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/Platform-Linux%20%2F%20GNOME-orange.svg" alt="Platform: Linux">
  <a href="https://ko-fi.com/n0ngXarm"><img src="https://img.shields.io/badge/Ko--fi-F16061?style=flat&logo=ko-fi&logoColor=white" alt="Ko-fi"></a>
  <a href="https://buymeacoffee.com/n0ngXarm"><img src="https://img.shields.io/badge/Buy_Me_A_Coffee-FFDD00?style=flat&logo=buy-me-a-coffee&logoColor=black" alt="Buy Me A Coffee"></a>
</p>

---

[ภาษาไทย](#ภาษาไทย) | [English](#english)

---

<a name="ภาษาไทย"></a>
## 🇹🇭 ภาษาไทย

**Allzip** เป็นเครื่องมือสำหรับบีบอัดไฟล์และโฟลเดอร์เป็นไฟล์ `.zip` อย่างรวดเร็ว ออกแบบมาให้ทำงานร่วมกับระบบปฏิบัติการ Linux ได้อย่างราบรื่น ไม่ว่าจะเป็นการคลิกขวาในตัวจัดการไฟล์ (Nautilus), การเปิดผ่านเมนูแอปพลิเคชัน, หรือการใช้งานผ่าน Command Line

### 🌟 คุณสมบัติเด่น
* **🖱️ 1-Click Compression**: คลิกขวาที่ไฟล์หรือโฟลเดอร์ใน Nautilus แล้วสั่งบีบอัดได้ทันที
* **🛡️ ป้องกันไฟล์ซ้ำอัจฉริยะ**: หากมีไฟล์ ZIP ชื่อเดิมอยู่แล้ว ระบบจะแสดงหน้าต่างถามว่าต้องการ *"เขียนทับ"*, *"สร้างชื่อใหม่ (เช่น Folder (1).zip)"* หรือ *"ยกเลิก"*
* **🇹🇭 รองรับชื่อไฟล์ภาษาไทย 100%**: ปลอดภัยกับชื่อโฟลเดอร์และไฟล์ภาษาไทย รวมถึงอักขระพิเศษ
* **📊 แสดง Progress Bar อัตโนมัติ**: เมื่อบีบอัดโฟลเดอร์ขนาดใหญ่ (>25 MB หรือ >50 ไฟล์) จะมีหน้าต่างความคืบหน้าแจ้งเตือน ไม่ต้องกลัวว่าโปรแกรมจะค้าง
* **🔔 แจ้งเตือน Desktop Notification**: เมื่อบีบอัดสำเร็จ จะมี Notification บอกขนาดไฟล์และตำแหน่งที่บันทึก
* **⚡ ความเร็วสูงสุด**: ใช้คำสั่ง `zip` ของระบบเป็นหลัก และมีตัวสำรอง Python `zipfile` ภายในตัว

---

### 🚀 วิธีติดตั้ง (Quick Install)

เปิด Terminal แล้วคัดลอกคำสั่งไปวาง:

```bash
git clone https://github.com/n0ngXarm/Allzip.git
cd Allzip
./install.sh
```

---

### 🖱️ วิธีใช้งาน

1. **ผ่านเมนูคลิกขวา (Nautilus):**
   * เลือกไฟล์หรือโฟลเดอร์ $\rightarrow$ คลิกขวา $\rightarrow$ **Scripts** $\rightarrow$ **บีบอัดเป็น ZIP** (หรือ **Compress to ZIP**)
2. **ผ่าน Application Launcher:**
   * เปิดเมนูแอปพลิเคชันในเครื่อง ค้นหา **"Allzip"** แล้วคลิกเปิดเพื่อเลือกไฟล์
3. **ผ่าน Terminal (CLI):**
   ```bash
   zip-folder /path/to/my-folder
   ```

---

<a name="english"></a>
## 🇬🇧 English

**Allzip** is a lightweight, high-performance 1-click ZIP compressor designed for Linux GNOME Nautilus desktop environments.

### 🌟 Features
* **1-Click Context Menu**: Right-click any file or folder to compress immediately.
* **Smart Collision Handling**: Prompts with Overwrite / New Name / Cancel if the target ZIP already exists.
* **Unicode & UTF-8 Safe**: Full support for international characters and empty folders.
* **Progress Indicator**: Automatic progress dialog for larger archives.
* **Desktop Notifications**: Instant notification upon completion displaying final archive size and path.

### 🚀 Installation
```bash
git clone https://github.com/n0ngXarm/Allzip.git
cd Allzip
./install.sh
```

---

## ☕ สนับสนุนผู้พัฒนา / Support & Donation
โปรเจกต์นี้เปิดให้ทุกคนใช้งานได้ **ฟรี 100% (Open Source)** ภายใต้สัญญาอนุญาต MIT  
หากเครื่องมือนี้ช่วยให้คุณบีบอัดไฟล์ได้สะดวกรวดเร็วขึ้น สามารถร่วมเลี้ยงกาแฟสนับสนุนผู้พัฒนาได้ผ่านช่องทางด้านล่างนี้ครับ:

<p align="left">
  <a href="https://ko-fi.com/n0ngXarm">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="ko-fi" height="36">
  </a>
  &nbsp;&nbsp;
  <a href="https://buymeacoffee.com/n0ngXarm">
    <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&emoji=☕&slug=n0ngXarm&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" height="36" alt="Buy Me A Coffee" />
  </a>
</p>

* **Ko-fi:** [ko-fi.com/n0ngXarm](https://ko-fi.com/n0ngXarm) *(0% fee - แนะนำ)*
* **Buy Me a Coffee:** [buymeacoffee.com/n0ngXarm](https://buymeacoffee.com/n0ngXarm)
* **GitHub Sponsor:** กดปุ่ม **Sponsor** 💖 ที่ด้านบนของ Repository ได้เลยครับ

---

## 📄 License
This project is licensed under the [MIT License](LICENSE).
