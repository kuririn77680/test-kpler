=================
Vessel Trips
=================
-------------------------
Kpler test
-------------------------

installation and run app
============

This project is set in a poetry env, and was made under
python3.10.6
You will need to have the poetry library.

install dependancies
----------

From the root folder of the project,
run :: poetry install :: to install all need libraries.

start a database
----------

With docker we will create a postgresl container with the following command
<docker run -d -e POSTGRES_HOST_AUTH_METHOD=trust -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=backenddb -p 5432:5432 postgres:13>

run  application
----------

From the root folder of the project,
run <poetry shell>
then
run <python -m backend>
your application is running.

execute unit tests
----------

You will need a test database, to do it run the following command:
<docker run -d -e POSTGRES_HOST_AUTH_METHOD=trust -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=test-backenddb -p 5432:5432 postgres:13>

From the root folder of the project,
run <poetry run pytest>
