import boto3
from botocore.auth import SigV4Auth
from botocore.awsrequest import AWSRequest

region = "us-east-1"
sts_url = f"https://sts.{region}.amazonaws.com/?Action=GetCallerIdentity&Version=2011-06-15"
request = AWSRequest(method="GET", url=sts_url)

SigV4Auth(boto3.Session().get_credentials(), "sts", region).add_auth(request)
signed_headers = dict(request.headers)


from datetime import timedelta, datetime
from conjur_api.client import Client
from conjur_api.models.general.conjur_connection_info import ConjurConnectionInfo
from conjur_api.providers.authn_authentication_strategy import AuthnAuthenticationStrategy
from conjur_api.models.ssl.ssl_verification_mode import SslVerificationMode
from conjur_api.providers import SimpleCredentialsProvider
from conjur_api.models.general.credentials_data import CredentialsData

# Fetch an API token from Conjur
conjur_url = "<insert conjur url>" #user defined
service_id = "<insert service id of authenticator>" #user defined
conjur_account = "<insert conjur account>" #user defined
conjur_host_id = "<insert host id for role>" #user defined

conjur_authenticate_uri = '{conjur_url}/authn-iam/{service_id}/{conjur_account}/{url_encoded_host_id}/authenticate'.format(
    conjur_url=conjur_url,
    service_id = service_id,
    conjur_account=conjur_account,
    url_encoded_host_id=conjur_host_id.replace('/', '%2F')
)
response = requests.post(conjur_authenticate_uri, data=signed_headers)
api_token = response.text

# Configure the Conjur Python SDK
connection_info = ConjurConnectionInfo(conjur_url, conjur_account, SslVerificationMode.INSECURE)
api_token_expiration = CredentialsData.convert_expiration_datetime_to_str(datetime.now() + timedelta(minutes=8))
credentials_data = CredentialsData(machine=conjur_url, api_token=api_token, api_token_expiration=api_token_expiration)
credentials_provider = SimpleCredentialsProvider()
credentials_provider.save(credentials_data)
del credentials_data
authn_strategy = AuthnAuthenticationStrategy(credentials_provider)
conjur_client: Client = Client(connection_info, authn_strategy=authn_strategy)

resp = conjur_client.whoami()

def lambda_handler(event, context):
    print(resp)