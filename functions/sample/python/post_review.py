import sys
from ibmcloudant.cloudant_v1 import CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
def main(dict):
    authenticator = IAMAuthenticator("EiL0F9hdPVoXkuZWhvK0IQ5P7mYE9Ya8GeL6pxyQym30")
    service = CloudantV1(authenticator=authenticator)
    service.set_service_url("https://apikey-v2-1gni6tilhs5uubrtjyllxetysphq3ux07dqyul0frpiq:83138939fd049776a2239f555d0e7456@e4bba7bb-ab33-43a9-bcf9-2ed4543b7610-bluemix.cloudantnosqldb.appdomain.cloud")
    response = service.post_document(db='reviews', document=dict["review"]).get_result()
    try:
    # result_by_filter=my_database.get_query_result(selector,raw_result=True)
        result= {
        'headers': {'Content-Type':'application/json'},
        'body': {'data':response}
        }
        return result
    except:
        return {
        'statusCode': 404,
        'message': 'Something went wrong'
        }