import json
import re
import time
import requests
from google import genai
from .utils import save_feedback, save_history, get_last_user_input, get_feedback_user_inputs

# --- Khởi tạo client Gemini ---
client = genai.Client(api_key="AIzaSyD09X-xh9HkghMk4eImIHXrqPw9Uy5hcIA")

# --- PROMPTS cho ghi chú ---
PROMPTS = {
    "summary": (
        "Bạn là Vịt, chatbot quản lý ghi chú. "
        "Người dùng muốn tóm tắt nội dung. Trả lời tự nhiên, rõ ràng, dễ hiểu.\n{data}"
    ),
    "search": (
        "Bạn là Vịt, chatbot quản lý ghi chú. "
        "Người dùng muốn tìm ghi chú theo từ khóa '{query}'. Trả về JSON các ghi chú khớp:\n{data}"
    ),
    "detail": (
        "Bạn là Vịt, chatbot quản lý ghi chú. "
        "Người dùng muốn xem chi tiết ghi chú. JSON dữ liệu:\n{data}"
    ),
    "translate": (
        "Bạn là Vịt, chatbot quản lý ghi chú. "
        "Dịch ghi chú theo từ khóa '{query}' sang tiếng Anh. Trả về JSON:\n{data}"
    ),
    "analyze": (
        "Bạn là Vịt, chatbot quản lý ghi chú. "
        "Người dùng muốn phân tích nội dung. Nêu ý chính và gợi ý bổ sung:\n{data}"
    ),
    "natural": (
        "Bạn là Vịt, chatbot quản lý ghi chú và task. "
        "Người dùng nói: '{query}'. Trả lời tự nhiên, thân thiện, không ký tự đặc biệt."
    ),
    "create": (
        "Bạn là Vịt, chatbot quản lý ghi chú. "
        "Người dùng muốn tạo ghi chú: '{query}'. "
        "Trả về JSON với nt_title, nt_subtitle nếu có, nt_content, nt_img='', nt_pdf='', nt_date (YYYY-MM-DD), us_id='{us_id}'."
    ),
    "create_multi": (
        "Bạn là Vịt, chatbot quản lý ghi chú. "
        "Người dùng muốn tạo {n} ghi chú: '{query}'. "
        "Trả về JSON mảng {n} phần tử gồm nt_title, nt_subtitle nếu có, nt_content, nt_img='', nt_pdf='', nt_date (YYYY-MM-DD), us_id='{us_id}'."
    )
}

# --- INTENTS ghi chú ---
INTENTS = {
    "summary": ["tóm tắt ghi chú", "summary note", "note ngắn gọn"],
    "search": ["tìm ghi chú", "search note", "tra cứu ghi chú", "lấy note", "ghi chú tìm"],
    "detail": ["chi tiết ghi chú", "full note", "xem đầy đủ ghi chú"],
    "translate": ["dịch ghi chú", "translate note", "note sang tiếng anh"],
    "analyze": ["phân tích ghi chú", "analyze note", "note topic"],
    "create": ["tạo ghi chú", "tạo mới note", "create note", "new note", "thêm ghi chú", "add note"],
    "feedback": ["feedback note", "sai note", "không đúng note", "nhầm note"]
}

API_ENDPOINTS = {
    "summary": "http://127.0.0.1:8000/note/note-list/?us_id={us_id}",
    "search": "http://127.0.0.1:8000/note/note-list/?us_id={us_id}",
    "detail": "http://127.0.0.1:8000/note/note-list/?us_id={us_id}",
    "translate": "http://127.0.0.1:8000/note/note-list/?us_id={us_id}",
    "analyze": "http://127.0.0.1:8000/note/note-list/?us_id={us_id}",
    "create": "http://127.0.0.1:8000/note/add/"
}

