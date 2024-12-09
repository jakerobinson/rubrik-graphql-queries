#!/bin/bash

# Path to the RSC Service Account file containing OAuth2 client credentials
CREDENTIALS_FILE="/path/to/service_account.json"
API_URL="https://REDACTED.my.rubrik.com/api/graphql"

# Authenticate to RSC via OAuth2 client credentials
authenticate() {
    CLIENT_ID=$(jq -r '.client_id' "$CREDENTIALS_FILE")
    CLIENT_SECRET=$(jq -r '.client_secret' "$CREDENTIALS_FILE")
    TOKEN_URI=$(jq -r '.access_token_uri' "$CREDENTIALS_FILE")

    # Get access token
    RESPONSE=$(curl -s -X POST "$TOKEN_URI" \
        -H 'Content-Type: application/json' \
        -d "{\"client_id\": \"$CLIENT_ID\", \"client_secret\": \"$CLIENT_SECRET\", \"grant_type\": \"client_credentials\"}")
    
    ACCESS_TOKEN=$(echo $RESPONSE | jq -r '.access_token')
    if [[ -z "$ACCESS_TOKEN" ]]; then
        echo "Failed to get access token"
        exit 1
    fi
}

# Function to read GraphQL file and variables
read_graphql_file() {
    GQL_FILE="$1"
    if [[ ! -f "$GQL_FILE" ]]; then
        echo "GraphQL file not found: $GQL_FILE"
        exit 1
    fi
    QUERY=$(<"$GQL_FILE")
    # Escape newlines and double quotes
    QUERY=$(echo "$QUERY" | jq -Rs .)
}

# Function to process graphql variables
process_variables() {
    shift # Remove the first argument (file path)
    VARIABLES='{}'
    while [[ "$#" -gt 0 ]]; do
        PAIR="$1"
        KEY=$(echo "$PAIR" | cut -d= -f1)
        VALUE=$(echo "$PAIR" | cut -d= -f2)
        
        VARIABLES=$(echo "$VARIABLES" | jq --arg key "$KEY" --arg value "$VALUE" '.[$key] = $value')
        
        shift
    done
}

# Function to post the query to the GraphQL API
post_graphql_query() {
    RESPONSE=$(curl -s -X POST "$API_URL" \
        -H "Authorization: Bearer $ACCESS_TOKEN" \
        -H "Content-Type: application/json" \
        -d "{\"query\": $QUERY, \"variables\": $VARIABLES}")
    
    echo "$RESPONSE" | jq
}

# Main script
if [[ "$#" -lt 1 ]]; then
    echo "Usage: $0 <path to gql file> [<variable>=<value> ...]"
    exit 1
fi

authenticate
read_graphql_file "$1"
process_variables "$@"
post_graphql_query