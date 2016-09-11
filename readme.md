# DiTech data competation

## log

### 2016-09-05
Finish basic data cleaning
Try to make a benchmark using kNN

convert all training data in one file

#### To Mrbean ####
* Data Cleaning Code is dcp.py
* Beside weather_data,traffic_data & time, I have included previous 3 gaps of each data points as their features as well. Just to remind you.
* didi_concat_data.ipynb is used to join training data different day to a single csv file.
* My knn code is in didi_knn_on_training_set.ipynb

The final MAE result on Training set is 1.538

To run `didi_knn_on_training_set.ipynb`, you only need to unzip TrainingData.zip

「以上」

### 2016-09-06

knn - benchmark on test-set-1 has been uploaded to UdaGroup

final MAE score = 9.6

#### what to do tomorrow ####
* rewrite dcp.py into a better looking form
* add `weekdays/weekend`, `price` as new features
* implement feature selection
* Try better regression algorithms
* Find a way to include POI as features 

「以上」

### 2016-09-11

add `weekdays/weekend`, `price` as new features
implement feature selection

data cleaning takes some time
check `ridge regression`, `GradientBoostTree`, and better `knn` tomorrow
=======

### 2016-09-12

most useful features are three previous gaps, and two previous counts

mae decrease to 5.3

Finished data cleaning process, result has been uploaded to Udacity slack

「以上」

