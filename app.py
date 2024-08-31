import validators
import streamlit as st
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from langchain.chains.summarize import load_summarize_chain
from langchain_community.document_loaders import YoutubeLoader,UnstructuredURLLoader


# Srreamlit App

st.set_page_config(page_title="Langchain: URL Summarizer",page_icon="🦜")
st.title("🦜LangChain: URL Summarizer")
st.subheader('Summarize Youtube or Website URL')



# Get Groq API Key and url to be summarized
with st.sidebar:
    groq_api_key=st.text_input("Groq API Key",type="password")


prompt_template="""
Provide a Summary of the following content in 300 words:
Content:{text}

"""
prompt=PromptTemplate(template=prompt_template,input_variables=['text'])


generic_url=st.text_input("Type the URL","https://docs.smith.langchain.com/")

if st.button("Summarize"):
    if not groq_api_key.strip() or not generic_url.strip():
        st.error("Please provide the information to get started")
    elif not validators.url(generic_url):
        st.error("Please enter a valid Url. It can may be a YT video url or website url")
    else:
        try:
            with st.spinner("Waiting..."):
                ## Load the website or yt video data
                llm=ChatGroq(model="Gemma-7b-It",groq_api_key=groq_api_key)
                if "youtube.com" in generic_url:
                    st.write("Working")
                    loader = YoutubeLoader.from_youtube_url(youtube_url=generic_url, add_video_info=True)
                else:
                    loader=UnstructuredURLLoader(urls=[generic_url],ssl_verify=False
                                                 )
                docs=loader.load()
                
                ## Chain for Summarization
                chain=load_summarize_chain(llm,chain_type="stuff",prompt=prompt)
                output_summary=chain.run(docs)

                st.success(output_summary)
        except Exception as e:
            st.exception(f"Exception:{e}")

