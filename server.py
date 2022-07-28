from cfenv import AppEnv
import requests
import base64
import pprint

######################################################################
############### Step 1: Read the environment variables ###############
######################################################################

env = AppEnv()
uaa_service = env.get_service(name='xsuaa-demo')
dest_service = env.get_service(name='destination1')
sUaaCredentials = dest_service.credentials["clientid"] + ':' + dest_service.credentials["clientsecret"]
sDestinationName = 'googleca'

######################################################################
#### Step 2: Request a JWT token to access the destination service ###
######################################################################

headers = {'Authorization': 'Basic '+base64.b64encode(bytes(sUaaCredentials,'utf-8')).decode(), 'content-type': 'application/x-www-form-urlencoded'}
form = [('client_id', dest_service.credentials["clientid"] ), ('grant_type', 'client_credentials')]

r = requests.post(uaa_service.credentials["url"] + '/oauth/token', data=form, headers=headers)

######################################################################
####### Step 3: Search your destination in the destination service #######
######################################################################

token = r.json()["access_token"]
headers= { 'Authorization': 'Bearer ' + token }

r = requests.get(dest_service.credentials["uri"] + '/destination-configuration/v1/destinations/'+sDestinationName, headers=headers)

######################################################################
############### Step 4: Access the destination securely ###############
######################################################################
destination = r.json()
print('***************************************destination info***************************************************',flush=True)

print(destination,flush=True)
pprint.pprint(destination)
#token = destination["authTokens"][0]
#headers= { 'Authorization': token["type"] + ' ' + token["value"] }

#r = requests.get(destination["destinationConfiguration"]["URL"] + '/secure/', headers=headers)
r = requests.get(destination["destinationConfiguration"]["URL"])
print(r.text)

