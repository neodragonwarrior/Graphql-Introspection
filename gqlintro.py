import subprocess
import requests

def test_introspection_endpoint(endpoint):
    # Create the introspection query
    query = """
    query IntrospectionQuery {
      __schema {
        queryType { name }
        mutationType { name }
        subscriptionType { name }
        types {
          ...FullType
        }
        directives {
          name
          description
          locations
          args {
            ...InputValue
          }
        }
      }
    }

    fragment FullType on __Type {
      kind
      name
      description
      fields(includeDeprecated: true) {
        name
        description
        args {
          ...InputValue
        }
        type {
          ...TypeRef
        }
        isDeprecated
        deprecationReason
      }
      inputFields {
        ...InputValue
      }
      interfaces {
        ...TypeRef
      }
      enumValues(includeDeprecated: true) {
        name
        description
        isDeprecated
        deprecationReason
      }
      possibleTypes {
        ...TypeRef
      }
    }

    fragment InputValue on __InputValue {
      name
      description
      type { ...TypeRef }
      defaultValue
    }

    fragment TypeRef on __Type {
      kind
      name
      ofType {
        kind
        name
        ofType {
          kind
          name
          ofType {
            kind
            name
            ofType {
              kind
              name
              ofType {
                kind
                name
                ofType {
                  kind
                  name
                }
              }
            }
          }
        }
      }
    }
    """

    # Send the query to the endpoint
    response = requests.post(endpoint, json={'query': query})

    # Check the response status code and the presence of the specific string in the response
    if response.status_code == 200 and '"data": {"__schema": {"queryType": {"' in response.text:
        print("Introspection is enabled")
    else:
        print("Introspection is not enabled")

def test_introspection_curl(curl_command):
    # Execute the curl command
    result = subprocess.run(curl_command, shell=True, stdout=subprocess.PIPE)

    # Check the response status code and the presence of the specific string in the response
    if result.returncode == 0 and '"data": {"__schema": {"queryType": {"' in result.stdout:
        print("Introspection is enabled")
    else:
        print("Introspection is not enabled")

# Accept user input
user_input = input("Enter a GraphQL endpoint URL or a curl command: ")

# Check if the user input is a valid URL
if user_input.startswith("http"):
    test_introspection_endpoint(user_input)
else:
    test_introspection_curl
