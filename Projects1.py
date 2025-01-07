# OBJECTIVE 
    # import the survey file and schema file
    # get the county and python developers in a list 
    # clean the data 
    # Prepare the data 
    # Plot the data 

import pandas as pd 
import matplotlib.pyplot as pt 
import numpy as np
import scipy.stats as st

# import the survey file and schema file
schema_df = pd.read_csv("Projects/RequiredData/Project1/survey_results_schema.csv")
survey_df = pd.read_csv("Projects/RequiredData/Project1/survey_results_public.csv", na_values="NA, NAN, Na, NaN", index_col="ResponseId")

# get the county and python developers in a list 
filter_df = survey_df[["Country", "LanguageHaveWorkedWith"]]

# clean the data
filter_df.dropna(how="any", inplace=True)
filter_df.drop_duplicates(inplace=True)

# Prepare the data
# To perpare a df with unique python dev
    # Group the data by the country.
    # Calculate the percentage of Python developers in each country.
    # Create a new DataFrame with the unique countries and their respective percentages.
prepared_df = filter_df.groupby("Country", group_keys=False).apply(
    lambda x: (x.loc[:, "LanguageHaveWorkedWith"] == "Python").mean() * 100
).reset_index(name="PythonPercentage")

# Shorten the country name 
prepared_df.loc[:, "Country"] = prepared_df["Country"].apply(lambda x : x[:3])

# change the PythonPercentage from string to float 
prepared_df.loc[:, "PythonPercentage"] = pd.to_numeric(prepared_df["PythonPercentage"], errors="coerce").fillna(0.0).astype("float16")

# sort the data frame based PythonPercentage
prepared_df.sort_values(by="PythonPercentage", inplace=True, ascending=False)

# outlier detection using zscore method 
# get the zscore of the data
z_score = st.zscore(prepared_df["PythonPercentage"])

# filter the data with zscore > 3 or zscore < -3
prepared_df = prepared_df[(z_score < 3) & (z_score > -3)]

# drop the values with 0.0
prepared_df = prepared_df.replace(0.0, pd.NA).dropna()

# Plot the data 
country_data = prepared_df["Country"].to_list()
pythonPercentage_data = prepared_df["PythonPercentage"].to_list()

# split the list into 4 parts 
country_data_splited = np.array_split(country_data, 4)
pythonPercentage_data_splited = np.array_split(pythonPercentage_data, 4)

# style
pt.style.use("dark_background")

# create a subplot to have more clarity 
figure, axes = pt.subplots(nrows=2, ncols=2)


# separate the axes
axis11 = axes[0][0]
axis12 = axes[0][1]
axis21 = axes[1][0]
axis22 = axes[1][1]

# plot the data as horizontal bar graphs
bars = axis11.bar(country_data_splited[0], pythonPercentage_data_splited[0], label="Python Dev percentage \nin each country")

# Set x-tick labels with specified font size
axis11.tick_params(axis='x', labelsize=8) 
axis11.tick_params(axis='y', labelsize=8)

# legend 
axis11.legend(loc="lower right")

# x and y values 
axis11.set_ylabel("Countries")
axis11.set_xlabel("Python dev percentage")

# pie chart for the first 6 countries and group the 7th as "Others"
top_7_countries = country_data_splited[0][:7]
top_7_percentages = pythonPercentage_data_splited[0][:7]
wedges, texts, autotexts = axis12.pie(top_7_percentages, labels=top_7_countries, autopct='%1.1f%%', startangle=140, wedgeprops={"edgecolor":"white", "linewidth": 1.5}, colors=["#7FFFAa","#B2DFAF","#40E0A6","#87CEBC","#C7F4C3","#9FE299","#00A878"], pctdistance=0.8)

# Change label color
for text in autotexts:
    text.set_color('black') 
    text.set_fontsize(8)
    text.set_weight('semibold') 

# Equal aspect ratio ensures that pie is drawn as a circle
axis12.set_aspect("equal")

# scatter plot for the data
axis21.scatter(country_data_splited[0], pythonPercentage_data_splited[0], label="Python Dev percentage \nin each country")

# Set x-tick labels with specified font size
axis21.tick_params(axis='x', labelsize=8) 
axis21.tick_params(axis='y', labelsize=8)

# line plot for the data
axis22.plot(country_data_splited[0], pythonPercentage_data_splited[0], label="Python Dev percentage \nin each country")

# Set x-tick labels with specified font size
axis22.tick_params(axis='x', labelsize=8) 
axis22.tick_params(axis='y', labelsize=8)

# rotate y-axis labels by 90 degrees
for ax in [axis11, axis21, axis22]:
    ax.set_yticklabels(ax.get_yticklabels(), rotation=90)

# tight layout
pt.tight_layout()

# legend 
axis11.legend(loc="lower right")

# x and y values 
axis11.set_ylabel("Countries")
axis21.set_xlabel("Python dev percentage")
axis21.set_ylabel("Countries")
axis22.set_xlabel("Python dev percentage")

# rotate y-axis labels by 90 degrees
for ax in [axis11, axis12, axis21, axis22]:
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

# tight layout
pt.tight_layout()

# title
axis11.set_title("Top 7 python dev percentage", 
                 fontsize=12, 
                 loc='right', pad=20, ha='center', fontweight='bold') 


# move the figure down
figure.subplots_adjust(top=0.9) 

# save the figure 
pt.savefig("Project1.png")

# show
pt.show()
