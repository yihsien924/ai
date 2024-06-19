import os
import sys
from groq import Groq

# 從命令列參數中取得語言設定，並轉換為小寫
language = sys.argv[1].lower()

# 根據語言設定組合問題，請求用中文或英文回答
if language == 'ch':
    question = " ".join(sys.argv[2:]) + "請用中文回答"
elif language == 'en':
    question = " ".join(sys.argv[2:]) + "請用英文回答"

# 印出所選語言和問題內容
print(f"選擇的語言：{language}")
print("問題：", question)

# 初始化 Groq 客戶端，使用特定的 API 金鑰
client = Groq(
    api_key="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",
)

# 發送聊天完成請求，將問題傳遞給模型處理
chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": question,
        }
    ],
    model="llama3-8b-8192",
)

# 印出模型返回的回答內容
print(chat_completion.choices[0].message.content)
