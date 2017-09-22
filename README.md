# Резервное копирование с litres.

Я купил 500+ книг с litres.ru. Внезапно мне показалось, что неплохо было-бы сделать резервную копию всех моих накоплений.

**Это не "бесплатная качалка платных книг". Скачивает только те книги, что есть в разделе "мои книги" на litres.ru**

_Базируется на litres api версии 3.31_

## Что надо для работы

- python
- интернет
- pip install tqdm
- pip install rfc6266

## Как пользоваться

```
$ ./litres-backup.py -h
usage: litres-backup.py [-h] [-u USER] [-p PASSWORD] [-f FORMAT] [-d] [-v]

litres.ru backup tool

optional arguments:
  -h, --help            show this help message and exit
  -u USER, --user USER  Username
  -p PASSWORD, --password PASSWORD
                        Password
  -f FORMAT, --format FORMAT
                        Downloading format. 'list' for available
  -d, --debug           Add debug output
  -v, --verbosedebug    You really want to see what happens?
```

Скачивает в текущий каталог, никаких проверок класса "есть ли этот фаил" не производится. Докачек и прочего тоже пока не предусмотрено.

## Что должно получиться

![alt text](https://raw.githubusercontent.com/kiltum/litres-backup/master/screen.png "How it works")

## Баги/хотелки

- Максимум качает 1000 первых книг.
- Надо сделать "скачать только эту книгу/полку"


