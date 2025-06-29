
import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("waterPollution.csv",index_col = 0)
df2 = pd.read_csv('cleaned_data.csv',index_col = 0)

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page:", ["Data", "Plots", "Custom Plot"])

# Page 1: Display Data
if page == "Data":
    st.title("Water Pollution Dataset")
    st.write("### Raw Data")
    st.dataframe(df)
    st.write("### Cleaned Data")
    st.dataframe(df2)

# Page 2: Plots
elif page == "Plots":
    st.title("Pollution Analysis Plots")

    st.subheader("1. Purest Countries by Safe Samples")
    puriest_country = df2[df2['pollution_status'] == 1].groupby('Country')['pollution_status'].count().sort_values(ascending=False).reset_index()
    fig1 = px.bar(puriest_country, x='Country', y='pollution_status', title='The Purest Countries by Count of Safe Samples', labels={'pollution_status': 'Safe Sample Count'})
    st.plotly_chart(fig1)

    st.subheader("2. Safe Water Samples vs Population Density")
    pop_poll = df2.groupby('Country')['PopulationDensity'].value_counts().sort_values(ascending=False).reset_index()
    pop_poll = pop_poll.sort_values(by='PopulationDensity', ascending=False).reset_index(drop=True)
    population_polluation = pd.merge(puriest_country, pop_poll, on='Country').drop('count', axis=1)
    fig2 = px.bar(population_polluation, x='Country', y='pollution_status', color='PopulationDensity', title='Safe Water Samples per Country (Sorted by Population Density)', labels={'pollution_status': 'Safe Sample Count','PopulationDensity': 'Population Density'}, color_continuous_scale='Viridis')
    st.plotly_chart(fig2)

    st.subheader("3. Safe Water Samples by Tourism Level")
    tour_pollution = df2.groupby('Country')['TouristMean_1990_2020'].value_counts().reset_index().sort_values(by='TouristMean_1990_2020',ascending = False)
    merged_df = pd.merge(puriest_country,tour_pollution, on = 'Country').drop('count',axis= 1)
    fig3 = px.bar(merged_df, x='Country', y='pollution_status', color='TouristMean_1990_2020', title='Safe Water Samples by Country (Colored by Tourism Level)', labels={'pollution_status': 'Safe Sample Count','TouristMean_1990_2020': 'Avg. Tourists (1990–2020)'}, color_continuous_scale='Blues')
    st.plotly_chart(fig3)


    st.subheader("4. Net Migration by Country and Pollution Status")
    migration_polliation_affect = (df2.groupby(['Country','pollution_status'])['netMigration_2011_2018'].value_counts().reset_index()).sort_values(by='netMigration_2011_2018',ascending = False)
    fig4 = px.bar(migration_polliation_affect,x='Country',y='netMigration_2011_2018',color='pollution_status',barmode='group',title='Net Migration by Country and Pollution Status',labels={'netMigration_2011_2018': 'Avg. Net Migration (2011–2018)','pollution_status': 'Pollution Status (0 = Unsafe, 1 = Safe, 2 = Unsure)'})
    st.plotly_chart(fig4)

    st.subheader("5. Protected Area vs Pollution Status")
    protected_area = df2.groupby(['Country', 'pollution_status'])['TerraMarineProtected_2016_2018'].count().reset_index()
    protected_area = protected_area.rename(columns={'TerraMarineProtected_2016_2018': 'count'})
    protected_area = protected_area.sort_values(by='count', ascending=False)    
    fig5 = px.bar(protected_area,x='Country',y='count',color='pollution_status',barmode='group',title='Protected Area Occurrences by Country and Pollution Status',labels={'count': 'Frequency','pollution_status': 'Pollution Status (0 = Unsafe, 1 = Safe, 2 = Unsure)','Country': 'Country'})   
    st.plotly_chart(fig5)

# Page 3: Custom Plot Builder
elif page == "Custom Plot":
    st.title("Create Your Own Plot")

    st.write("Select columns and plot type to generate a custom visualization.")
    x_col = st.selectbox("Select X-axis column:", df2.columns)
    y_col = st.selectbox("Select Y-axis column:", df2.columns)
    plot_type = st.selectbox("Select Plot Type:", ["Scatter", "Line", "Bar", "Box", "Violin"])

    if plot_type == "Scatter":
        fig = px.scatter(df2, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
    elif plot_type == "Line":
        fig = px.line(df2, x=x_col, y=y_col, title=f"Line Plot: {x_col} vs {y_col}")
    elif plot_type == "Bar":
        fig = px.bar(df2, x=x_col, y=y_col, title=f"Bar Plot: {x_col} vs {y_col}")
    elif plot_type == "Box":
        fig = px.box(df2, x=x_col, y=y_col, title=f"Box Plot: {x_col} vs {y_col}")
    elif plot_type == "Violin":
        fig = px.violin(df2, x=x_col, y=y_col, box=True, title=f"Violin Plot: {x_col} vs {y_col}")

    st.plotly_chart(fig)
