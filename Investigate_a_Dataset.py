#!/usr/bin/env python
# coding: utf-8

# 
# # Project: Investigate a TMDb Movies Database
# ## Table of Contents
# <ul>
# <li><a href="#intro">Introduction</a></li>
# <li><a href="#wrangling">Data Wrangling</a></li>
# <li><a href="#eda">Exploratory Data Analysis</a></li>
# <li><a href="#conclusions">Conclusions</a></li>
# </ul>

# <a id='intro'></a>
# ## Introduction
# 
# In this project, I will focus on investigating the TMDb Movies Database from Kaggle which contains important details of over 10,000 movies such as their genres, runtime, budget, revenue, realease date, etc. 
# There are some questions that will be investigated as follows:
# 1. Which year has the highest release of movies? How much has the movies industry grown over the years?
# 2. What is average runtime of movies from year to year?
# 3. Which movie had the highest and lowest profit?
# 4. Which movie had the highest and lowest budget? Is there a relationship between profit and budget?
# 5. How many movies of a particular genre have been released? And how do those release compared over the time?
# 6. Which genres have the largest revenue and largest budgets? Which genres are most profitable after working out Return on Investment?

# To get started, I will import the neccessary libraries to complete the project which are Numpy, Pandas, Matplotlib, Seaborn and then import the csv file named 'tmdb-movies.csv'.

# In[1]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')

df=pd.read_csv('tmdb-movies.csv')


# <a id='wrangling'></a>
# ## Data Wrangling
# 
# The csv has already been imported, we can now explore the dataset for our futher analysis practice.
# 
# ### General Properties

# In[2]:


# print the first five rows of the entire dataset
df.head(5)


# In[3]:


# print the last two rows of the entire dataset
df.tail(2)


# In[4]:


# print the concise sumary of the dataset to examine the datasettypes associated with each column
# and the total number of non-null values per column
df.info()


# In[5]:


# As we can see above the dataset contain the null values
# let's count the total rows in each columns which contain null values
df.isnull().sum()


# In[6]:


# examine the basic statistics of the dataset such as min, max, mean,etc..
df.describe()


# **Observation:**  It was noticed from the above result that some of the values under study were showing odd values. For example, the budget, revenue and runtime columns had a min value of 0 which is an unusual occurence.

# In[7]:


# total of duplicate rows in the dataset
df.duplicated().sum()


# In[8]:


# number of non-null unique values for features in the dataset
df.nunique()


# ## Data Cleaning
# In this part, we need to remove or modify some features in the dataset in the following ways:
# 1. Drop the unused colums that are not necessary in the analysis process
# 2. Fill rows with missing values 
# 3. Drop any duplicated rows
# 4. Replace zero value in budget, revenue, runtime

# ### Drop Extraneous Columns

# In[9]:


# drop columns from 2018 dataset
df.drop(['imdb_id','cast','homepage','tagline','overview','budget_adj','revenue_adj'], axis=1, inplace=True)
# confirm change
df.head(1)


# ### Fill Rows with Missing Values 

# In[10]:


# view missing value count for each feature 
df.isnull().sum()


# In[11]:


# fill the null value with zero using 'fillna' function
df=df.fillna(0)


# In[12]:


# checks if any of columns in the dataset have null values - should print False
df.isnull().sum().any()


# ### Drop Duplicate Rows

# In[13]:


# print number of duplicates in the datasets
print(df.duplicated().sum())


# In[14]:


# drop duplicates 
df.drop_duplicates(inplace=True)


# In[15]:


# print number of duplicates again to confirm dedupe - should both be 0
print(df.duplicated().sum())


# ### Replace Zero Values

# During the wrangling process, it was noticed that some of the values under study were showing odd values. For example, the budget, revenue and runtime columns had a min value of 0 which is an unusual occurence. Therefore, I will convert them to null values.

# In[16]:


# check zero values in budget
df_budget=df.loc[(df[['budget']] == 0).all(axis=1)]
df_budget.head(1)


# As we can see, the movie **Mr.Holmes** has the budget of 0; however, it does not make sense since it has an estimated budget of $10,000,000.00 based on IMDB. Thus, this value is unreliable

# In[17]:


# check zero values in revenue
df_revenue=df.loc[(df[['revenue']] == 0).all(axis=1)]
df_revenue.sample(1)


# In[18]:


# check zero values in runtime
df_runtime=df.loc[(df[['runtime']]==0).all(axis=1)]
df_runtime.tail(1)


# We noticed that the values displayed under these columns are incorrect. In order to maintain record of the remaining columns which may need to use for analysis in other questions, it's better to replace those zero values with null values.

# In[19]:


# replace zero values with null values
cols=['budget','revenue','runtime']
df[cols]=df[cols].replace(0,np.nan)
# check result
df.describe()


