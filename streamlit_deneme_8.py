import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import random

st.set_page_config(layout="wide")

def initialize_session_state():
    session_state_defaults = {
        'username': '',
        'username_2': '',
        'password': '',
        'password_2': '',
        'counter1_value': 0,
        'start_date': pd.to_datetime('2023-01-01'),
        'start_date_2': pd.to_datetime('2023-01-01'),
        'end_date': pd.to_datetime('2023-05-01'),
        'end_date_2': pd.to_datetime('2023-05-01'),
        'start_date_min': pd.to_datetime('2023-01-01'),
        'end_date_max': pd.to_datetime('2023-05-01')
    }
    
    for key, value in session_state_defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value

initialize_session_state()

def login_callback():
    st.session_state['counter1_value'] += 1

    
def login_another_callback():

    st.session_state['username'] = st.session_state['username_2']
    st.session_state['password'] = st.session_state['password_2']
    st.session_state['counter1_value'] = 0
    
def start_date_callback():
    global start_date
    global end_date
    start_date = pd.to_datetime(st.session_state['start_date_2'])
    end_date = pd.to_datetime(st.session_state['end_date_2'])
    
def end_date_callback():
    global start_date
    global end_date
    start_date = pd.to_datetime(st.session_state['start_date_2'])
    end_date = pd.to_datetime(st.session_state['end_date_2'])

    
def refresh_callback():
    global start_date
    global end_date
    start_date = st.session_state['start_date']
    end_date = st.session_state['end_date']

def all_dates_callback():
    global start_date
    global end_date
    start_date = st.session_state['start_date_min']
    end_date = st.session_state['end_date_max']
    
    st.session_state['start_date'] = start_date
    st.session_state['end_date'] = end_date

    
def login_page():
    st.title('Login Page')
    st.write('You only need to press the Login button at this stage')
    st.write('\n')
    
    username_input = st.text_input('Username', key='username', value=st.session_state['username_2'])
    password_input = st.text_input('Password', type='password', key='password', value=st.session_state['password_2'])
    st.write('\n')
    
    st.button('Login', key = 'login_button_value', on_click=login_callback)
    
    st.session_state['username_2'] = username_input
    st.session_state['password_2'] = password_input
    
    return st.session_state['username_2'], st.session_state['password_2']

