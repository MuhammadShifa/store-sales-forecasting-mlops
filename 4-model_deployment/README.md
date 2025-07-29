# Model Deployment

There are two ways to deploy a model :

1. Offline - Batch Deployment
2. Online - Web Service and Streaming

## 1. Offline - Batch Deployment

Batch deployment is used when we need our predictions at regular interval of time for example, daily, hourly, weekly or monthly.
We have a database with all our data. We have a scoring job, which has our model. It pulls the data from database and applies the model to return the predictions at regular interval of time.

## 2. Online - Web Service and Streaming

Online mode is always available for predictions. There are two ways to deploy online model : 

* Deployment as a Web Service 
* Deployment as a Stream

### 2a. Deployment as a Web Service

The web service contains our model. The app talks to backend, and backend talks to web service by sending the query and web service applies the model and the result(prediction) is sent back to the user.

Web service is one-to-one relationship and it needs to be up and running all the time. 

### 2b. Deployment as Stream

Streaming is used when there are stream of events. Model services listen for these events on the stream and output the predictions.

Streaming has three components : Event Stream, Producers, and Consumers.

Producer produces the events. It pushes some events to an event stream and the consumer reads from this event stream and reacts to the events.

Event streams and consumers are hosted by online services. Some of these services are : 

* Event Stream : Kafka, AWS Kinesis
* Consumers : AWS Lambda

Streaming can be one-to-many or many-to-many relationship.

More details about deployment are available [mlops-zoomcamp2025 - README.md](https://github.com/MuhammadShifa/mlops-zoomcamp2025/blob/main/04-deployment/README.md)

---

#### Model Deployment Sequence

The model deployment has been structured in the following sequence. It is important to follow this exact order, as some modules depend on the previous ones:

1. `web-services`
2. `web-services-mlflow`
3. `batch`
4. `streaming`

> **Note:** Please follow the order strictly. Each module includes a `README.md` file with instructions to help you run it correctly.

### Folder Structure  

**1. web-service**
   
Here, I have used Flask and Docker for making predictions on my dataset. I have put the script in a Flask app and have packaged the app to Docker.


**2. web-service-mlflow**
   
Here, I have used MLflow to train and log model. The model is deployed to cloud (S3 bucket) and used for prediction in flask app from mlflow.


**3. Batch**
   
In this module, I perform batch predictions using a trained model from MLflow, wIt loads the trained model from MLflow (S3), applies it to a CSV dataset, and saves the output predictions to a file.



Each folder has its own README which states how to run the scripts.
