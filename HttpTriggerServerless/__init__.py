import logging
import json
import azure.functions as func
'''from azure.storage.blob import BlobClient #Pour charger un fichier disponible dans un container
from azure.storage.blob import ContainerClient #Pour enregistrer un fichier dans un container
import pandas as pd
from io import StringIO
import pickle'''

''' *******Chargement des fichiers********'''

#1. chargement du fichier embedding
'''sas_url= "https://conteneur3.blob.core.windows.net/conteneur3/df_embeddings_inter.csv"
blob_client = BlobClient.from_blob_url(sas_url)
blob_data = blob_client.download_blob()
df_embeddings = pd.read_csv(StringIO(blob_data.content_as_text()), index_col=0)'''

#2. chargement du fichier interactions
'''sas_url = "https://conteneur3.blob.core.windows.net/conteneur3/clicks2.csv"
blob_client = BlobClient.from_blob_url(sas_url)
blob_data = blob_client.download_blob()
df_clicks = pd.read_csv(StringIO(blob_data.content_as_text()),chunksize=10 ** 6)'''

#3. chargement du modèle
'''sas_url = "https://conteneur3.blob.core.windows.net/conteneur3/recommender.model"
blob_client = BlobClient.from_blob_url(sas_url)
blob_data = blob_client.download_blob()
with open('blob_data', 'rb') as filehandle:
    model = pickle.load(filehandle)'''



#sas_url = "https://conteneur3.blob.core.windows.net/conteneur3"
#container_client = ContainerClient.from_container_url(sas_url)
#output = io.StringIO()
#head = ["col1" , "col2" , "col3"]
#l = [[1 , 2 , 3],[4,5,6] , [8 , 7 , 9]]
#df = pd.DataFrame(l , columns = head)
#print(df)
#output = df.to_csv(index_label="idx", encoding = "utf-8")
#blob_client = container_client.upload_blob(name="myblob", data=output)


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')

    name = req.params.get('userID')
    df_clicks=req.params.get('df_clicks')
    
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('userID')

    if name:
        #print("La taille de la dataframe embedding est :", df_embeddings.shape)
        #print("La taille de la dataframe intéractions est :", {df_clicks.shape})
        
        
        print("lancement recoms")
        recommendations = ['Article 1', 'Article 2', 'Article 3', 'Article 4', 'Article 5']
        response_data = {'userID': name,'recommendations': recommendations[:5]}
        response_body = json.dumps(response_data)
        
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully. Response is : {response_body}")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )
                                                                