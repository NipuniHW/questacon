import streamlit as st
from connection import Connection
import random
import time
from utils import get_tags_list
# ip='172.16.35.227' # questacon ip

# Play an animation
def animation(button_name):
    try:
        st.session_state.behavior_mng_service.stopAllBehaviors()
        st.session_state.behavior_mng_service.startBehavior("questacon/"+button_name)
    except RuntimeError as e:
        st.error(f"Got runtime error as: {e}\nTry to reconnect")
# Function to play a random animation
def play_random_animation():
    animations = ["space_and_time", "self_and_others", "affirmation","exclamation","enumeration"]
    selected_animation = random.choice(animations)
    animation(selected_animation)  # Call your animation function here
    time.sleep(st.session_state.anim_time)  # Wait for few seconds

def pepper_reconnect(ip,port=9559):
    st.session_state.pepper = Connection()
    st.session_state.session = st.session_state.pepper.connect(ip, port)

    # Create a proxy to the AL services
    st.session_state.behavior_mng_service = st.session_state.session.service("ALBehaviorManager")

def set_line_count():
    st.session_state.line_count=int(st.session_state.line_value)-1

#creating the connection
if 'pepper' not in st.session_state:
    st.session_state.pepper = Connection()
    # st.session_state.ip='localhost'
    # st.session_state.ip='127.0.0.1'
    # port=39673
    # st.session_state.ip='10.0.0.244'
    # st.session_state.ip='172.16.35.227' # questacon ip
    # st.session_state.ip='172.20.10.4'
    st.session_state.ip='10.230.227.40'
    port=9559
    st.session_state.session = st.session_state.pepper.connect(st.session_state.ip, port)

    # Create a proxy to the AL services
    st.session_state.behavior_mng_service = st.session_state.session.service("ALBehaviorManager")

    # Sleep button behaviour
    st.session_state.sleep_state=0

    # speaking button behavior
    st.session_state.speaking=0
    st.session_state.start_time=0

    # Script button behavior
    st.session_state.tag_list=get_tags_list()
    # st.session_state.line_count=len(st.session_state.tag_list)-1
    st.session_state.line_count=0
    # st.session_state.line_value=0
    st.session_state.anim_time=1.2    #single animation play time


# UI layout
st.markdown("<h1 style='text-align: center;'>Questacon App</h1>", unsafe_allow_html=True)

col1, col2 = st.columns([3,1])
with col1:
    st.header("Interactive Actions with Pepper")
    st.text("Click any button below to see Pepper in action:")
with col2:
    st.write("")
    st.write("")
    if st.button("Sleep"):
        st.session_state.sleep_state=1
        animation('sleep')
    if st.button("\nStop Animation\n", type="primary"):  # Create the button
        st.session_state.behavior_mng_service.stopAllBehaviors()
        st.session_state.sleep_state=0
        animation("stand")
       #  st.success("Button pressed...")
