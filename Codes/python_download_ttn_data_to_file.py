# %% -----------------------------------Header-----------------------------------------------------
__title__ = "TTN-DATA TO FILE"
__version__ = "2.1"
__description__ = "Download Temperature and Humidity values from TTN over MQTT and save them into csv-file (set save_values=True)"
__author__ = "Freddy Jeufack Fotsop"
print("\n", "##"*25, "\n\t\t", __title__, "\n\t\t Version:", __version__, "\n\tAuthor:", __author__, "\n", "##"*25, "\n")

# %% -----------------------------Imports ----------------------------------------------------------
import paho.mqtt.client as mqtt # pip install paho-mqtt
import json
import csv

# ---------------------------------------Variables----------------------------------------------
save_values = True
csv_name = "air_quality.csv" 
data = []

# ---------------------------------------Functions----------------------------------------------
def to_csv(timestamp, temp, hum):
    with open(csv_name, 'a') as myfile:
        wr = csv.writer(myfile)
        wr.writerow([timestamp, temp, hum])

# The callback for when the client receives a CONNECT response from the server.
def on_connect(client, userdata, flags, rc):
    print('Connected to TTN with result code '+str(rc), "\nWaiting for data transmission to server...") # code 0 =successful connection
    client.subscribe('v3/app-ma-jf@ttn/devices/dev-ma-jeuf-final/up')
 
# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    ergebnis = json.loads(msg.payload)
    values = ergebnis['uplink_message']['decoded_payload']
    ts = ergebnis['received_at'].replace('T', ' ')
    ts = ts[ : ts.find('.')]
    t = values['temperature']
    h = values['humidity']
    print("{} GMT \t Temperature: {} \t Humidity: {}".format(ts, t, h))
    
    # Save as csv
    if save_values:
        to_csv(ts, t, h)

# -------------------------------Main Function---------------------------------------------
def main():
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.tls_set()
    client.username_pw_set('app-ma-jf@ttn', password='*******************************************************')
    client.connect('eu1.cloud.thethings.network', 8883, 60)

    if save_values:
        print(("Saving values to csv"))
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        exit(0)
    
# %% ------------------------------------Run--------------------------------------------
if __name__ == "__main__":
    main()