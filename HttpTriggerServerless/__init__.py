import logging
import json
import azure.functions as func

from azure.storage.blob import BlobClient #Pour charger un fichier disponible dans un container
import pandas as pd
from io import StringIO
from scipy.sparse import csr_matrix
from implicit.bpr import BayesianPersonalizedRanking


''' *******Chargement des fichiers********'''

#1. chargement du fichier embedding
sas_url= "https://conteneur3.blob.core.windows.net/conteneur3/df_embeddings_inter.csv"
blob_client = BlobClient.from_blob_url(sas_url)
blob_data = blob_client.download_blob()
df_embeddings = pd.read_csv(StringIO(blob_data.content_as_text()), index_col=0)

#2. chargement du fichier interactions
sas_url = "https://conteneur3.blob.core.windows.net/conteneur3/clicks2_azure.csv"
blob_client = BlobClient.from_blob_url(sas_url)
blob_data = blob_client.download_blob()
df_clicks = pd.read_csv(StringIO(blob_data.content_as_text()), index_col=0)


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
        print("La taille de la dataframe embedding est :", df_embeddings.shape)
        print("La taille de la dataframe df_clicks est :", df_clicks.shape)
        
        
        csr_item_user, csr_user_item = compute_interaction_matrix(df_clicks)
        
        print("La taille de la dataframe csr_item_user est :", csr_item_user.shape)
        print("La taille de la dataframe csr_user_item est :", csr_user_item.shape)
                
        recommendations = get_cf_reco(df_clicks, int(name), csr_item_user, csr_user_item, model_path=None, n_reco=5, train=True)

        return func.HttpResponse(f"{recommendations}")
    else:
        return func.HttpResponse(
             "Aucun utilisateur n'a été renseigné",
             status_code=200
            )


def compute_interaction_matrix(clicks):
    # Création de la dataframe d'interaction entre users et articles
    interactions = clicks.groupby(['user_id','click_article_id']).size().reset_index(name='count')
    print('Interactions DF shape: ', interactions.shape)

    # csr = compressed sparse row (format adapté au opérations mathématiques sur les lignes )
    # Création de la sparse matrix de taille (number_items, number_user)
    csr_item_user = csr_matrix((interactions['count'].astype(float),
                                (interactions['click_article_id'],
                                 interactions['user_id'])))
    print('CSR Shape (number_items, number_user): ', csr_item_user.shape)
    
    # Création de la sparse matrix de taille (number_user, number_items)
    csr_user_item = csr_matrix((interactions['count'].astype(float),
                                (interactions['user_id'],
                                 interactions['click_article_id'])))
    print('CSR Shape (number_user, number_items): ', csr_user_item.shape)
    
    
    return csr_item_user, csr_user_item




def get_cf_reco(clicks, userID, csr_item_user, csr_user_item, model_path=None, n_reco=5, train=True):

   
    # Entrainement du modele sur la sparse matrix de taille (number_items, number_user)
    
    if train or model_path is None:
        #model = LogisticMatrixFactorization(factors= 128, random_state=42)
        model = BayesianPersonalizedRanking(factors=100, regularization=0.01, use_gpu=False, iterations=5, random_state=55)
        print("[INFO] : Début de l'entrainement du modèle")
        model.fit(csr_user_item)

    
    # Recommandation de N articles depuis la sparse matrix de taille (number_user, number_items)
    # Utilisation de Implicit built-in method
    # N (int) : nombre d'article à recommander
    # filter_already_liked_items (bool) : Si true, ne pas retourner d'articles présent dans le traing set qui ont déjà été consulté par le user
    recommendations_list = []
    
    recommendations = model.recommend(userID, csr_user_item[userID], N=n_reco, filter_already_liked_items=True)

    recommendations = [elt[:n_reco] for elt in recommendations]
    
    recoms=recommendations[0].tolist()
    
  
    
    return  json.dumps(recoms)