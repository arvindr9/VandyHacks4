import boto3
import os
import random


data_path = os.path.dirname(__file__)
ml_client = session.client('machinelearning')
ecosystem = "ecosystem.csv"
s3_bucket_name = "welocate-data"
s3_folder_name = "v1"
randomNum = str(random.randrange(1,999999,1))
databaseID = ""

#Upload Files
def upload_files_to_s3():
		s3Client = session.resource('s3')
		fileNames = [ecosystem]
		for fileName in fileNames:
			filePath = os.path.join(data_path,fileName)
			print(filePath)
			s3Client.Bucket(s3_bucket_name).upload_file(filePath,s3_folder_name+"/"+fileName)

upload_files_to_s3()
#Create Datasource
def create_data_source(dataset_name, 
                       s3_data_uri,  
                       ds_type, percent_begin, 
                       percent_end, 
                       compute_statistics):
    ds_id = "ds-eco" + randomNum + "predict-{0}".format(ds_type)
    databaseID = ds_id
    data_spec = {}
    data_spec['DataLocationS3'] = s3_data_uri
    data_spec['DataRearrangement'] = \
        '{{"splitting":{{"percentBegin":{0},"percentEnd":{1},"strategy":"sequential"}}}}'.format(
        percent_begin, percent_end)
    
    response = ml_client.create_data_source_from_s3(
        DataSourceId=ds_id,
        DataSourceName="{0}_[percentBegin={1}, percentEnd={2}]".format(dataset_name, percent_begin, percent_end),
        DataSpec=data_spec,    
        ComputeStatistics=compute_statistics)
    
    print("Creating {0} datasource".format(ds_type))
    return response
 #Actually Create Source
 s3_predict_schema_uri = "s3://{0}/{1}/{2}".format(s3_bucket_name, s3_folder_name,ecosystem)

train_datasource = create_data_source(
    'eco_predicting',
    s3_train_uri,
    'Batch',0,100,False)

#Read model ID from file
f = open('helloworld.txt','r')
modelID = f.read()
f.close()
#Create Batch Prediction
predictionId ='ecosystem-' + randomNum
response = ml_client.create_batch_prediction(
    BatchPredictionId=predictionId,
    BatchPredictionName='ChosenLocation',
    MLModelId=modelID,
    BatchPredictionDataSourceId=databaseID,
    OutputUri='s3://welocate-data/'
)
#Storing the Manifest
response = client.get_batch_prediction(
    BatchPredictionId='predictionId'
)
def findReviews(fileName):
#Downloading the files in the manifest
for key,value in response:
	s3.Bucket("welocate-data").download_file(key,value)
	
