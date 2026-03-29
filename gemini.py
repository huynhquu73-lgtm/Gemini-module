#!/usr/bin/env python3
import os
import sys
import time
import json
import requests
from datetime import datetime

# ------------------- CẤU HÌNH MÀU -------------------
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BOLD = "\033[1m"
RESET = "\033[0m"
DIM = "\033[2m"

# ------------------- CHỌN API KEY -------------------
API_KEYS = {
    "1": "AIzaSyDJvrzMm0sCdpb9EKMQSkl5z6vVXg_8oiI",
    "2": "AIzaSyAIRCAEyHnhamfcA2Z_9wv9O6xaE1slMh4",
    "3": "AIzaSyCeRAn6wsiG4L9mUTl-oQSQgRqNRFer2Uk",
    "4": "AIzaSyCJ1De_8vgoiQwaydUqKp0mSdl8n75HYQ0"
}

print(f"{GREEN}{BOLD}--- CHỌN API KEY ---{RESET}")
print("1. API Key 1")
print("2. API Key 2")
print("3. API Key 3")
print("4. API Key 4")

while True:
    choice = input(f"{YELLOW}Vui lòng chọn API key (1-4): {RESET}").strip()
    if choice in API_KEYS:
        API_KEY = API_KEYS[choice]
        print(f"{GREEN}✓ Đã chọn API Key {choice}{RESET}\n")
        break
    else:
        print(f"{RED}⚠️ Lựa chọn không hợp lệ. Vui lòng nhập số từ 1 đến 4.{RESET}")

# ------------------- CẤU HÌNH -------------------
AVAILABLE_MODELS = {
    "1": "gemini-2.0-flash-exp",
    "2": "gemini-1.5-pro",
    "3": "gemini-1.5-flash"
}
DEFAULT_MODEL = "gemini-2.0-flash-exp"
MODEL = DEFAULT_MODEL
HISTORY_FILE = "conversation_history.txt"

# ------------------- LỊCH SỬ -------------------
conversation_history = []

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
    try:
        with open("texture.txt", "r", encoding="utf-8") as f:
            banner = f.read()
        print(f"{GREEN}{BOLD}{banner}{RESET}")
    except FileNotFoundError:
        print(f"{RED}{BOLD}⚠️ Không tìm thấy texture.txt{RESET}")
    print(f"{DIM}    model: {MODEL} | /help for commands | type 'exit' to quit{RESET}")
    print(f"{DIM}    [Ctrl+C] to interrupt{RESET}\n")

