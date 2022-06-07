import logging
import logging.handlers

CLIENT_LOG = logging.getLogger('client_mess')
CLIENT_LOG.setLevel(logging.DEBUG)

log_format = logging.Formatter("%(asctime) - 5s %(levelname) - 10s module: %(module) - 5s message: %(message)s line № %(lineno)d")

handler = logging.handlers.TimedRotatingFileHandler('log/client.log', when='D', interval=1, encoding='utf-8')
handler.setLevel(logging.DEBUG)
handler.setFormatter(log_format)

CLIENT_LOG.addHandler(handler)