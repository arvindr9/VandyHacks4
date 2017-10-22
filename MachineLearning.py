import boto3
import os
import random
data_path = os.path.dirname(__file__)

training_file = "shops_final.csv"
training_schema_file = "shops_final.csv.schema"

s3_bucket_name = "welocate-data"
s3_folder_name = "v1"

session = boto3.Session(region_name='us-east-1',profile_name='ml_user')
ml_client = session.client('machinelearning')
randomNum = str(random.randrange(1,999999,1))
def upload_files_to_s3():
		s3Client = session.resource('s3')
		fileNames = [training_file,training_schema_file]
		for fileName in fileNames:
			filePath = os.path.join(data_path,fileName)
			print(filePath)
			s3Client.Bucket(s3_bucket_name).upload_file(filePath,s3_folder_name+"/"+fileName)

upload_files_to_s3()

def create_data_source(dataset_name, 
                       s3_data_uri, s3_schema_uri, 
                       ds_type, percent_begin, 
                       percent_end, 
                       compute_statistics):
    ds_id = "ds-boto3-" + randomNum + "shop-{0}".format(ds_type)
    data_spec = {}
    data_spec['DataLocationS3'] = s3_data_uri
    data_spec['DataSchemaLocationS3'] = s3_schema_uri
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

# Create Training Data Source
s3_train_uri = "s3://{0}/{1}/{2}".format(s3_bucket_name, s3_folder_name,training_file)
s3_train_schema_uri = "s3://{0}/{1}/{2}".format(s3_bucket_name, s3_folder_name,training_schema_file)

train_datasource = create_data_source(
    'shop_training',
    s3_train_uri,
    s3_train_schema_uri,
    'Training',0,70,True)

eval_datasource = create_data_source(
    'shop_evaluation',
    s3_train_uri,
    s3_train_schema_uri,
    'Evaluation',70,100,False)

print(train_datasource['DataSourceId'])
print(eval_datasource['DataSourceId'])

model_create_response = ml_client.create_ml_model(
    MLModelId='ml-' + randomNum + "-store",
    MLModelName='ML model: store-from-code',
    MLModelType='REGRESSION',    
    TrainingDataSourceId=train_datasource['DataSourceId'])

model_create_response

ml_client.get_ml_model(MLModelId = model_create_response['MLModelId'])['Status']

evaluation_response = ml_client.create_evaluation (
    EvaluationId="eval-" + randomNum + "-store",
    EvaluationName='Eval ML model: Store-demo-from-code',
    MLModelId = model_create_response['MLModelId'],    
    EvaluationDataSourceId=eval_datasource['DataSourceId'])
evaluation_response
eval_result = ml_client.get_evaluation(EvaluationId=evaluation_response['EvaluationId'])
eval_result['Status']
eval_result