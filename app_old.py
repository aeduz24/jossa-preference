import streamlit as st
import pandas as pd

# Sample DataFrame (replace with your DataFrame)

# df1 = pd.DataFrame('2023-round1.csv')

# Function to filter DataFrame based on user inputs
def filter_data(df, gender, seat_type, quota, rank):
    filtered_df = df[
        (df['Gender'] == gender) &
        (df['Seat Type'] == seat_type) &
        (df['Quota'] == quota) &
        (df['Opening Rank'] <= rank) &
        (df['Closing Rank']>= rank)
    ]
    return filtered_df

st.title('AeduZ College Finder (Yearwise)')

# User inputs
# year = st.number_input('Enter Year:', min_value=2000, step=1)
# year=st.selectbox('select Year',[2023])
# round_num = st.selectbox('Select Round:', [1,2,3,4,6])
# gender = st.selectbox('Select Gender:', ['Gender-Neutral', 'Female-only (including Supernumerary)'])
# seat_type = st.selectbox('Select Seat Type:', ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'OBC-NCL (PwD)', 'EWS (PwD)', 'ST (PwD)', 'SC (PwD)'])
# quota = st.selectbox('Select Quota:', ['AI', 'HS', 'OS', 'GO', 'JK', 'LA'])
# rank = st.number_input('Enter Rank:', min_value=0, step=1)
st.sidebar.title('Filters')

# User inputs in the sidebar
year = st.sidebar.selectbox('Select Year', [2020,2021,2022,2023])
college=st.sidebar.selectbox('Select college',["IIT","NIT"])
round_num = st.sidebar.selectbox('Select Round:', [1, 2, 3, 4, 6])
gender = st.sidebar.selectbox('Select Gender:', ['Gender-Neutral', 'Female-only (including Supernumerary)'])
seat_type = st.sidebar.selectbox('Select Seat Type:', ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'OBC-NCL (PwD)', 'EWS (PwD)', 'ST (PwD)', 'SC (PwD)'])
if college=="IIT":
    quota = st.sidebar.selectbox('Select Quota:', ['AI', 'HS', 'OS', 'GO', 'JK', 'LA'])
if college=="NIT":
    quota = st.sidebar.selectbox('Select Quota:', ['HS', 'OS', 'GO', 'JK', 'LA'])
rank = st.sidebar.number_input('Enter Rank:', min_value=0, step=1)


# Load CSV based on user inputs
filename = f'{year}_round{round_num}_{college.lower()}.csv'
try:
    df = pd.read_csv(filename)
except FileNotFoundError:
    st.error(f"Error: File '{filename}' not found.")
    st.stop()
df['Closing Rank']=df['Closing Rank'].astype(str)
df['Opening Rank']=df['Opening Rank'].astype(str)
df=df[~df['Closing Rank'].str.contains('P')]
df=df[~df['Opening Rank'].str.contains('P')]
df['Opening Rank']=df['Opening Rank'].astype(float)
df['Closing Rank']=df['Closing Rank'].astype(float)


if st.button('Find'):
    # Filter DataFrame based on user inputs
    filtered_df = filter_data(df, gender, seat_type, quota, rank)
    
    # Display filtered DataFrame
    st.write('Filtered DataFrame:')
    st.write(filtered_df.loc[:,['Institute', 'Academic Program Name']].reset_index(drop=True))