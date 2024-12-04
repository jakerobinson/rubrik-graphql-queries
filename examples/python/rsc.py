import requests

class Client:
    def __init__(self, fqdn, client_id, client_secret):
        self.rsc_instance = fqdn
        self.token_url = f"https://{self.rsc_instance}/api/client_token"
        self.gql_endpoint = f"https://{self.rsc_instance}/api/graphql"
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None
        self.get_token()

    def get_token(self):
        payload = {
            'grant_type': 'client_credentials',
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        response = requests.post(self.token_url, data=payload)
        if response.status_code == 200:
            self.token = response.json().get('access_token')
        else:
            raise Exception('Failed to get token: {}'.format(response.text))

    def invoke_query(self, query, variables=None):
        headers = {
            'Authorization': 'Bearer {}'.format(self.token),
            'Content-Type': 'application/json'
        }
        payload = {'query': query}
        if variables:
            payload['variables'] = variables
        response = requests.post(self.gql_endpoint, json=payload, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception('GraphQL query failed: {}'.format(response.text))

    def get_sla_by_name(self, name):
        query = """
        query getSlaByName($name: String) {
            slaDomains(filter: { field: NAME, text: $name }) {
                nodes {
                    name
                    id
                }
            }
        }
        """
        variables = {'name': name}
        return self.invoke_query(query, variables)

    def assign_sla(self, slaDomainAssignType, objectIds, slaOptionalId=None, shouldApplyToExistingSnapshots=None, shouldApplyToNonPolicySnapshots=None, existingSnapshotRetention=None):
        valid_types = ['noAssignment', 'doNotProtect', 'protectWithSlaId']
        if slaDomainAssignType not in valid_types:
            raise ValueError(f"Invalid slaDomainAssignType: {slaDomainAssignType}. Must be one of {valid_types}.")

        query = """
        mutation assignSla($input: AssignSlaInput!) {
            assignSla(input: $input) {
                success
            }
        }
        """
        variables = {
            'input': {
                'slaDomainAssignType': slaDomainAssignType,
                'objectIds': objectIds,
                'slaOptionalId': slaOptionalId,
                'shouldApplyToExistingSnapshots': shouldApplyToExistingSnapshots,
                'shouldApplyToNonPolicySnapshots': shouldApplyToNonPolicySnapshots,
                'existingSnapshotRetention': existingSnapshotRetention
            }
        }
        return self.invoke_query(query, variables)