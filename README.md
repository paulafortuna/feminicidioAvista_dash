# feminicidioAvista_dash ![icons](https://github.com/paulafortuna/images/blob/main/icons.jpg)

This repository presents the front-end app developed for the "Feminicidio à Vista" project.
This Github Repository it is continously deployed in Heroku and you can find the running app [here]( https://feminicidioavista.herokuapp.com/).

In terms of technologies it uses Dash which is a framework for deploying simple dashboards on top of Flask, Plotly and Python. This repository follows a typical dash architechture:


```bash
- app.py
- runtime.txt
- requirements.txt
- Procfile
- assets/
    |-- typography.css
    |-- header.css
- data_to_visualize
    |-- ... 
```
 
 These files contain:
 - The app.py file contains the main code to run the app.
 - The runtime contains the python version that heroku should run in deployment.
 - The requirements contain the python packages heroku should install with pip in deployment.
 - Procfile contains the gunicorn instruction that heroku will run in deployment.
 - The assets directory contains personalized css documents for the the app design.
 - The data_to_visualize contains the pre-computed tables and plotly plots to increase eficiency. This means that no computations are done in this dash front-end module.
