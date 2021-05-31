import streamlit as st
import plotly.figure_factory as ff
from PIL import Image
import requests
import numpy as np

# setting page title
st.set_page_config(page_title="Discerning Deepfake Videos")

# loading CSS file 
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        
local_css("style.css")

# defining chart method
def show_chart(value):
    import plotly.graph_objects as go
    import plotly.figure_factory as ff
    
    y=np.arange(start=0.0, stop=1.0, step=0.1)
    color=np.array(['rgb(255,255,255)']*y.shape[0])
    color[y<0.2]='rgb(204,204, 205)'
    color[y>=0.2]='rgb(130, 0, 0)'
    
    bars = []
    data=[dict(type='bar',
       y=y,
       marker=dict(color=color.tolist()) 
      )]

    bars.append(go.Bar(x=[value],
                       y=['Real'],
                       name='Real',
                       orientation='h',
                       marker={'color': 'green'}))
    bars.append(go.Bar(x=[1-value],
                       y=['Fake'],
                       name='Fake',
                       orientation='h',
                       marker={'color': 'red'}))
    
    return go.FigureWidget(data=bars)


# defining sidebar 
with st.sidebar:
    URL = st.text_input("Server URL:", "")
    threshold = st.number_input("Threshold Value:", min_value=0.0, max_value=1.0, step=0.01, value=0.5)

# defining page layout
header_logo, header_text = st.beta_columns((1, 4))
video_input = st.beta_container()
video_frame = st.beta_container()
video_output = st.empty()
video_output_text = st.beta_container()

# setting header logo 
with header_logo:
    logo = Image.open("logo.png")
    st.image(logo, use_column_width=True)

# setting header text 
with header_text:
    header_string = """
                <h1 style='
                    text-align: center;
                    font-family: Arial;'
                >
                Discerning Deepfake Videos
                </h1>
                """
    st.markdown(header_string, unsafe_allow_html=True) 

# reading video as input from the user
with video_input:
    video_file = st.file_uploader("Upload video file:", type = ["mp4"])

# if user inputs video file
if video_file is not None:
    file_details = {"FileName":video_file.name}
    print(file_details)
    
    # display video
    with video_frame: 
        st.video(video_file)
    
    # displaying processing
    with video_output:
        loading_string = """
                <h1 
                class='blinking'
                style='text-align: center; color: yellow;'
                >
                Processing...
                </h1>
                """
        st.markdown(loading_string, unsafe_allow_html=True) 
    
    # sending request to server 
    BACKEND_URL = f"{URL}/demo/"
    files = {
        'vid': (video_file.name, video_file, "multipart/form-data")
    }
    response = requests.post(BACKEND_URL, files=files)
    result = response.json()
    print(result)
    
    # clearing loading message 
    # processing_frame = st.empty() 
    # del process
    
    # displaying results
    with video_output: 
        st.markdown("<span></span>", unsafe_allow_html=True)
    
    with video_output_text: 
        st.markdown("<h2>Result:</h2>", unsafe_allow_html=True)
        isReal = result['prediction'] > threshold
        if isReal: 
            result_string = """
                <h4 
                style='text-align: center; color: green; font-size: 60px;'
                >
                &#10004; Real
                </h4>
                """
        else:
            result_string = """
                <h4 
                style='text-align: center; color: red; font-size: 60px;'
                >
                &#10006; Deepfake
                </h4>
                """
        st.markdown(result_string, unsafe_allow_html=True)
        st.plotly_chart(show_chart(round(result['prediction'], 2)), use_container_width=True)
    
    
    
    
        
    
    

    
    