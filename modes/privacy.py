import streamlit as st

def page_privacy():
    st.title(":primary[Privacy Statement]")

    st.write("""
            - **Your chat files are never stored by chat2playlist**. They are processed in memory and discarded, and only the extracted URL information is used.
            - Saving a permalink saves only a unique link ID, and the final playlist link, or list of extracted music information. No personal information, either from the uploaded file or about your device, is stored.
            - This is an open source project - you can view the [source code](https://github.com/ajhenne/chat2playlist) to see how your data is handled. 
             
            External services:
            - This tool is built on Streamlit. You may view their [privacy policy](https://streamlit.io/privacy-policy) to see how they handle data.
            - Odseli API is used to convert links between different services and/or obtain song metadata. Only the extracted music is sent to their API.
            - Google Sheets is used as a database to store permalink IDs and playlist information.
            """)