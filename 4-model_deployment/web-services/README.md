## Model Deployment reading loading local model

This section aims to deploy model as web-service using Flask and Docker. The model has been taken from the module-`1-introduction`.
The model deployment code is containerized.

**NOTE :** I have used `pipenv`for this section to create virtual environment. I have provided the Pipfile if you are facing issues with the environment. You can create a virtual environment using Pipfile by running the command : 
```
pipenv install
```
or with `pipenv` create a new virtual environment:
```bash
pipenv install scikit-learn==1.0.2 flask requests --python=3.9
```
Activate the environment

```bash
pipenv install
```

More information on how to create a virtual environment using Pipfile can be found [here](https://stackoverflow.com/questions/52171593/how-to-install-dependencies-from-a-copied-pipfile-inside-a-virtual-environment)

## Steps to run the script in SSH terminal using Flask

1. Open two terminal windows, Terminal 1 and Terminal 2. In both the terminals, activate virtual environment which has the libraries mentioned in Pipfile. You should be inside web-service directory in both the terminals.

Activate the virtual environment by running the following command in SSH terminals :

```bash
pipenv shell
```
2. In terminal 1, to start the server, execute the following command :
```bash
python app_predict.py
```
**NOTE :** The server should keep running, and you should go to terminal 2 to execute the test script.

1. In terminal 2, execute the following command :
```bash
 python test.py
```
This will send the json data to the flask app running.
**Note:** Current flask set up is for the development environment. Install gunicorn and configure in order to solve the following production environment type warning.
```bash
pipenv install gunicorn
gunicorn --bind=0.0.0.0:9696 predict:app
```

Note: our Flask application is ready to dockerized


## Steps to run the script in terminal using Docker

1. Stop the web services running in terminal CTRL + C

2. Here, we are using docker to run the model. The code is containerized. In terminal 1, execute the following commands :
```bash
docker build -t store-sales-prediction:v1 .
```
This command will build a Docker image "store-sales-prediction" from the Dockerfile.

**NOTE :** Do not forget to include the "." at the end of Command-1

3. After the image is built, start the gunicorn server by running the following command in terminal 1 : 

```bash
docker run -it --rm -p 9696:9696 store-sales-prediction:v1
```
**NOTE :** The services should keep running, and you should go to terminal 2 to execute the test script.

4. To get response from the server, execute the following command in terminal 2 : 
```python
python test.py
```