# In[20]:


# confirm changes again
df.info()


# <a id='eda'></a>
# ## Exploratory Data Analysis
# ### Research Question 1: Which year has the highest release of movies? How much has the movies industry grown over the years?

# Let's look at number of the movies for each year

# In[21]:


# make group for each year and count the number of movies in each year
year=df.groupby('release_year').count()['id']
year.tail(5)


# In[22]:


# plot
plt.subplots(figsize=(10,5))
plt.bar(year.index, year)
plt.title('Year Vs Number Of Movies',fontsize = 14)
plt.xlabel('Release year',fontsize = 13)
plt.ylabel('Number Of Movies',fontsize = 13);


# **According to the above result,** we can see that year 2014 has the highest release of movies (700) followed by year 2013 (659) and year 2015 (629). The movie industry has been growing exponentially over the past half a century with an immense growth starting from the 1990s.

# ### Research Question 2 : What is average runtime of movies from year to year?

# In[23]:


# # make group for each year and find the mean of runtime
avr_runtime=df.groupby('release_year').mean()['runtime']
avr_runtime.head(5)


# In[24]:


# plot
avr_runtime.plot(xticks = np.arange(1960,2016,5))
#setup the figure size.
sns.set(rc={'figure.figsize':(10,5)})
plt.title("Runtime Vs Year")
plt.xlabel('Year')
plt.ylabel('Runtime')
sns.set_style("whitegrid")


# **According to the plot,** the average runtime of movies has been dcreasing from year to year. After the year 1985, the average runtime duraion of the movies are around 100 minutes and tend to be lower. This is true fact since nobody wants to watch the long duration movies 

# ### Research Question 3 : Which movie had the highest and lowest profit?

# We first need to calculate profit and add to a new column

# In[25]:


# To calculate profit, we substract the budget from the revenue.
df['profit'] = df['revenue'] - df['budget']
# Lets look at the new dataset
df.head(1)


# In[26]:


# Movie with highest profit
df.loc[df['profit'].idxmax()]


# In[27]:


# Movie with lowest profit
df.loc[df['profit'].idxmin()]


# **Based on the above result, we can conclude that:**
# - Movie has the highest profits is Avatar with profit of 2.5445 billion dollars
# - Movie has the lowest profits is The Warrior's Way with profit of - 413 million dollars

# ### Research Question 4 : Which movie had the highest and lowest budget? Is there a relationship between profit and budget?

# In[28]:


# Movie with highest budget
df.loc[df['budget'].idxmax()]


# In[29]:


# Movie with highest budget
df.loc[df['budget'].idxmin()]


# **As we can from the result:**
# - Movie has the highest budget is The Warrior's Way
# - Movie has the lowest budget is Fear Clinic

# *Now let's check if there is a relationship between budget and profit*

# In[30]:


plt.xlabel('Budget in Dollars')
plt.ylabel('Profit in Dollars')
plt.title('Relationship between budget and profit')
plt.scatter(df['budget'], df['profit'], alpha=0.5)
plt.show()


# In[31]:


#find the correlation using 'corr()' function.
#it returns a dataframe which contain the correlation between all the numeric columns.
data_corr=df.corr()
data_corr.loc['profit','budget']


# Profit And Budget both have positive correlation (0.53) between them. It means that there is a good possibility that movies with higher investments result in better profit.

# ### Research Question 5 : How many movies of a particular genre have been released? And how do those release compared over the time?

# In[32]:


# First of all, let's take a look at the unique genres column
df['genres'].unique()


# In[33]:


# count the number of unique genres
df['genres'].nunique()


# Due to genres column containing multiple values separated by pipe (|), there are way too many unique points. To resolve this, we will need to segregate the values under genre by splitting them from the pipes and creating a new unique row for each genre.

# In[34]:


genres_split = df['genres'].str.split('|').apply(pd.Series, 1).stack()
genres_split.index = genres_split.index.droplevel(-1)
genres_split.name = 'genres'

del df['genres']

df_genres = df.join(genres_split)

df_genres.head()


# Now lets count the number of movies aggregated by each genre over the years using the groupby function, assign it to a new dataframe and view the results

# In[35]:


# let's see total movies by each genres
df_genres_count=df_genres.groupby(['genres']).count()['id'].sort_values(ascending=False)
df_genres_count


# Now, let's plot to get better view of the number of release for each genre

# In[36]:


sns.set_style('whitegrid')

# plot data
fig, ax = plt.subplots(figsize=(15,10))

sns.set_palette("Set1", 10, .65)

# use unstack()
df_genres_count.plot(kind="bar",  ax=ax);
ax.set(xlabel='Genre', ylabel='Number of Movies', title = 'Number Movie Releases by Genres');


