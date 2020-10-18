## Steps to run the project

### Before running the code it is necessary to download these files
- Download google embedding

https://drive.google.com/file/d/0B7XkCwpI5KDYNlNUTTlSS21pQmM/edit

- Dowload validation, test_embeddings, prepared_test, prepared_train, test, train. 

https://drive.google.com/drive/folders/1sRGbLqDEGDoOVlayHdgSqRWhdbjpDMTs?usp=sharing


### Preprocessing is located in the project folder in the NLP_similarity_models.ipynb file.

- Download the repository and save it somewhere on your computer. Then get the location and write it inside the os.chdir and os.environ.

The first step in preprocessing was to remove URLs, mentions and hashtags. The second step was to convert the letters of all the tweets to lowercase. Then, emoticons were replaced by its meaning in words through the use of the Python library emoji. Finally, empty rows were removed from all tweets. Next, the tweets were translated from spanish to english using Google Api Services. The purpose of this translation was to uniform the language to the one used by Google News Embedding, in order to be able to vectorize the Tweets.

Additionally, the following methods are employed to determine the performance of each model: hitsCount and dcgScore. These methods define the percentage of success of being able to rank a question as positive or negative regarding the similarity with a given question.

### Clusters and Analysis

First in the data folder we have 4 excel files:
- usuarios: Is a database composed by two columns, users and tweets for the experiment 1
- resultados: Is a database that has the cosine distances matrix between the tweets from the experiment 1, also has a final column with the cluster of each tweet
- usuarios2: Is a database composed by two columns, users and tweets for the experiment 2
- resultados2: Is a database that has the cosine distances matrix between the tweets from the experiment 2, also has a final column with the cluster of each tweet


Into the project folder exists a python code called: procesamiento_final.py. The code run the experiment 2 so if you want to change to verify the experiment 1 results, change the database read and continue with the steps commented into the code.

"procesamiento_final.py" has three sections:
- Start
- Plot cluster results
- Sentimental Analysis
- Aggresive users

In the first section, you can obtain the "resultados" file depending which is the experiment that you analize.

In the second section, you plot the clusters of the cosine distances matrix of an experiment, the results that you obtain are show into the images folder in the data folder.

In the third section, you plot the sentimental analysis plots that you can compare with the images in the images folder.

Finally in the aggresive users section we select a set of potential aggresive users.



