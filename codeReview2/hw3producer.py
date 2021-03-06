#!/home/jiang6/confluent-exercise/bin/python3
# Copyright 2020 Confluent Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

# =============================================================================
#
# Produce messages to Confluent Cloud
# Using Confluent Python Client for Apache Kafka
#
# =============================================================================

from confluent_kafka import Producer, KafkaError
import json
import ccloud_lib
from datetime import date
import logging
import re
import pandas as pd
from bs4 import BeautifulSoup
from urllib.request import urlopen


def get_trip_id(soup):
    tripId = soup.find_all('h3')
    id_list = []
    for everyId in tripId:
        str_tripId = str(everyId)
        clean_tripId = BeautifulSoup(str_tripId, 'lxml').get_text()
        num = re.findall(r'\d+', clean_tripId)
        num = str(num)
        new_str = num[2:-2]
        id_list.append(new_str)

    return id_list

def get_data_from_url():
    url = 'http://rbi.ddns.net/getStopEvents'
    html = urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    tables = soup.find_all('table')

    data = []
    trip_ids = get_trip_id(soup)
    i = 0
    for table in tables:
        trs = table.find_all('tr')
        trip_id = trip_ids[i]
        i += 1
        for tr in trs[1:]:
            element = '{"trip_id":"","direction":"","route_number":"","service_key":""}'
            obj = json.loads(element)
            tds = tr.find_all('td')
            obj['trip_id'] = trip_id
            obj['direction'] = str(tds[4])[4:-5]
            obj['route_number'] = str(tds[3])[4:-5]
            obj['service_key'] = str(tds[5])[4:-5]
            data.append(obj)
    return data

if __name__ == '__main__':

    # Read arguments and configurations and initialize
    args = ccloud_lib.parse_args()
    config_file = args.config_file
    topic = args.topic
    conf = ccloud_lib.read_ccloud_config(config_file)

    # Create Producer instance
    producer = Producer({
        'bootstrap.servers': conf['bootstrap.servers'],
        'sasl.mechanisms': conf['sasl.mechanisms'],
        'security.protocol': conf['security.protocol'],
        'sasl.username': conf['sasl.username'],
        'sasl.password': conf['sasl.password'],
    })

    # Create topic if needed
    ccloud_lib.create_topic(conf, topic)
    delivered_records = 0

    # Optional per-message on_delivery handler (triggered by poll() or flush())
    # when a message has been successfully delivered or
    # permanently failed delivery (after retries).
    def acked(err, msg):
        global delivered_records
        """Delivery report handler called on
        successful or failed delivery of message
        """
        if err is not None:
            logging.info("Failed to deliver message: {}".format(err))
        else:
            delivered_records += 1
            logging.info(
                "Produced record to topic {} partition [{}] @ offset {}" .format(
                    msg.topic(), msg.partition(), msg.offset()))

    data = get_data_from_url()
    print("Total data:")
    print(len(data))
    print("---------------------------------")
    i = 0
    for _ in data:
        i += 1
        if i % 10 == 0:
            print(i)

        record_key = 'stop'
        record_value = json.dumps(_)

        logging.info(
            "Producing record: {}\t{}".format(
                record_key, record_value))
        producer.produce(topic,
                         key=record_key,
                         value=record_value,
                         on_delivery=acked
                         )
        # p.poll() serves delivery reports (on_delivery)
        # from previous produce() calls.
        producer.poll()

    producer.flush()

    print(
        "{} messages were produced to topic {}!".format(
            delivered_records,
            topic))
