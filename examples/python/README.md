# Generic Python example class to run GraphQL queries against Rubrik Security Cloud

## Authentication
Authenticating to the Rubrik Security Cloud API requires a Rubrik Security Cloud Service Account. The service account is OAuth2 client credentials. Basically, this means you will have a clientId and secret that are used to retrieve an access token. The access token is legitimate for 12 hours.

Instantiate RSC client and connect:
```
import rsc
rsc = rsc.Client("INSTANCE_NAME.my.rubrik.com","CLIENT ID GOES HERE","CLIENT SECRET GOES HERE")
```

## Query Invocation
The `invoke` method will accept a query file path string and variables.

Getting a VM using the `getVmByName.gql` file from the examples and supplying query variables:
```
query_file = "../../getVmByName.gql"
variables = {"name": "sh1-fs-01"}
result = rsc.invoke(query_file,variables)
```

