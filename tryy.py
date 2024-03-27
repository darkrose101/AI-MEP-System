import streamlit as st
import pandas as pd
import tensorflow as tf
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import uuid
from textblob import TextBlob
from drive import c_specific


model = tf.keras.models.load_model('model/model1')

#                 ---- [[USING & INITIALIZING the TEXBLOB model and tokenizer for TEXT SUMMARIZATION ]] ----


department_options = ['HR', 'Sales', 'IT', 'Finance', 'Engineering']
sentiment_options = ['great', 'cool', 'nice', 'awesome', 'good', 'outstanding',
                    'poor', 'lacking', 'dreadful', 'bad', 'weak', 'underwhelming'
                    ]
team_options = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

emp_df = pd.read_csv('employees.csv')
names = emp_df['First Name'].tolist()
total = emp_df['Hours'].sum()
emp_df['Percentages(H)'] = ( emp_df['Hours'] / total ) * 100
emp_df['Percentages(EH)'] = ( (total - emp_df['Hours'] )  / total) * 100
emp_df['Percentages(TW)'] = ( emp_df['Team Score'] / 10 ) * 100
emp_df.to_csv('employees_p.csv', index=False)
selected_emp_data = None

def generate_unique_key():
    return str(uuid.uuid4())

def generate_charts(selected_emp_data):
    selected_emp_data = pd.read_csv('employees_p.csv')
    print("Selected Employee Data:")
    print(selected_emp_data)


    results = selected_emp_data[['Percentages(H)', 'Percentages(EH)', 'Percentages(TW)']]
    results.columns = ['Work Hours', 'Extra Hours', 'Team Work']

    st.write(results)

    # Generate pie chart
    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(results.iloc[0], labels=results.columns, autopct='%1.1f%%')
    ax.axis('equal')
    st.pyplot(fig)

    # Generate bar chart
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.barplot(x=results.columns, y=results.iloc[0], ax=ax)
    st.pyplot(fig)

    # Generate count plot
    fig, ax = plt.subplots(figsize=(6, 6))
    sns.countplot(data=results, ax=ax)
    st.pyplot(fig)


def MEP():

    """
    st.set_page_config(page_title="ME&P Page",
                    page_icon=":tada:",
                    layout="wide")
    """

    with st.container():
        with st.sidebar:
            config = generate_unique_key()

            st.title('🏂 Blue Lotus Employee')
            selected_emp = st.selectbox('Select an employee', names, key=config)
            st.write(f"Currently logged in as: [ { selected_emp } ]")

        st.subheader("Try out the new model trained by Lawrence! :wave:")
        st.title("A Template for Smart Monitoring, Evaluation and Performance System")
        st.write("Let's see how this will fun out :)")

        # Create input fields for the user to fill
        input1 = st.selectbox('Department', department_options)
        input2 = st.number_input('Employee Id')
        input3 = st.number_input('Work Hors')
        input4 = st.number_input('Bonuses')
        input5 = st.number_input('Leaves/Offs (0/1)')
    

        # Create a button for the user to submit their inputs
        submit = st.button('Submit')


    with st.container():
        st.write("---")
        if submit:
            department_index = department_options.index(input1)
            input_encoded = np.zeros(len(department_options))
            input_encoded[department_index] = 1
            inputs = np.concatenate([input_encoded, [input2, input3, input4, input5]])
            inputs = np.array([inputs])


            inputs = tf.convert_to_tensor(inputs, dtype=tf.float32)
            prediction = model.predict(inputs)
            st.write("[Real-Time] Bobby's Prediction:", prediction[0][0])

            if prediction[0][0] == 0.0:
                st.write("The employee is likely to be absent in the coming week, and not eligible for a bonus, unless stated otherwise [P: --> 99.7%]")
            else:
                st.write("The employee is likely to be Present in the coming week, definitely eligible for a bonus! [P: --> 99.7%]")

    with st.container():
        st.write("---")
        st.title("Employee Feedback System")

        with st.form("feedback_form"):
            st.write("Please provide your feedback on the employee (at least 10 words):")
            feedback_text = st.text_area("Type your feedback here:", height=200)

            submitted = st.form_submit_button("Submit Feedback")

            if submitted:
                if len(feedback_text.split()) < 10:
                    st.error("Please provide a feedback of at least 10 words.")
                else:
                    st.success("Feedback submitted successfully!")

                    blob = TextBlob(feedback_text)
                    sentiment = blob.sentiment.polarity

                    st.write("Sentiment Analysis:")
                    if sentiment > 0:
                        st.write("Positive sentiment. Thank You")
                    elif sentiment < 0:
                        st.write("Negative sentiment. Thank You")
                    else:
                        st.write("Neutral sentiment. Thank You")

            st.write("Now leave a sincere review on the person's:")

            st.write("[A]: Communication skills:")
            unique_keyy = generate_unique_key()
            input1 = st.selectbox('Select:', sentiment_options, key=unique_keyy)

            st.write("[B]: TeamWork skills:")
            unique_key = generate_unique_key()
            input1 = st.selectbox('Select:', team_options, key=unique_key)

    with st.container():
        st.write("---")
        col1, col2 = st.columns(2)

        with col1:
            st.title("Employees past week's performance review")
            name = st.text_input('Enter Employee Name:')
            position = st.text_input("Select their Position:")
            st.title(f"{name}'s past week's performance review")
            bk = generate_unique_key


            if name:
                    if name in emp_df['First Name'].values and position in emp_df['Position'].values:
                        st.write("Personnel Found!")
                        selected_emp_data = emp_df[emp_df['First Name'] == name]
                        generate_charts(name)

                    else:
                        st.write("Employee not found. Check the spelling, department or confirm in the HR if they are still working here.")
                        
            st.write("Employee name and position?")