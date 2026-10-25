# Allzip

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
## ภาษาไทย

**Allzip** เป็นเครื่องมือสำหรับบีบอัดไฟล์และโฟลเดอร์เป็นไฟล์ `.zip` อย่างรวดเร็ว ออกแบบมาให้ทำงานร่วมกับระบบปฏิบัติการ Linux ได้อย่างราบรื่น ไม่ว่าจะเป็นการคลิกขวาในตัวจัดการไฟล์ (Nautilus), การเปิดผ่านเมนูแอปพลิเคชัน, หรือการใช้งานผ่าน Command Line

### คุณสมบัติเด่น
* **1-Click Compression**: คลิกขวาที่ไฟล์หรือโฟลเดอร์ใน Nautilus แล้วสั่งบีบอัดได้ทันที
* **Multi-core Turbo Speed**: ตรวจจับและใช้เอนจิน **7-Zip (`7z`)** แบบ Multi-threading อัตโนมัติ บีบอัดเร็วเต็มสปีดทุกคอร์ ไม่ทำให้เครื่องค้างแม้โฟลเดอร์ใหญ่ระดับ 10+ GB (มี fallback ไปยัง `zip` และ Python `zipfile`)
* **ป้องกันบีบไฟล์ซ้ำอัตโนมัติ**: เมื่อเลือกหลายไฟล์พร้อมกัน ระบบจะข้ามไฟล์ที่เป็น `.zip` อยู่แล้วให้อัตโนมัติ ป้องกันการเกิดไฟล์ `.zip.zip`
* **ข้ามไฟล์ติดสิทธิ์อย่างปลอดภัย**: จัดการไฟล์ติดสิทธิ์ (`Permission Denied`) หรือไฟล์ระบบที่ถูกล็อกได้อย่างราบรื่น ไม่ทำให้การบีบอัดทั้งหมดล้มเหลว
* **ป้องกันไฟล์ซ้ำอัจฉริยะ**: หากมีไฟล์ ZIP ชื่อเดิมอยู่แล้ว ระบบจะแสดงหน้าต่างถามว่าต้องการ *"เขียนทับ"*, *"สร้างชื่อใหม่ (เช่น Folder (1).zip)"* หรือ *"ยกเลิก"*
* **แสดง Progress Bar พร้อมปุ่มยกเลิก**: เมื่อบีบอัดโฟลเดอร์ขนาดใหญ่ (>25 MB หรือ >50 ไฟล์) จะมีหน้าต่างแจ้งเตือนและสามารถกดยกเลิกกลางคันได้ตลอดเวลา
* **รองรับชื่อไฟล์ภาษาไทย 100%**: ปลอดภัยกับชื่อโฟลเดอร์และไฟล์ภาษาไทย รวมถึงอักขระพิเศษ
* **แจ้งเตือน Desktop Notification**: เมื่อบีบอัดสำเร็จ จะมี Notification บอกขนาดไฟล์และตำแหน่งที่บันทึก

---

### วิธีติดตั้ง (Quick Install)

เปิด Terminal แล้วคัดลอกคำสั่งไปวาง:

```bash
git clone https://github.com/n0ngXarm/Allzip.git
cd Allzip
./install.sh
```

---

### วิธีใช้งาน

1. **ผ่านเมนูคลิกขวา (Nautilus):**
   * เลือกไฟล์หรือโฟลเดอร์ $\rightarrow$ คลิกขวา $\rightarrow$ **Scripts** $\rightarrow$ **Allzip**
2. **ผ่าน Application Launcher:**
   * เปิดเมนูแอปพลิเคชันในเครื่อง ค้นหา **"Allzip"** แล้วคลิกเปิดเพื่อเลือกไฟล์
3. **ผ่าน Terminal (CLI):**
   ```bash
   zip-folder /path/to/my-folder
   ```

---

<a name="english"></a>
## English

**Allzip** is a lightweight, high-performance 1-click ZIP compressor designed for Linux GNOME Nautilus desktop environments.

### Features
* **1-Click Context Menu**: Right-click any file or folder in Nautilus to compress immediately.
* **Multi-core Turbo Speed**: Automatically leverages **7-Zip (`7z`)** multi-threading across all CPU cores for ultra-fast compression of huge archives (10+ GB) without desktop freezes, with fallback to system `zip` and pure Python `zipfile`.
* **Smart Duplicate Archive Prevention**: Automatically skips existing `.zip` archives when multiple files are selected, preventing redundant `.zip.zip` archives.
* **Permission & Error Resilient**: Gracefully bypasses locked or permission-denied files without failing or corrupting the archive.
* **Smart Collision Handling**: Prompts with Overwrite / New Name / Cancel if the target ZIP already exists.
* **Cancellable Progress Indicator**: Shows an automatic progress dialog for larger archives with a working Cancel button.
* **Unicode & UTF-8 Safe**: Full support for international characters (Thai, Chinese, etc.) and empty folders.
* **Desktop Notifications**: Instant notification upon completion displaying final archive size and path.

### Installation
```bash
git clone https://github.com/n0ngXarm/Allzip.git
cd Allzip
./install.sh
```

---

## สนับสนุนผู้พัฒนา / Support & Donation
โปรเจกต์นี้เปิดให้ทุกคนใช้งานได้ **ฟรี 100% (Open Source)** ภายใต้สัญญาอนุญาต MIT  
หากเครื่องมือนี้ช่วยให้คุณบีบอัดไฟล์ได้สะดวกรวดเร็วขึ้น สามารถร่วมสนับสนุนผู้พัฒนาได้ครับ:

<details>
<summary><b>สแกนผ่าน PromptPay QR (คลิกเพื่อดู QR Code)</b></summary>
<br>
<p><i>สแกนผ่านแอปธนาคารไทยได้ทุกธนาคาร (เงินเข้าบัญชีผู้พัฒนาโดยตรง 0% ค่าธรรมเนียม):</i></p>
<p align="left">
  <img src="assets/promptpay.jpeg" alt="PromptPay QR Code" width="220">
</p>
</details>

<br>

<details>
<summary><b>ช่องทางสนับสนุนสากล (Ko-fi / Buy Me a Coffee)</b></summary>
<br>
<p align="left">
  <a href="https://ko-fi.com/n0ngXarm">
    <img src="https://ko-fi.com/img/githubbutton_sm.svg" alt="ko-fi" height="34">
  </a>
  &nbsp;&nbsp;
  <a href="https://buymeacoffee.com/n0ngXarm">
    <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a coffee&slug=n0ngXarm&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" height="34" alt="Buy Me A Coffee" />
  </a>
</p>
<ul>
  <li><b>Ko-fi:</b> <a href="https://ko-fi.com/n0ngXarm">ko-fi.com/n0ngXarm</a></li>
  <li><b>Buy Me a Coffee:</b> <a href="https://buymeacoffee.com/n0ngXarm">buymeacoffee.com/n0ngXarm</a></li>
  <li><b>GitHub Sponsor:</b> กดปุ่ม <b>Sponsor</b> ที่ด้านบนของ Repository ได้เลยครับ</li>
</ul>
</details>

---

## License
This project is licensed under the [MIT License](LICENSE).
