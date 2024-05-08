import streamlit as st
import pandas as pd
import plotly.express as px
import os
import warnings
import plotly.figure_factory as ff
import plotly.graph_objects as go
import matplotlib.pyplot as plt


warnings.filterwarnings('ignore')

# Setting the Streamlit page configuration
st.set_page_config(page_title="Superstoredata!!!", page_icon=":bar_chart:", layout="wide")

# Main heading
st.title("Global Superstore Lite")
df = pd.read_csv("Global_Superstore_Lite.csv", encoding="ISO-8859-1")

# Getting the min and max date
startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()

df["Order Date"] = pd.to_datetime(df["Order Date"])


# Streamlit dashboard layout and configuration
st.markdown('<style>div.block-container{padding-top:1rem;}</style>', unsafe_allow_html=True)


# association rule results
association_results = {
'Phones': [('Machines', 3), ('Appliances', 3), ('Phones', 3), ('Bookcases', 2), ('Copiers', 1), ('Machines', 1), ('Appliances', 1), ('Bookcases', 2), ('Copiers', 1)],
    'Chairs': [('Tables', 3), ('Accessories', 2), ('Copiers', 1), ('Machines', 1), ('Tables', 1), ('Bookcases', 1), ('Chairs', 2), ('Copiers', 1), ('Machines', 1), ('Chairs', 1), ('Phones', 1)],
    'Accessories': [('Tables', 1), ('Machines', 1), ('Chairs', 2), ('Tables', 1), ('Chairs', 1), ('Machines', 1), ('Appliances', 1), ('Copiers', 1)],
    'Tables': [('Chairs', 3), ('Bookcases', 1), ('Phones', 1), ('Tables', 1), ('Chairs', 1), ('Bookcases', 1), ('Phones', 1)],
    'Storage': [('Chairs', 1), ('Copiers', 2), ('Chairs', 1), ('Copiers', 2)],
    'Machines': [('Accessories', 1), ('Phones', 3), ('Copiers', 1), ('Machines', 1), ('Phones', 3), ('Appliances', 1), ('Bookcases', 1), ('Copiers', 1), ('Machines', 1), ('Machines', 1)],
    'Appliances': [('Accessories', 1), ('Copiers', 2), ('Phones', 1), ('Bookcases', 1), ('Accessories', 1), ('Copiers', 2), ('Phones', 1), ('Bookcases', 1)],
    'Bookcases': [('Supplies', 1), ('Tables', 1), ('Chairs', 1), ('Bookcases', 2), ('Supplies', 1), ('Tables', 1), ('Chairs', 1), ('Bookcases', 2)],
    'Copiers': [('Phones', 1), ('Bookcases', 3), ('Appliances', 2), ('Copiers', 1), ('Storage', 2), ('Machines', 1), ('Chairs', 1), ('Phones', 1), ('Bookcases', 3), ('Appliances', 2), ('Copiers', 1), ('Storage', 2), ('Machines', 1), ('Chairs', 1)],
    'Supplies': [('Bookcases', 1), ('Bookcases', 1)],
}
# impact on sales
data = {
    'antecedents': [
        ('item_1_Accessories'), ('item_2_Tables'), ('item_1_Appliances'), ('item_2_Accessories'),
        ('item_2_Accessories'), ('item_2_Supplies'), ('item_1_Bookcases'), ('item_2_Phones'),
        ('item_1_Chairs'), ('item_1_Machines'), ('item_1_Phones'), ('item_2_Appliances'),
        ('item_1_Storage'), ('item_2_Copiers')
    ],
    'consequents': [
        ('item_2_Tables'), ('item_1_Accessories'), ('item_2_Accessories'), ('item_1_Appliances'),
        ('item_1_Machines'), ('item_1_Bookcases'), ('item_2_Supplies'), ('item_1_Chairs'),
        ('item_2_Phones'), ('item_2_Accessories'), ('item_2_Appliances'), ('item_1_Phones'),
        ('item_2_Copiers'), ('item_1_Storage')
    ],
    'impact_on_sales': [
        9623.541667, 15455.812500, 21563.212500, 12052.125000, 26860.275000, 17706.000000,
        17891.718750, 5694.000000, 16390.125000, 31774.750000, 17350.208333, 19275.625000,
        8723.200000, 7406.000000
    ]
}

