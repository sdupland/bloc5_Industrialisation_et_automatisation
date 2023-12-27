# bloc5 Industrialisation et automatisation

Industrialisation d'un algorithme d'apprentissage automatique et automatisation des processus de décision

[GetAround](https://www.getaround.com/?wpsrc=Google+Organic+Search) is the Airbnb for cars. You can rent cars from any person for a few hours to a few days! Founded in 2009, this company has known rapid growth. In 2019, they count over 5 million users and about 20K available cars worldwide.

When renting a car, our users have to complete a checkin flow at the beginning of the rental and a checkout flow at the end of the rental.

When using Getaround, drivers book cars for a specific time period, from an hour to a few days long. They are supposed to bring back the car on time, but it happens from time to time that drivers are late for the checkout.

Late returns at checkout can generate high friction for the next driver if the car was supposed to be rented again on the same day : Customer service often reports users unsatisfied because they had to wait for the car to come back from the previous rental or users that even had to cancel their rental because the car wasn’t returned on time.

In order to mitigate those issues we’ve decided to implement a minimum delay between two rentals. A car won’t be displayed in the search results if the requested checkin or checkout times are too close from an already booked rental.

It solves the late checkout issue but also potentially hurts Getaround/owners revenues: we need to find the right trade off.

This project is divided into three parts :
- give some insights about delay and turnover
- help to calibrate the minimum delay between two rentals
- developped a machine learning model in order to suggest optimum price for a car according to these characteristics.

The two first points will be proposed through a dashboard.
The optimum price will be delivered through an API.

you will find in this projetct different folders :
- getaround_dashboard with .... the dashboard ans all the files needed (included dataset used). Dashboard can be found at this link : https://dashboard-getaround-sndd.streamlit.app/
- getaround_ml_local with the notebook used to get thet raw data, transform it, create, train models and choose one
- getaround_ml_api with a script using fast_api in order to deliver the predicted rental price of a car
- getaround_mlflow with a script using heroku and mlflow



