# Generic Ansible Example to run GraphQL queries against Rubrik Security Cloud

You can run any GraphQL query/mutation with the rubrik.yml sample. You will need to pass in `query_file` and `query_variables`. In this example, I pass them in from the command-line as `extra-vars`.

The `query_variables` must match the naming and format of what is in the GQL query file.

```
ansible-playbook ./rubrik.yml --ask-vault-pass --extra-vars '{"query_file":"~/rubrik-graphql-queries/snapshotMailbox.gql","query_variables":{"mailboxIds":["555e2b65-6590-4c2e-9e70-ba68b314767a"]}}'
```

I have my service account credentials stored in an Ansible Vault. The rubrik.yml playbook expects it to be in this format:

```
rsc_instance:
  client_id: "client|abcdefghijketcetc"
  client_secret: "SECRETGOESHERE"
  uri: "https://YOURORG.my.rubrik.com"

```

You'll also need to change or delete the `vars_files` in the rubrik.yml file to meet your vault/variables location needs.