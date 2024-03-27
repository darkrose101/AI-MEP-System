from textblob import TextBlob
#from transformers import pipeline

"""
#                 ---- [[USING & INITIALIZING the BART model and tokenizer for TEXT SUMMARIZATION ]] ----
model_name = "facebook/bart-large-cnn"
model = pipeline("summarization", model=model_name, tokenizer=model_name)

input_text = "James has a good teamwork score. He's really fun to work with, super friendly and very useful in discussions. I wouldn't change a thing"

summary = model(input_text, max_length=17, min_length=10, do_sample=False)
learn = summary[0]['summary_text']
"""


##                               ---- [[ USING TEXTBLOB as a SENTIMENT ANALYZER]] ----
input_text = "James has a good teamwork score. He's really fun to work with, super friendly and very useful in discussions. I wouldn't change a thing"

blob = TextBlob(input_text)
sentiment = blob.sentiment.polarity

print(" ")
if sentiment > 0:
    print("Positive sentiment")
elif sentiment < 0:
    print("Negative sentiment")
else:
    print("Neutral sentiment")







"""
test1 = work_hours(data1.fetch()[1][3])
print(f"Janet has worked a total of {test1}% hours in the past week")

test2 = extra_hours(data1.fetch()[1][3])
print(f"Janet has worked a total of {test2}% extra hours in the past week")

test3 = team_Work(data1.fetch()[1][6])
print(f"Janet has worked an impressice score of {test1} in teamwork")

test4 = comms(data1.fetch()[1][-3])
print(f"Janet's coomunication score hinges a {test4}% in the past week")

#print(data0.fetch()[1][1])
#print(data1.fetch())
"""