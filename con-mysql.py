import boto3
import subprocess
import json
import sys

def get_mysql_credentials(secret_name, region='us-east-1'):
    # Create Secrets Manager client
    client = boto3.client('secretsmanager', region_name=region)

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
        secret_string = get_secret_value_response['SecretString']
        credentials = json.loads(secret_string)
        return credentials
    except Exception as e:
        print(f"Error retrieving secret '{secret_name}':", e)
        sys.exit(1)

def connect_mysql_cli(credentials):
    try:
        host = credentials['host']
        port = credentials.get('port', '3306')
        user = credentials['user']
        password = credentials['password']

        # Prepare the command
        cmd = [
            "mysql",
            "-h", host,
            "-P", port,
            "-u", user,
            f"-p{password}"
        ]

        # Start the mysql CLI
        subprocess.run(cmd)

    except KeyError as e:
        print(f"Missing expected credential field: {e}")
    except Exception as e:
        print("Failed to launch mysql CLI:", e)

if __name__ == "__main__":
    secret_name = "rds-secret"
    region = "us-east-1"

    creds = get_mysql_credentials(secret_name, region)
    connect_mysql_cli(creds)

