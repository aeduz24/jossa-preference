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
        
        (df['Closing Rank']>= rank)
    ]
    return filtered_df

st.title("AeduZ's Counselling Helper")

st.sidebar.title('Filters')

# User inputs in the sidebar
seat_type = st.sidebar.selectbox('Select Category :', ['OPEN', 'EWS', 'OBC-NCL', 'SC', 'ST', 'OPEN (PwD)', 'OBC-NCL (PwD)', 'EWS (PwD)', 'ST (PwD)', 'SC (PwD)'])
gender = st.sidebar.selectbox('Select Gender:', ['Gender-Neutral', 'Female-only (including Supernumerary)'])
rank = st.sidebar.number_input('Enter Category Rank:', min_value=0, step=1)
year = st.sidebar.selectbox('Select Year', [2023,2022,2021,2020])
college=st.sidebar.selectbox('Select college',["IIT","NIT"])
# round_num = st.sidebar.selectbox('Select Round:', [1, 2, 3, 4, 6])
round_num = 6
if college=="IIT":
    quota = st.sidebar.selectbox('Select Quota:', ['All India (AI)'])
if college=="NIT":
    quota = st.sidebar.selectbox('Select Quota:', [' Other State (OS)','Home State (HS)', ' Goa (GO)', ' Jammu & Kashmir (JK)', ' Ladakh (LA)'])
import re
quota=re.findall(r'\((.*?)\)', quota)[0]
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
nirf_iit=pd.read_csv('nirf_rank_iit.csv')
nirf_nit=pd.read_csv('nirf_rank_nit.csv')

sort_options = ['College Rank', 'Engineering Branch', 'Dual degree']
selected_sort = st.selectbox("Select criteria to sort by:", sort_options)

if selected_sort=="Engineering Branch":
    branches = [
        "Computer Science Engineering",
        "Electrical Engineering",
        "Mechanical Engineering",
        "Electronics Engineering",
        "Civil Engineering",
        "Chemical Engineering",
        "Aerospace Engineering",
        "Metallurgical Engineering"
        ]


    new_order = st.multiselect(
    "Drag to reorder:",
    branches,
    default=branches,
    format_func=lambda x: x
    )
        
    new_order=list(map(lambda x:x.replace(" Engineering",""),new_order))
    order_dict={new_order[i]:i for i in range(len(new_order))}
    # print(order_dict)
    def branch_func(branch):
        for el in new_order:
            if el in branch:
                return order_dict[el]
        return 100



if st.button('Give preference'):
    # Filter DataFrame based on user inputs
    filtered_df = filter_data(df, gender, seat_type, quota, rank)
    if college=="IIT":
        df_merge=filtered_df.merge(nirf_iit[['college', 'rank']], left_on='Institute', right_on='college', how='left')
    if college=="NIT":
        df_merge=filtered_df.merge(nirf_nit[['college', 'rank']], left_on='Institute', right_on='college', how='left')
    # Display filtered DataFrame

    df_final=df_merge.loc[:,['Institute', 'Academic Program Name','rank']].reset_index(drop=True)
    df_final.fillna(1000,inplace=True)
    df_final['rank_dual']=df_final['Academic Program Name'].apply(lambda x:1 if "5 Years" in x else 0)
    df_final['rank_branch']=df_final['Academic Program Name'].apply(branch_func)
    # ordered_items=df_final['Academic Program Name'].unique()
    
    st.write('Recommended Jossa list')

    

    if 'College Rank' == selected_sort:
        df_final.sort_values(by='rank', ascending=True,inplace=True)
        df_final.reset_index(drop=True,inplace=True)
        print('sorting based on rank')

    if 'Engineering Branch' == selected_sort:
        df_final.sort_values(by='rank_branch', ascending=True,inplace=True)
        df_final.reset_index(drop=True,inplace=True)
        print('sorting based on brank')

    if 'Dual degree' == selected_sort:
        df_final.sort_values(by='rank_dual', ascending=True,inplace=True)
        df_final.reset_index(drop=True,inplace=True)
        print('sorting based degree')


    st.write(df_final)
   