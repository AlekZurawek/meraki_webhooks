import logging
from flask import Flask, request, abort
import sqlite3
import json

app = Flask(__name__)

# This is your shared secret
SHARED_SECRET = 'XXXXX' # CHANGE TO YOUR OWN SECRET

# Set up the database connection and create table if it doesn't exist
def setup_database():
    conn = sqlite3.connect('/home/admin-az/webhooks/receiver_python/webhooks.db') # CHANGE TO YOUR OWN DIRECTORY
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS webhooks (
        id INTEGER PRIMARY KEY,
        version TEXT,
        sharedSecret TEXT,
        sentAt TEXT,
        organizationId TEXT,
        organizationName TEXT,
        organizationUrl TEXT,
        networkId TEXT,
        networkName TEXT,
        networkUrl TEXT,
        networkTags TEXT,
        deviceSerial TEXT,
        deviceMac TEXT,
        deviceName TEXT,
        deviceUrl TEXT,
        deviceTags TEXT,
        deviceModel TEXT,
        alertId TEXT,
        alertType TEXT,
        alertTypeId TEXT,
        alertLevel TEXT,
        occurredAt TEXT,
        alertData TEXT
    )
    ''')
    conn.commit()
    conn.close()

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        payload = request.json

        # Check the shared secret
        if payload.get('sharedSecret') != SHARED_SECRET:
            abort(403)

        conn = sqlite3.connect('/home/admin-az/webhooks/receiver_python/webhooks.db') # CHANGE TO YOUR OWN DIRECTORY
        cursor = conn.cursor()

        cursor.execute('''
        INSERT INTO webhooks (
            version,
            sharedSecret,
            sentAt,
            organizationId,
            organizationName,
            organizationUrl,
            networkId,
            networkName,
            networkUrl,
            networkTags,
            deviceSerial,
            deviceMac,
            deviceName,
            deviceUrl,
            deviceTags,
            deviceModel,
            alertId,
            alertType,
            alertTypeId,
            alertLevel,
            occurredAt,
            alertData
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            payload.get('version'),
            payload.get('sharedSecret'),
            payload.get('sentAt'),
            payload.get('organizationId'),
            payload.get('organizationName'),
            payload.get('organizationUrl'),
            payload.get('networkId'),
            payload.get('networkName'),
            payload.get('networkUrl'),
            json.dumps(payload.get('networkTags', [])),
            payload.get('deviceSerial'),
            payload.get('deviceMac'),
            payload.get('deviceName'),
            payload.get('deviceUrl'),
            json.dumps(payload.get('deviceTags', [])),
            payload.get('deviceModel'),
            payload.get('alertId'),
            payload.get('alertType'),
            payload.get('alertTypeId'),
            payload.get('alertLevel'),
            payload.get('occurredAt'),
            json.dumps(payload.get('alertData'))
        ))

        conn.commit()
        conn.close()

        # Log the received payload
        logging.info(f'Received and stored webhook: {json.dumps(payload)}')

        return '', 200
    else:
        abort(400)

if __name__ == '__main__':
    # Set up logging
    logging.basicConfig(filename='/home/admin-az/webhooks/receiver_python/webhook.log', level=logging.INFO) # CHANGE TO YOUR OWN DIRECTORY

    setup_database()
    context = ('/etc/letsencrypt/live/webhook.zurawek.co.uk/fullchain.pem', '/etc/letsencrypt/live/webhook.zurawek.co.uk/privkey.pem') # CHANGE TO YOUR OWN DIRECTORY
    app.run(host='0.0.0.0', port=9443, ssl_context=context) # CHANGE TO YOUR OWN PORT
