import pandas as pd
import numpy as np
import streamlit as st
import matplotlib 
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import json
import folium
from folium.plugins import MarkerCluster  




# 파일 읽기
df_station = pd.DataFrame(pd.read_csv('data/merged_data.csv',encoding='cp949',index_col = 0))
df_outside = pd.read_csv('data/pub_rest_gu.csv', encoding='cp949')
group = pd.read_csv('data/grouped_stations.csv',encoding='cp949')



# 멘트
st.title("🚽화장실 급하시죠?🚽")
st.write('---------------------------------------------')
st.sidebar.title("현재 위치를 알려주세요")




# ---------------------------그래프 시작-----------------------------------


# 호선 별 리모델링연도 평균 ( line )
df_st = df_station[['리모델링연도']]
df_st = df_st.reset_index()

fig_line = go.Figure()

df_first = df_st.groupby(['운영노선명'], as_index=False).mean()

fig_line.add_trace(go.Line(
    x = df_first.운영노선명,
    y = df_first.리모델링연도,
))

fig_line.update_layout(title_text=f"운영 노선별 리모델링연도 평균", title_x = 0.4)
fig_line.update_xaxes(title_text='운영노선명')
fig_line.update_yaxes(title_text='연도평균')
    
# 구 별 화장실 개수
df_gu = pd.value_counts(df_outside['구명'])
df_gu = pd.DataFrame(df_gu).reset_index()

# 역 별 화장실 개수
df_stt = pd.value_counts(df_station.reset_index().운영노선명)
df_stt = pd.DataFrame(df_stt).reset_index()


# 두 개의 그래프를 그리기 위해 subplot을 사용
fig_bar = make_subplots(rows=1, cols=2, column_widths=[0.5, 0.5])


# 두 개의 Bar를 추가
fig_bar.add_trace(go.Bar(
    x=df_gu.구명, 
    y=df_gu.iloc[:,1], 
    showlegend=False,
    marker=dict(
        color=['aliceblue', 'antiquewhite', 'aqua', 'aquamarine', 'azure',
        'beige', 'bisque', 'black', 'blanchedalmond', 'blue',
        'blueviolet', 'brown', 'burlywood', 'cadetblue',
        'chartreuse', 'chocolate', 'coral', 'cornflowerblue',
        'cornsilk', 'crimson', 'cyan', 'darkblue', 'darkcyan',
        'darkgoldenrod', 'darkgray'],
        line=dict(color='black', width=3),
        pattern=dict(shape='x')
    ),  
    width=0.5
    ), row=1, col=1)

fig_bar.add_trace(go.Bar(
    x=df_stt.운영노선명,
    y=df_stt.iloc[:,1], 
    showlegend=False,

    # 꾸미기
    marker=dict(
        color=['#A05EB5', '#00B140', '#A9431E', '#67823A', '#E31C79', '#00A9E0', '#FC4C02', '#0032A0'],  # 색상 리스트
        line=dict(color='black', width=3),
        pattern=dict(shape='/')
    ),  
    width=0.5
    ), row=1, col=2)
fig_bar.update_layout(
    title={
        'text':"구 / 역 별 화장실 개수",
        'font':{'size':40, 'color':'white'}},
    paper_bgcolor='#2C2C2C',
    plot_bgcolor='#1F1F2E',
    
    
    xaxis=dict(
        title='구 명',
        titlefont=dict(color='white'), 
        tickfont=dict(color='white', size = 5)
    ),
    yaxis=dict(
        title='화장실 개수', 
        titlefont=dict(color='white'),
        tickfont=dict(color='white')
    ),
    xaxis2=dict( 
        title='노선명', 
        titlefont=dict(color='white'),
        tickfont=dict(color='white')
    ),
    yaxis2=dict( 
        title='화장실 개수',  
        titlefont=dict(color='white'), 
        tickfont=dict(color='white') 
    )
)


# ---------------------------그래프 끝-----------------------------------




# 구 입력
gu = st.sidebar.selectbox(
    "가까운 구 이름을 선택하세요",
    (sorted(set(df_station['구']))),
    index=None,
    placeholder="ex) 노원구",
)

fs = group[group['구'] == gu].역사명


# 역 입력
station =st.sidebar.selectbox(
    "가까운 역 이름을 선택하세요",
    (sorted(set(fs))),
    index=None,
    placeholder="ex) 서울역",
)


