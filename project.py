import pandas as pd
import numpy as np
import streamlit as st
import plotly.express as px
import json
import folium
import plotly.graph_objects as go  
from folium.plugins import MarkerCluster  

# 파일 읽기
df_station = pd.DataFrame(pd.read_csv('C:/ITStudy/fisa_streamlit_project/data/merged_data.csv',encoding='cp949',index_col = 0))
df_outside = pd.read_csv('C:/ITStudy/fisa_streamlit_project/data/pub_rest_gu.csv', encoding='cp949')
group = pd.read_csv('C:/ITStudy/fisa_streamlit_project/data/grouped_stations.csv',encoding='cp949')


# 멘트
st.title("🚽화장실 급하시죠?🚽")
st.write('---------------------------------------------')
st.sidebar.title("현재 위치를 알려주세요")


# 호선 별 리모델링연도 평균 ( line )



df_st = df_station[['리모델링연도']]
df_st = df_st.reset_index()

fig = go.Figure()

df_first = df_st.groupby(['운영노선명'], as_index=False).mean()

fig.add_trace(go.Line(
    x = df_first.운영노선명,
    y = df_first.리모델링연도,
))

fig.update_layout(title_text=f"운영 노선별 리모델링연도 평균", title_x = 0.4)
fig.update_xaxes(title_text='운영노선명')
fig.update_yaxes(title_text='연도평균')
        


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


    if df_station[df_station.역명 == station].empty:
        st.write('### 어머 !! 내부화장실만 있나봐요 ㅠㅠ 어떡해')
    else:
        st.write(f'### {station}엔 외부화장실이 {len(df_st)}개 있어요 !!')
        st.dataframe(df_st[['역명', '리모델링연도', '위도', '경도']])
        
    
    if df_outside[df_outside.가까운역 == station2].empty:
        st.write('### 다른 역이 더 가까운걸까요~~~?')
    else:
        st.write(f'### {station2}역 근처엔 공중화장실이 {len(df_os)}개 있어요 !!')
        left_column, right_column = st.columns(2)
        left_column.dataframe(df_os[['구명', '위도', '경도']])
        right_column.write("##### \n 🍄🦋🌸♏️💗 \n")
        right_column.write("##### 르끼비끼잖아 ?!??")
    
    
    
    
    

    

    

    file_path = 'C:/ITStudy/fisa_streamlit_project/data/seoulsigungu.geojson'


    with open(file_path, 'r', encoding='utf-8') as file:
        seoulsigungu = json.load(file)    
    toilet = df_outside.groupby(['구명'])['가까운역'].count().sort_values(ascending = False)
    none_lat = df_outside.위도.mean()
    none_lon = df_outside.경도.mean()
    print('------', none_lat, none_lon)
    if df_station[(df_station.역명 == station)].empty:
        fig = px.choropleth_map(toilet, geojson=seoulsigungu, locations=toilet.index, color='가까운역',
                                color_continuous_scale="Viridis",
                                map_style="carto-positron",
                                zoom=9, center = {"lat":none_lat , "lon":none_lon},
                                    featureidkey='properties.SIG_KOR_NM'
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        st.plotly_chart(fig, use_container_width = True)


        st.write('### 제 맘대로 위치를 정할게요~')
        map = folium.Map(location=[none_lat, none_lon], zoom_start=16)


        for idx, row in df_outside.iterrows(): 
            folium.CircleMarker([row['위도'], row['경도']], radius = 4, color = 'red' ,fill= True,
                                fill_color = 'red', fill_opacity = 1).add_to(map)

        folium.Marker(location=[none_lat, none_lon]).add_to(map)

        st.components.v1.html(map._repr_html_(), height=1200)
    else:
        
        lat_lon = df_station[(df_station.역명 == station)].iloc[0]

        fig = px.choropleth_map(toilet, geojson=seoulsigungu, locations=toilet.index, color='가까운역',
                                color_continuous_scale="Viridis",
                                map_style="carto-positron",
                                zoom=9, center = {"lat":lat_lon.위도 , "lon":lat_lon.경도},
                                    featureidkey='properties.SIG_KOR_NM'
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        st.plotly_chart(fig, use_container_width = True)


        st.write(f'### {station}으로 설정할게요.\n')
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

    st.write("## 잠깐❗❗❗")
    st.write("### 깨끗할수록 좋잖아요~ ヾ( ˃ᴗ˂ )◞ • *✰")
    st.plotly_chart(fig, use_container_width = True)