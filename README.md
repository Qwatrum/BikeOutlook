# BikeOutlook

---
###### A mobile app using machine learning to forecast the availability of rental bikes in cities

---

### TL;DR:
BikeOutlook is a mobile app developed to predict the availability of rental bikes in a city. It uses XGBoost and real time information from the stations and weather. Its objective is to promote the use of sustainable transportation, here rental bikes. Making it easier for the client to know whether they can be sure to get a rental bike at their desired place and time, this project tries to empower and strengthen this opportunity.

> [!NOTE]
> This project is split into two branches. 
> 1. The `master` branch with the app
> 2. The `python-code` branch [here](https://github.com/Qwatrum/BikeOutlook/tree/python-code) with the ML stuff
> 
> This README covers everything


## Table of contents:
1. [Description](#description)
   1. [The problem](#the-problem)
   2. [What are rental bikes](#what-are-rental-bikes)
   3. [The case](#the-case)
   4. [Solution](#solution)
2. [Architecture](#architecture)
   1. [Phase 1: Data collecting](#phase-1-data-collecting)
   2. [Phase 2: Model training](#phase-2-model-training)
   3. [Phase 3: Accessibility for the user](#phase-3-accessibility-for-the-user)
3. [The app](#the-app)
   1. [Images](#example-images)
4. [Do it yourself](#do-it-yourself)
5. [Known problems and ways to improve](#known-problems-and-ways-to-improve)
6. [License](#license)
7. [About me](#about-me)
8. [References](#references)

## Description:
### The problem:
> Assume Bob wants to go in a large city in the evening. He lives quite outside the city, his only two options are: a. taking his car or b. using one of the new rental bikes of a station near him. He quickly finds that near where he wants to go, there is another station. But wait! This station only has two bikes at the moment. With his, that would be three. But *what if* when he wants to return all the bikes are **gone**?  
> Therefore, he simply takes the car.

By being unsure whether one can surely get back home, one understandably prefers the safer but more expensive and worse for the environment option. By increasing the knowledge of the client with providing useful information regarding the availability, they might use (given that it is likely to get a bike) the more sustainable option.

### What are rental bikes:
In short rental bikes are bikes which are available in public often larger cities, to be rented and drive from one rental station to another. The client pays for example for the driven distance or used time. This is also called 'Bikesharing' and in many countries a thing.

In the following the focus lies on the service from nextbike GmbH (located in Germany). Nextbike offers Bikesharing in more than 300 cities worldwide[^1].  

### The case:
Further this project is about rental bikes in Hanover (Germany, "Hannover") as an example. Hanover has a population of ~522,000 (2024) on an area of 204.01 km²[^2]. At the time of writing, Hanover has 120 Nextbike bikesharing stations, distributed in the whole city but concentrated in the center. 

### Solution:
The solution is a mobile app displaying a map of Hanover with each station highlighted. When clicked the station shows information about the current availability and a forecast for the future. The forecast is made by a XGBoost model hosted on a server.


## Architecture:
The whole service from BikeOutlook is split into three phases:  
1. Data collecting
2. Model training
3. Accessibility for the user

### Phase 1: Data collecting
Nextbike offers as a part of GBFS (general bikeshare feed specification) opendata about the status in real time.  
By visiting `https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_{CITY-CODE}/gbfs.json` with a correct CITY CODE (such as `bn` for Berlin) one sees possible feeds. For this projects case important are:  
* https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_dh/de/station_information.json (Station information)
* https://gbfs.nextbike.net/maps/gbfs/v2/nextbike_dh/de/station_status.json (Station status)

The city code is "dh" which stands for Hanover.  
Station information provides us with the necessary information about the id, name, location of each station.  
Station status provides us the necessary information about how many bikes are available.

The first one must be called regularly to update which stations even exist anymore (during the development of this project some stations were added and some were removed).  
The second one must be called often as this is the heart of our project. I've run a cronjob on a server fetching every 15 minutes the amounts. It saves the current Datetime and the count of each station into a csv file. Here is what a shorted example entry looks like:  
`2026-05-24 15:45:00,6,1,4,2,3,8,11,4,0,0,1,0,9,3,0,7,0,4,3,1,0,2,...,0,4,0,9,0`

The first column is the Datetime, then the weekday and whether it is a weekend, after that each station follows with the current amount. If a station is removed the script recognized this and leaves the cell blank. When a new station is added, a new column is added to the back with all prior rows filled with a 0 for this station. E.g.:  

````
Before: 2026-05-24 15:45:00,6,1,4,2,3,8,11,4,0,0,1,0,9,3,0,7,0,4,3,1,0,2,...,0,4,0,9,0
New row: 2026-05-24 16:00:00,6,1,4,2,3,8,11,4,0,0,1,,9,3,0,7,0,4,3,1,0,2,...,0,4,0,9,0,1
After:
2026-05-24 15:45:00,6,1,4,2,3,8,11,4,0,0,1,0,9,3,0,7,0,4,3,1,0,2,...,0,4,0,9,0,**0**
2026-05-24 16:00:00,6,1,4,2,3,8,11,4,0,0,1,,9,3,0,7,0,4,3,1,0,2,...,0,4,0,9,0,1
````

Sadly the server is not perfect. All Datetimes are two hours off compared to Hanover time. This is not a big problem, all hours are offset by two using pandas timdedelta and empty cells are filled with a 0. This means newly added stations are treated like they were empty before and the model can learn that now they act like an actual station. And now not existing stations are also treated empty, but they can't be reached via the app.

The app also uses weather data as the usage of bikes is obviously highly dependent on the weather. The weather is fetched from open-meteo.com. Used elements are: temperature, humidity, surface pressure, rain, cloud cover, wind speed and the weather code (WMO standards).  
The weather is only on an hourly rate available that means only an entry for each hour when looking up the past weather. That's why the same weather is used for multiple times (e.g. 14:00 weather for 14:15).

### Phase 2: Model training
To develop a good model, several different approaches were tested. Tested were:
* A neural network, sequential with one and two hidden layer(s)
* Random Forest Regressor
* Random Forest Classifier
* XGB Regressor
* XGB Classifier
* LightGBM Regressor
* LightGBM Classifier

And for each model (where applicable) different test data categories:
* Absolute (the real amount of bikes)
* Categorical (5 categories depending on how many bikes available)
* Available (1 or 0 whether at least on bike is available)
* Change (the change of bikes relative to the predicted time)

Those model and categories were tested and evaluated what did better than other models or other categories.

For almost every model the train data was: 
1. (Time related) Year, month, month encoded in sin, month encoded in cosine, day of the week, day of the week encoded in sine, day of the week encoded in cosine, is weekend, hour, minute, total minutes, total minutes in sine, total minutes in cosine
2. (Weather related) Temperature, humidity, surface pressure, rain, cloud cover, wind speed, the weather code
3. (Stations related) Current amount of target station, fifteen minutes ago, thirty minutes ago, forty-five minutes ago, sixty minutes ago, two hours ago, one day ago, the difference between now and fifteen minutes ago, "" now and thirty minutes ago, "" now and sixty minutes ago, "" now and two hours ago, the average of the amount of bikes from now to thirty minutes ago, the average of the amount of bikes from now to sixty minutes ago, the std of now to sixty ago, the sum of all available bikes in the city, the difference of the sum from now and fifteen minutes ago

It was also tested with adding the information from 3 from **all** stations, but the models did worse.
Using this approach the models quickly got an accuracy of around 96%. One flaw explains this good result. The model always predicted the same as current. This is a well known occurence. My workaround was to oversample the rarer data, reducing the size of the train set but increasing other metrics which measure accucarcy for unbalanced data.
XGB Classifier did the best job classifying if a station will have at least one bike available in the future.
One train data example looks like this:
``0,2026,5,0.5,-0.866,0,0.0,1.0,0,19,15,1155,-0.9299,0.3679,24,37,0.0,0,1024,9,0,562880614,3,3,6,6,8,8,0,0,-3,-3,-5,-5,4.0,5.2,1.9391,233,-2``

0 is the target, followed by the other data

The data is split into train and test, but not shuffled before so no leaks should occur.

### Phase 3: Accessibility for the user
So the user can actually use the service it must be accessible. For that the trained model is hosted on a server and via a URL the app can retrieve information about stations. When the app calls the URL the data for the model is collected by getting the current station's status and weather. The response is the current amount followed by the probability of the station having at least one bike or being empty for 1, 2, 3 and 6 hours. An example response looks like this:
``[2, [[0.27824079990387, 0.72175920009613]], [[..., ...]], [[..., ...]], [[..., ...]]]``

This means currently there are 2 bikes and for the next hour, the model thinks the station being empty is possible but unlikely with 27 percent.

## The app:
The app is an android app providing a map of Hanover with each station highlighted. When a station is clicked a widget opens showing the current amount and a forecast. The data is requested live from the database. Using the output from the models, the prediction gets calculated. When the model is unsure (i.e. a difference smaller than 16%) a "~" is displayed otherwise a cross or check. The models certainty is also displayed below giving a feel of how certain the model is.

For the map is osmdroid used. If you build the app on your own, you should do: 1. set the URL to your database in the `MainActivity.java` file and 2. add the domain in `app/res/xml/network_security_config.xml` to the trusted domains.

Depending on your Android version you might need to handle permissions differently. And update the `strings.xml` for your language you want.

Lastly the station data is saved in the app, which you can acquire by going on the station information link and reformat it like you need.
### Example images:

![Stations near the main train station](img/example%20(2).png)

The app displaying stations near the main train station. Each icon is placed right there were the real station is.

![All the stations in Hanover in the app](img/example%20(3).png)

All the stations in Hanover. They are mostly in the city center but als some outside. For example in living areas.

![Example view of a station](img/example%20(1).png)

An example view of a widget of a station showing the current count and the prediction.


## Do it yourself:
If you want to do it for yourself follow these steps:

| Step | What                         | Why                             | How                                                                                                                                                            | Additional Info                                                                                                                     | Read more here             | Where                                                     |
|------|------------------------------|---------------------------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------|----------------------------|-----------------------------------------------------------|
| 1.   | Collect data                 | For training                    | Run a cronjob e.g. every 15 min<br/>For example with `pm2`: <br/> `pm2 start scrap_d.py --name "get-data" --interpreter python3` and `pm2 startup && pm2 save` | Make sure it is up and running few missing rows lead to more lost data. Also before you start update the IDs in the station_id list | Data Collecting            | `python-code`/src/data_preparation/scrap_d.py             |
| 2.   | Clean the data               | For better results              | Fill missing values                                                                                                                                            | It highly depends on how you got the data                                                                                           | Data Collecting            | `python-code`/src/data_preparation/clean_data.py          |
| 3.   | Collect weather data         | For training                    | Either you take the historical data from an API (e.g. open-meteo.com) or you request it also every 15 min                                                      | Be careful with different metrics, and timezones                                                                                    | Data Collecting            | `python-code`/src/data_preparation/restructure_weather.py |
| 4.   | Setup the train data         | For training                    | Think which features you want and add them                                                                                                                     | Depending on your model, encode some features with e.g. sine and cosine                                                             | Model training             | `python-code`/src/data_preparation/setup_data.py          |
| 5.   | Train the model              | This is what you want           | Split the data and train the model and evaluate it                                                                                                             | Be careful when splitting, do not shuffle the data to prevent leaks. And use good metrics                                           | Model training             | `python-code`/src/model/model7.py                         |
| 6.   | Load the model on the server | So the app can make predictions | Save the model e.g. as a `.bst` and put up a API using for example `Fast API`                                                                                  | Make sure you give the model the correct data                                                                                       | Accessibility for the user | `python-code`/src/model/get_prediction.py                 |
| 7.   | Deploy the app               | Would be useful right?          | The app should display the stations, use for example Android Studio                                                                                            | Add the URL to the server so it can make requests                                                                                   | The app                    | `master` branch                                           |


## Known problems and ways to improve
* Long (few seconds) loading times
* The models accuracy
* Change the XGB params, more data, more or less features

## License:
BikeOutlook is licensed under the GNU General Public License v3.0 (GPLv3).

**IMPORTANT:** This license only applies to this projects code. Third-party APIs, etc may be subject to their own terms and licenses. Please make sure you comply with those terms when using or distributing this project.

Weather data provided by Open-Meteo is licensed under CC BY 4.0.



## About me:
I only did the project for fun, this is **not** something like a case study. I like machine learning but this was my first ml project.

## References:
[^1]: [nextbike hompage](https://www.nextbike.de/en/)  
[^2]: [wikipedia](https://en.wikipedia.org/wiki/Hanover)



made by Qwatrum  
Copyright (c) 2026 Qwatrum
