# WebSocket


## Event List
| event                  | namespace | publisher | subscriber | timeout | broadcast | description                                                 |
| ---------------------- | --------- | --------- | ---------- | ------- | --------- | ----------------------------------------------------------- |
| sensor_data_pub_pi     | /pi       | System    | Flask      | 30      | False     | To automate fetch the sensor data and send to Flask server. |
| sensor_data_pub_client | /client   | Flask     | Client     | None    | True      | To send realtime sensor data to client.                     |
