import streamlit as st

st.title("HELLO! :blue[cool] :sunglasses:")
st.write("Hello World!")
st.write("Goodbye Moon!")
# We need a streaming object for this to work
# st.write_stream("Where are you Mars?!")

st.markdown("""
## Hello
- This
- Is
- Magic Formating!
""")
st.header("One", divider=True)

import pandas as pd
df = pd.DataFrame({'col1': [1,2,3]})
st.write(df)

st.subheader("This is a subheader with a divider", divider="gray")

import matplotlib.pyplot as plt
import numpy as np

arr = np.random.normal(1, 1, size=100)
fig, ax = plt.subplots()
ax.hist(arr, bins=20)

st.write(fig)

code = '''def hello():
    print("Hello, Streamlit!")'''
st.code(code, language="python")

st.metric(label="Temperature", value="70 °F", delta="1.2 °F")