def save_history_to_file():
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            f.write(f"# Gemini Conversation History\n# Last saved: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"# Model: {MODEL}\n\n")
            for msg in conversation_history:
                role = "User" if msg["role"] == "user" else "Gemini"
                f.write(f"{role}: {msg['text']}\n\n")
            f.write("--- End of conversation ---\n")
        return True
    except Exception as e:
        print(f"{RED}Lỗi lưu lịch sử: {e}{RESET}")
        return False

def load_history_from_file():
    global conversation_history
    conversation_history = []
    if not os.path.exists(HISTORY_FILE):
        print(f"{DIM}Không tìm thấy file lịch sử cũ. Bắt đầu hội thoại mới.{RESET}")
        return

    try:
        with open(HISTORY_FILE, "r", encoding="utf-8") as f:
            content = f.read()
        lines = content.split('\n')
        current_role = None
        current_text = []
        for line in lines:
            if line.startswith("User: "):
                if current_role and current_text:
                    conversation_history.append({"role": current_role, "text": " ".join(current_text).strip()})
                current_role = "user"
                current_text = [line[6:].strip()]
            elif line.startswith("Gemini: "):
                if current_role and current_text:
                    conversation_history.append({"role": current_role, "text": " ".join(current_text).strip()})
                current_role = "model"
                current_text = [line[8:].strip()]
            elif line.startswith("#") or line.startswith("---"):
                continue
            else:
                if current_role and line.strip():
                    current_text.append(line.strip())
        if current_role and current_text:
            conversation_history.append({"role": current_role, "text": " ".join(current_text).strip()})
        print(f"{GREEN}✓ Đã tải {len(conversation_history)//2} lượt hội thoại từ {HISTORY_FILE}{RESET}")
    except Exception as e:
        print(f"{RED}Lỗi tải lịch sử: {e}{RESET}")
        conversation_history = []

def build_url():
    return f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def convert_history_to_gemini_format():
    gemini_msgs = []
    for msg in conversation_history:
        gemini_msgs.append({
            "role": msg["role"],
            "parts": [{"text": msg["text"]}]
        })
    return gemini_msgs

def send_prompt_stream(prompt):
    global conversation_history
    conversation_history.append({"role": "user", "text": prompt})
    gemini_payload = convert_history_to_gemini_format()
    url = build_url()
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": gemini_payload}
    url += "&alt=sse"

    start_time = time.time()
    full_answer = ""
    tokens_info = ""

    try:
        with requests.post(url, headers=headers, json=payload, stream=True, timeout=60) as resp:
            if resp.status_code != 200:
                error_data = resp.json()
                err_msg = error_data.get('error', {}).get('message', 'Unknown error')
                conversation_history.pop()
                return None, f"API Error {resp.status_code}: {err_msg}", 0

            for line in resp.iter_lines(decode_unicode=True):
                if line and line.startswith("data: "):
                    data_str = line[6:]
                    if data_str == "[DONE]":
                        break
                    try:
                        chunk = json.loads(data_str)
                        if 'candidates' in chunk and chunk['candidates']:
                            text_part = chunk['candidates'][0].get('content', {}).get('parts', [{}])[0].get('text', '')
                            if text_part:
                                full_answer += text_part
                                sys.stdout.write(text_part)
                                sys.stdout.flush()
                        if 'usageMetadata' in chunk:
                            usage = chunk['usageMetadata']
                            tokens_info = f"Tokens: prompt={usage.get('promptTokenCount',0)} | answer={usage.get('candidatesTokenCount',0)} | total={usage.get('totalTokenCount',0)}"
                    except json.JSONDecodeError:
                        continue
    except Exception as e:
        conversation_history.pop()
        return None, f"Error: {e}", 0

    latency = time.time() - start_time
    if full_answer:
        conversation_history.append({"role": "model", "text": full_answer})
        return full_answer, tokens_info, latency
    else:
        conversation_history.pop()
        return None, "No response from model", latency

def send_prompt_normal(prompt):
    global conversation_history
    conversation_history.append({"role": "user", "text": prompt})
    gemini_payload = convert_history_to_gemini_format()
    url = build_url()
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": gemini_payload}
    start_time = time.time()
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        data = resp.json()
        latency = time.time() - start_time
        if 'error' in data:
            conversation_history.pop()
            return None, f"API Error: {data['error']['message']}", latency
        if 'candidates' in data and data['candidates']:
            answer = data['candidates'][0]['content']['parts'][0]['text']
            usage = data.get('usageMetadata', {})
            tokens_info = f"Tokens: prompt={usage.get('promptTokenCount',0)} | answer={usage.get('candidatesTokenCount',0)} | total={usage.get('totalTokenCount',0)}"
            conversation_history.append({"role": "model", "text": answer})
            return answer, tokens_info, latency
        else:
            conversation_history.pop()
            return None, f"Invalid response", latency
    except Exception as e:
        conversation_history.pop()
        return None, f"Error: {e}", 0

def send_prompt(prompt, use_stream=True):
    if use_stream:
        answer, info, latency = send_prompt_stream(prompt)
        if answer is None and info and "not support" in info.lower():
            return send_prompt_normal(prompt)
        return answer, info, latency
    else:
        return send_prompt_normal(prompt)

def clear_history():
    global conversation_history
    conversation_history = []
    print(f"{YELLOW}[SYSTEM] Đã xóa lịch sử trò chuyện (bộ nhớ).{RESET}")

def show_help():
    help_text = f"""
{BOLD}📖 CÁC LỆNH KHẢ DỤNG:{RESET}
  {GREEN}/clear{RESET}          - Xóa lịch sử hội thoại hiện tại
  {GREEN}/save{RESET}           - Lưu lịch sử hiện tại vào file {HISTORY_FILE} (txt)
  {GREEN}/load{RESET}           - Tải lịch sử từ file (ghi đè)
  {GREEN}/model{RESET}          - Xem model đang dùng
  {GREEN}/model <số>{RESET}     - Đổi model: 1=Flash 2.0, 2=Pro 1.5, 3=Flash 1.5
  {GREEN}/history{RESET}        - Hiển thị số lượt hội thoại
  {GREEN}/export{RESET}         - Xuất lịch sử ra file markdown (Gemini_export.md)
  {GREEN}/exit{RESET}           - Thoát (tự động lưu lịch sử)
  {GREEN}/help{RESET}           - Hiện bảng này
    """
    print(help_text)

def export_markdown():
    filename = f"Gemini_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
    try:
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"# Gemini Conversation\n**Model:** {MODEL}\n**Exported:** {datetime.now()}\n\n")
            for msg in conversation_history:
                role = "**User**" if msg["role"] == "user" else "**Gemini**"
                f.write(f"{role}:\n{msg['text']}\n\n---\n\n")
        print(f"{GREEN}✓ Đã xuất lịch sử ra file {filename}{RESET}")
    except Exception as e:
        print(f"{RED}Lỗi xuất file: {e}{RESET}")

