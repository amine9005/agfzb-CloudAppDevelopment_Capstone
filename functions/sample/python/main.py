"""IBM Cloud Function that gets all reviews for a dealership

Returns:
    List: List of reviews for the given dealership
"""
import requests
import sys 
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

def main(param_dict):
    
    
    authenticator = IAMAuthenticator("UA37ZXE1uPKccaL9sd3DjpcirgDeAcHMUAKOMJTGx-lJ")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://apikey-v2-k2c3zaorv3b5hb7ro6w2kq1ibgf6ygdvmjsh071ur0n:8b8756854b26cafb53606633c8c744da@9d7ee7e6-fc62-4d0d-92f6-9eaabd3b83e2-bluemix.cloudantnosqldb.appdomain.cloud/")
    
    response = service.post_find(
                db='reviews',
                selector={'dealership': {'$eq': int(param_dict['id'])}},
            ).get_result()
    try: 
        # result_by_filter=my_database.get_query_result(selector,raw_result=True) 
        result= {
            'headers': {'Content-Type' : 'application/json'}, 
            'body': {'data' : response} 
            }        
        return result
    except :
        print("unable to connect")
