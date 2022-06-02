import logging
import logging.handlers

# Создаем объект Logger и устанавливаем уровень важности
SERVER_LOG = logging.getLogger('server_mess')
SERVER_LOG.setLevel(logging.DEBUG)

# Создаем Formatter, в сообщение будет указано время, уровень важности, имя модуля, сообщение и номер строки
log_format = logging.Formatter("%(asctime) - 5s %(levelname) - 10s module: %(module) - 5s message: %(message)s line № %(lineno)d")

# Создаем обработчик, устанавливаем его уровень важности и форматтер
handler = logging.handlers.TimedRotatingFileHandler('log/server.log', when='midnight', interval=1, encoding='utf-8')
handler.setLevel(logging.DEBUG)
handler.setFormatter(log_format)

# Подключаем обработчик к логеру
SERVER_LOG.addHandler(handler)