# --- PROMPTS cho task ---
TASK_PROMPTS = {
    "summary": (
        "Bạn là Vịt, chatbot quản lý task. "
        "Người dùng muốn tóm tắt các task. Trả lời tự nhiên, rõ ràng, dễ hiểu.\n{data}"
    ),
    "search": (
        "Bạn là Vịt, chatbot quản lý task. "
        "Người dùng muốn tìm task theo từ khóa '{query}'. Trả về JSON các task khớp:\n{data}"
    ),
    "detail": (
        "Bạn là Vịt, chatbot quản lý task. "
        "Người dùng muốn xem chi tiết task. JSON dữ liệu:\n{data}"
    ),
    "translate": (
        "Bạn là Vịt, chatbot quản lý task. "
        "Dịch task theo từ khóa '{query}' sang tiếng Anh. Trả về JSON:\n{data}"
    ),
    "analyze": (
        "Bạn là Vịt, chatbot quản lý task. "
        "Người dùng muốn phân tích task. Nêu ý chính và gợi ý:\n{data}"
    ),
    "natural": (
        "Bạn là Vịt, chatbot quản lý task. "
        "Người dùng nói: '{query}'. Trả lời tự nhiên, thân thiện, không ký tự đặc biệt."
    ),
    "create": (
        "Bạn là Vịt, chatbot quản lý task. "
        "Người dùng muốn tạo task: '{query}'. "
        "Trả về JSON với ts_title, ts_content, ts_deadline (YYYY-MM-DD), us_id='{us_id}'."
    ),
    "create_multi": (
        "Bạn là Vịt, chatbot quản lý task. "
        "Người dùng muốn tạo {n} task: '{query}'. "
        "Trả về JSON mảng {n} phần tử gồm ts_title, ts_content, ts_deadline (YYYY-MM-DD), us_id='{us_id}'."
    )
}

# --- INTENTS task ---
TASK_INTENTS = {
    "summary": ["tóm tắt task", "summary task", "task ngắn gọn"],
    "search": ["tìm task", "search task", "tra cứu task", "lấy task"],
    "detail": ["chi tiết task", "full task", "xem đầy đủ task"],
    "translate": ["dịch task", "translate task", "task sang tiếng anh"],
    "analyze": ["phân tích task", "analyze task", "task topic"],
    "list": ["danh sách task", "list task", "tất cả task", "task list"],
    "create": ["tạo task", "thêm task", "create task", "new task", "add task"],
    "feedback": ["feedback task", "sai task", "nhầm task"]
}

TASK_API_ENDPOINTS = {
    "summary": "http://127.0.0.1:8000/task/person/task-list/?us_id={us_id}",
    "search": "http://127.0.0.1:8000/task/person/task-list/?us_id={us_id}",
    "detail": "http://127.0.0.1:8000/task/person/task-list/?us_id={us_id}",
    "translate": "http://127.0.0.1:8000/task/person/task-list/?us_id={us_id}",
    "analyze": "http://127.0.0.1:8000/task/person/task-list/?us_id={us_id}",
    "list": "http://127.0.0.1:8000/task/person/task-list/?us_id={us_id}",
    "create": "http://127.0.0.1:8000/task/person/add/"
}

# --- Detect intent tách rõ note/task ---
def detect_intent(user_input: str):
    user_input_lower = user_input.lower().strip()

    # Kiểm tra task trước
    if "task" in user_input_lower or "công việc" in user_input_lower:
        for intent, keywords in TASK_INTENTS.items():
            if any(kw.lower() in user_input_lower for kw in keywords):
                return intent, "task"
    # Kiểm tra note
    elif "note" in user_input_lower or "ghi chú" in user_input_lower:
        for intent, keywords in INTENTS.items():
            if any(kw.lower() in user_input_lower for kw in keywords):
                return intent, "note"
    return "natural", "unknown"

# --- Gọi Gemini AI ---
def call_gemini(prompt, retries=3, wait=3):
    for attempt in range(retries):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
            return response.text
        except Exception as e:
            print(f"Lỗi server Gemini, thử lại ({attempt+1}/{retries}) sau {wait}s...")
            time.sleep(wait)
    return "Server Gemini quá tải, vui lòng thử lại sau."

# --- Xử lý note ---
def run_note_ai(user_input: str, us_id: str):
    intent, _ = detect_intent(user_input)
    result_text = ""

    if intent in ["summary", "search", "detail", "translate", "analyze"]:
        try:
            resp = requests.get(API_ENDPOINTS[intent].format(us_id=us_id))
            data = resp.json()
        except Exception as e:
            result_text = f"Lỗi khi gọi API note: {e}"
            save_history(user_input, intent, result_text, us_id)
            return result_text, intent
        prompt = PROMPTS[intent].format(data=json.dumps(data, ensure_ascii=False, indent=2), query=user_input)
        result_text = call_gemini(prompt)

    elif intent == "create":
        match = re.search(r'tạo (\d+) (note|ghi chú)', user_input.lower())
        if match:
            n = int(match.group(1))
            prompt = PROMPTS["create_multi"].format(query=user_input, n=n, us_id=us_id)
        else:
            prompt = PROMPTS["create"].format(query=user_input, us_id=us_id)

        generated_json = call_gemini(prompt).strip()
        if generated_json.startswith("```"):
            generated_json = "\n".join(generated_json.split("\n")[1:-1])
        try:
            note_json = json.loads(generated_json)
        except Exception as e:
            result_text = f"Lỗi JSON note: {e}\n{generated_json}"
            save_history(user_input, intent, result_text, us_id)
            return result_text, intent

        try:
            api_url = API_ENDPOINTS["create"]
            if isinstance(note_json, list):
                success_count = 0
                for nj in note_json:
                    nj['us_id'] = us_id
                    resp = requests.post(api_url, json=nj)
                    if resp.status_code in [200, 201]:
                        success_count += 1
                result_text = f"{success_count}/{len(note_json)} ghi chú đã tạo thành công!"
            else:
                note_json['us_id'] = us_id
                resp = requests.post(api_url, json=note_json)
                result_text = f"Ghi chú đã tạo: {resp.json()}" if resp.status_code in [200,201] else f"Lỗi POST: {resp.text}"
        except Exception as e:
            result_text = f"Lỗi POST note: {e}"

    else:
        prompt = PROMPTS["natural"].format(query=user_input)
        result_text = call_gemini(prompt)

    save_feedback(user_input, intent, result_text, us_id)
    save_history(user_input, intent, result_text, us_id)
    return result_text, intent