# Creating the  DataFrame
association_sales_summary = pd.DataFrame(data)

# Display DataFrame
print(association_sales_summary)

# bar graph
import plotly.express as px

# Bar graph on impact on sales
fig = px.bar(association_sales_summary, 
             x=association_sales_summary.index, 
             y='impact_on_sales', 
             color='impact_on_sales', 
             color_continuous_scale='reds',
             labels={'impact_on_sales': 'Impact on Sales', 'index': 'Association Rule'},
             title='Impact on Sales for Each Association Rule')

fig.update_layout(xaxis={'tickvals': list(range(len(association_sales_summary))),
                          'ticktext': [f"{ant} -> {cons}" for ant, cons in zip(association_sales_summary['antecedents'], association_sales_summary['consequents'])],
                          'tickangle': 90})
st.plotly_chart(fig, use_container_width=True)


# Creating a DataFrame for association results
association_df = pd.DataFrame([(item, assoc_item, freq) for item, assoc_items in association_results.items() for assoc_item, freq in assoc_items], columns=['Item', 'Associated Item', 'Frequency'])

#side bar title
st.sidebar.markdown("<h1 style='text-align: center; font-size: 35px;'>Your Choice</h1>", unsafe_allow_html=True)

# Sidebar filter for selecting an item
selected_item = st.sidebar.selectbox("Select an item:", list(association_results.keys()))

# Displaying the selected item and its associated items
st.sidebar.subheader(f"Associated Items with {selected_item}:")
selected_associations = association_results.get(selected_item, [])
if selected_associations:
    associated_items = [assoc_item for assoc_item, _ in selected_associations]
    st.sidebar.write(pd.DataFrame(selected_associations, columns=['Associated Item', 'Frequency']))
    st.sidebar.write(f"You may also like: {', '.join(associated_items)}")
else:
    st.sidebar.write("No associations found for the selected item.")



#Defining col1 and col2 together in a single block
col1, col2 = st.columns((2))

with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))

df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()

st.sidebar.header("Choose your filter: ")

# Creating a side bar for Region
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]

# Creating a side bar for State
state = st.sidebar.multiselect("Pick the State", df2["State"].unique())
if not state:
    df3 = df2.copy()
else:
    df3 = df2[df2["State"].isin(state)]

# Creating a side bar for City
city = st.sidebar.multiselect("Pick the City",df3["City"].unique())

# Filter the data based on Region, State, and City
if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df["Region"].isin(region)]
elif not region and not city:
    filtered_df = df[df["State"].isin(state)]
elif state and city:
    filtered_df = df3[df["State"].isin(state) & df3["City"].isin(city)]
elif region and city:
    filtered_df = df3[df["Region"].isin(region) & df3["City"].isin(city)]
elif region and state:
    filtered_df = df3[df["Region"].isin(region) & df3["State"].isin(state)]
elif city:
    filtered_df = df3[df3["City"].isin(city)]
else:
    filtered_df = df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

category_df = filtered_df.groupby(by=["Category"], as_index=False)["Sales"].sum()

#creating charts for category wise sales and region wise sales
with col1:
    st.subheader("Category wise Sales")
    fig = px.bar(category_df, x="Category", y="Sales", text=['${:,.2f}'.format(x) for x in category_df["Sales"]],
                 template="seaborn")
    st.plotly_chart(fig, use_container_width=True, height=200)

with col2:
    st.subheader("Region wise Sales")
    fig = px.pie(filtered_df, values="Sales", names="Region", hole=0.5)
    fig.update_traces(text=filtered_df["Region"], textposition="outside")
    st.plotly_chart(fig, use_container_width=True)

#adding the exanders for category wise sales and region wise sales
cl1, cl2 = st.columns((2))
with cl1:
    with st.expander("Category_ViewData"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv = category_df.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Category.csv", mime="text/csv",
                           help='Click here to download the data as a CSV file')

