from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage, ImageSendMessage
import random

app = Flask(__name__)

# Channel Access Token 和 Channel Secret
line_bot_api = LineBotApi('yOBTbdC80uJmcmPQDFW+20TWectJYFzIkXoThbUVsi0Et9jQXecQWnDoK4UzUShO1Q+HoFNimovw1X+zqAhGbaREvHsKm/f0iLIJn9/sP0UWe4I884BgKV+iC5TUKIQRRPA96p02d7OJjoMdnCioowdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('29f84578040cbbb8466a96bcf2c02972')

# 定義MBTI問題
mbti_questions_full = [
    "1. 當你參加一個聚會時，你更傾向於：\na) 與很多人交流，感覺充滿能量\nb) 與幾個熟悉的朋友深度交談，感覺放鬆",
    "2. 當你面對新任務時，你更傾向於：\na) 注意具體的細節和實際步驟\nb) 想像整體的可能性和未來的結果",
    "3. 當你做決定時，你更傾向於：\na) 根據邏輯和客觀事實\nb) 根據個人價值和他人感受來決定",
    "4. 當你安排日程時，你更傾向於：\na) 提前計劃，喜歡有條理和結構\nb) 隨機應變，喜歡靈活和自發性",
    "5. 當你在學習新知識時，你更喜歡：\na) 實際應用和現實世界的例子\nb) 理論概念和抽象的思考",
    "6. 當你與人交流時，你更傾向於：\na) 直接而坦率\nb) 委婉而顧及他人感受",
    "7. 當你處理問題時，你更傾向於：\na) 以冷静、理性的方式分析和解決\nb) 以同情心和情感的方式理解和處理",
    "8. 當你處於壓力下時，你更傾向於：\na) 維持日常的常規和結構\nb) 尋找新的方法和變通",
    "9. 當你與他人合作時，你更傾向於：\na) 明確的角色和責任分配\nb) 開放的溝通和靈活的合作方式",
    "10. 當你考慮未來時，你更傾向於：\na) 專注於可以預測和控制的事情\nb) 期待未知和新奇的可能性",
    "11. 當你處理工作時，你更傾向於：\na) 根據計劃和日程完成\nb) 按照當時的靈感和情況完成",
    "12. 當你做事情時，你更喜歡：\na) 按部就班地進行\nb) 嘗試不同的方法",
    "13. 當你學習新知識時，你更傾向於：\na) 關注事實和數據\nb) 關注理論和理念",
    "14. 當你表達自己的觀點時，你更喜歡：\na) 直接明了\nb) 委婉含蓄",
    "15. 當你處理衝突時，你更傾向於：\na) 理智冷靜地面對\nb) 理解和考慮他人的感受",
    "16. 當你計劃未來時，你更喜歡：\na) 詳細計劃和安排\nb) 保持靈活和開放的選擇",
    "17. 當你面對新挑戰時，你更喜歡：\na) 依靠過去的經驗和知識\nb) 探索新的方法和創意",
    "18. 當你與他人溝通時，你更傾向於：\na) 直截了當\nb) 考慮他人的感受",
    "19. 當你處理事情時，你更喜歡：\na) 根據邏輯和事實\nb) 根據價值觀和感受",
    "20. 當你安排活動時，你更傾向於：\na) 預先計劃和組織\nb) 即興發揮和變通",
    "21. 當你做決策時，你更重視：\na) 客觀的數據和信息\nb) 主觀的感受和直覺",
    "22. 當你表達自己時，你更傾向於：\na) 直率和直接\nb) 委婉和間接",
    "23. 當你面對壓力時，你更傾向於：\na) 保持穩定和一致\nb) 尋找新的應對方法",
    "24. 當你與他人合作時，你更喜歡：\na) 明確的分工和責任\nb) 開放的交流和合作",
    "25. 當你處理問題時，你更傾向於：\na) 根據經驗和知識\nb) 探索新的可能性",
    "26. 當你學習新東西時，你更傾向於：\na) 關注具體的事實\nb) 關注整體的概念",
    "27. 當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和含蓄",
    "28. 當你與他人交流時，你更喜歡：\na) 講述事實和細節\nb) 討論想法和觀點",
    "29. 當你做決策時，你更依賴：\na) 邏輯和事實\nb) 感受和價值觀",
    "30. 當你處理日常事務時，你更傾向於：\na) 按計劃進行\nb) 靈活變通",
    "31. 當你面對挑戰時，你更傾向於：\na) 使用已知的方法\nb) 探索新的途徑",
    "32. 當你與他人溝通時，你更傾向於：\na) 直截了當\nb) 委婉和考慮他人",
    "33. 當你安排日程時，你更傾向於：\na) 提前計劃和準備\nb) 隨機應變和變通",
    "34. 當你面對新任務時，你更喜歡：\na) 運用過去的經驗\nb) 探索新的方法",
    "35. 當你學習新知識時，你更傾向於：\na) 聚焦於具體的細節\nb) 聚焦於概念和理論",
    "36. 當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和考慮他人",
    "37. 當你處理問題時，你更傾向於：\na) 邏輯分析\nb) 情感理解",
    "38. 當你安排活動時，你更喜歡：\na) 提前計劃和組織\nb) 靈活和即興發揮",
    "39. 當你做決策時，你更依賴：\na) 邏輯和事實\nb) 感受和價值觀",
    "40. 當你面對壓力時，你更傾向於：\na) 維持穩定\nb) 尋找新方法",
    "41. 當你與他人合作時，你更傾向於：\na) 明確的分工\nb) 開放的合作",
    "42. 當你處理問題時，你更傾向於：\na) 使用已知的方法\nb) 探索新的可能性",
    "43. 當你學習新知識時，你更喜歡：\na) 關注具體事實\nb) 關注整體概念",
    "44. 當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和含蓄",
    "45. 當你與他人交流時，你更喜歡：\na) 講述事實\nb) 討論想法",
    "46. 當你做決策時，你更依賴：\na) 邏輯和事實\nb) 感受和價值觀",
    "47. 當你處理日常事務時，你更傾向於：\na) 按計劃進行\nb) 靈活變通",
    "48. 當你面對挑戰時，你更傾向於：\na) 使用已知的方法\nb) 探索新途徑",
    "49. 當你與他人溝通時，你更傾向於：\na) 直截了當\nb) 委婉和考慮他人",
    "50. 當你安排日程時，你更傾向於：\na) 提前計劃和準備\nb) 隨機應變和變通",
    "51. 當你面對新任務時，你更喜歡：\na) 運用過去的經驗\nb) 探索新的方法",
    "52. 當你學習新知識時，你更喜歡：\na) 聚焦於具體的細節\nb) 聚焦於概念和理論",
    "53. 當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和考慮他人",
    "54. 當你處理問題時，你更傾向於：\na) 邏輯分析\nb) 情感理解",
    "55. 當你安排活動時，你更喜歡：\na) 提前計劃和組織\nb) 靈活和即興發揮",
    "56. 當你做決策時，你更依賴：\na) 邏輯和事實\nb) 感受和價值觀",
    "57. 當你面對壓力時，你更傾向於：\na) 維持穩定\nb) 尋找新方法",
    "58. 當你與他人合作時，你更傾向於：\na) 明確的分工\nb) 開放的合作",
    "59. 當你處理問題時，你更傾向於：\na) 使用已知的方法\nb) 探索新的可能性",
    "60. 當你學習新知識時，你更喜歡：\na) 關注具體事實\nb) 關注整體概念",
    "61. 當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和含蓄",
    "62. 當你與他人交流時，你更喜歡：\na) 講述事實\nb) 討論想法",
    "63. 當你做決策時，你更依賴：\na) 邏輯和事實\nb) 感受和價值觀",
    "64. 當你處理日常事務時，你更傾向於：\na) 按計劃進行\nb) 靈活變通",
    "65. 當你面對挑戰時，你更傾向於：\na) 使用已知的方法\nb) 探索新途徑",
    "66. 當你與他人溝通時，你更傾向於：\na) 直截了當\nb) 委婉和考慮他人",
    "67. 當你安排日程時，你更傾向於：\na) 提前計劃和準備\nb) 隨機應變和變通",
    "68. 當你面對新任務時，你更喜歡：\na) 運用過去的經驗\nb) 探索新的方法",
    "69. 當你學習新知識時，你更喜歡：\na) 聚焦於具體的細節\nb) 聚焦於概念和理論",
    "70. 當你做事情時，你更傾向於：\na) 直接和明了\nb) 委婉和考慮他人"
]



# 各维度问题索引
ei_questions = [0, 7, 14, 21, 28, 35, 42, 49, 56, 63]
sn_questions = [1, 2, 8, 9, 15, 16, 22, 23, 29, 30, 36, 37, 43, 44, 50, 51, 57, 58, 64, 65]
tf_questions = [3, 4, 10, 11, 17, 18, 24, 25, 31, 32, 38, 39, 45, 46, 52, 53, 59, 60, 66, 67]
jp_questions = [5, 6, 12, 13, 19, 20, 26, 27, 33, 34, 40, 41, 47, 48, 54, 55, 61, 62, 68, 69]

def select_random_questions():
    selected_ei_questions = random.sample([mbti_questions_full[i] for i in ei_questions], 2)
    selected_sn_questions = random.sample([mbti_questions_full[i] for i in sn_questions], 4)
    selected_tf_questions = random.sample([mbti_questions_full[i] for i in tf_questions], 4)
    selected_jp_questions = random.sample([mbti_questions_full[i] for i in jp_questions], 4)

    return selected_ei_questions + selected_sn_questions + selected_tf_questions + selected_jp_questions

mbti_questions = select_random_questions()

# 用户回答存储
mbti_user_answers = {}

# MBTI 结果和描述及對應圖片URL
mbti_results = {
    "INTJ": {
        "description": "你的MBTI為INTJ，你可能是一個獨立、思想深邃的人，善於分析和解決問題。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2815.JPG?raw=true"
    },
    "INTP": {
        "description": "你的MBTI為INTP，你可能是一個理性、好奇的人，喜歡獨自探索和思考。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2814.JPG?raw=true"
    },
    "ENTJ": {
        "description": "你的MBTI為ENTJ，你可能是一個果斷、領導能力強的人，善於組織和規劃。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2813.JPG?raw=true"
    },
    "ENTP": {
        "description": "你的MBTI為ENTP，你可能是一個充滿創意、善於挑戰傳統的人，喜歡嘗試新的事物。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2812.JPG?raw=true"
    },
    "INFJ": {
        "description": "你的MBTI為INFJ，你可能是一個理想主義者，具有強烈的直覺和同情心。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2811.JPG?raw=true"
    },
    "INFP": {
        "description": "你的MBTI為INFP，你可能是一個理想主義者，關心他人的感受和內心世界。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2810.JPG?raw=true"
    },
    "ENFJ": {
        "description": "你的MBTI為ENFJ，你可能是一個富有魅力和感染力的領袖，善於激勵和引導他人。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2809.JPG?raw=true"
    },
    "ENFP": {
        "description": "你的MBTI為ENFP，你可能是一個充滿熱情和創造力的人，喜歡探索新的可能性。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2808.JPG?raw=true"
    },
    "ISTJ": {
        "description": "你的MBTI為ISTJ，你可能是一個實事求是、責任感強的人，重視傳統和穩定。",
        "image_url": "https://example.com/istj.png"
    },
    "ISFJ": {
        "description": "你的MBTI為ISFJ，你可能是一個細心周到、富有同情心的人，重視和諧和合作。",
        "image_url": "https://example.com/isfj.png"
    },
    "ESTJ": {
        "description": "你的MBTI為ESTJ，你可能是一個實幹型的人，喜歡組織和管理工作，注重效率和結果。",
        "image_url": "https://github.com/EthanChu890515/linebot_openai/blob/master/IMG_2816.JPG?raw=true"
    },
    "ESFJ": {
        "description": "你的MBTI為ESFJ，你可能是一個熱心助人、樂於奉獻的人，重視他人的需求和感受。",
        "image_url": "https://example.com/esfj.png"
    },
    "ISTP": {
        "description": "你的MBTI為ISTP，你可能是一個獨立、實用的人，喜歡解決具體的問題和挑戰。",
        "image_url": "https://example.com/istp.png"
    },
    "ISFP": {
        "description": "你的MBTI為ISFP，你可能是一個溫和、靈活的人，喜歡追求個人的自由和創造力。",
        "image_url": "https://example.com/isfp.png"
    },
    "ESTP": {
        "description": "你的MBTI為ESTP，你可能是一個熱愛冒險、富有活力的人，喜歡嘗試新的經歷和挑戰。",
        "image_url": "https://example.com/estp.png"
    },
    "ESFP": {
        "description": "你的MBTI為ESFP，你可能是一個活潑、熱情的人，喜歡與他人互動和享受生活。",
        "image_url": "https://example.com/esfp.png"
    }
}

@app.route("/callback", methods=['POST'])
def callback():
    # 获取请求头中的签名
    signature = request.headers['X-Line-Signature']

    # 获取请求正文
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # 处理 webhook 请求
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text.strip().lower()

    if user_id not in mbti_user_answers:
        mbti_user_answers[user_id] = {
            "current_question_index": 0,
            "answers": []
        }

    user_data = mbti_user_answers[user_id]
    current_question_index = user_data["current_question_index"]

    if current_question_index < len(mbti_questions):
        # 存储用户回答
        if user_message in ['a', 'b']:
            user_data["answers"].append(user_message)
            user_data["current_question_index"] += 1
            current_question_index += 1

        # 发送下一个问题
        if current_question_index < len(mbti_questions):
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=mbti_questions[current_question_index])
            )
        else:
            # 所有问题回答完毕，计算MBTI结果
            mbti_result = calculate_mbti_result(user_data["answers"])
            result_description = mbti_results[mbti_result]["description"]
            result_image_url = mbti_results[mbti_result]["image_url"]

            line_bot_api.reply_message(
                event.reply_token,
                [
                    TextSendMessage(text=f"你的MBTI測試結果是：{mbti_result}\n{result_description}"),
                    ImageSendMessage(original_content_url=result_image_url, preview_image_url=result_image_url)
                ]
            )

            # 清除用户数据
            del mbti_user_answers[user_id]
    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="请回答问题 'a' 或 'b'。")
        )

def calculate_mbti_result(answers):
    ei_score = sum(1 if answers[i] == 'a' else -1 for i in range(2))
    sn_score = sum(1 if answers[i] == 'a' else -1 for i in range(2, 6))
    tf_score = sum(1 if answers[i] == 'a' else -1 for i in range(6, 10))
    jp_score = sum(1 if answers[i] == 'a' else -1 for i in range(10, 14))

    ei = 'E' if ei_score > 0 else 'I'
    sn = 'S' if sn_score > 0 else 'N'
    tf = 'T' if tf_score > 0 else 'F'
    jp = 'J' if jp_score > 0 else 'P'

    return f"{ei}{sn}{tf}{jp}"

if __name__ == "__main__":
    app.run()