#encoding: utf-8
from config import Config
from selector.atreader import AtRealtimeReader
import logging
import pika
import at.task_pb2


class ConnectorAT(object):
    def __init__(self):
        self.connection = None
        self.channel = None
        self.at_realtime_reader = None
        self._init_logger()
        self.config = Config()

    def init(self, filename):
        """
        initialise le service via le fichier de conf passer en paramétre
        """
        self.config.load(filename)
        self.at_realtime_reader = AtRealtimeReader(self.config)
        self._init_rabbitmq()

    def _init_logger(self, filename='', level='debug'):
        """
        initialise le logger, par défaut level=Debug
        et affichage sur la sortie standard
        """
        level = getattr(logging, level.upper(), logging.DEBUG)
        logging.basicConfig(filename=filename, level=level)

        if level == logging.DEBUG:
            #on active les logs de sqlalchemy si on est en debug:
            #log des requetes et des resultats
            logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)
            logging.getLogger('sqlalchemy.pool').setLevel(logging.DEBUG)
            logging.getLogger('sqlalchemy.dialects.postgresql') \
                .setLevel(logging.INFO)

    def _init_rabbitmq(self):
        """
        initialise les queue rabbitmq
        """
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=self.config.rabbitmq_host,
            port=self.config.rabbitmq_port,
            virtual_host=self.config.rabbitmq_vhost,
            credentials=pika.credentials.PlainCredentials(
                self.config.rabbitmq_username, self.config.rabbitmq_password)
        ))
        self.channel = self.connection.channel()
        exchange_name = self.config.exchange_name
        self.channel.exchange_declare(exchange=exchange_name, type='topic',
                                      durable=True)

    def run(self):
        self.at_realtime_reader.execute()
        logging.getLogger('connector').info("put message to following topics: "
                                            "%s", self.config.rt_topics)
        for message in self.at_realtime_reader.message_list:
            task = at.task_pb2.Task()
            task.action = 1
            task.message.MergeFrom(message)
            for routing_key in self.config.rt_topics:
                exchange_name = self.config.exchange_name
                self.channel.basic_publish(exchange=exchange_name,
                                           routing_key=routing_key,
                                           body=task.SerializeToString())