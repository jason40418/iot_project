# WebSocket


## Event List
| event                            | namespace | publisher | subscriber | timeout | broadcast | description                                                              |
| -------------------------------- | --------- | --------- | ---------- | ------- | --------- | ------------------------------------------------------------------------ |
| sensor_data_pub_pi               | /pi       | System    | Flask      | 30      | False     | To automate fetch the sensor data and send to Flask server.              |
| sensor_data_pub_client           | /client   | Flask     | Client     | None    | True      | To send realtime sensor data to client.                                  |
| server_clean_pub                 | /pi       | Flask     | System     | None    | True      | To send a force turing off signal to all accessories except the sensors. |
| accessory_status_pub_client      | /client   | Flask     | Client     | None    | True      | To send the accessories status to client.                                |
| LED_status_check_pub_system      | /pi       | Flask     | System     | None    | True      | To emit a signal make the LED report its status.                         |
| LED_status_pub_pi                | /pi       | System    | Flask      | 30      | False     | To recive the status publish to Flask server regularly.                  |
| LED_off_publish_server           | /pi       | Flask     | System     | None    | True      | To send the turning off breahth light signal.                            |
| infrared_status_check_pub_system | /pi       | Flask     | System     | None    | True      | To emit a signal make the infrared sensor report its status.             |
| infrared_status_pub_pi           | /pi       | System    | Flask      | 30      | False     | To recive the status publish to Flask server regularly.                  |
| infrared_off_publish_server      | /pi       | Flask     | System     | None    | True      | To send the turning off infrared sensor signal.                          |
| model_train_pub_pi               | /pi       | System    | Flask      | 30      | False     | To send the model train finish to Server.                                |
| model_train_pub_client           | /client   | Flask     | Client     | None    | True      | To send the model train status to client.                                |
