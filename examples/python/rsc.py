import requests, os
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

class Client:
    def __init__(self):
        self.gql_endpoint = f"https://{os.getenv('RSC_FQDN')}/api/graphql"
        self.token = self.get_oauth_token()

    def get_oauth_token(self):
        client = BackendApplicationClient(client_id=os.getenv("RSC_CLIENT_ID"))
        oauth = OAuth2Session(client=client)
        token = oauth.fetch_token(
            token_url=f"https://{os.getenv('RSC_FQDN')}/api/client_token", 
            client_id=os.getenv("RSC_CLIENT_ID"), 
            client_secret=os.getenv("RSC_CLIENT_SECRET"),
            auth=None,
            include_client_id=True
            )
        return token["access_token"]

    def invoke(self, query_file, variables=None):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json'
        }
        query_contents = open(query_file)
        query = query_contents.read()


        if variables is None:
            variables = {}

        all_results = []
        variables['after'] = None  # Start without a cursor

        while True:
            payload = {'query': query, 'variables': variables}
            response = requests.post(self.gql_endpoint, json=payload, headers=headers)

            if response.status_code != 200:
                raise Exception('GraphQL query failed: {}'.format(response.text))

            data = response.json()

            # Extract nodes
            nodes = data.get('data', {}).get('objects', []).get('nodes', [])
            all_results.extend(nodes)

            # Get pagination info
            page_info = data.get('data', {}).get('pageInfo', {})
            has_next = page_info.get('hasNext', False)
            end_cursor = page_info.get('endCursor', None)

            if not has_next:
                break  # Stop if there's no next page

            # Set the 'after' cursor for the next iteration
            variables['after'] = end_cursor

        return all_results