# ------------------- CHƯƠNG TRÌNH CHÍNH -------------------
def main():
    global MODEL  # <--- MÌNH ĐÃ THÊM DÒNG NÀY VÀO ĐẦU HÀM ĐỂ FIX LỖI
    clear_screen()
    print_banner()
    load_history_from_file()

    try:
        while True:
            try:
                user_input = input(f"{GREEN}{BOLD}[Đức Nhân@Gemini]>> {RESET}").strip()
                if not user_input:
                    continue

                cmd = user_input.lower()
                if cmd in ['exit', 'thoát', 'quit']:
                    if save_history_to_file():
                        print(f"{GREEN}✓ Đã lưu lịch sử vào {HISTORY_FILE}{RESET}")
                    print(f"\n{YELLOW}[SYSTEM] Shutting down...{RESET}")
                    time.sleep(0.5)
                    break

                if cmd == '/clear':
                    clear_history()
                    continue

                if cmd == '/save':
                    if save_history_to_file():
                        print(f"{GREEN}✓ Đã lưu {len(conversation_history)//2} lượt hội thoại.{RESET}")
                    continue

                if cmd == '/load':
                    load_history_from_file()
                    continue

                if cmd == '/history':
                    print(f"{DIM}Số tin nhắn trong lịch sử: {len(conversation_history)} (={len(conversation_history)//2} lượt hỏi-đáp){RESET}")
                    continue

                if cmd == '/export':
                    export_markdown()
                    continue

                if cmd == '/help':
                    show_help()
                    continue

                if cmd.startswith('/model'):
                    parts = user_input.split()
                    if len(parts) == 1:
                        print(f"{GREEN}Model hiện tại: {MODEL}{RESET}")
                    else:
                        choice = parts[1]
                        if choice in AVAILABLE_MODELS:
                            # global MODEL <--- DÒNG CŨ Ở ĐÂY GÂY LỖI NÊN MÌNH ĐÃ XÓA (VÌ CÓ Ở TRÊN RỒI)
                            MODEL = AVAILABLE_MODELS[choice]
                            print(f"{GREEN}✓ Đã chuyển sang model: {MODEL}{RESET}")
                        else:
                            print(f"{RED}Model không hợp lệ. Các lựa chọn: 1,2,3{RESET}")
                    continue

                print(f"\r{DIM}{GREEN}[>] Đang gửi...{RESET}", end="")
                sys.stdout.flush()
                answer, info, latency = send_prompt(user_input, use_stream=True)
                print("\r" + " " * 40 + "\r", end="")

                if answer:
                    if info:
                        print(f"{DIM}{info} | ⏱️ {latency:.2f}s{RESET}")
                    else:
                        print(f"{DIM}⏱️ {latency:.2f}s{RESET}")
                else:
                    print(f"\n{RED}{BOLD}[ERROR] {info}{RESET}")

            except KeyboardInterrupt:
                print(f"\n\n{YELLOW}[SYSTEM] Interrupted. Lưu lịch sử trước khi thoát...{RESET}")
                save_history_to_file()
                break
            except Exception as e:
                print(f"\n{RED}Unexpected error: {e}{RESET}")
    finally:
        if save_history_to_file():
            print(f"{GREEN}✓ Đã tự động lưu lịch sử vào {HISTORY_FILE} khi thoát{RESET}")
        time.sleep(0.5)

if __name__ == "__main__":
    main()
