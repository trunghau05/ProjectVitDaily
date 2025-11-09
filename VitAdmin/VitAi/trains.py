import json
import re
import time
import requests
from google import genai
from .utils import *

client = genai.Client(api_key="AIzaSyD09X-xh9HkghMk4eImIHXrqPw9Uy5hcIA") 

PROMPTS = {
    "summary": (
        "Bạn là Vịt, một chatbot hỗ trợ quản lý ghi chú và công việc. "
        "Có thể thêm các kiến thức chuyên sâu có liên quan để người dùng nắm bắt. "
        "Người dùng muốn tóm tắt nội dung. Hãy trả lời tự nhiên, rõ ràng, dễ hiểu, giống người nhất. "
        "Không sử dụng các ký tự đặt biệt vào câu trả lời như: **,*,#,$ mà thay vào đó dùng các dấu - và + để thể hiện ý cha và con, nhớ cách dòng để dễ nhìn ."
        "Tóm tắt các ý chính của ghi chú được chỉ định trong JSON sau:\n{data}"
    ),
    "search": (
        "Bạn là Vịt, một chatbot hỗ trợ quản lý ghi chú và công việc. "
        "Người dùng muốn tìm ghi chú theo từ khóa '{query}'. "
        "Trả lời tự nhiên, vui tính, đừng nhắc đến việc chỉ xuất JSON cho người dùng nhưng chỉ xuất đúng JSON các ghi chú khớp:\n{data}"
    ),
    "detail": (
        "Bạn là Vịt, một chatbot quản lý ghi chú. "
        "Người dùng muốn xem chi tiết. Hãy trả lời tự nhiên, mô tả chi tiết nhưng rõ ràng. "
        "JSON dữ liệu:\n{data}"
    ),
    "translate": (
        "Bạn là Vịt, một chatbot quản lý ghi chú. "
        "Chỉ dịch toàn bộ ghi chú khi người dùng yêu cầu dịch toàn bộ danh sách ghi chú"
        "Người dùng muốn dịch các ghi chú theo id, theo ghi chú được chỉ định, theo từ khóa '{query}'. "
        "Người dùng muốn dịch sang tiếng Anh. Trả lời tự nhiên, vui tính, đừng nhắc đến việc chỉ xuất JSON cho người dùng nhưng chỉ xuất đúng JSON các ghi chú khớp, dưới dạng JSON đã dịch:\n{data}"
    ),
    "analyze": (
        "Bạn là Vịt, một chatbot quản lý ghi chú. "
        "Người dùng muốn phân tích nội dung. Trả lời tự nhiên bằng tiếng Việt, nêu các ý chính, "
        "gợi ý bổ sung hoặc chỉnh sửa phù hợp, giống như phân tích của một người:\n{data}"
    ),
    "natural": (
        "Bạn là Vịt, một chatbot hỗ trợ quản lý ghi chú và công việc. "
        "Người dùng nói: '{query}'. Hãy trả lời tự nhiên, thân thiện và phù hợp với ngữ cảnh. "
        "Trả lời dạng văn bản, không có ký tự gì đặt biệt. "
        "Không sử dụng các ký tự đặt biệt vào câu trả lời như: **,*,#,$ mà thay vào đó dùng các dấu - và + để thể hiện ý cha và con, nhớ cách dòng để dễ nhìn ."
        "Nếu cần, Vịt có thể hỏi thêm để làm rõ ý muốn của người dùng."
        "Không thêm ký tự đặt biệt như emoji"
    ),
    "create": (
        "Bạn là Vịt, một chatbot quản lý ghi chú. "
        "Người dùng muốn tạo ghi chú mới với nội dung: '{query}'. "
        "Hãy trả về **chỉ JSON** với các trường chính xác của backend Django model Note: "
        "nt_title, nt_subtitle nếu có, nt_content, nt_img='', nt_pdf='', nt_date (YYYY-MM-DD), us_id='US001'. "
        "Không thêm bình luận hay văn bản ngoài JSON. "
    ),
    "create_multi": (
        "Bạn là Vịt, một chatbot quản lý ghi chú. "
        "Người dùng muốn tạo {n} ghi chú mới với nội dung: '{query}'. "
        "Hãy trả về **chỉ JSON** dạng mảng với {n} phần tử, mỗi phần tử gồm các trường của backend Django model Note: "
        "nt_title, nt_subtitle nếu có, nt_content, nt_img='', nt_pdf='', nt_date (YYYY-MM-DD), us_id='US001'. "
        "Không thêm bình luận hay văn bản ngoài JSON."
    )
}

