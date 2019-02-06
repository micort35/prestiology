# Prestiology
Suite of unique tools for advanced fantasy basketball analyses

## Description
Prestiology, named after Oklahoma City Thunder General Manager Sam Presti, aims to provide users with an increased amount of customization and depth in their toolset. In addition, another target of the site is to provide tools not found elsewhere, or not utilized much within the context of fantasy basketball, to expand on the number of analyses one can use in creating the ultimate fantasy basketball team.

## Design
The front-end uses minimal Javascript and relies on Bootstrap to style a large portion of the elements. The back-end is written in Python and uses Postgres for the database. Data is aggregated using a Basketball-Reference web scraper (see contributions). Psycopg2 is used for interfacing with Postgres through Python, and Flask gets the entirety of the project up and running.

## TODO:
* Improve documentation
* Expand trading tool to multiple players
* Matchup Analysis
* Player Impact Analysis
* Sentiment Analysis
* Error, info pages
* Move scraper to SQLAlchemy
* Add filters for certain seasonal periods

## Contributions:
* Jae Bradley, [basketball_reference_web_scraper](https://github.com/jaebradley/basketball_reference_web_scraper)