# **According to the plot Drama genre has the highest release of movies (4760) followed by Comedy (3793) and Thriller(2907).**

# We now have our genre types, we have our total releases - but how do those releases compare over time?
# Lets group by release year and genre, and compare using an area chart

# In[37]:


# let's see number of movies groupby each release year and genres 
df_genres_year=df_genres.groupby(['release_year','genres']).count()['id'].unstack()
# confirm 
df_genres_year.tail(5)


# In[38]:


sns.set_style('darkgrid')

# plot data
fig, ax = plt.subplots(figsize=(15,10))

sns.set_palette("Set1", 20, .65)

# use unstack()
df_genres_year.plot.area(ax=ax);
ax.set(xlabel='Release Year', ylabel='Number of Movies', title = 'Trend of Movie Releases over Time by Genres');


# 
# The popularity of movie released has generally grown over time, from 1960 til around 2015 where the numbers contract slightlty.

# ### Research Question 6: Which genres have the largest revenue and largest budgets? Which genres are most profitable after working out Return on Investment?

# Let's see the mean revenues, budgets for each genre, then plot them in a bar chart to make them easier to analyse

# In[39]:


df_new=df_genres[['genres','revenue','budget']].groupby(['genres']).mean()


# In[40]:


# plot data
f,ax=plt.subplots(figsize=(20, 10))

df_genres[['genres','revenue','budget']].groupby(['genres']).mean().sort_values(["revenue","budget"], ascending=False).plot(kind="bar",  ax=ax);
plt.xticks(rotation=75,fontsize=20)

ax.set(ylabel = 'Monetary Amount', title = 'Average Budget verses Average Revenue for Genres')

plt.show()


# Looks like we have a better graph sorted list of genres by their average budget and revenue! Animation is a huge earner, and then there is Adventure - but their budget are also higher definitely. That means that in Return on Investment terms, it's less successful? Look at the bottom of the list, Horror, TV Movie, Documentary have less budget compare to their revenue. Are they successfull as well? Let's check it out.

# In[41]:


# Create our new dataframe to work on ROI
df_new.head()

# Add a new attribute with the calculated ROI
df_new['ROI'] = df_new['revenue']/df_new['budget']

# confirm
df_new.head(2)


# In[42]:


# plot data
# ROI of each genres' movies
f,ax=plt.subplots(figsize=(20, 10))
df_new['ROI'].sort_values(ascending=False).plot(kind="bar",  ax=ax);
plt.xticks(rotation=75,fontsize=20)

ax.set(ylabel = 'ROI', title = 'Return on Investment for Genres')

plt.show()


# As we can see, TV Movie has less budget compare to the other geners in previous graph. However, its ROI is highest in all genres followed by Horror. They both ar on top of the high ROI genres. It means that they invested less but their revenue is great higher. 

# ## Limitation
# 1. Units of revenue and budget column: I am not sure that the budgets and revenues all in US dollars? It might be possible different movies have budget in different currency according to the country they were produced. Therefore, a possible inconsistency arises here which can state the incorrect analysis.
# 2. Data quality: althought I assume the zero values in revenue and budget column are missing, there are still a lot of unreasonable small/big value in the both of the columns. 
# 3. Although the dataset provide the adjusted data for revenue and budget, I only used the revenue and budget data to explore. It might have the inflation effect
# 

# <a id='conclusions'></a>
# ## Conclusions

# In conclusion, the main purpose of investigating The Movie Database (TMDB) is to explore the relationship between certain parameters and the evolution of the movie industry over the years. 
# Using the neccessary functions and visualization tools, we can see that the movie industry is growing at an exponential rate where the number of movies per year has increased from about 30 per year to about 700 per year which was more than 20 fold. Also the average movie runtime has considerably decreased from year to year by 20% from around 120 minutes to 95 minutes today and tend to be lower.
# 
# It as also noticed that'Avatar' movie released in 2010 is still the movie receiving the highest profit until now. 
# But, the movie with highest budget is The Warrior's Way released in 2014. 
# 
# We found that Drama, comedy and thriller were the 3 top most frequent type of movies. The popularity of movie releases has generally grown over time, from 1960 til 2015 where the numbers contract slightlty. 
# 
# When looking at the success of genres, we analysed a list of genres by their average budget and revenue. It looked like animation is a huge earner, followed by Adventure while foreign movies, documentaries and TV Movies are at the bottom in terms of revenue. If we calculated a return on investment by dividing revenue by budget, TV Movies moved to the top of the RoI analysis results, meaning it earned the most per the amount of budget spent.
# 

# In[1]:


from subprocess import call
call(['python', '-m', 'nbconvert', 'Investigate_a_Dataset.ipynb'])


# In[ ]:




