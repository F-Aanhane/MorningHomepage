# MorningHomepage

## Purpose
This personal project is initiated to centralize all relevant information that is relevant to start your day.
The project can run locally, setup on a private server within your home network, or even run on cloud services to be
accessible from the web.

## Information offerings
Currently the project produces information of 2 different subjects: Dutch Railroads (NS) and general weather information.
The weather information consists of temperature, precipitation (chance) and cloud cover. Open source APIs are used to 
retrieve the necessary information. 
The information presented can be expanded with information of other public transport companies, private or work-related 
calendar feed, or traffic information on preferred routes.

## Architecture and techstack
The project is built on Python, makes use of flask to publish webpages and furthermore uses pandas, dotenv and open-meteo
libraries. More info can be found in requirements.txt. A NS API account is needed to get a key that is used for
authentication to the API.