# 검색 버튼으로 내용 표시
bt = st.sidebar.button('검색')
if bt:
    df_st = df_station[df_station.역명 == station]
    station2 = station.rstrip('역')
    df_os = df_outside[df_outside.가까운역 == station2]

    # 역 외부에 화장실이 없을 경우
    if df_station[df_station.역명 == station].empty:
        st.write('### 어머 ❗❗ 내부화장실만 있나봐요 ㅠㅠ 어떡해⏱⏱')
    else: # 역 외부에 화장실이 있을 경우
        st.write(f'### ➤ {station}엔 외부화장실이 {len(df_st)}개 있어요 !!')
        st.dataframe(df_st[['역명', '리모델링연도', '위도', '경도']])
        
    # 다른 역보다 거리상으로 가까운 공중화장실이 없을 경우
    if df_outside[df_outside.가까운역 == station2].empty:
        st.write('### 다른 역이 더 가까운걸까요~~~?😨')
    else:# 다른 역보다 거리상으로 가까운 공중화장실이 있을 경우
        st.write(f'### ➤ {station2}역 근처엔 공중화장실이 {len(df_os)}개 있어요 !!')
        left_column, right_column = st.columns(2)
        left_column.dataframe(df_os[['구명', '위도', '경도']])
        right_column.write("##### \n 🍀🍄🦋🌸♏️💗🍀 \n")
        right_column.write("##### 르끼비끼잖아 ❓❗❓❓")
    
    

    
    # 서울시군구 정보를 담은 geojson파일 읽어오기
    file_path = 'data/seoulsigungu.geojson'
    with open(file_path, 'r', encoding='utf-8') as file:
        seoulsigungu = json.load(file)    


    toilet = df_outside.groupby(['구명'])['가까운역'].count().sort_values(ascending = False)
    
    # 가까운 화장실이 없을 경우 전체 화장실의 위도 평균, 경도 평균을 내 위치로 설정
    none_lat = df_outside.위도.mean()
    none_lon = df_outside.경도.mean()

    

    # 가까운 화장실이 없을 경우
    if df_station[(df_station.역명 == station)].empty:
        fig = px.choropleth_map(toilet, geojson=seoulsigungu, locations=toilet.index, color='가까운역',# 가까운 역이지만 count된 숫자임
                                color_continuous_scale="Viridis",
                                map_style="carto-positron",
                                zoom=9, center = {"lat":none_lat , "lon":none_lon},
                                    featureidkey='properties.SIG_KOR_NM'
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        


        st.write('### ➤ 제 맘대로 위치를 정할게요~')

        map = folium.Map(location=[none_lat, none_lon], zoom_start=16)

        for idx, row in df_outside.iterrows(): 
            folium.CircleMarker([row['위도'], row['경도']], radius = 4, color = 'red' ,fill= True,
                                fill_color = 'red', fill_opacity = 1).add_to(map)
        folium.Marker(location=[none_lat, none_lon]).add_to(map)
        st.components.v1.html(map._repr_html_(), height=600)

        # 화장실 분포를 색으로 표현
        st.write("### ➤ 구 별 화장실 분포")
        st.plotly_chart(fig, use_container_width = True)
    else: # 가까운 곳에 화장실이 있을 경우
        
        # 역을 내 위치로 설정
        lat_lon = df_station[(df_station.역명 == station)].iloc[0]

        fig = px.choropleth_map(toilet, geojson=seoulsigungu, locations=toilet.index, color='가까운역',
                                color_continuous_scale="Viridis",
                                map_style="carto-positron",
                                zoom=9, center = {"lat":lat_lon.위도 , "lon":lat_lon.경도},
                                    featureidkey='properties.SIG_KOR_NM'
                                )
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
        
        


        st.write(f'### ➤ {station}으로 설정할게요.\n')
        map = folium.Map(location=[lat_lon.위도, lat_lon.경도], zoom_start=16)


        for idx, row in df_outside.iterrows(): 
            folium.CircleMarker([row['위도'], row['경도']], radius = 4, color = 'red' ,fill= True,
                                fill_color = 'red', fill_opacity = 1).add_to(map)

        folium.Marker(location=[lat_lon.위도, lat_lon.경도]).add_to(map)
        # location = []
        # for idx, row in df_outside.iterrows(): 
        #     location.append([row['위도'], row['경도']])
        
        # MarkerCluster( location, overlay=True).add_to(map)

        st.components.v1.html(map._repr_html_(), height=600)
        st.write("### ➤ 구 별 화장실 분포")
        st.plotly_chart(fig, use_container_width = True)


    # 리모델링연도 평균 line 그래프
    st.write("## 잠깐❗❗❗")
    st.write("### 깨끗할수록 좋잖아요~ ヾ( ˃ᴗ˂ )◞ • *✰")
    st.plotly_chart(fig_line, use_container_width = True)
    st.write('## 🤶🏻햅삐뉴이어〰〰〰')
    st.plotly_chart(fig_bar, use_container_width= True)