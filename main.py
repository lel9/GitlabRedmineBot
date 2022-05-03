from redminelib import Redmine
from flask import Flask, request
import json
from model import on_event
import configparser


try:
  # загружаем настройки
  config = configparser.ConfigParser()  # создаём объекта парсера
  config.read('settings.ini')  # читаем конфиг

  if 'Redmine' not in config:
    raise AttributeError('Redmine config not found')
  if 'redmine_host' not in config['Redmine']:
    raise AttributeError('redmine_host not found')
  if 'redmine_key' not in config['Redmine']:
    raise AttributeError('redmine_key not found')
  
  # загружаем переходы по статусам
  path_to_sts = 'sts.json'
  if 'Statuses' in config:
    if 'path_to_sts' in config['Statuses']:
        path_to_sts = config['Statuses']['path_to_sts']
  with open(path_to_sts) as file:
      sts_settings = json.load(file)

  # порт где запустимся
  port = 8000
  if 'App' in config:
    if 'port' in config['App']:
      port = int(config['App']['port'])
      
except json.JSONDecodeError as je:
  print ('JSON (statuses) error: ')
  print (je)
  exit(1)
except AttributeError as ae:
  print ('Config error: ')
  print (ae)
  exit(1)
except Exception as e:
  print('Unknown error')
  print(e)
  exit(1)

# запускаем сервер
app = Flask(__name__)


@app.route('/',methods=['POST'])
def foo():
   data = json.loads(request.data)
   redmine = Redmine(config['Redmine']['redmine_host'],  
                     key = config['Redmine']['redmine_key'])
   on_event(data, redmine, sts_settings)
   return "OK"


if __name__ == '__main__':
  app.run(port = port)
  