INTENTS = {
    "summary": ["tóm tắt", "ngắn gọn", "summary"],
    "search": ["tìm", "search", "tra cứu", "lấy"],
    "detail": ["chi tiết", "full", "đầy đủ"],
    "translate": ["dịch", "translate", "english"],
    "analyze": ["phân tích", "analyze", "topic"],
    "create": ["tạo", "tạo mới", "create", "new note", "thêm mới", "add", "thêm ghi chú", "tạo ghi chú"],
    "feedback": ["feedback", "sai", "không đúng", "nhầm", "góp ý", "lỗi", "đừng", "không cần", "bỏ qua", "từ giờ", "đừng hỏi"],  
}

API_ENDPOINTS = {
    "summary": "http://127.0.0.1:8000/note/note-list/?us_id=US001",
    "search": "http://127.0.0.1:8000/note/note-list/?us_id=US001",
    "detail": "http://127.0.0.1:8000/note/note-list/?us_id=US001",
    "translate": "http://127.0.0.1:8000/note/note-list/?us_id=US001",
    "analyze": "http://127.0.0.1:8000/note/note-list/?us_id=US001",
    "create": "http://127.0.0.1:8000/note/add/",
}

def detect_intent(user_input: str):
    user_input_lower = user_input.lower().strip()
    for intent, keywords in INTENTS.items():
        if any(kw.lower() in user_input_lower for kw in keywords):
            return intent
    return "natural"

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

def run_ai(user_input: str):
    intent = detect_intent(user_input)
    result_text = ""
    
    history_context = get_last_user_input()  
    feedback_context = get_feedback_user_inputs() 
    user_input_with_context = ""

    if feedback_context:
        user_input_with_context += "\n".join(feedback_context) + "\n\n"
    if history_context:
        user_input_with_context += history_context + "\n\n"

    user_input_with_context += f"{user_input}"

    if intent in ["summary", "search", "detail", "translate", "analyze"]:
        api_url = API_ENDPOINTS[intent]
        try:
            resp = requests.get(api_url)
            data = resp.json()
        except Exception as e:
            result_text = f"Lỗi khi gọi API: {e}"
            save_history(user_input, intent, result_text)
            return result_text, intent

        prompt = PROMPTS[intent].format(
            data=json.dumps(data, ensure_ascii=False, indent=2),
            query=user_input_with_context
        )
        result_text = call_gemini(prompt)

    elif intent == "create":
        match = re.search(r'tạo (\d+) ghi chú', user_input.lower())
        if match:
            n = int(match.group(1))
            prompt = PROMPTS["create_multi"].format(query=user_input_with_context, n=n)
        else:
            prompt = PROMPTS["create"].format(query=user_input_with_context)

        generated_json = call_gemini(prompt)
        generated_json_clean = generated_json.strip()

        if generated_json_clean.startswith("```"):
            generated_json_clean = "\n".join(generated_json_clean.split("\n")[1:-1])

        try:
            note_json = json.loads(generated_json_clean)
        except Exception as e:
            result_text = f"Lỗi khi phân tích JSON từ Gemini: {e}\nGenerated text: {generated_json}"
            save_history(user_input, intent, result_text)
            return result_text, intent

        api_url = API_ENDPOINTS["create"]
        try:
            if isinstance(note_json, list):
                success_count = 0
                for nj in note_json:
                    resp = requests.post(api_url, json=nj)
                    if resp.status_code in [200, 201]:
                        success_count += 1
                result_text = f"{success_count}/{len(note_json)} ghi chú đã được tạo thành công!"
            else:
                resp = requests.post(api_url, json=note_json)
                if resp.status_code in [200, 201]:
                    result_text = f"Ghi chú đã được tạo thành công: {resp.json()}"
                else:
                    result_text = f"Lỗi khi tạo ghi chú, status_code={resp.status_code}, response={resp.text}"
        except Exception as e:
            result_text = f"Lỗi khi gọi API POST: {e}"

    else:  
        prompt = PROMPTS["natural"].format(query=user_input_with_context)
        result_text = call_gemini(prompt)

    save_feedback(user_input, intent, result_text)
    save_history(user_input, intent, result_text)

    return result_text, intent

def main():
    print("Vịt sẵn sàng! Gõ 'exit' để thoát.\n")
    while True:
        user_input = input("Bạn: ")
        if user_input.lower() in ["exit", "quit", "bye"]:
            print("Tạm biệt nhé!")
            break
        result, intent = run_ai(user_input)
        print(f"\n=== Intent: {intent} ===")
        print("Vịt:", result, "\n")

if __name__ == "__main__":
    main()
