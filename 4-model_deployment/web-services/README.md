## Model Deployment using local model

This section aims to deploy model as web-service using Flask and Docker. The model has been taken from the module-`1-introduction`.
The model deployment code is containerized.

**NOTE :** I have used `pipenv`for this section to create virtual environment. I have provided the Pipfile for easy installation of required packages. Follow the instruction to install all the required packages: 

Activate the virtual environment
```
pipenv shell
```
Install the packages from Pipefile
```bash
pipenv install
```

or with `pipenv` we can also install packages and create a new virtual environment:
```bash
pipenv install scikit-learn==1.0.2 flask requests --python=3.9
```

More information on how to create a virtual environment using Pipfile can be found [here](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment)

## Steps to run the script in SSH terminal using Flask

1. Open two terminal windows/Linux. In both terminals, activate the virtual environment with `pipenv shell` and ensure you are inside the `web-service` directory.

2. In terminal 1, to start the server, execute the following command :
```bash
python app_predict.py
```
**NOTE :** The server should keep running, and you should go to terminal 2 to execute the test script.

1. In terminal 2, execute the following command :
```bash
 python test.py
```
This testing script will send the json data to the flask app running.

**Note:** Current flask set up is for the development environment. Install gunicorn and configure in order to solve the following production environment type warning.
```bash
pipenv install gunicorn
# Run the application
gunicorn --bind=0.0.0.0:9696 app_predict:app
```

Note: After sucessful testing of gunicorn app, our flask application is ready to dockerized

## Steps to run the script in terminal using Docker

1. Stop the web services running in terminal CTRL + C

2. Here, we are using docker to run the model. The code is containerized. In terminal 1, execute the following commands :
```bash
docker build -t store-sales-prediction:v1 .
```
This command will build a Docker image "store-sales-prediction" from the Dockerfile.

**NOTE :** Do not forget to include the "." at the end of Command-1

3. After the image is built, start the application server by running the following command: 

```bash
docker run -it --rm -p 9696:9696 store-sales-prediction:v1
```
**NOTE :** The services should keep running, and you should go to another terminal to execute the test script.

4. To get response from the server, execute the following command: 
```bash
python test.py
```
All Set!!
