import os
import requests
import snowflake.connector

def get_oauth_token():
    url = os.environ["az_OAUTH_TOKEN_URL"]
    data = {
        'grant_type': 'client_credentials',
        'client_id': os.environ["az_OAUTH_CLIENT_ID"],
        'client_secret': os.environ["az_OAUTH_CLIENT_SECRET"],
        'scope': 'session:role-any'  # Adjust scope as needed
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()['access_token']

def run_query(token):
    ctx = snowflake.connector.connect(
        user=os.environ["SF_USER"],
        account=os.environ["SF_ACCOUNT"],
        authenticator='oauth',
        token=token,
        role=os.environ.get("SF_ROLE"),
        warehouse=os.environ.get("SF_WAREHOUSE"),
        database=os.environ.get("SF_DATABASE"),
        schema=os.environ.get("SF_SCHEMA")
    )
    cs = ctx.cursor()
    try:
        cs.execute("SELECT CURRENT_TIMESTAMP();")
        for row in cs:
            print("Query Result:", row)
    finally:
        cs.close()
        ctx.close()

if __name__ == "__main__":
    token = get_oauth_token()
    run_query(token)
