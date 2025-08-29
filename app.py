import streamlit as st  
from debate import debate,teamConfig
import asyncio
st.title("Agent Debate!")

topic=st.text_input("Enter the topic of the debate","shall US government ban tiktok?")

clicked=st.button('Start',type='primary')
chat=st.container()

if clicked:
    chat.empty()
    async def main():
        team= await teamConfig(topic)
        with chat:
             async for message in debate(team):
                    if message.startswith("Jane"):
                         with st.chat_message(name="Jane",avatar="🤖"):
                              st.write(message)
                    elif message.startswith("John"):  #thumbs up emoji
                         with st.chat_message(name="John",avatar="👍"):
                              st.write(message)
                    elif message.startswith("Jack"):  #thumbs down emoji
                         with st.chat_message(name="Jack",avatar="👎"):
                                st.write(message)   
    
    asyncio.run(main())

    st.balloons()