# Apply CSS to ensure buttons have the same width
st.markdown("""
    <style>
    .stButton button {
        width: 100%;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

st.subheader("Eyes")
col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Red"):
        animation("eyes_red")

with col2:
    if st.button("Green"):
        animation("eyes_green")

with col3:
    if st.button("Normal"):
        animation("eyes")

st.subheader("Dialog Animations")

# Create two columns for the 7 buttons
col1, col2 = st.columns(2)

with col1:
    if st.button("Space & time"):
        animation("space_and_time")
       #  st.success("Button pressed...")
    if st.button("Self & others"):
        animation("self_and_others")
       #  st.success("Button pressed...")
    if st.button("Affirmation"):
        animation("affirmation")
       #  st.success("Button pressed...")
    if st.button("Negation"):
        animation("negation")
       #  st.success("Button pressed...")

with col2:
    if st.button("Question"):
        animation("question")
       #  st.success("Button pressed...")
    if st.button("Exclamation"):
        animation("exclamation")
       #  st.success("Button pressed...")
    if st.button("Enumeration"):
        animation("enumeration")
       #  st.success("Button pressed...")
    if st.button("Facepalm"):
        animation("facepalm")


st.subheader("Moods")

# Create two columns for the 9 buttons
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("<h3 style='text-align: center;'>Positive</h3>", unsafe_allow_html=True)
    if st.button("Happy"):
        animation("happy")
       #  st.success("Button pressed...")
    if st.button("Kisses"):
        animation("kisses")
       #  st.success("Button pressed...")
    if st.button("Excited"):
        animation("excited")
       #  st.success("Button pressed...")
    if st.button("Wave"):
        animation('wave')

with col2:
    st.markdown("<h3 style='text-align: center;'>Neutral</h3>", unsafe_allow_html=True)
    if st.button("Thinking"):
        animation("thinking")
       #  st.success("Button pressed...")
    if st.button("Curious"):
        animation("curious")
       #  st.success("Button pressed...")
    if st.button("Chill"):
        animation("chill")
       #  st.success("Button pressed...")

with col3:
    st.markdown("<h3 style='text-align: center;'>Negative</h3>", unsafe_allow_html=True)
    if st.button("Fear"):
        animation("fear")
       #  st.success("Button pressed...")
    if st.button("Confused"):
        animation("confused")
       #  st.success("Button pressed...")
    if st.button("Bored"):
        animation("bored")
       #  st.success("Button pressed...")

st.subheader("Pepper Speaking")

col1, col2 = st.columns(2)

with col1:
    #only 2 min speach. 
    # if st.button("Start Speaking"):
    #     st.session_state.speaking=1
    #     while(st.session_state.speaking==1):
    #         play_random_animation()
    if st.button("Start Speaking"):
        st.session_state.speaking = 1
        st.session_state.start_time = time.time()  # Record the start time
        while st.session_state.speaking == 1:
            play_random_animation()
            if time.time() - st.session_state.start_time > 120:  # Stop after 2 minutes
                st.session_state.speaking = 0
                st.session_state.start_time=0
                animation("stand")
                break

with col2:
    if st.button("Stop Speaking"):
        st.session_state.speaking=0
        animation("stand")

st.subheader("Script")

col1, col2, col3 = st.columns(3)

eyes_tags=['eyes_green','eyes_red', 'eyes']

with col1:
    if st.button("Next"):
        for tag in st.session_state.tag_list[st.session_state.line_count]:
            animation(tag)
            if tag in eyes_tags:
                continue
            time.sleep(st.session_state.anim_time)
        st.session_state.line_count+=1
        st.success("Line No: "+str(st.session_state.line_count))
    
        if  st.session_state.line_count==28:
            st.session_state.line_count=0

    if st.button("Transition"):
        animation('transition')
with col3:
    if st.button("Go to first"):
        st.session_state.line_count=0
        for tag in st.session_state.tag_list[st.session_state.line_count]:
            animation(tag)
            if tag in eyes_tags:
                continue
            time.sleep(st.session_state.anim_time)
        st.session_state.line_count+=1
        st.success("Line No: "+str(st.session_state.line_count))

    if st.button("Previous"):
        st.session_state.line_count-=1
        if(st.session_state.line_count<0):
            st.session_state.line_count=len(st.session_state.tag_list)-1
        for tag in st.session_state.tag_list[st.session_state.line_count]:
            animation(tag)
            if tag in eyes_tags:
                continue
            time.sleep(st.session_state.anim_time)
        st.success("Line No: "+str(st.session_state.line_count+1))

    if st.button("Reset"):
        st.session_state.line_count=0
        st.success("Reset to 1st")

st.subheader("Reconnect")
col1, col2 = st.columns([3,1])

with col1:
    ip_value = st.text_input("Ip:", key='ip_value',value=st.session_state.ip)
    port_value = st.text_input("Port:", value=9559,key='port_value', max_chars=5)
    line_value = st.text_input("Line:", value=st.session_state.line_count,key='line_value', max_chars=2,on_change=set_line_count)

with col2:
    st.write("")
    st.write("")
    st.write("")
    if st.button("Reconnect"):
        pepper_reconnect(ip_value,port_value)
        st.session_state.line_count=st.session_state.line_value
        # st.session_state.port_value = '9559'