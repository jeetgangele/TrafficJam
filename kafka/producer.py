# Kafka producer that reads the input data in a loop in order to simulate real time events
from kafka import KafkaClient
from kafka.producer import SimpleProducer
import time
import progressbar
import glob
import sys
import datetime

#kafka = KafkaClient("54.175.15.242:9092")
kafka = KafkaClient("localhost:9092")


class Printer():
    """
    Print things to stdout on one line dynamically
    """
    def __init__(self, data):
        sys.stdout.write(data.__str__() + "\r")
        sys.stdout.flush()


def send_message(topic):
    producer = SimpleProducer(kafka)
    bksize = 500  # bulk size
    while True:
        csvfiles = sorted(glob.glob("/home/ubuntu/*.csv"))    # get all data files
        for csv in csvfiles:
            #nol = sum(1 for line in open(csv))
            #bar = progressbar.ProgressBar(maxval=nol,
                    #widgets=[progressbar.Bar('=', '[', ']'), ' ',
                    #progressbar.Percentage()])
            c = 0
            ifile = open(csv)
            msg_bulk = []
            #bar.start()
            for line in ifile:
                msg_bulk.append(line)
                if len(msg_bulk) >= bksize:
                    _send_bulk(producer, topic, msg_bulk)
                    #bar.update(c + 1)
                    c += bksize
                    msg_bulk = []
                    # Creating some delay to allow proper rendering of the locations on the map
                    time.sleep(1)
            #bar.finish()
            #print "File " + csv + " completed!"
            dt = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            Printer("File " + csv + " completed at " + dt)
            sys.stdout.flush()
            ifile.close()


def _send_bulk(producer, topic, msg_bulk):
    producer.send_messages(topic, *msg_bulk)

send_message("traffic_info")
