## ApplaudMe
ApplaudMe's insights helps writers increase their chances to publish one of the top 20% most applauded articles in Medium. ApplaudMe analyzes features in an article and uses machine learning to predict if this article is likely meet an applause target.   

## How ApplaudMe works?
Medium is a growing online publishing platform, which shares its revenues with contributing writers. Writer's earnings and popularity is proportional to the number of claps their articles receive in Medium.    
ApplaudMe looks at article features-see here for a list-to determine the probability that the article will receive enough number of claps to be in the top 20% rank. If an article is not likely to meet its applause metric, ApplaudMe provides insights about what features most significantly influenced this negative prediction, so writers can focus on improving those features and potentially increase their earnings. 

## Motivation
I built ApplaudMe because I wanted to help writers improve their communications skills. There are several tools that writers use to check spelling and grammar before publishing an article. ApplaudMe incorporate features such as readability and sentiment in the article to contribute to a writer's workflow. 

## Next Steps
In a future release, ApplaudMe would highlight which article sentences are affecting the prediction. ApplaudMe could also use provide suggestions for powerful titles, and subtitles that can increase user engagement. Image quality can also be added to the feature space to provide additional dimensions that writers could realistically focus on to increase their chances of applause. 

## Project codebase and data
ApplaudMe uses data from Medium. A first dataset of over 240,000 article metadata records was created using the collect_article_metadata.py program. This dataset was used to select a sample of articles to include in a classification model.
An exploratory analysis of this dataset is available in a [Jupyter notebook](Notebooks/ApplaudMe - Exploratory Data Analysis.ipynb)
A second dataset is then created by extracting article text from the selected articles. The article text is used to create features that will be used to classify popular and not popular articles.
A second [Jupyter notebook](Notebooks/ApplaudMe -  Classifier Modeling.ipynb) includes a description of feature engineering and classifier training. 








