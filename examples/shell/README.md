# RSC Shell script example

This Bash script authenticates via OAuth2 client credentials, reads a GraphQL query from a file, processes optional variables, and posts the query to a specified GraphQL API endpoint. The response is formatted and outputted using `jq`.

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

1. Create a JSON file containing your OAuth2 client credentials (e.g., `credentials.json`):

    ```json
    {
        "client_id": "client|338b2794-f908-4dbc-a874-ba24c3948cfd",
        "client_secret": "REDACTED",
        "name": "foo",
        "access_token_uri": "https://REDACTED.my.rubrik.com/api/client_token"
    }
    ```

2. Update the script (`graphql_client.sh`) to set the path to your credentials file and your API endpoint:

    ```bash
    # Configuration
    CREDENTIALS_FILE="./credentials.json"
    API_URL="https://REDACTED.my.rubrik.com/api/graphql"
    ```

## Usage

1. Ensure your GraphQL query is saved in a file (e.g., `query.gql`), for example:

    ```graphql
    query getUser($id: ID!) {
        user(id: $id) {
            name
            email
        }
    }
    ```

2. Run the script with the path to the GraphQL query file and any optional variables (key=value pairs):

    ```bash
    ./graphql_client.sh /path/to/query.gql id=123
    ```

### Example

Save your GraphQL query to a file:

```graphql
query getUser($id: ID!) {
    user(id: $id) {
        name
        email
    }
}
