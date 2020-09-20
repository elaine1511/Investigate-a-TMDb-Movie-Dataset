# Udacity - DAND - Investigate-a-TMDb-Movie-Dataset
## Project 2
## Overview
In this project, I will focus on investigating the TMDb Movies Database from Kaggle which contains important details of over 10,000 movies such as their genres, runtime, budget, revenue, realease date, etc
To complete this project, I will be using Python plus the following libraries:
- Pandas and NumPy 
- Matplotlib 
- Seaborn

The project primary goal is to go through the general data analysis process, so the project report is including four parts:
- Asking questions
- Data wrangling 
- Exploratory data analysis
- Limitations and conclusion

## Asking questions
There are some questions that will be investigated as follows:
1. Which year has the highest release of movies? How much has the movies industry grown over the years?
2. What is average runtime of movies from year to year?
3. Which movie had the highest and lowest profit?
4. Which movie had the highest and lowest budget? Is there a relationship between profit and budget?
5. How many movies of a particular genre have been released? And how do those release compared over the time?
6. Which genres have the largest revenue and largest budgets? Which genres are most profitable after working out Return on Investment?

## Data Wrangling
### Acess and gather data
### Cleaning data
In this part, we need to remove or modify some features in the dataset in the following ways:
- Drop the unused colums that are not necessary in the analysis process
- Fill rows with missing values
- Drop any duplicated rows
- Replace zero value in budget, revenue, runtime

## Exploratory data analysis

## Limitations and conclusion
### Limitations
1. Units of revenue and budget column: I am not sure that the budgets and revenues all in US dollars? It might be possible different movies have budget in different currency according to the country they were produced. Therefore, a possible inconsistency arises here which can state the incorrect analysis.
2. Data quality: althought I assume the zero values in revenue and budget column are missing, there are still a lot of unreasonable small/big value in the both of the columns.
3. Although the dataset provide the adjusted data for revenue and budget, I only used the revenue and budget data to explore. It might have the inflation effect

### My findings
- The movie industry is growing at an exponential rate where the number of movies per year has increased from about 30 per year to about 700 per year which was more than 20 fold. Also the average movie runtime has considerably decreased from year to year by 20% from around 120 minutes to 95 minutes today and tend to be lower.
- It as also noticed that'Avatar' movie released in 2010 is still the movie receiving the highest profit until now. But, the movie with highest budget is The Warrior's Way released in 2014.
- Drama, comedy and thriller were the 3 top most frequent type of movies. The popularity of movie releases has generally grown over time, from 1960 til 2015 where the numbers contract slightlty.
- Animation is a huge earner, followed by Adventure while foreign movies, documentaries and TV Movies are at the bottom in terms of revenue. If we calculated a return on investment by dividing revenue by budget, TV Movies moved to the top of the RoI analysis results, meaning it earned the most per the amount of budget spent.

