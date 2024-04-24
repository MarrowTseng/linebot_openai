from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi(os.getenv('CHANNEL_ACCESS_TOKEN'))
# Channel Secret
handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))

# 定義MBTI問題和答案
mbti_questions = {
    "E": "你更喜歡關注外在世界（外向 - E）還是你自己的內在世界（內向 - I）？",
    "S": "你更注重通過五官感官獲得的信息（感知 - S），還是你更注重在接收的信息中看到的模式和可能性（直覺 - N）？",
    "T": "在做決定時，你更傾向於首先看邏輯和一致性（思維 - T），還是首先看人和特殊情況（情感 - F）？",
    "J": "在處理外部世界時，你更喜歡做出決定（判斷 - J）還是更喜歡保持對新信息和選擇的開放（感知 - P）？"
}

# 全局變量來存儲用戶的答案
user_answers = {}

# 問題回答處理
def handle_mbti_response(event):
    answer = event.message.text.upper()
    question_key = list(mbti_questions.keys())[len(user_answers)]
    if answer in ['E', 'I', 'S', 'N', 'T', 'F', 'J', 'P']:
        user_answers[question_key] = answer
        if len(user_answers) < len(mbti_questions):
            ask_mbti_question(event)
        else:
            analyze_mbti_type(event)
    else:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text="請回答以下選項中的一個：E、I、S、N、T、F、J、P"))

# MBTI類型分析
def analyze_mbti_type(event):
    mbti_type = ""
    for key in mbti_questions.keys():
        mbti_type += user_answers[key]
    result_message = f"你的MBTI人格類型是{mbti_type}。"
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=result_message))

# 處理MBTI測試的開始
@handler.add(MessageEvent, message=TextMessage)
def start_mbti_test(event):
    if event.message.text.lower() == "開始mbti測試":
        ask_mbti_question(event)

# 處理MBTI測試期間的使用者回答
@handler.add(MessageEvent, message=TextMessage)
def handle_mbti_test(event):
    if event.message.text.lower() != "開始mbti測試" and len(user_answers) < len(mbti_questions):
        handle_mbti_response(event)

# 問題回答處理
def ask_mbti_question(event):
    question_key = list(mbti_questions.keys())[len(user_answers)]
    question = mbti_questions[question_key]
    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=question))

# 其他事件處理
# 在這裡添加現有的事件處理程序...

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 運行Flask應用
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
