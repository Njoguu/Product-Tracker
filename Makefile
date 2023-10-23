# Variables
APP_NAME = JumiaProductTracker

#====================================
#== PYTHON DJANGO ENVIRONMENT Targets
#====================================

PYTHON = @python

makemigrations:
	${PYTHON} product_tracker/manage.py makemigrations

migrate:
	${PYTHON} product_tracker/manage.py migrate

start-api:
	${PYTHON} product_tracker/manage.py runserver

createsuperuser:
	${PYTHON} product_tracker/manage.py createsuperuser

update-app: makemigrations migrate start-server


#====================================
#== NODE JS ENVIRONMENT Targets
#====================================
NODE := @node

start-frontend:
	${NODE} frontend_sample/index.js


#====================================
#===== DOCKER ENVIRONMENT Targets
#====================================