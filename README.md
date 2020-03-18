# Dash-Covid

Application that utilizes Dash and several sources to vizualise coronavirus data.

## Data sources and services

 * [NovelCOVID/API](https://github.com/NovelCOVID/API)
    
    * Global Stats
    * Global Bar Chart
    * Country datatable 
    
    All the NovelCOVID/API related code is at service/data_service.py
 * [WHO data files](https://github.com/CSSEGISandData/COVID-19)
    
    * Confirmed cases, deaths and recoveries timeline

    All the WHO data files related code is at service/who_service.py

The service/service.py simply acts as a dispatcher for the other two services.

## Dash components

Three types of graphs are used from the dash components:

### Bar Chart
![Bar Chart](https://user-images.githubusercontent.com/25746825/76995265-44c4ad00-6958-11ea-99d5-e4fd6e6009f2.png)

Very simple chart that is provided a list of values and list of headers. Headers are used as x axis labels and values as y axis values. Updated constantly via NovelCOVID/API.

### Line Chart
![Timeline](https://user-images.githubusercontent.com/25746825/76995274-48583400-6958-11ea-8f61-079da8506e54.png)
Multiline chart that is used as timeline. Data is updated daily from the file provided from WHO.
### Data Table
![Datatable](https://user-images.githubusercontent.com/25746825/76995253-3f676280-6958-11ea-9ce7-e54726df16c2.png)
Datatable that include full country data and also highlights new cases and deaths. Filtering and sorting are enabled as provided natively from Dash. Updated constantly via NovelCOVID/API.

## Other files

* Procfile: File used to deploy in Heroku
* .gitignore: Boilerplate gitignore file for Python projects
* assets/theme.css: Dash provides some styling from codepen (can be found in app.py as external stylesheet). In order to have the application's theme modified a custom theme has been created. Majority of the styling is in here and is related to the Div and Graph dash components.


## Using the app

Create a new folder for the project and initialize git and virual environment and activate the latter:

```console
$ mkdir dash-covid
$ cd dash-covid
$ git clone https://github.com/karolosk/dash_example.git
$ cd dash_example       
$ virtualenv venv 
$ source venv/bin/activate 
```

Install the needed dependecies in your virual environment:


```console
$ pip install -r requirements.txt
```

Finally run the application:

```console
$ python app.py # or python3 app.py if you have both versions
```

Application will start at port 8050


## Heroku deployment


[App Link](https://dash-covid.herokuapp.com)

