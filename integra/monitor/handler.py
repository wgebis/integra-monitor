import socketserver
import crcmod.predefined
import smtplib
from email.mime.text import MIMEText
import time
import datetime as dt
from integra.monitor.dict import dict_helpers as dh
from elasticsearch import Elasticsearch
from integra.monitor.payload import *
from flask import Flask
from integra.monitor.dict.slow import Event


class IntegraTCPServer(socketserver.TCPServer):
    def __init__(self, server_address, RequestHandlerClass, bind_and_activate=True, app: Flask=None, slow=None):
        self.slow = slow
        self.app = app

        if 'ES_URL' in self.app.config:
            self.es = Elasticsearch([self.app.config['ES_URL']])

        super().__init__(server_address, RequestHandlerClass, bind_and_activate)

    app: Flask = None
    slow = None
    es: Elasticsearch = None


class IntegraTCPHandler(socketserver.BaseRequestHandler):

    _end = b'\x0d'
    _start = b'\x0a'

    def handle(self):

        data = self.request.recv(1024)

        self.server.app.logger.debug('Received payload "%s"' % data)

        if self._end in data:

            message = IntegraMessage(data[data.find(self._start) + 1:data.find(self._end)])

            if message.payload:

                event: Event = self.get_slow_item(message)

                self.server.app.logger.info('acct_numer={0}, q={1}, xyz={2}, ss={3}, ccc={4}, type="{5}", ind="{6}" desc="{7}"' \
                      .format(message.payload.acct_number,
                              message.payload.q,
                              message.payload.xyz,
                              message.payload.ss,
                              message.payload.ccc,
                              event.k_desc,
                              dh.format_s_field(event.s, message.payload.ccc, message.payload.ss),
                              event.desc))

                if self.server.es:
                    self.send_es(message, event)

                if IntegraTCPHandler.is_email_required(event):
                    self.send_email(message, event)

            self.send_ack(message)

    def send_ack(self, message: IntegraMessage):
        ans = b'"ACK"' + message.header.seq + message.header.lprev + b'#' + message.header.acct + b'[]'

        crc16 = crcmod.predefined.Crc('crc16')
        crc16.update(ans)
        to_send = bytearray(crc16.hexdigest(), "utf-8") + bytearray(hex(len(ans))[2:].rjust(4, "0"), "utf-8") + ans
        self.request.sendall(self._start + to_send + self._end)

    def send_es(self, message: IntegraMessage, event: Event):

        print(IntegraTCPHandler.format_datetime_with_utc(message.header.ts))

        doc = {
            'acct': message.payload.acct_number.decode("utf-8"),
            'q': message.payload.q,
            'xyz': message.payload.xyz,
            'ss': message.payload.ss,
            'ccc': message.payload.ccc,
            'type': event.k_desc,
            'ind': dh.format_s_field(event.s, message.payload.ccc, message.payload.ss),
            'desc': event.desc,
            'timestamp': IntegraTCPHandler.format_datetime_with_utc(message.header.ts),
        }

        try:
            self.server.es.index(index="integra", doc_type='integra_event', body=doc)
        except Exception as e:
            self.server.app.logger.error("An error during sending massages to ES: " + e)

    @staticmethod
    def is_email_required(stype):
        return stype.s == 'A' or stype.s == 'F' or stype.s == 'N'

    def send_email(self, message: IntegraMessage, event: Event):

        if 'TO_EMAIL' in self.server.app.config:
            msg = MIMEText('Kod zdarzenia: "{0} {1}"\nTyp zdarzenia: "{2}"\nOpis zdarzenia: "{3}"\nInformacja dodatkowa: "{4}"'
                           .format(message.payload.q, message.payload.xyz, event.k_desc, event.desc, dh.format_s_field(event.k, message.payload.ccc, message.payload.ss)))
            msg['Subject'] = 'ALARM'
            msg['From'] = 'Konary310 Integra<fax@kancelaria-gebis.pl>'
            msg['To'] = self.server.app.config["TO_EMAIL"]

            s = smtplib.SMTP_SSL('poczta.webserwer.pl', 465)
            s.set_debuglevel(5)

            try:
                s.ehlo()
                s.login('fax@kancelaria-gebis.pl','xxxxxx')
                s.sendmail(msg['From'], msg['To'], msg.as_string())
            except Exception as e:
                self.server.app.logger.error("An error during email sending accures: " + e)
            finally:
                s.quit()
        else:
            self.server.app.logger.debug("Email recipient doesn't configure")

    def get_slow_item(self, message: IntegraMessage):
        return self.server.slow[message.payload.xyz][message.payload.q]

    @staticmethod
    def format_datetime_with_utc(date):
        return date.replace(tzinfo=dt.timezone.utc).isoformat()
