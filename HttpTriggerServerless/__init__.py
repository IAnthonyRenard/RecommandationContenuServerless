import logging
#test2
import azure.functions as func


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
        #recommendations = ['Article 1', 'Article 2', 'Article 3', 'Article 4', 'Article 5']
        #response_data = {'user_id': id,'recommendations': recommended_articles[:5]}
        #response_body = json.dumps(response_data)
        
        return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    else:
        return func.HttpResponse(
             "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
             status_code=200
        )


'''def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    # Récupérer les paramètres de la requête
    id = req.params.get('id')
    rec_type = req.params.get('type')
    # Effectuer ici la logique nécessaire pour obtenir la liste d'articles recommandés
    # en fonction de l'ID utilisateur et du type de recommandation
    # Exemple factice : renvoyer une liste de 5 articles recommandés statiques
    recommended_articles = ['Article 1', 'Article 2', 'Article 3', 'Article 4', 'Article 5']
    # Générer la réponse JSON
    response_data = {
        'user_id': id,
        'recommendations': recommended_articles[:5]  # Prendre les 5 premiers articles recommandés
    }
    response_body = json.dumps(response_data)
    # Renvoyer la réponse HTTP
    return func.HttpResponse(
        response_body,
        mimetype='application/json',
        status_code=200
    )'''                                                                 