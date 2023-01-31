import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

st.title("Netflix EDA")
@st.cache        
def pre_processing():
    
    df = pd.read_csv("data.csv")
    df['director'] = df['director'].fillna("Other")
    df['cast'] = df['cast'].fillna("Other")
    df['country'] = df['country'].fillna("Other")
    
    df.dropna(how="any", subset=["date_added", "rating"], inplace=True)
    
    
    return df

clean_df = pre_processing()
count_value = clean_df['rating'].value_counts()
genre_count = clean_df['genres'][:15].value_counts()

if st.button("Show Duration vs Release Year"):
    fig = plt.figure(figsize=(10, 4))
    sns.lineplot(x = "release_year", y = "duration", data = clean_df)
    st.pyplot(fig)

if st.button("Show Data"):
    st.dataframe(clean_df)
    
if st.button("Average Releases Comparison"):
    
    df_year_count = clean_df.groupby(['release_year']).size().reset_index(name='number_of_movies_released')

    year = st.number_input("Enter The Year", value=2000)
    result=df_year_count.loc[df_year_count['release_year'] == year,'number_of_movies_released'].values[0]
    st.write(result)
    average_num_of_movies = round(df_year_count['number_of_movies_released'].mean())

    df_to_plot = pd.DataFrame([[result, average_num_of_movies]], columns=['Number of Movies Released in The Year', 'Average Number of Movies Released'])
    st.table(data=df_to_plot)
    st.bar_chart(df_to_plot)



if st.button("Show Rating Data"):
    
    st.bar_chart(count_value)
    
if st.button("Genre Distribution"):
    fig1, ax1 = plt.subplots()
    ax1.pie(genre_count,labels=clean_df['genres'][:15], autopct='%1.1f%%',
        shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    st.pyplot(fig1)