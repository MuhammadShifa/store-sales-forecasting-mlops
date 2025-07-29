## Model Deployment: Loading Model from S3 Bucket

* Train another model, track the experiment with remote MLflow server
* Put the model into a scikit-learn pipeline
* Model deployment when the tracking server is down

In this section, we will deploy the trained model to an AWS S3 bucket (cloud storage).

Before proceeding, ensure that the remote MLflow tracking server is already configured and running on your EC2 instance.

Next, execute all the cells in the notebook: `4.1 store-sales-prediction-remote-ec2-mlflow.ipynb`. This notebook will:

- Train the model
- Log all relevant metrics and artifacts to MLflow
- Store the model in the S3 bucket you set up earlier

🖼️ <img src="result_images/1-mlfow_exp.png" alt="ML Workflow" width="600"/>



We will use the trained model directly from the MLflow tracking server within our Flask-based web service application. This allows us to serve the latest logged model without manually downloading or copying model files.

🖼️ <img src="result_images/2-saved-model.png" alt="ML Workflow" width="600"/>


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


## Steps to execute the script

In the this step, we  need to export the `RUN_ID` of the model, `EXP_ID` and `S3_BUCKET_NAME` which was logged to our S3 bucket. Go to AWS account and open S3 (buckets).

RUN_ID can be found at : Amazon S3 > Buckets > {bucket-which-we-created-earlier} > {EXP_ID}/ > {RUN_ID}

For example, if bucket name is "mlops-zoomcamp-project", RUN_ID can be found at : Amazon S3 > Buckets > mlops-zoomcamp-project > {EXP_ID}/ > {RUN_ID}.

Export the `RUN_ID`, `EXP_ID` and `S3_BUCKET_NAME` byrunning the following command in terminal: 
```bash
export RUN_ID="run-id"
export EXP_ID='experiment-id'
export S3_BUCKET_NAME="bucket-name"
```
Verify the export value:
```bash
echo $RUN_ID
```
After exporting the `RUN_ID`, `EXP_ID`  and `S3_BUCKET_NAME`, execute the following command in same terminal: 

```bash
python app_predict.py
```
This command will start the server, load the model from s3 bucket and waits for incoming data.

**NOTE :** The server in terminal should keep running, and you should go to next terminal to execute the testing script.
```bash
python test.py
```
This command will send input data to the server and return the predicted store-sales based on the features we have sent. 
