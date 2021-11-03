import requests as reqs
import yelpapi
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
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
import json
import sys

# class postgrescon:
#     def __init__(self):
#         self.conn = psycopg2.connect(
#             database="postgres",
#             user="postgres",
#             password="1123",
#             host='localhost',
#             port='5432')

#         self.cursor = self.conn.cursor()
class apiconfig:
    def yapiconvert():
        pd.set_option('max_colwidth', 400)
#define api key, endpoint and header for request to yelp API
        api_key = 'api_key_here'
        end_point = 'https://api.yelp.com/v3/businesses/search'

        resp_header = {'Authorization': 'bearer {}'.format(api_key)}

#define parameters
        parameters = {'term':'gym',
                        'limit':5,
                        'radius':3200,
                        'location':'{}'.format(11214),
                        'sort-by':'rating'
                        }
        
        parameters2 = {
                            }
#make api call
        response = reqs.get(url=end_point, params=parameters, headers=resp_header)

#Change json into dict then to pandas dataframe
        gym_dict = response.json()

        gym_df = pd.DataFrame(columns=('Picture','Name','Location','Rating','Phone#','Business ID'))
        df = pd.DataFrame(columns=['Reviews','Rating'])



        for valg in gym_dict['businesses']:
            #only display street address
            valg['location']['display_address'] = valg['location']['display_address'][0]
            '''create dataset. This will result in a creation of a tuple, which then can turned into a list and 
            then into a panda series which then can be appended onto the dataframe.
            This function is so we can choose which specific information we want from yelp.
            '''
            data = valg['image_url'],valg['name'],valg['location']['display_address'],valg['rating'],valg['phone'],valg['id']
            datalist = list(data)
            seriesly = pd.Series(datalist, index = gym_df.columns)
            business_id = seriesly['Business ID']
            end_point2 = 'https://api.yelp.com/v3/businesses/{}/reviews'.format(business_id)
            response2 = reqs.get(url=end_point2, params=parameters2, headers=resp_header)
            gym_dict2 = response2.json()


            for valr in gym_dict2['reviews']:
                data1 = valr['text'],valr['rating']
                datalist1 = list(data1)
                seriesly1 = pd.Series(datalist1, index = df.columns)
                df = df.append(seriesly1, ignore_index=True)
                #df.insert(6, ['Reviews','Rating'] , seriesly1)
            else:
                print('...next')
                #gym_df = gym_df.append(seriesly, ignore_index=True)   
        df['Word Count'] = df['Reviews'].apply(lambda x: len(x.split()))
        #sns.countplot(x='Rating', data=df, palette='rainbow')   
        #plt.show()
        print(gym_dict2)

        #print(valr['text'])
    
if __name__ == '__main__':
    apiconfig.yapiconvert()
    
    