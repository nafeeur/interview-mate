import streamlit as st
from configure import key, key_two
import requests
import paralleldots
import pandas as pd
import sys
import time

filename = "/Users/naf/Documents/interview.mp4"

paralleldots.set_api_key(key_two)


st.title("Interview Mate")


def read_file(filename, chunk_size=5242880):
    with open(filename, 'rb') as _file:
        while True:
            data = _file.read(chunk_size)
            if not data:
                break
            yield data

headers = {'authorization': key}
response = requests.post('https://api.assemblyai.com/v2/upload',
                         headers=headers,
                         data=read_file(filename))

response = response.json()

url = response['upload_url']

endpoint = "https://api.assemblyai.com/v2/transcript"

json = {
    "audio_url": url
}

headers = {
    "authorization": key,
    "content-type": "application/json"
}

response2 = requests.post(endpoint, json=json, headers=headers)

response2 = response2.json()

id = response2['id']

endpoint2 = "https://api.assemblyai.com/v2/transcript/"+id

headers = {
    "authorization": key,
}

response3 = requests.get(endpoint2, headers=headers)
response3 = response3.json()

while response3['status'] != 'completed':
    response3 = requests.get(endpoint2, headers=headers)
    response3 = response3.json()
    if response3['status'] == 'completed':
        response3 = requests.get(endpoint2, headers=headers)
        response3 = response3.json()
        st.title("Interview Transcript (Ben's Interview)")
        st.write(response3['text'])

text = response3['text']

keywrds = paralleldots.keywords(text)

sentmnt = paralleldots.sentiment(text)
list = []
st.text(keywrds["keywords"])
for i in keywrds["keywords"]:
    list = i['keyword']

st.write(list)

data = pd.DataFrame({
    "sentiment" : ['extrovert', 'neutral', 'introvert'],
    'values': [sentmnt["sentiment"]["positive"],sentmnt["sentiment"]["neutral"],sentmnt["sentiment"]["negative"]],
}).set_index('sentiment')


## More criteria can be added
if sentmnt["sentiment"]["positive"] > 0.1 and sentmnt["sentiment"]["neutral"] > 0.2:
    st.bar_chart(data)
    st.markdown("### Qualified for Job")








