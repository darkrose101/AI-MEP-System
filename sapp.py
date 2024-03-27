import streamlit as st
import logging
import threading
import sqlite3
import requests
import uuid
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from drive import e_specific, c_specific, x


data0 = e_specific()
data1 = c_specific()

total = []
names = []


less = data1.fetch()


emp_df = pd.DataFrame(less)

for x in less:
    names.append(x[0])
    total.append(x[3])

total = sum(total)

def work_hours(data):
    hours = ( data / total ) * 100
    return hours

def extra_hours(data):
    rel = total - data
    ext = rel / total
    return rel

def team_Work(data):
    team = ( data / 10 ) * 100
    return team

def comms(data):
    pass

#             [[ FUNCTIONS of THREADING, STATUS, STYLE and PERFORMANCE ]]
_thread_local = threading.local()

def get_db_conn():
    if not hasattr(_thread_local, 'db'):
        _thread_local.db = sqlite3.connect('database.db', check_same_thread=False)
    return _thread_local.db

def get_status_indicator(name):
    url = f'http://localhost:5000/status?name={name}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        if response.text:
            status = response.json()['status']
            return status
        else:
            logging.warning("Empty response from server")
    except requests.exceptions.HTTPError as errh:
        logging.error("HTTP Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        logging.error("Error Connecting to Server:", errc)
    except requests.exceptions.Timeout as errt:
        logging.error("Timeout Error:", errt)
    except requests.exceptions.RequestException as err:
        logging.error("Something went wrong:", err)
    return None

def get_status(name):
    # get the status from the session state
    if 'status' not in st.session_state:
        # if the status is not set in the session state, send a request to the Flask app to get the status
        response = requests.get('http://localhost:5000/status', params={'name': name})
        
        # check the response status code
        if response.status_code != 200:
            print(f"Error: Unexpected response status code: {response.status_code}")
            return None
        
        status = response.json()['status']
        st.session_state.status = status
    return st.session_state.status

def colored(input_color):
    if input_color == 'blue':
        chart_color = ('#29b5e8', '#155F7A')
    elif input_color == 'green':
        chart_color = ('#27AE60', '#12783D')
    elif input_color == 'orange':
        chart_color = ('#F39C12', '#875A12')
    elif input_color == 'red':
        chart_color = ('#E74C3C', '#781F16')
    else:
        chart_color = ('#29b5e8', '#155F7A')

    return chart_color

def generate_charts(data):
    work_hours_data = work_hours(data)
    extra_hours_data = extra_hours(data)
    team_work_data = team_Work(data)

    results = pd.DataFrame({
        'Category': ['Work Hours', 'Extra Hours', 'Team Work'],
        'Percentage': [work_hours_data, extra_hours_data, team_work_data]
    })

    chart_color = colored(selected_color_theme)[0]
    sns.set_palette(selected_color_theme)

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(results['Percentage'], labels=results['Category'], autopct='%1.1f%%', colors=sns.color_palette())
    ax.axis('equal')
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(6, 6))
    sns.barplot(x='Category', y='Percentage', data=results, ax=ax, color=chart_color)
    st.pyplot(fig)

    fig, ax = plt.subplots(figsize=(6, 6))
    sns.countplot(x='Category', data=results, ax=ax, color=chart_color)
    st.pyplot(fig)  

    x.close()

def generate_unique_key():
    return str(uuid.uuid4())

#######################################################################


st.set_page_config(page_title="First website",
                   page_icon=":tada:",
                   layout="wide")

# CSS styling
st.markdown("""
<style>

[data-testid="block-container"] {
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 1rem;
    padding-bottom: 0rem;
    margin-bottom: -7rem;
}

[data-testid="stVerticalBlock"] {
    padding-left: 0rem;
    padding-right: 0rem;
}

[data-testid="stMetric"] {
    background-color: #393939;
    text-align: center;
    padding: 15px 0;
}

[data-testid="stMetricLabel"] {
  display: flex;
  justify-content: center;
  align-items: center;
}

[data-testid="stMetricDeltaIcon-Up"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

[data-testid="stMetricDeltaIcon-Down"] {
    position: relative;
    left: 38%;
    -webkit-transform: translateX(-50%);
    -ms-transform: translateX(-50%);
    transform: translateX(-50%);
}

</style>
""", unsafe_allow_html=True)


with st.container():
    st.subheader("Hello, I finally took the leap of faith :wave:")
    st.title("A Template for Smart Monitoring, Evaluation and Performance System")
    st.write("Let's see how this will fun out :)")

with st.container():
    st.write("---")
    left_c, right_c = st.columns(2)
    with left_c:
        st.header("Brief summary")
        st.write("###")
        st.write(
            """
            The above project aims to improve the current MEP systems with the inclunsion of AI.
            It is my final year project, and i'm going to ace it without a swear.
            Feel free to look at the code, and add any thing you think will improve on it  
            """
        )

with st.container():
    st.write("---")
    st.write("Below is a simple demonstration of the employee's performance reviews")
    data = 100
    col1, col2 = st.columns(2)
    with st.sidebar:
        st.title('🏂 Blue Lotus Employees')
        
        emp_list = emp_df

        selected_emp = st.selectbox('Select an employee', names)

        color_theme_list = ['deep', 'muted', 'pastel', 'bright', 'dark']
        selected_color_theme = st.selectbox('Select a color theme', color_theme_list)


    with col1:
        generate_charts(total, selected_color_theme)

    with col2:
        st.title('🏂 Status of Blue Lotus Employees')
        
        emp_list = emp_df
        unique_key = generate_unique_key()
        selected_emp = st.selectbox('Select an employee', names, key=unique_key)
        
        status = get_status(selected_emp)

        if status == 'online':
            st.write('🟢 Online')
        else:
            st.write('🔴 Offline')