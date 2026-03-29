#!/usr/bin/env python3
import os
import sys
import time
import json
import requests

# ------------------- CẤU HÌNH MÀU -------------------
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"

# ------------------- LẤY API KEY -------------------
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    print(f"{RED}{BOLD}⚠️ LỖI: Chưa thiết lập biến môi trường GEMINI_API_KEY{RESET}")
    print(f"{YELLOW}👉 Hãy chạy: export GEMINI_API_KEY='your_key_here'{RESET}")
    print(f"👉 Hoặc tạo file .env theo hướng dẫn trong README{RESET}")
    sys.exit(1)

MODEL = "gemini-2.5-flash"
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

# ------------------- LỊCH SỬ HỘI THOẠI -------------------
conversation_history = []  # Mỗi phần tử: {"role": "user"/"model", "parts": [{"text": "..."}]}

# ------------------- HÀM TIỆN ÍCH -------------------
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def typewriter(text, delay=0.02):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def print_banner():
    """Đọc banner từ texture.txt và in với màu xanh"""
    try:
        with open("texture.txt", "r", encoding="utf-8") as f:
            banner = f.read()
        print(f"{GREEN}{BOLD}{banner}{RESET}")
    except FileNotFoundError:
        print(f"{RED}{BOLD}⚠️ Không tìm thấy texture.txt{RESET}")
    print(f"{DIM}    model: {MODEL} | type 'exit' to quit | '/clear' to reset history{RESET}")
    print(f"{DIM}    [Ctrl+C] to interrupt{RESET}\n")

def send_prompt(prompt):
    """Gửi prompt kèm lịch sử hội thoại, trả về (answer, tokens_info)"""
    # Thêm tin nhắn của user vào lịch sử
    conversation_history.append({"role": "user", "parts": [{"text": prompt}]})

    headers = {'Content-Type': 'application/json'}
    payload = {"contents": conversation_history}  # Gửi toàn bộ lịch sử

    try:
        resp = requests.post(URL, headers=headers, json=payload, timeout=30)
        data = resp.json()

        if 'error' in data:
            # Nếu lỗi, xóa tin nhắn user vừa thêm khỏi lịch sử
            conversation_history.pop()
            return None, f"API Error: {data['error']['message']} ({data['error']['status']})"

        if 'candidates' in data and data['candidates']:
            answer = data['candidates'][0]['content']['parts'][0]['text']
            usage = data.get('usageMetadata', {})
            tokens_info = f"Tokens: prompt={usage.get('promptTokenCount',0)} | answer={usage.get('candidatesTokenCount',0)} | total={usage.get('totalTokenCount',0)}"

            # Thêm câu trả lời của model vào lịch sử
            conversation_history.append({"role": "model", "parts": [{"text": answer}]})
            return answer, tokens_info
        else:
            conversation_history.pop()
            return None, f"Invalid response: {data}"
    except Exception as e:
        # Nếu có lỗi kết nối, xóa tin nhắn user vừa thêm
        conversation_history.pop()
        return None, f"Error: {e}"

def clear_history():
    """Xóa toàn bộ lịch sử hội thoại"""
    global conversation_history
    conversation_history = []
    print(f"{YELLOW}[SYSTEM] Đã xóa lịch sử trò chuyện.{RESET}")

# ------------------- CHƯƠNG TRÌNH CHÍNH -------------------
def main():
    clear_screen()
    print_banner()
    while True:
        try:
            user_input = input(f"{GREEN}{BOLD}[Đức Nhân@Gemini]>> {RESET}").strip()
            if not user_input:
                continue

            # Xử lý lệnh đặc biệt
            if user_input.lower() in ['exit', 'thoát', 'quit']:
                print(f"\n{YELLOW}[SYSTEM] Shutting down...{RESET}")
                time.sleep(0.5)
                break
            if user_input == '/clear':
                clear_history()
                continue

            # Gửi prompt và nhận phản hồi
            print(f"\r{DIM}{GREEN}[>] Sending request...{RESET}", end="")
            sys.stdout.flush()
            answer, info = send_prompt(user_input)
            print("\r" + " " * 40 + "\r", end="")

            if answer:
                print(f"\n{GREEN}{BOLD}[AI] >{RESET} ")
                typewriter(answer, delay=0.01)
                if info:
                    print(f"{DIM}{info}{RESET}")
            else:
                print(f"\n{RED}{BOLD}[ERROR] {info}{RESET}")

        except KeyboardInterrupt:
            print(f"\n\n{YELLOW}[SYSTEM] Interrupted. Exiting...{RESET}")
            break
        except Exception as e:
            print(f"\n{RED}Unexpected error: {e}{RESET}")

if __name__ == "__main__":
    main()
