import sys

import boto3
import os
import random
import csv
from locationer import Ecosystem

data_path = os.path.dirname(__file__)
print(sys.argv)
eco = Ecosystem(36, -84, 1, 1)
eco.to_file()
training_file = "ecosystem.csv"

s3_bucket_name = "welocate-data"
s3_folder_name = "v1"

session = boto3.Session(region_name='us-east-1',profile_name='ml_user')
ml_client = session.client('machinelearning')
randomNum = str(random.randrange(1,999999,1))

f = open('ml_model_id.txt','r')
modelID = f.read()
f.close()

response = ml_client.create_realtime_endpoint(
    MLModelId=modelID
)

endpointURL = response['RealtimeEndpointInfo']['EndpointUrl']
ice_file = os.path.join(data_path, 'ecosystem.csv')
ice_pre = open(ice_file, 'r')
icereader = csv.reader(ice_pre, delimiter=',')
final = []
for row in icereader:

    prediction = ml_client.predict(
    MLModelId=modelID,
    Record={
        '_Target_': row[1],
        'Var04': row[3],
        'Var09': row[8],
        'Var10': row[9],
        'Var11': row[10]
        
        },
        PredictEndpoint= endpointURL
    )
    line = row[4] + "," + row[5] + "," + str(prediction["Prediction"]["predictedValue"])
    final.append(line.split(','))

with open(os.path.join(data_path, "lines.csv"), 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(final)

def upload_files_to_s3():
        s3Client = session.resource('s3')
        fileNames = ["lines.csv"]
        for fileName in fileNames:
            filePath = os.path.join(data_path,fileName)
            print(filePath)
            s3Client.Bucket(s3_bucket_name).upload_file(filePath,s3_folder_name+"/"+fileName)

upload_files_to_s3()
