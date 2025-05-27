import boto3
import json
import sys
import os

def get_mysql_credentials(secret_name, region='us-east-1'):
    client = boto3.client('secretsmanager', region_name=region)
    try:
        response = client.get_secret_value(SecretId=secret_name)
        secret_string = response['SecretString']
        credentials = json.loads(secret_string)
        return credentials
    except Exception as e:
        print(f"Error retrieving secret '{secret_name}':", e)
        sys.exit(1)

def generate_connector_config(credentials, output_file='mysql-connector.json'):
    try:
        config = {
            "name": "rds-cdc-connector",
            "config": {
                "connector.class": "io.debezium.connector.mysql.MySqlConnector",
                "database.hostname": credentials['host'],
                "database.port": credentials.get('port', "3306"),
                "database.user": credentials['user'],
                "database.password": credentials['password'],
                "database.server.id": "184054",
                "topic.prefix": "rds_mysql",
                "database.include.list": credentials['db_name'],
                "include.schema.changes": "true",
                "schema.history.internal.kafka.bootstrap.servers": "kafka:9092",
                "schema.history.internal.kafka.topic": "schema-changes.rds_mysql"
            }
        }

        with open(output_file, 'w') as f:
            json.dump(config, f, indent=2)

        print(f"Debezium connector config written to {output_file}")

    except KeyError as e:
        print(f"Missing field in credentials: {e}")
        sys.exit(1)

if __name__ == "__main__":
    secret_name = "rds-secret"
    region = "us-east-1"
    creds = get_mysql_credentials(secret_name, region)
    generate_connector_config(creds)

