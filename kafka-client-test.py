import subprocess

def run_kafka_cmd(cmd):
    full_cmd = f"kubectl exec kafka-client -- bash -c '{cmd}'"
    print(f"▶ Running: {full_cmd}")
    result = subprocess.run(full_cmd, shell=True, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"❌ Error:\n{result.stderr}")
    else:
        print(f"✅ Output:\n{result.stdout}")
    return result

## 1. Create a topic
#run_kafka_cmd("kafka-topics.sh --create --topic test-topic --bootstrap-server kafka:9092 --partitions 1 --replication-factor 1")
#
## 2. Produce a message to the topic
#run_kafka_cmd("echo 'hello from python' | kafka-console-producer.sh --broker-list kafka:9092 --topic test-topic")
#
## 3. Consume messages from the topic
#run_kafka_cmd("kafka-console-consumer.sh --bootstrap-server kafka:9092 --topic test-topic --from-beginning --timeout-ms 5000")

run_kafka_cmd("echo 'hello from python' | kafka-console-producer.sh --broker-list kafka:9092 --topic test-topic")

