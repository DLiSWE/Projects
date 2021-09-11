import requests
import yelpapi
import pandas as pd
from IPython.display import display
from flask import Flask

zip_code = '11214'#input('Zipcode')

#Client ID
client_id = 'Cev8jNKeXB1tVYbl3wwIUw'

#define api key, endpoint and header for request to yelp API
api_key = 'Uwp9Zz4K0F4VfCus7U3GWbbKbik7sX4UOdA7r8ir2XONuRcg1natwEwxNsxfeshBwvzxuBDuKJMziT9JnkJhQU6Ez20FGer5h-CJiVJW35DIbXvgnLol6IJ2EW47YXYx'
end_point = 'https://api.yelp.com/v3/businesses/search'
resp_header = {'Authorization': 'bearer {}'.format(api_key)}

#define parameters
parameters = {'term':'gym',
                'limit':10,
                'radius':3200,
                'location':'{}'.format(zip_code),
                'sort-by':'rating'}

#make api call
response = requests.get(url=end_point, params=parameters, headers=resp_header)

#Change json into dict then to pandas dataframe
gym_dict = response.json()

#set columns we want to display
gym_df = pd.DataFrame(columns=('Picture','Name','Location','Rating','Website Link','Phone#','distance(m)','business_id'))

#print(subcat)
#gym_pandas = pd.json_normalize(gym_dict)
#print(gym_pandas)
#gym_pand = pd.DataFrame.to_dict(gym_dict)
def unpacker(*args):
    global gym_df
    #unpack the json
    for unpac in gym_dict['businesses']:
        #only display street address
        unpac['location']['display_address'] = unpac['location']['display_address'][0]
        '''create dataset. This will result in a creation of a tuple, which then can to turned into a list and then into a panda series which then can be appended onto the dataframe
        This function is so we can choose which specific information we want from yelp.
        '''
        #print(unpac)
        data = unpac['image_url'],unpac['name'],unpac['location']['display_address'],unpac['rating'],unpac['url'],unpac['phone'],unpac['distance'],unpac['id']
        datalist = list(data)
        seriesly = pd.Series(datalist, index = gym_df.columns)
        gym_df = gym_df.append(seriesly, ignore_index=True)

unpacker()
display(gym_df)

#Take the top 3 most useful/helpful comments



#send dataframe to HTML table
#TODO:FLASK <--LOOK
# @app.route("/")
# def home():
#     return render_template('index.html' column_names=gym_df.columns.values, row_data=list(gym_df.values.tolist()), zip=zip))

