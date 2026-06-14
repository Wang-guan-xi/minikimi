import streamlit
from langchain.memory import ConversationBufferMemory

from utils import get_chat_response

streamlit.title("💬 mini版kimi")
with streamlit.sidebar:
    openai_api_key=streamlit.text_input("请输入MOONSHOT API秘钥：",type="password")
    streamlit.markdown("[获取MOONSHOT API秘钥] https://platform.moonshot.cn")

if "memory" not in streamlit.session_state:
    streamlit.session_state["memory"]=ConversationBufferMemory(return_messages=True)
    streamlit.session_state["messages"]=[{"role":"ai","content":"你好，我是你的AI助手"}]

for message in streamlit.session_state["messages"]:
    streamlit.chat_message(message["role"]).write(message["content"])

prompt=streamlit.chat_input()
if prompt:
    if not openai_api_key:
        streamlit.info("请输入MOONSHOT API秘钥")
        streamlit.stop()
    streamlit.session_state["messages"].append({"role":"human","content":prompt})
    streamlit.chat_message("human").write(prompt)

    with streamlit.spinner("AI正在思考中，请稍等..."):
        response=get_chat_response(prompt,streamlit.session_state["memory"],openai_api_key)

    msg={"role":"ai","content":response}
    streamlit.session_state["messages"].append(msg)
    streamlit.chat_message("ai").write(msg["content"])


