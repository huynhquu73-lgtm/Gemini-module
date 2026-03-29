# 🤖 Gemini Hacker Terminal

Giao diện terminal phong cách hacker cho Google Gemini AI – chạy trên **Termux** (Android), **Windows**, **Linux**, **macOS**.

## ✨ Tính năng
- Banner ASCII ma trận xanh lục
- Hiệu ứng gõ chữ (typewriter)
- Hiển thị số lượng token tiêu thụ
- Prompt `[Đức Nhân@Gemini]>>`
- Tự động xoá màn hình khi khởi động

## 📦 Yêu cầu chung
- Python 3.7+
- Git
- API key Gemini (lấy miễn phí tại [Google AI Studio](https://aistudio.google.com/app/apikey))

---

## 📱 Cài đặt trên Termux (Android)

# 1. Cập nhật gói và cài đặt Python, Git
```
pkg update && pkg upgrade -y
```
```
pkg install python git -y
```
# 2. Clone dự án
```
git clone https://github.com/DcnhanZz/Gemini-module.git
```
```
cd Gemini-module
```
# 3. Cài đặt thư viện requests
```
pip install requests
```
# 5. Chạy chương trình
```
python gemini.py
```

---

🪟 Cài đặt trên Windows (Command Prompt hoặc PowerShell)

Bước 1: Cài đặt Git và Python

· Tải và cài Git từ git-scm.com
· Tải Python từ python.org (nhớ chọn Add Python to PATH)

Bước 2: Mở Command Prompt (cmd) và chạy

```cmd
cd %USERPROFILE%
git clone https://github.com/DcnhanZz/Gemini-module.git
```
```
cd Gemini-module
```
```
pip install requests

```

Bước 3: Chạy chương trình

```cmd
python gemini.py
```

---

🐧 Cài đặt trên Linux (Ubuntu/Debian, Fedora, Arch...)


# 1. Cài đặt Python, Git và pip (nếu chưa có)
# Ubuntu/Debian
```
sudo apt update && sudo apt install python3 python3-pip git -y
```

# Fedora
```
sudo dnf install python3 python3-pip git -y
```
# Arch
```
sudo pacman -S python python-pip git
```
# 2. Clone dự án
```
git clone https://github.com/DcnhanZz/Gemini-module.git
```
```
cd Gemini-module
```
# 3. Cài đặt thư viện
```
pip3 install requests
```

# 5. Chạy chương trình
```
python3 gemini.py
```

---

🍎 Cài đặt trên macOS

# 1. Cài đặt Homebrew (nếu chưa có)
```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```
# 2. Cài đặt Python, Git
```
brew install python git
```

# 3. Clone dự án
```
git clone https://github.com/DcnhanZz/Gemini-module.git
```
```
cd gemini-hacker
```
# 4. Cài đặt requests
```
pip3 install requests
```

# 6. Chạy chương trình
```
python3 gemini.py
```

---
