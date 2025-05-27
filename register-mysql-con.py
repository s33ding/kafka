import subprocess

def run_cmd(cmd):
    print(f"▶ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error:\n{result.stderr}")
    else:
        print(f"✅ Output:\n{result.stdout}")
    return result

# 1. Copy the JSON file into the kafka-client pod
run_cmd("kubectl cp mysql-connector.json kafka-client:/tmp/mysql-connector.json")

# 2. Post the connector config to Debezium
run_cmd("kubectl exec kafka-client -- curl -X POST http://debezium-connect:8083/connectors "
        "-H 'Content-Type: application/json' "
        "-d @/tmp/mysql-connector.json")

# 3. Verify that the connector is now listed
run_cmd("kubectl exec kafka-client -- curl http://debezium-connect:8083/connectors")

