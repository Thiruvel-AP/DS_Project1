# OBJECTIVE 
    # import the survey file and schema file
    # get the county and python developers in a list 
    # clean the data 
    # Prepare the data 
    # Plot the data 

import pandas as pd 
import matplotlib.pyplot as pt 
import numpy as np

# import the survey file and schema file
schema_df = pd.read_csv("RequiredData/Project1/survey_results_schema.csv")
survey_df = pd.read_csv("RequiredData/Project1/survey_results_public.csv", na_values="NA, NAN, Na, NaN", index_col="ResponseId")

# get the county and python developers in a list 
filter_df = survey_df[["Country", "LanguageHaveWorkedWith"]]

# clean the data
filter_df.dropna(how="any", inplace=True)
filter_df.drop_duplicates()

# Prepare the data
# To perpare a df with unique python dev
    # Group the data by the country.
    # Calculate the percentage of Python developers in each country.
    # Create a new DataFrame with the unique countries and their respective percentages.
prepared_df = (
    filter_df.groupby("Country", group_keys=False).apply(lambda x : (x.loc[:,"LanguageHaveWorkedWith"] == "Python").mean() * 100).reset_index(name="PythonPercentage")
)

# Shorten the country name 
prepared_df["Country"] = prepared_df["Country"].apply(lambda x : x[:15])

# change the PythonPercentage from string to float 
prepared_df["PythonPercentage"] = pd.to_numeric(prepared_df["PythonPercentage"],errors="coerce").fillna(0.0).astype("float16")

# sort the data frame based PythonPercentage
prepared_df.sort_values(by="PythonPercentage", inplace=True, ascending=False)

# drop the values with 0.o
prepared_df = prepared_df.replace(0.0, pd.NA).dropna()

# Plot the data 
country_data = prepared_df["Country"].to_list()
pythonPercentage_data = prepared_df["PythonPercentage"].to_list()

# split the list into 4 parts 
country_data_splited = np.array_split(country_data,4)
pythonPercentage_data_splited = np.array_split(pythonPercentage_data,4)

# style
pt.style.use("dark_background")

# create a subplot to have more clarity 
figure,axes = pt.subplots(nrows=2,ncols=2)

# seperate the axes
axis11 = axes[0][0]
axis12 = axes[0][1]
axis21 = axes[1][0]
axis22 = axes[1][1]

# plot the data as horizondal bar grpahs
axis11.barh(country_data_splited[0],pythonPercentage_data_splited[0], label="Python Dev percentage \nin each country")
axis12.barh(country_data_splited[1],pythonPercentage_data_splited[1], label="Python Dev percentage \nin each country")
axis21.barh(country_data_splited[2],pythonPercentage_data_splited[2], label="Python Dev percentage \nin each country")
axis22.barh(country_data_splited[3],pythonPercentage_data_splited[3], label="Python Dev percentage \nin each country")

# legend 
axis11.legend("bottom right")
axis12.legend("bottom right")
axis21.legend("bottom right")
axis22.legend("bottom right")

# x and y values 
axis11.set_ylabel("Countries")
axis21.set_xlabel("Python dev perecentage")
axis21.set_ylabel("Countries")
axis22.set_xlabel("Python dev perecentage")


# tight layout
pt.tight_layout()

# title
axis11.set_title("Perecentage of Python know dev in each country")
axis12.set_title("Perecentage of Python know dev in each country")

# save the figure 
pt.savefig("Project1.png")

# show
pt.show()