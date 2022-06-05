from flask import Flask, request, abort
from linebot import exceptions
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import configparser


app = Flask(__name__)

config = configparser.ConfigParser()
config.read('config.ini')

line_bot_api = LineBotApi(config.get('line-bot', 'channel_access_token'))
handler = WebhookHandler(config.get('line-bot', 'channel_secret'))


@app.route("/", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=(TextMessage, ImageMessage))
def handle_message(event):
    if isinstance(event.message, TextMessage):

        user_id = event.source.user_id

        replymessage = event.message.text  # 使用者所傳送的訊息

        if replymessage == '我帥嗎':
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="你好帥")
            )
        elif replymessage == '你是誰':
            line_bot_api.reply_message(
                event.reply_token,
                ImageSendMessage(
                    original_content_url='https://imgur.com/o7Lqlmp.jpg',
                    preview_image_url='https://imgur.com/Rm7inOG.jpg'
                )
            )


@ handler.add(FollowEvent)
def handle_follow(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text="你好，這是我的LINE機器人",)
    )


if __name__ == "__main__":
    app.run()
