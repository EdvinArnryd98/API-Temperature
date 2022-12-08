from flask import Flask
from flask_mqtt import Mqtt

app = Flask(__name__)
app.config['MQTT_BROKER_URL'] = 'broker.hivemq.com'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 5
app.config['MQTT_TLS_ENABLED'] = False
topic = 'topicTester/10'
mqtt_client = Mqtt(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
    if rc == 0:
        print('Connected successfully')
        mqtt_client.subscribe(topic)
    else:
        print('Something went wrong:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
    m_topic = message.topic
    m_payload = message.payload.decode('utf-8')
    print(f'Received message on topic: {m_topic}: {m_payload}')
    with open(file='storage.txt', mode='w', encoding='utf-8') as file:
        file.write(m_payload)


@app.route('/get/')
def get_message():
    with open(file='storage.txt', mode='r', encoding='utf-8') as file:
        data = file.read()
    return ({'Temperature': data}), 200


if __name__ == '__main__':
    app.run(debug=False)