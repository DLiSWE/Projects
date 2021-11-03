import requests
import yelpapi
import pandas as pd
from IPython.display import display
from flask import Flask, request, session, url_for, render_template, flash, redirect
import psycopg2
import psycopg2.extras
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
import datetime
import pytz
from werkzeug.security import generate_password_hash, check_password_hash
import re

#TODO: DEVELOP LOGIN SYSTEM
#Create SQL connection using psycopg2
"""Connect to POSTGRESQL"""
conn = psycopg2.connect(
    database="postgres",
    user="postgres",
    password="1123",
    host='localhost',
    port='5432')
cursor = conn.cursor()
#Create cursor object using built in cursor() method
cursor.execute("CREATE TABLE IF NOT EXISTS webapplogin (full_name VARCHAR ( 250 ) NOT NULL, username VARCHAR( 200 ) UNIQUE NOT NULL, password VARCHAR( 250 ) NOT NULL, email VARCHAR ( 200 ) NOT NULL)")
# conn.commit()
# conn.close()
#cursor.execute('SELECT * FROM gym_df')
zip_code = 11214
#Client ID
clientid = 'Cev8jNKeXB1tVYbl3wwIUw'
#define api key, endpoint and header for request to yelp API
api_key = 'Uwp9Zz4K0F4VfCus7U3GWbbKbik7sX4UOdA7r8ir2XONuRcg1natwEwxNsxfeshBwvzxuBDuKJMziT9JnkJhQU6Ez20FGer5h-CJiVJW35DIbXvgnLol6IJ2EW47YXYx'
end_point = 'https://api.yelp.com/v3/businesses/search'
resp_header = {'Authorization': 'bearer {}'.format(api_key)}

#define parameters
parameters = {'term':'gym',
                'limit':5,
                'radius':3200,
                'location':'{}'.format(zip_code),
                'sort_by':'rating',
                }

#make api call
response = requests.get(url=end_point, params=parameters, headers=resp_header)

#Change json into dict then to pandas dataframe
gym_dict = response.json()

#set columns we want to display
gym_df = pd.DataFrame(columns=('Picture','Name','Location','Rating','Phone#'))
#unpack the json
for valg in gym_dict['businesses']:
    if valg in gym_dict['businesses']:
        #only display street address
        valg['location']['display_address'] = valg['location']['display_address'][0]
        '''create dataset. This will result in a creation of a tuple, which then can turned into a list and 
        then into a panda series which then can be appended onto the dataframe.
        This function is so we can choose which specific information we want from yelp.
        '''
        data = valg['image_url'],valg['name'],valg['location']['display_address'],valg['rating'],valg['phone']
        datalist = list(data)
        seriesly = pd.Series(datalist, index = gym_df.columns)
        gym_df = gym_df.append(seriesly, ignore_index=True)
        #ORDER DATAFRAME BY RATING
        gym_df = gym_df.sort_values(by=['Rating'], ascending=False)
        #gym_df.to_html(headers='True', table_id='my_table')

display(gym_df)
    #ORDER DATAFRAME BY RATING
#gym_df = gym_df.sort_values(by=['Rating'], ascending=False)

