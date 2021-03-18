import pandas as pd

# read data
df = pd.read_csv('./data/annotated_data.tsv', sep='\t')

# crimes per year
df['arquivo_date'] = pd.to_datetime(df.arquivo_date, errors='coerce')
df_crimes = df[df['annotated_data'] == 'y']
df_crimes['dateyear'] = df_crimes['arquivo_date'].dt.year
res = pd.DataFrame(df_crimes.groupby(['dateyear']).size())
res['year'] = res.index
res.to_csv('./data/crimes_per_year.tsv',sep='\t',index=False)

# table crimes
df_crimes[['news_site_title','search_newspaper','dateyear']].to_csv('./data/table_crimes.tsv',sep='\t',index=False)

# News per location
# we will use geo locator to help us getting the country and region
import spacy
from geopy.geocoders import Nominatim
import time

nlp = spacy.load('pt_core_news_lg')
geolocator = Nominatim(user_agent="dictionary_experiment")

# we define a minimum quality for the result from the geolocator
geo_quality_threshold = 0.55

# we define new dataframe columns with values to replace late
df_crimes['country'] = 'missing'
df_crimes['region'] = 'missing'
df_crimes['lat'] = 999
df_crimes['lon'] = 999

# for every row we try to compute those values
for iter, row in df_crimes.iterrows():

    if (row['annotated_data'] == 'y'):

        # help debug
        print('')
        print(row['news_site_title'])

        # this will extract entities from spacy
        doc = nlp(row['news_site_text'] + ' ' + row['news_site_title'])

        # define storage variables
        locals_name = []
        locals_country = []
        locals_region = []
        locals_lat = []
        locals_lon = []

        # for every identified entity
        for entity in doc.ents:
            # we only want location entities
            if entity.label_ == 'LOC':
                # for debug
                print(entity.label_)
                print(entity.text)
                # we try to locate the entity
                try:
                    lc = geolocator.geocode(entity.text, timeout=10)
                    time.sleep(2)

                    # sometimes the geo object returned is none
                    if lc is not None:
                        geo_evaluation = lc.raw['importance']

                        # when the result has a certain quality
                        if geo_evaluation > geo_quality_threshold:
                            print(lc.raw)
                            # we get the desired variables
                            type_org = lc.raw['type']
                            lat = lc.raw['lat']
                            lon = lc.raw['lon']
                            relc = geolocator.reverse([lc.latitude, lc.longitude], language='en')
                            print(relc.raw['address'])
                            country = relc.raw['address']['country']

                            # if country is portugal we want to know the district, we dont ask for all because the json names vary according to country
                            if country == 'Portugal':
                                try:
                                    region = relc.raw['address']['state_district']
                                except:
                                    try:
                                        region = relc.raw['address']['state']
                                    except:
                                        region = 'unknown'
                            else:
                                region = 'unknown'

                            # we store the found values
                            locals_name.append(entity.text)
                            locals_country.append(country)
                            locals_region.append(region)
                            locals_lat.append(lat)
                            locals_lon.append(lon)

                except Exception as e:
                    print('')
                    print('error')
                    print(e)

        # helps debug
        print(locals_name)
        print(locals_country)
        print(locals_region)
        print(locals_lat)
        print(locals_lon)

        country = 'unknown'
        region = 'unknown'
        lat = 999
        lon = 999
        # choose the country that is the majority and add this to the country column
        percentage_portugal = 0
        # prevents division by 0
        if len(locals_country) > 0:
            percentage_portugal = locals_country.count('Portugal') / len(locals_country)
            if percentage_portugal >= 0.5:
                country = 'Portugal'
            else:
                country = max(set(locals_country), key=locals_country.count)

            # make the average of latitude and longitude, because they are very close so we can just average
            msk = [el == country for el in
                   locals_country]  # mask to select in a list the elements that are for the desired country
            locals_lat = [locals_lat[i] for i in range(len(locals_lat)) if msk[i]]
            locals_lon = [locals_lon[i] for i in range(len(locals_lon)) if msk[i]]
            locals_lat = list(map(float, locals_lat))
            locals_lon = list(map(float, locals_lon))
            lat = sum(locals_lat) / len(locals_lat)
            lon = sum(locals_lon) / len(locals_lon)

            # and ask to the api again to which region does it correspond and add it to the dataframe
            try:
                relc = geolocator.reverse([lat, lon], language='en')
                time.sleep(2)
            except:
                region = 'unknown'

            try:
                region = relc.raw['address']['state_district']
            except:
                try:
                    region = relc.raw['address']['state']
                except:
                    region = 'unknown'

        print(region)

        # add values in the dataframe column
        df_crimes['country'].iloc[iter] = country
        df_crimes['region'].iloc[iter] = region
        df_crimes['lat'].iloc[iter] = lat
        df_crimes['lon'].iloc[iter] = lon

df_crimes.to_csv('.data/df_crimes_geo_location.tsv',sep='\t',index=False)

### prepare data for maps

from shapely.geometry import Point, Polygon
import pandas as pd
import geopandas as gpd
import numpy as np
import matplotlib.pyplot as plt

# read geo maps
continental_states = gpd.read_file('pt_continental.geojson')
azores_states = gpd.read_file('pt_açores.geojson')
madeira_states = gpd.read_file('pt_madeira.geojson')

# read  crimes data
df_crimes = pd.read_csv('.data/df_crimes_geo_location.tsv', sep='\t')
df_crimes_portugal = df_crimes[df_crimes['country'] == 'Portugal']

# give a region to a crime
import json
from shapely.geometry import shape, Point

def point_which_portuguese_district(point):
  msk = continental_states.contains(point)
  if sum(msk) != 0:
    return [continental_states['Distrito'][i] for i in range(len(continental_states['Distrito'])) if msk[i]][0]
  msk = azores_states.contains(point)
  if sum(msk) != 0:
    return [azores_states['NUT1_DSG'][i] for i in range(len(azores_states['NUT1_DSG'])) if msk[i]][0]
  msk = madeira_states.contains(point)
  if sum(msk) != 0:
    return [madeira_states['Ilha'][i] for i in range(len(madeira_states['Ilha'])) if msk[i]][0]
  return 'none'

df_crimes_portugal['district'] = 'empty'
for iter, row in df_crimes_portugal.iterrows():
  district = point_which_portuguese_district(Point(row['lon'],row['lat']))
  df_crimes_portugal.at[iter,'district'] = district

print(df_crimes_portugal)

#Divide crimes per continental, madeira, azores
df_crimes_portugal['cont_mad_azo'] = 'unknown'
df_crimes_portugal.loc[df_crimes_portugal['district'].isin(continental_states['Distrito'].values),'cont_mad_azo'] = 'continental'
df_crimes_portugal.loc[df_crimes_portugal['district'].isin(azores_states['NUT1_DSG'].values),'cont_mad_azo'] = 'açores'
df_crimes_portugal.loc[df_crimes_portugal['district'].isin(madeira_states['Ilha'].values),'cont_mad_azo'] = 'madeira'

# Continental
res = df_crimes_portugal.groupby(['district']).size()
dict_crimes_district = dict(res)

res = []
for state in continental_states['Distrito']:
  if state in dict_crimes_district:
    res.append(dict_crimes_district[state])
  else:
    res.append(0)
print(res)

continental_states['Count_Placeholder'] = 0
continental_states['Count_Placeholder'][:18] = res
