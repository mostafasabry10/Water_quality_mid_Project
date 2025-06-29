

import streamlit as st
import pandas as pd
import plotly.express as px

# Load data
df = pd.read_csv("cleaned_data.csv",index_col = 0)  

# Sidebar for navigation
page = st.sidebar.selectbox("Choose a page:", ["Data", "Plots", "Custom Plot"])

# Page 1: Display Data
if page == "Data":
    st.title("Water Pollution Dataset")
    st.write("### Cleaned Data")
    st.dataframe(df)

# Page 2: Plots
elif page == "Plots":
    st.title("Pollution Analysis Plots")

    st.subheader("1. Purest Countries by Safe Samples")
    puriest_country = df[df['pollution_status'] == 1].groupby('Country')['pollution_status'].count().sort_values(ascending=False).reset_index()
    fig1 = px.bar(puriest_country, x='Country', y='pollution_status', title='The Purest Countries by Count of Safe Samples', labels={'pollution_status': 'Safe Sample Count'})
    st.plotly_chart(fig1)

    st.subheader("2. Safe Water Samples vs Population Density")
    pop_poll = df.groupby('Country')['PopulationDensity'].value_counts().sort_values(ascending=False).reset_index()
    pop_poll = pop_poll.sort_values(by='PopulationDensity', ascending=False).reset_index(drop=True)
    population_polluation = pd.merge(puriest_country, pop_poll, on='Country').drop('count', axis=1)
    fig2 = px.bar(population_polluation, x='Country', y='pollution_status', color='PopulationDensity', title='Safe Water Samples per Country (Sorted by Population Density)', labels={'pollution_status': 'Safe Sample Count','PopulationDensity': 'Population Density'}, color_continuous_scale='Viridis')
    st.plotly_chart(fig2)

    st.subheader("3. Safe Water Samples by Tourism Level")
    tour_pollution = df.groupby('Country')['TouristMean_1990_2020'].value_counts().reset_index().sort_values(by='TouristMean_1990_2020',ascending = False)
    merged_df = pd.merge(puriest_country,tour_pollution, on = 'Country').drop('count',axis= 1)
    fig3 = px.bar(merged_df, x='Country', y='pollution_status', color='TouristMean_1990_2020', title='Safe Water Samples by Country (Colored by Tourism Level)', labels={'pollution_status': 'Safe Sample Count','TouristMean_1990_2020': 'Avg. Tourists (1990–2020)'}, color_continuous_scale='Blues')
    st.plotly_chart(fig3)

    st.subheader("4. Yearly Water Pollution Rate")
    pollution_rate_yearly = df[df['pollution_status'] == 0].groupby('phenomenonTimeReferenceYear')['pollution_status'].value_counts().reset_index().drop('pollution_status',axis = 1)
    pollution_rate_yearly = pollution_rate_yearly.sort_values(by='count',ascending = False).reset_index(drop=True)
    fig4 = px.line(pollution_rate_yearly, x='phenomenonTimeReferenceYear', y='count', title='Yearly Water Pollution Rate', labels={'phenomenonTimeReferenceYear': 'Year','count': 'Polluted Sample Count'})
    st.plotly_chart(fig4)

    st.subheader("5. Net Migration by Country and Pollution Status")
    migration_polliation_affect = (df.groupby(['Country','pollution_status'])['netMigration_2011_2018'].value_counts().reset_index()).sort_values(by='netMigration_2011_2018',ascending = False)
    fig5 = px.bar(migration_polliation_affect,x='Country',y='netMigration_2011_2018',color='pollution_status',barmode='group',title='Average Net Migration by Country and Pollution Status',labels={'netMigration_2011_2018': 'Avg. Net Migration (2011–2018)','pollution_status': 'Pollution Status (0 = Unsafe, 1 = Safe, 2 = Unsafe)'})
    st.plotly_chart(fig5)

    st.subheader("6. Protected Area vs Pollution Status")
    protected_area = df.groupby(['Country', 'pollution_status'])['TerraMarineProtected_2016_2018'].count().reset_index()
    protected_area = protected_area.rename(columns={'TerraMarineProtected_2016_2018': 'count'})
    protected_area = protected_area.sort_values(by='count', ascending=False)    
    fig6 = px.bar(protected_area,x='Country',y='count',color='pollution_status',barmode='group',title='Protected Area Occurrences by Country and Pollution Status',labels={'count': 'Frequency','pollution_status': 'Pollution Status (0 = Unsafe, 1 = Safe, 2 = Unsafe)','Country': 'Country'})   
    st.plotly_chart(fig6)

# Page 3: Custom Plot Builder
elif page == "Custom Plot":
    st.title("Create Your Own Plot")

    st.write("Select columns and plot type to generate a custom visualization.")
    x_col = st.selectbox("Select X-axis column:", df.columns)
    y_col = st.selectbox("Select Y-axis column:", df.columns)
    plot_type = st.selectbox("Select Plot Type:", ["Scatter", "Line", "Bar", "Box", "Violin"])

    if plot_type == "Scatter":
        fig = px.scatter(df, x=x_col, y=y_col, title=f"Scatter Plot: {x_col} vs {y_col}")
    elif plot_type == "Line":
        fig = px.line(df, x=x_col, y=y_col, title=f"Line Plot: {x_col} vs {y_col}")
    elif plot_type == "Bar":
        fig = px.bar(df, x=x_col, y=y_col, title=f"Bar Plot: {x_col} vs {y_col}")
    elif plot_type == "Box":
        fig = px.box(df, x=x_col, y=y_col, title=f"Box Plot: {x_col} vs {y_col}")
    elif plot_type == "Violin":
        fig = px.violin(df, x=x_col, y=y_col, box=True, title=f"Violin Plot: {x_col} vs {y_col}")

    st.plotly_chart(fig)
