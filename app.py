from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    PushMessageRequest,   #匯入
    BroadcastRequest,   #匯入
    MulticastRequest,   #匯入
    TextMessage
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)
import os
app = Flask(__name__)

configuration = Configuration(access_token=os.getenv('CHANNEL_ACCESS_TOKEN'))
line_handler = WebhookHandler(os.getenv('CHANNEL_SECRET'))
##
from bs4 import BeautifulSoup
import requests #導入雙套件

while True:
url = 'http://icwanglearn.blogspot.com' #變數設網址
resp = requests.get(url)    #設定變數 是取得url內容
soup = BeauyifulSoup(resp,'htmp.parser')
ul = soup.find=('htmp.parser','D(f)' Fld(c) Flw(w) H(192px) Mx(-16px'))
lilist = ul.find_all('li')
      print(len(lilist))



with open('icwang.html','w',encoding='utf-8') as fobj: #和打開檔案 寫入 編碼 給予暱稱
    fobj.write(resp.text) #抓回來之後寫入
    
##

@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

# 訊息事件
@line_handler.add(MessageEvent, message=TextMessageContent)
def message_text(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        # Reply message

        line_bot_api.reply_message(                         #訊息串接api
            ReplyMessageRequest(
                reply_token=event.reply_token,
                messages=[TextMessage(text ='reply message0')]
            )
        )

        result = line_bot_api.reply_message_with_http_info(     #傳訊息後回覆內容
             ReplyMessageRequest(
                 reply_token=event.reply_token,
                 messages=[TextMessage(text = "reply message with http info")]
             )
         )

         #Push message          #指定傳送對象給誰
         #line_bot_api.push_message_with_http_info(
           #  PushMessageRequest(
            #     to=event.source.user_id,
             #    messages=[TextMessage(text='PUSH!')]
             #)
         #)
#
        # Broadcast message     #簡單傳送沒差異
        # line_bot_api.broadcast_with_http_info(
        #     BroadcastRequest(
        #         messages=[TextMessage(text='BROADCAST!')]
        #     )
        # )

        



if __name__ == "__main__":
    app.run()