with cl2:
    with st.expander("Region_ViewData"):
        region = filtered_df.groupby(by="Region", as_index=False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv = region.to_csv(index=False).encode('utf-8')
        st.download_button("Download Data", data=csv, file_name="Region.csv", mime="text/csv",
                          help='Click here to download the data as a CSV file')

filtered_df["month_year"] = filtered_df["Order Date"].dt.to_period("M")
st.subheader('Time Series Analysis')

# Group by month and year and calculate sum of Sales and Profit
linechart = pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b")).agg({"Sales": "sum", "Profit": "sum"})).reset_index()

# line chart for Sales and Profit over time
fig2 = px.line(linechart, x="month_year", y=["Sales", "Profit"], 
               labels={"value": "Amount"}, height=500, width=1000, 
               template="gridon", color_discrete_sequence=['red', 'green'])

# Update layout
fig2.update_layout(title="Sales and Profit Over Time",
                   xaxis_title="Month-Year",
                   yaxis_title="Amount")
# Ploting the graph 
st.plotly_chart(fig2, use_container_width=True)

with st.expander("View Data of TimeSeries:"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv = linechart.to_csv(index=False).encode("utf-8")
    st.download_button('Download Data', data=csv, file_name="TimeSeries.csv", mime='text/csv')


import plotly.express as px
import numpy as np

# Creating scatter plot for Sales and Profit
# Creating a scatter plot for sales and discount
data1 = px.scatter(filtered_df, x="Sales", y="Profit",color_discrete_sequence=['orange'])
data1['layout'].update(title="Relationship between Sales and Profit using Scatter Plot.",
                       titlefont=dict(size=20), xaxis=dict(title="Sales", titlefont=dict(size=19)),
                       yaxis=dict(title="Profit", titlefont=dict(size=19)))
st.plotly_chart(data1, use_container_width=True)


# Creating a scatter plot for sales and discount
data1 = px.scatter(filtered_df, x="Sales", y="Discount")
data1['layout'].update(title="Relationship between Sales and Discount using Scatter Plot.",
                       titlefont=dict(size=20), xaxis=dict(title="Sales", titlefont=dict(size=19)),
                       yaxis=dict(title="Discount", titlefont=dict(size=19)))
st.plotly_chart(data1, use_container_width=True)


# Create a DataFrame from association rules data
data = {
    "Antecedents": ['Accessories', 'Tables', 'Appliances', 'Accessories', 'Supplies', 'Bookcases', 'Phones', 'Chairs', 'Machines', 'Accessories', 'Appliances', 'Storage', 'Copiers'],
    "Consequents": ['Tables', 'Accessories', 'Accessories', 'Appliances', 'Bookcases', 'Supplies', 'Chairs', 'Phones', 'Accessories', 'Machines', 'Phones', 'Copiers', 'Storage'],
    "Support": [0.08, 0.06, 0.12, 0.04, 0.02, 0.16, 0.16, 0.04, 0.08, 0.04, 0.24, 0.06, 0.20],
    "Confidence": [0.25, 0.33, 0.17, 0.50, 1.0, 0.12, 0.12, 0.50, 0.25, 0.50, 0.25, 0.67, 0.20],
    "Lift": [4.17, 4.17, 4.17, 4.17, 6.25, 6.25, 3.13, 3.13, 6.25, 6.25, 4.17, 3.33, 3.33],
    "Zhangs_metric": [0.826087, 0.808511, 0.863636, 0.791667, 0.857143, 1.0, 0.809524, 0.708333, 0.913043, 0.875, 1.0, 0.744681, 0.875]
}

# Creating the DataFrame from the association rules data
df_assoc_rules = pd.DataFrame(data)

#Reorganizing the DataFrame to form a matrix structure
heatmap_data = df_assoc_rules.pivot(index='Antecedents', columns='Consequents', values='Zhangs_metric')

# Creating the heatmap using Plotly
fig_heatmap = go.Figure(data=go.Heatmap(
    z=heatmap_data.values,
    x=heatmap_data.columns,
    y=heatmap_data.index,
    colorscale='YlOrRd',
    colorbar=dict(title='Zhangs_metric')
))

fig_heatmap.update_layout(
    title="Association Rules Heatmap",
    xaxis_title="Consequents",
    yaxis_title="Antecedents"
)

st.subheader("Association Rules Heatmap")
st.plotly_chart(fig_heatmap, use_container_width=True)

with st.expander("View Association Rules Data"):
    st.write(df_assoc_rules)

