# 🤖 Gemini Hacker Terminal

Một giao diện terminal phong cách hacker cho Google Gemini AI, chạy được trên **Termux** (Android) và các terminal Linux/macOS/Windows.

## ✨ Tính năng
- Banner ASCII ma trận xanh lục
- Hiệu ứng gõ chữ (typewriter)
- Hiển thị số lượng token tiêu thụ
- Prompt `[Đức Nhân@Gemini]>>`
- Tự động xoá màn hình khi khởi động

## 📦 Cài đặt(Termux)

pkg update && pkg upgrade -y
pkg install python git -y
mkdir -p ~/gemini_hacker
cd ~/gemini_hacker
echo "requests" > requirements.txt
pip install -r requirements.txt

## 📦 Cài đặt(Window)

*Tạo thư mục cần thiết

cd %USERPROFILE%
mkdir gemini_hacker
cd gemini_hacker

*Tải các file cần thiết

    Tạo lần lượt các file gemini.py,texture.txt, requirements.txt,bằng cách copy nội dung từ bên dưới(hoặc dùng NotePad,VS Code).
    Để tạo nhanh bằng cmd:
    
echo requests > requirements.txt

    Sau đó dùng NotePad để tạo gemini.py và texture.txt(xem nội dung các file ở cuối README).
*Cài đặt thư viện
    
pip install requests

*Thiết lập API Key

set GEMINI_API_KEY=AIzaSy...

Để lưu vĩnh viễn:

· Mở System Properties → Environment Variables → thêm biến GEMINI_API_KEY với giá trị key của bạn.

*Khởi chạy chương trình

python gemini.py

## 📦 Cài đặt(Linux,Debian,Ubuntu,...)

1.Cài đặt python và pip nếu chưa có

# Ubuntu/Debian
sudo apt update && sudo apt install python3 python3-pip -y

# Fedora
sudo dnf install python3 python3-pip -y

# Arch
sudo pacman -S python python-pip
2.Tạo thư mục dự án

mkdir -p ~/gemini_hacker
cd ~/gemini_hacker

3.Tạo các file

Dùng nano hoặc vim để tạo từng file(nội dung giống như phần Termux).
Hoặc nhanh hơn,clone từ GitHub nếu đã có repo.

4.Cài đặt thư viện

pip3 install requests

5.Thiết lập API Key

export GEMINI_API_KEY='AIzaSy...'

*Để lưu vĩnh viễn thì hãy thêm vào ~/.bashrc hoặc ~/.zshrc:

echo "export GEMINI_API_KEY='AIzaSy...'" >> ~/.bashrc
source ~/.bashrc
6.Chạy chương trình
python3 gemini.py


#Tôi có chơi free fire(uid: 8028236431)
