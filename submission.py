from google.oauth2 import service_account
import requests
import google.auth.transport.requests
from google.auth.transport.requests import AuthorizedSession
from google.auth.transport.requests import Request
from google.oauth2 import id_token
import google.oauth2.credentials

class Submission:

    # https://developers.google.com/identity/protocols/oauth2/service-account
    # https://stackoverflow.com/questions/66600940/authenticating-a-gcp-service-account-using-identity-aware-proxy-iap-in-python
    # https://github.com/salrashid123/google_id_token/blob/master/python/main.py

    def __init__(self):
        """ Constructor to initialize 3 variables required for submission
        """

        self.name = "Rachit Trivedi"
        self.email_id = "rachitt96@gmail.com"
        self.submission_rest_api = "https://ld-ds-take-home-test.appspot.com/submissions"

    def submit_result_to_api(self, recommendations_by_id_dict, service_account_path='./ld-ds-take-home-service-account.json'):
        """ A function to submit the recommendations in REST API

        Arguments:
            recommendations_by_id_dict: (dict{str:list[str]}) A dictionary with
                                        key = product_id
                                        value = list of 5 recommended products name
            service_account_path: (str) Location of service account json file to authenticate the REST API
        
        Returns:
            None. (This function just submits the recommendation to REST API)
        """

        submission_dict = {}
        submission_dict['name'] = self.name
        submission_dict['email'] = self.email_id
        for product_id in recommendations_by_id_dict:
            submission_dict[product_id] = recommendations_by_id_dict[product_id]
        
        token = self.GetIDTokenFromServiceAccount(service_account_path)
        
        resp = requests.request(
            'POST', 
            self.submission_rest_api,
            headers={'Authorization': 'Bearer {}'.format(token)}, 
            data=submission_dict
        )
        
        print(resp, resp.text) 

    def GetIDTokenFromServiceAccount(self, svcAccountFile):
        """ A function to get OpenID token from GCP service account file

        Arguments:
            svcAccountFile: (str) Location of service account json file

        Returns:
            token: OpenID Connection token
        """

        creds = service_account.IDTokenCredentials.from_service_account_file(svcAccountFile, target_audience='459957645727-m8ksvmqcp3sk4ok9cgh61u2q85knaqjg.apps.googleusercontent.com')
        request = google.auth.transport.requests.Request()
        creds.refresh(request)
        return creds.token