from flask import Flask, request, jsonify
from openai import OpenAI
from flask_cors import CORS
import os
os.environ["HTTP_PROXY"] = "127.0.0.1:7897"
os.environ["HTTPS_PROXY"] = "127.0.0.1:7897"
os.environ["OPENAI_API_KEY"] = "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"

# 初始化 Flask 应用
app = Flask(__name__)
# 启用 CORS 支持
CORS(app)
client = OpenAI()



@app.route('/chat', methods=['POST'])
def handle_post_request():
    try:
        # 获取请求数据
        request_data = request.get_json()

        if not request_data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        # 处理请求数据
        message = request_data.get("message", "")
        messageList = request_data.get("messageList", "")

        completion = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messageList
        )

        # 模拟返回处理结果
        response_data = {
            "message": "Data received successfully",
            "content":completion.choices[0].message.content
        }
        return jsonify(response_data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)