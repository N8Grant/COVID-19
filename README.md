# COVID-19 Simulation Model
## Overview
This project uses a spatial SIR model to predict the number of cases in the United States at a county level. At the time of inception of this project, no county numbers were available to the public so I was forced to use some web scraping to complete the task. Below I will outline the method I use in order to collect, clean , and use the data. The next part involved prediction of parameters and adding proper random conditions so that the model performed optimally. Finally, plotly was used in order to visualize the virus dynamics through time. The model ended up overestimating the number of cases when it was first used, however it stood as a great example in visualizing the dynamics of the spread.

## Data Collection
### Web Scraping
Since popular databases like John Hopkins were not tracking cases at a county level, web scraping had to be used in order to collect the data. Using a simple google search like "Number of COVID-19 cases in _ county" I took the top 4 news links and got the raw text data from each website. Next I would parse the raw text to find the paragraphs containing information about the number of cases. 

### BERT QA
Using a distilled version of a BERT QA model from huggingface, I fed the paragraphs containing relevent information into the model along with the question, "how many cases are in _ county". Some websites would have multiple locations with relevent information, so for each website, the result with the highest confidence from the model was taken. In the end, each website would yield a set of locations where the answer was determined to lie.

### Cleaning the Answer
Even though the answers were readable to humans, it still wasnt in a useable number format, and still had much more cleaning to be done. First, I had to discriminate between the news links for their relavance. For, for this I chose to just take the newest information in order for the models numbers to be as up to date as possible. In hindsight, a combinaton of date and also model score would have been the better option as there was a lot of variance in results from smaller counties with less news coverage. In some situations the cases were just stated as a number, which just required a regular expression in order to parse out the answer. In other cases the number was stated in words, which required me to use a package that converted the word to an integer. If the package threw and error then I just set the number of cases to 0 in the county.

## Modeling
### Spatial SIR
The spatial SIR model is an extention of the well known SIR model that takes into account an areas surroundings. Its as if each county has its own SIR model and other surrounding areas also contribute to the caseload. The reason why I chose this model is because one of the biggest fears I was hearing from people was the uncertanty of when it would hit an area near them. When it was first happening the virus seemed very distant to many not in cities, so it begged the question of how long it would take. The initial SIR models that I had seen didnt take this into account and instead just modeled the spread as a whole, not really showing the local impact. Of course there were other models out there that were more sophisticated in terms of taking into account more variables, but none that I had seen pertaining to spatial data. I also added air travel transmission between major cities because the spatial model only takes into account neighboring counties which doesnt capture the whole picture.

### Initial Parameterization
After colelcting data for about a week from the web scraping process, the numbers were used to perform logistic regression to find unique beta values (rate of spread) for each county. The other paramters were determined by using popular parameters form other covid models. Unfortunatley there was no way to determine the other parameters for each county even though in reality they are county specific. In later iterations, the beta values were just set to the conventional values form other models as there was a large variance in the emerging data causing some counties to have exorbinantly high rates of transmission.

## Visualization
## Plotly
Plotly was the perfect library for this use case. They already had maps available with county level seperation and overlays that could display the virus dynamics. Numbers were normalized based on county population. Below is a video displaying virus dynamics.



https://user-images.githubusercontent.com/18035858/136096914-43fb5d06-3f86-47ff-9326-d332cfecad42.mp4


## Other Ambitions
I had planned on using this in accordance with hospital bed data in orer to take the risk of covid for each county to a new level. Unfortunatley the results which the model yielded were too innacurate to give respectable risk assessment. The best part of the model was how it captured the inital boom of cases in the cities, and lack of cases in less densely populated areas. It was very interesting to see the political narratives that were shaped based off of the relative lack of cases, however the model above shows how the virus catches up and then gets very serious in the rural areas.
