import pandas as pd
import json
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objects as go

## This file is working as of OCT30


def createSaskMap():
    # First import of data to provide NGHD_ID to identify neighborhoods
    df = pd.read_csv('NeighbourhoodArea.csv', dtype={'NGHD_ID': str})
    df_test = df[['NGHD_ID', 'gid', 'Name']]
    df_data = pd.read_csv('NeighbourhoodHousingCosts.csv')
    df_data.rename(columns={'neighbourhood' : 'Name'}, inplace=True)
    # Merge the two dataframes using neighbourhood name.
    # Keeps all neighbourhoods found in df_test
    df_final = pd.merge(df_test, df_data, how = 'left', on='Name')

    # df_final.columns

    # #df_data.head()

    # Import CSV file for NeighbourhoodArea from saskatoon
    url2 = 'http://opendata-saskatoon.cloudapp.net/DataBrowser/DownloadCsv?container=SaskatoonOpenDataCatalogueBeta&entitySet=NeighbourhoodArea&filter=NOFILTER'
    df_url = pd.read_csv(url2)
    df_url.rename(columns = {'name':'Name'}, inplace=True)
    df_url.drop(columns = ['entityid'], inplace=True)
    df_url['blank'] = 1


    url_population = 'http://opendata-saskatoon.cloudapp.net/DataBrowser/DownloadCsv?container=SaskatoonOpenDataCatalogueBeta&entitySet=NeighbourhoodPopulation&filter=NOFILTER'
    #url_income = 'http://opendata-saskatoon.cloudapp.net/DataBrowser/DownloadCsv?container=SaskatoonOpenDataCatalogueBeta&entitySet=NeighbourhoodPersonalIncome&filter=NOFILTER'

    df_url_pop = pd.read_csv(url_population)
    df_url_pop.rename(columns = {'neighbourhood':'Name'}, inplace=True)
    df_url_pop.drop(columns = ['entityid'], inplace = True)

    # df_url_inc = pd.read_csv(url_income)
    # df_url_inc.rename(columns = {'neighbourhood':'Name'}, inplace=True)

    df_url_merge = pd.merge(df_url, df_url_pop, on='Name', how='left')
    df_url_merge = df_url_merge.apply(pd.to_numeric, errors="ignore")

    # df_url_merge[["year_2012", "year_2013", "year_2014", "year_2015"]] = df_url_merge.to_nurmeric([["year_2012", "year_2013", "year_2014", "year_2015"]])

    #df_url_merge = df_url_merge.dropna()

    # Imports geojson map data to draw the map. 
    inMap = 'NeighbourhoodArea.geojson'
    with open(inMap) as response:
        sask_map = json.load(response)

    # Adds an 'id' key to the data which corresponds to NGHD_ID
    # Allows the imported data above to match the id key here
    geo_sask_map = sask_map.copy()
    #print(geo_sask_map['features'][2]['properties']['Name'])
    for neighborhood in geo_sask_map['features']:
        ID = neighborhood['properties']['Name']
        neighborhood['id'] = ID


    fig = px.choropleth_mapbox(df_url_merge, geojson=geo_sask_map, locations='Name', color='blank',
                            color_continuous_scale="Viridis", 
                            #range_color=(0, 12),
                            # mapbox_style="carto-positron",
                            # zoom=10, center = {"lat": 52.1080, "lon": -106.6700},
                            opacity=0.1,
                            hover_name='Name', hover_data = ['year_2012']
    #                           labels={'unemp':'unemployment rate'}
                            )
    
    overlay = px.choropleth_mapbox(df_url_merge.dropna(), geojson=geo_sask_map, locations='Name', color='year_2012',
                            #    color_continuous_scale="Viridis", 
                            range_color=(500, 11000),
                            #    mapbox_style="carto-positron",
                            #    zoom=10, center = {"lat": 52.1080, "lon": -106.6700},
                            opacity=0.5,
                            hover_name='Name', 
                            hover_data = ['year_2012'],
                                labels={'unemp':'unemployment rate'}
                            ).data[0]
    fig.add_trace(overlay)
    fig.update_layout(mapbox_style="carto-positron",
                    mapbox_zoom=10, mapbox_center = {"lat": 52.1080, "lon": -106.6700})
    return fig

if __name__ == "__main__":
    figure = createSaskMap()
    pyo.plot(figure)