try: 

    if st.session_state['counter1_value'] == 0:
        col0, col00, col000 = st.columns([1,3,1])
        with col00:
            for i in range(4):
                st.write('\n')
                
            st.session_state['username_2'] , st.session_state['password_2'] = login_page()
                
    else:

        col1,  col2,  col3 = st.columns([2,7,1.1])
        
        @st.cache_data
        def load_data():
            df = pd.read_csv('https://raw.githubusercontent.com/okanstreamlit/IK_DATA/main/streamlit_ise_girisler.csv').groupby(['sirket', 'ise_giris_tarihi'], as_index=False)['No'].count()
            df['ise_giris_tarihi'] = pd.to_datetime(df['ise_giris_tarihi'])
            return df
        
        df = load_data()
        
        
        with col3:
            
            st.button('Refresh', on_click=refresh_callback)
        
        colt1, colt2, colt3 = st.columns([1,5,1])
        
        with colt2:
            st.title(' Secilen Sirketler ve Tarihlere Gore Ise Alimlar')
        
        with col1:
            
            login_another_input = st.button('Login with Another Account', key = 'login_another_value', on_click=login_another_callback)
            
        sirket_multiselect = st.multiselect('Sirket Sec', df['sirket'].unique(), default=['ATA Holding', 'ATA Sancak'])

        df1 = df[df['sirket'].isin(sirket_multiselect)]
        
        st.session_state['start_date_min'] = df1['ise_giris_tarihi'].min()
        st.session_state['end_date_max'] = df1['ise_giris_tarihi'].max()
            
        col5, col6, col7 = st.columns([1,1,0.22])
            
            
        with col5:
            start_date = pd.to_datetime(st.date_input('Baslangic Tarihi', min_value = df1['ise_giris_tarihi'].min(), max_value = df1['ise_giris_tarihi'].max(), value = df1['ise_giris_tarihi'].min(), key='start_date'))
            start_date_callback() 
            
        with col6:
            end_date = pd.to_datetime(st.date_input('Bitis Tarihi', min_value = start_date + pd.DateOffset(days=1), max_value = df1['ise_giris_tarihi'].max(), value = df1['ise_giris_tarihi'].max(), key = 'end_date'))
            end_date_callback()  

        with col7:
            
            for i in range(2):
                st.write('\n')
            all_dates_button = st.button('See All Dates', on_click=all_dates_callback)

            if all_dates_button:
                start_date = st.session_state['start_date_min']
                end_date = st.session_state['end_date_max']
            
        
        df2 = df1[(df1['ise_giris_tarihi']>=pd.to_datetime(st.session_state['start_date'])) & (df1['ise_giris_tarihi']<=pd.to_datetime(st.session_state['end_date']))] 
        
  
        ## Plot ##
        
        
        fig = px.line(
            df2,
            x='ise_giris_tarihi',
            y='No',
            color='sirket',
            markers=True,
            height=550,
            width=1300,
            color_discrete_sequence=px.colors.qualitative.Plotly
            )
        
        fig.update_traces(
            text=df2['sirket'],
            textposition='top center',
            mode='lines+markers',
            marker=dict(size=9)
            )

        fig.update_layout(
            plot_bgcolor='mintcream',
            paper_bgcolor = 'maroon',
            title = '', 
            xaxis=dict(title="Ise Giris Tarihi", title_standoff=10, showgrid=False),
            yaxis = dict(title = 'Ise Alim Adeti',title_standoff = 10, showgrid = False, zeroline = False ),
            showlegend=False,
            margin = dict(l=20, r=70, t=60, b=20),
            autosize = False,
            )
        

        random.seed(30)

        number_of_sirket = df['sirket'].nunique()
        random_array_negatives = np.linspace(-4, -2, int(number_of_sirket / 2))
        random_array_positives = np.linspace(2, 4, int((number_of_sirket + 1) / 2))
        random_array = np.sort(np.concatenate((random_array_negatives, random_array_positives)))
        
        number_of_numbers = len(random_array)
        used_indices = []
    
        last_entries = df2.sort_values(by=['sirket', 'ise_giris_tarihi'], ascending=False).groupby('sirket').head(1)
        last_entry_and_no_values = [(row['No'], row['ise_giris_tarihi']) for index, row in last_entries.iterrows()]  
        
        for sirket_name in sirket_multiselect:
            
            sirket_data = df2[df2['sirket'] == sirket_name]
            last_entry = sirket_data.iloc[-1]
            
            remaining_indices = [i for i in range(number_of_numbers) if i not in used_indices]
            random_index = random.choice(remaining_indices)
            used_indices.append(random_index)
            random_number = random_array[random_index]
            
            adjusted_y = last_entry['No'] + random_number
            y_difference = adjusted_y - last_entry['No']
            
            last_entry_tuple = (last_entry['No'], last_entry['ise_giris_tarihi'])

            if last_entry_and_no_values.count(last_entry_tuple) > 1:
                for n in range(2):
                    n_negative = (-n + 1)
                    tuple_row = sirket_data.iloc[n_negative]
                    tuple_time = tuple_row['ise_giris_tarihi']
                    st.write(tuple_time)
                    if tuple_time not in last_entries[~(last_entries['sirket']==sirket_name)]['ise_giris_tarihi'].unique():
                        last_entry = sirket_data.iloc[n_negative]
                        break
                    st.write(last_entry)
            
            fig.add_annotation(
                x=last_entry['ise_giris_tarihi'],
                y=last_entry['No'],
                xref="x",
                yref="y",
                axref="x",
                ayref="y",
                ax=last_entry['ise_giris_tarihi'],
                ay=adjusted_y,
                text=sirket_name,
                showarrow=True,
                arrowhead=4,
                arrowwidth=1.5,
                arrowcolor='black',
                font=dict(size=13, color='black')
                )
            
        st.plotly_chart(fig)
        
except ValueError as e:
    st.error(f'Lutfen En Az Bir Sirket Secin {e}')
        


        
        
