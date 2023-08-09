import pandas as pd
import numpy as np
import streamlit as st
import plotly
import plotly.express as px




st.set_page_config(layout="wide")


if 'username' not in st.session_state:
    st.session_state['username'] = ''
    
if 'username_2' not in st.session_state:
    st.session_state['username_2'] = ''

if 'password' not in st.session_state:
    st.session_state['password'] = ''
    
if 'password_2' not in st.session_state:
    st.session_state['password_2'] = ''
    
if 'counter1_value' not in st.session_state:
    st.session_state['counter1_value'] = 0
    
if 'start_date' not in st.session_state:
    st.session_state['start_date'] = pd.to_datetime('2023-01-01')
    
if 'start_date_2' not in st.session_state:
    st.session_state['start_date_2'] = pd.to_datetime('2023-01-01')
    
if 'end_date' not in st.session_state:
    st.session_state['end_date'] = pd.to_datetime('2023-05-01')
    
if 'end_date_2' not in st.session_state:
    st.session_state['end_date_2'] = pd.to_datetime('2023-05-01')
    
if 'start_date_min' not in st.session_state:
    st.session_state['start_date_min'] = pd.to_datetime('2023-01-01')
    
if 'end_date_max' not in st.session_state:
    st.session_state['end_date_max'] = pd.to_datetime('2023-05-01')


def login_callback():
    st.session_state['counter1_value'] += 1

    
def login_another_callback():

    st.session_state['username'] = st.session_state['username_2']
    st.session_state['password'] = st.session_state['password_2']
    st.session_state['counter1_value'] = 0
    
def start_date_callback():
    st.session_state['start_date'] = st.session_state['start_date_2']
    
    
def end_date_callback():
    st.session_state['end_date'] = st.session_state['end_date_2']
    
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

        col1, col2, col20, col25, col3 = st.columns([2,1,6,1,0.85])
        
        @st.cache_data
        def load_data():
            df = pd.read_csv('/Users/okankoklu/Desktop/TAB_HR/tab_hr_ise_girisler_clean_pkl.pkl').groupby(['sirket', 'ise_giris_tarihi'], as_index=False)['No'].count()
            df['ise_giris_tarihi'] = pd.to_datetime(df['ise_giris_tarihi'])
            return df
        
        df = load_data()
        
        with col3:

            st.button('Refresh', on_click=refresh_callback)
        
        with col1:
            
            login_another_input = st.button('Login with Another Account', key = 'login_another_value', on_click=login_another_callback)
            
        sirket_multiselect = st.multiselect('Sirket Sec', df['sirket'].unique(), default='ATA Holding')
        df1 = df[df['sirket'].isin(sirket_multiselect)]
        
        st.session_state['start_date_min'] = df1['ise_giris_tarihi'].min()
        st.session_state['end_date_max'] = df1['ise_giris_tarihi'].max()
            
        col5, col6, col7 = st.columns([1,1,0.22])
            
        with col5:
            
            start_date = pd.to_datetime(st.date_input('Baslangic Tarihi', min_value = df1['ise_giris_tarihi'].min(), max_value = df1['ise_giris_tarihi'].max(), value = df1['ise_giris_tarihi'].min(), key='start_date'))
            st.session_state['start_date_2'] = start_date
            
            if start_date:
                start_date = pd.to_datetime(st.session_state['start_date'])
        
        with col6:
            
            end_date = pd.to_datetime(st.date_input('Bitis Tarihi', min_value = start_date + pd.DateOffset(days=1), max_value = df1['ise_giris_tarihi'].max(), value = df1['ise_giris_tarihi'].max(), key = 'end_date'))
            st.session_state['end_date_2'] = end_date
            
            if end_date:
                end_date = pd.to_datetime(st.session_state['end_date_2'])

        with col7:
            
            for i in range(2):
                st.write('\n')
            all_dates_button = st.button('See All Dates', on_click=all_dates_callback)

            if all_dates_button:
                start_date = st.session_state['start_date_min']
                end_date = st.session_state['end_date_max']
            
        df2 = df1[(df1['ise_giris_tarihi']>=start_date) & (df1['ise_giris_tarihi']<=end_date)]  
        

        
        fig = px.line(
            df2,
            x='ise_giris_tarihi',
            y='No',
            color='sirket',
            markers=True,
            height=600,
            width=1300,
            color_discrete_sequence=px.colors.qualitative.Plotly
            )
        
        fig.update_layout(
            plot_bgcolor='seashell',
            paper_bgcolor = 'firebrick',
            title = dict(text='Secilen Sirketler ve Tarihlere Gore Ise Alimlar', x=0.05, font=dict(size=20)), 
            legend=dict(orientation='h',  x=0.35,  y=-0.085, title_text=''),
            xaxis=dict(title="Ise Giris Tarihi", title_standoff=40)
            )
        
        fig.update_yaxes(showgrid=False)
        
        st.plotly_chart(fig)
        
except ValueError as e:
    st.error(f'Lutfen En Az Bir Sirket Secin {e}')
        


        
        
