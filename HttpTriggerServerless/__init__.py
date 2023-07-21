import logging
import json
import azure.functions as func
from azure.storage.blob import BlobClient
import pandas as pd
from io import StringIO

sas_url = "https://conteneur3.blob.core.windows.net/conteneur3/clicks2.csv"
blob_client = BlobClient.from_blob_url(sas_url)
blob_data = blob_client.download_blob()
df = pd.read_csv(StringIO(blob_data.content_as_text()))
print(df)

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('userID')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('userID')

    if name:
        #chargement du fichier d'interactions
        
        
        recommendations = ['Article 1', 'Article 2', 'Article 3', 'Article 4', 'Article 5']
        response_data = {'userID': name,'recommendations': recommendations[:5]}
        response_body = json.dumps(response_data)
        
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. Response is : {response_body}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
                                                                