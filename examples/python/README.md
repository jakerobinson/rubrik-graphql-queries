# Generic Python example class to run GraphQL queries against Rubrik Security Cloud

## Setup
  - To Authenticate to the Rubrik API, follow the steps in [Adding a Service Account](https://docs.rubrik.com/en-us/saas/saas/adding_a_service_account.html)
  - Create environment variables for RSC_FQDN, RSC_CLIENT_ID, and RSC_CLIENT_SECRET using the service account
  - NOTE: RSC_FQDN is the FQDN of the RSC instance, NOT the client_token_uri from the service account details.

```bash
export RSC_CLIENT_ID="your-client-id"
export RSC_CLIENT_SECRET="your-client-secret"
export RSC_FQDN="YOUR_INSTANCE.my.rubrik.com"
```

## Authentication
Authenticating to the Rubrik Security Cloud API requires a Rubrik Security Cloud Service Account. The service account is OAuth2 client credentials. Basically, this means you will have a clientId and secret that are used to retrieve an access token. The access token is legitimate for 12 hours.

Instantiate RSC client and connect:
```
import rsc
rsc = rsc.Client()
```

## Query Invocation
The `invoke` method will accept a query file path string and variables.

Getting a VM using the `getVmByName.gql` file from the examples and supplying query variables:
```
query_file = "../../getVmByName.gql"
variables = {"name": "sh1-fs-01"}
result = rsc.invoke(query_file,variables)
```

## Output
The resulting output will be in json format.