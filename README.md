
```markdown
# 🤖 Gemini Hacker Terminal

Giao diện terminal phong cách hacker cho Google Gemini AI, chạy được trên **Termux** (Android), **Windows**, **Linux**, **macOS**.

## ✨ Tính năng
- Banner ASCII ma trận xanh lục
- Hiệu ứng gõ chữ (typewriter)
- Hiển thị số lượng token tiêu thụ
- Prompt `[Đức Nhân@Gemini]>>`
- Tự động xoá màn hình khi khởi động

---

## 📦 Cài đặt

### 📱 Termux (Android)

```bash
pkg update && pkg upgrade -y
pkg install python git -y
mkdir -p ~/gemini_hacker
cd ~/gemini_hacker
echo "requests" > requirements.txt
pip install -r requirements.txt
```

Sau đó tạo các file gemini.py, texture.txt (xem nội dung ở cuối README).

```bash
export GEMINI_API_KEY='AIzaSy...'   # thay key thật
python gemini.py
```

---

🪟 Windows (Command Prompt)

Tạo thư mục dự án

```cmd
cd %USERPROFILE%
mkdir gemini_hacker
cd gemini_hacker
```

Tạo file requirements.txt

```cmd
echo requests > requirements.txt
```

Cài đặt thư viện

```cmd
pip install requests
```

Thiết lập API key (tạm thời)

```cmd
set GEMINI_API_KEY=AIzaSy...
```

Để lưu vĩnh viễn: Mở System Properties → Environment Variables → thêm biến GEMINI_API_KEY với giá trị key của bạn.

Chạy chương trình

```cmd
python gemini.py
```

---

🐧 Linux (Ubuntu/Debian, Fedora, Arch...)

1. Cài đặt Python & pip

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip -y

# Fedora
sudo dnf install python3 python3-pip -y

# Arch
sudo pacman -S python python-pip
```

2. Tạo thư mục dự án

```bash
mkdir -p ~/gemini_hacker
cd ~/gemini_hacker
```

3. Tạo các file cần thiết (xem nội dung ở cuối README)

4. Cài đặt thư viện

```bash
pip3 install requests
```

5. Thiết lập API key

```bash
export GEMINI_API_KEY='AIzaSy...'
```

Để lưu vĩnh viễn, thêm vào ~/.bashrc hoặc ~/.zshrc:

```bash
echo "export GEMINI_API_KEY='AIzaSy...'" >> ~/.bashrc
source ~/.bashrc
```

6. Chạy chương trình

```bash
python3 gemini.py
```

---

📄 Nội dung các file cần tạo

requirements.txt

```txt
requests
```

texture.txt

```text
