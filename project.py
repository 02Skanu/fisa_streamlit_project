import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import json
import folium
from folium.plugins import MarkerCluster  

df_station = pd.DataFrame(pd.read_csv('C:/ITStudy/fisa_streamlit_project/data/merged_data.csv',encoding='cp949',index_col = 0))
df_outside = pd.read_csv('C:/ITStudy/fisa_streamlit_project/data/pub_rest_gu.csv', encoding='cp949')
group = pd.read_csv('C:/ITStudy/fisa_streamlit_project/data/grouped_stations.csv',encoding='cp949')

st.title("화장실 급하시죠?")
st.write('---------------------------------------------')
st.write('### 근처 공중 및 지하철역 화장실을 알려드려요!!')
st.sidebar.title("현재 위치를 알려주세요")



gu = st.sidebar.selectbox(
    "가까운 구 이름을 선택하세요",
    (sorted(set(group['구']))),
    index=None,
    placeholder="ex) 노원구",
)

fs = group[group['구'] == gu].역사명

station =st.sidebar.selectbox(
    "가까운 역 이름을 선택하세요",
    (sorted(set(fs))),
    index=None,
    placeholder="ex) 서울역",
)



bt = st.sidebar.button('검색')
if bt:
    
    df_st = df_station[df_station.역명 == station]
    station2 = station.rstrip('역')
    
    df_os = df_outside[df_outside.가까운역 == station2]
    st.write('### 가까운 지하철역 화장실 좌표')
    st.dataframe(df_st[['역명', '리모델링연도', '위도', '경도']])
    st.write('### 가까운 공중화장실 좌표')
    st.dataframe(df_os[['구명', '위도', '경도', '가까운역']])


    

    file_path = 'C:/ITStudy/fisa_streamlit_project/data/seoulsigungu.geojson'

# 파일을 안전하게 열고 JSON 데이터를 로드
    with open(file_path, 'r', encoding='utf-8') as file:
        seoulsigungu = json.load(file)    #geojson['features'][]['properties']['SIG_KOR_NM'] # 구 이름
    # 매장수2에 있는 시군구명을 기준으로 seoulsigungu의 SIG_KOR_NM이 일치하면 그 자리에 상호명에 들어있는 숫자를 색깔로 표현
    toilet = df_outside.groupby(['구명'])['가까운역'].count().sort_values(ascending = False)
    
    lat_lon = df_station[(df_station.역명 == station)].iloc[0]


    fig = px.choropleth_map(toilet, geojson=seoulsigungu, locations=toilet.index, color='가까운역',
                            color_continuous_scale="Viridis",
                            map_style="carto-positron",
                            zoom=9, center = {"lat":lat_lon.위도 , "lon":lat_lon.경도},
                                featureidkey='properties.SIG_KOR_NM'
                            )
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
    
    st.plotly_chart(fig, use_container_width = True)


    
    map = folium.Map(location=[lat_lon.위도, lat_lon.경도], zoom_start=16)


    for idx, row in df_outside.iterrows(): 
        folium.CircleMarker([row['위도'], row['경도']], radius = 4, color = 'red' ,fill= True,
                            fill_color = 'red', fill_opacity = 1).add_to(map)

    folium.Marker(location=[lat_lon.위도, lat_lon.경도]).add_to(map)
    # location = []
    # for idx, row in df_outside.iterrows(): 
    #     location.append([row['위도'], row['경도']])
    
    # MarkerCluster( location, overlay=True).add_to(map)

    st.components.v1.html(map._repr_html_(), height=1200)