from flask import Flask, render_template
import sqlite3
import json
from datetime import datetime

app = Flask(__name__)

@app.route('/webhooks', methods=['GET'])
def display_webhooks():
    conn = sqlite3.connect('/home/admin-az/webhooks/receiver_python/webhooks.db') ### MAKE SURE TO CHANGE TO YOUR OWN DIRECTORY
    cursor = conn.cursor()

    cursor.execute('SELECT * FROM webhooks')
    data = cursor.fetchall()

    print(data)  # Debug print statement

    # Convert the tuples into a list of dictionaries representing each webhook
    webhooks = []
    for row in data:
        # Parse the date-time string and format it for 'sentAt'
        dt_sent = datetime.strptime(row[3], "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_sent_at = dt_sent.strftime("%Y-%m-%d %H:%M:%S")

        # Parse the date-time string and format it for 'occurredAt'
        dt_occurred = datetime.strptime(row[21], "%Y-%m-%dT%H:%M:%S.%fZ")
        formatted_occurred_at = dt_occurred.strftime("%Y-%m-%d %H:%M:%S")

        webhooks.append({
            "id": row[0],
            "version": row[1],
            "sharedSecret": row[2],
            "sentAt": formatted_sent_at,
            "organizationId": row[4],
            "organizationName": row[5],
            "organizationUrl": row[6],
            "networkId": row[7],
            "networkName": row[8],
            "networkUrl": row[9],
            "networkTags": json.loads(row[10]),
            "deviceSerial": row[11],
            "deviceMac": row[12],
            "deviceName": row[13],
            "deviceUrl": row[14],
            "deviceTags": json.loads(row[15]),
            "deviceModel": row[16],
            "alertId": row[17],
            "alertType": row[18],
            "alertTypeId": row[19],
            "alertLevel": row[20],
            "occurredAt": formatted_occurred_at,
            "alertData": json.loads(row[22]),
        })

    return render_template('webhooks.html', webhooks=webhooks)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)  # adjust the host and port as needed