# --- Xử lý task ---
def run_task_ai(user_input: str, us_id: str):
    intent, _ = detect_intent(user_input)
    result_text = ""

    if intent in ["summary", "search", "detail", "translate", "analyze"]:
        try:
            resp = requests.get(TASK_API_ENDPOINTS[intent].format(us_id=us_id))
            data = resp.json()
        except Exception as e:
            return f"Lỗi API task: {e}", intent
        prompt = TASK_PROMPTS[intent].format(data=json.dumps(data, ensure_ascii=False, indent=2), query=user_input)
        result_text = call_gemini(prompt)

    elif intent == "list":
        try:
            resp = requests.get(TASK_API_ENDPOINTS["list"].format(us_id=us_id))
            data = resp.json()
        except Exception as e:
            return f"Lỗi khi gọi API task list: {e}", intent
        prompt = TASK_PROMPTS["summary"].format(data=json.dumps(data, ensure_ascii=False, indent=2))
        result_text = call_gemini(prompt)
        save_feedback(user_input, intent, result_text, us_id)
        save_history(user_input, intent, result_text, us_id)
        return result_text, intent

    elif intent == "create":
        match = re.search(r'tạo (\d+) (task|công việc)', user_input.lower())
        if match:
            n = int(match.group(1))
            prompt = TASK_PROMPTS["create_multi"].format(query=user_input, n=n, us_id=us_id)
        else:
            prompt = TASK_PROMPTS["create"].format(query=user_input, us_id=us_id)

        generated_json = call_gemini(prompt).strip()
        if generated_json.startswith("```"):
            generated_json = "\n".join(generated_json.split("\n")[1:-1])
        try:
            task_json = json.loads(generated_json)
        except Exception as e:
            return f"Lỗi JSON task: {e}\n{generated_json}", intent

        try:
            api_url = TASK_API_ENDPOINTS["create"]
            if isinstance(task_json, list):
                success_count = 0
                for tj in task_json:
                    tj['us_id'] = us_id
                    resp = requests.post(api_url, json=tj)
                    if resp.status_code in [200, 201]:
                        success_count += 1
                result_text = f"{success_count}/{len(task_json)} task đã tạo thành công!"
            else:
                task_json['us_id'] = us_id
                resp = requests.post(api_url, json=task_json)
                result_text = f"Task đã tạo: {resp.json()}" if resp.status_code in [200,201] else f"Lỗi POST: {resp.text}"
        except Exception as e:
            result_text = f"Lỗi POST task: {e}"

    else:
        prompt = TASK_PROMPTS["natural"].format(query=user_input)
        result_text = call_gemini(prompt)

    save_feedback(user_input, intent, result_text, us_id)
    save_history(user_input, intent, result_text, us_id)
    return result_text, intent

# --- AI tổng hợp ---
def run_ai(user_input: str, us_id: str):
    intent, type_ = detect_intent(user_input)

    if type_ == "task":
        return run_task_ai(user_input, us_id)
    elif type_ == "note":
        return run_note_ai(user_input, us_id)
    else:
        prompt = PROMPTS["natural"].format(query=user_input)
        result_text = call_gemini(prompt)
        save_feedback(user_input, intent, result_text, us_id)
        save_history(user_input, intent, result_text, us_id)
        return result_text, intent

# --- Main loop ---
def main():
    us_id = input("Nhập us_id của bạn: ").strip() or "US001"
    print("Vịt sẵn sàng! Gõ 'exit' để thoát.\n")
    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Tạm biệt nhé!")
            break
        result, intent = run_ai(user_input, us_id)
        print(f"\n=== Intent: {intent} ===")
        print("Vịt:", result, "\n")

if __name__ == "__main__":
    main()
