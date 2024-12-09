# RSC Shell script example

This shell script reads an RSC Service Account file, reads a GraphQL query from a file, processes optional variables, and posts the query the RSC API. 

The response is formatted and outputted using `jq`.

## Prerequisites

Ensure you have the following installed on your machine:
- `jq`: Command-line JSON processor
- `curl`: Command-line tool for transferring data

You can install `jq` and `curl` using your package manager. For example, on Debian-based systems:

```
sudo apt-get update
sudo apt-get install jq curl
```

## Configuration

1. Your RSC Service Account file should be downloaded and stored in a secure location. The content should look like the following:

    ```json
    {
        "client_id": "client|REDACTED",
        "client_secret": "REDACTED",
        "name": "foo",
        "access_token_uri": "https://REDACTED.my.rubrik.com/api/client_token"
    }
    ```

2. Update the script (`invokeRscQuery.sh`) to set the path to your credentials file and your API endpoint:

    ```bash
    # Configuration
    CREDENTIALS_FILE="/path/to/service_account.json"
    API_URL="https://REDACTED.my.rubrik.com/api/graphql"
    ```

3. Make sure the script is executable:
```
chmod +x ./invokeRscQuery.sh
```

## Usage

1. Run the script with the path to the GraphQL query file and any optional variables (key=value pairs). The variables required for the query can be found in the query files in this examples repo.

    ```bash
    ./invokeRscQuery.sh ../../getSLADomainByName.gql slaName=bronze
    ```
