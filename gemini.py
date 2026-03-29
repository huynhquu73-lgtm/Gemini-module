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

# ------------------- CẤU HÌNH MODEL -------------------
AVAILABLE_MODELS = {
    "1": "gemini-2.0-flash-exp",
    "2": "gemini-1.5-pro",
    "3": "gemini-1.5-flash"
}
DEFAULT_MODEL = "gemini-2.0-flash-exp"
MODEL = DEFAULT_MODEL
HISTORY_FILE = "conversation_history.json"

# ------------------- LỊCH SỬ HỘI THOẠI -------------------
conversation_history = []  # format Gemini API

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
    """Lưu lịch sử hội thoại ra file JSON"""
    try:
        with open(HISTORY_FILE, "w", encoding="utf-8") as f:
            json.dump(conversation_history, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        print(f"{RED}Lỗi lưu lịch sử: {e}{RESET}")
        return False

def load_history_from_file():
    """Tải lịch sử từ file JSON (nếu có)"""
    global conversation_history
    try:
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, "r", encoding="utf-8") as f:
                conversation_history = json.load(f)
            print(f"{GREEN}✓ Đã tải {len(conversation_history)//2} lượt hội thoại từ {HISTORY_FILE}{RESET}")
        else:
            print(f"{DIM}Không tìm thấy file lịch sử cũ. Bắt đầu hội thoại mới.{RESET}")
    except Exception as e:
        print(f"{RED}Lỗi tải lịch sử: {e}{RESET}")
        conversation_history = []

def build_url():
    return f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent?key={API_KEY}"

def send_prompt_stream(prompt):
    """Gửi prompt với streaming, trả về (full_answer, tokens_info, latency)"""
    global conversation_history
    conversation_history.append({"role": "user", "parts": [{"text": prompt}]})

    url = build_url()
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": conversation_history}
    # Thêm streaming
    url += "&alt=sse"  # Server-Sent Events

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

            # Đọc từng dòng SSE
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
                                # In real-time nếu muốn (tắt typewriter sau)
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
        conversation_history.append({"role": "model", "parts": [{"text": full_answer}]})
        return full_answer, tokens_info, latency
    else:
        conversation_history.pop()
        return None, "No response from model", latency

def send_prompt_normal(prompt):
    """Phiên bản không streaming (dùng nếu stream lỗi)"""
    conversation_history.append({"role": "user", "parts": [{"text": prompt}]})
    url = build_url()
    headers = {'Content-Type': 'application/json'}
    payload = {"contents": conversation_history}
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
            conversation_history.append({"role": "model", "parts": [{"text": answer}]})
            return answer, tokens_info, latency
        else:
            conversation_history.pop()
            return None, f"Invalid response", latency
    except Exception as e:
        conversation_history.pop()
        return None, f"Error: {e}", 0

def send_prompt(prompt, use_stream=True):
    """Wrapper: thử stream trước, nếu lỗi thì fallback normal"""
    if use_stream:
        answer, info, latency = send_prompt_stream(prompt)
        if answer is None and "not support" in info.lower():
            # Nếu model không hỗ trợ stream, thử normal
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
  {GREEN}/save{RESET}           - Lưu lịch sử hiện tại vào file {HISTORY_FILE}
  {GREEN}/load{RESET}           - Tải lịch sử từ file (ghi đè)
  {GREEN}/model{RESET}          - Xem model đang dùng
  {GREEN}/model <số>{RESET}     - Đổi model: 1=Flash 2.0, 2=Pro 1.5, 3=Flash 1.5
  {GREEN}/history{RESET}        - Hiển thị số lượt hội thoại
  {GREEN}/exit{RESET}           - Thoát (tự động lưu lịch sử)
  {GREEN}/help{RESET}           - Hiện bảng này
    """
    print(help_text)

# ------------------- CHƯƠNG TRÌNH CHÍNH -------------------
def main():
    clear_screen()
    print_banner()
    # Tự động load lịch sử cũ nếu có
    load_history_from_file()

    while True:
        try:
            user_input = input(f"{GREEN}{BOLD}[Đức Nhân@Gemini]>> {RESET}").strip()
            if not user_input:
                continue

            # Xử lý lệnh
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
                        global MODEL
                        MODEL = AVAILABLE_MODELS[choice]
                        print(f"{GREEN}✓ Đã chuyển sang model: {MODEL}{RESET}")
                    else:
                        print(f"{RED}Model không hợp lệ. Các lựa chọn: 1,2,3{RESET}")
                continue

            # Gửi prompt bình thường (có stream)
            print(f"\r{DIM}{GREEN}[>] Đang gửi...{RESET}", end="")
            sys.stdout.flush()
            answer, info, latency = send_prompt(user_input, use_stream=True)
            print("\r" + " " * 40 + "\r", end="")

            if answer:
                # Nếu đã stream thì không cần typewriter nữa (vì đã in real-time)
                # Nhưng để giữ phong cách, nếu không có stream (fallback) thì dùng typewriter
                if not info:  # nếu info rỗng tức là đã dùng stream? Thực tế stream đã in rồi
                    pass
                else:
                    # Fallback normal: in ra với typewriter
                    print(f"\n{GREEN}{BOLD}[AI] >{RESET} ")
                    typewriter(answer, delay=0.01)
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

if __name__ == "__main__":
    main()
