# Резервное копирование с litres. 

Я купил 589 книг с litres.ru. Внезапно мне показалось, что неплохо было-бы сделать резервную копию всех моих накоплений. 

** Это не "бесплатная качалка платных книг". Скачиват только те книги, что есть в разделе "мои книги" на litres.ru **

_Базируется на litres api версии 3.31_

## Что надо для работы

- python
- интернет
- pip install tqdm
- pip install rfc6266

## Как пользоваться

``` bash
./litres-backup.py -u пользователь -p пароль -f ios.epub
```
- -d включить отладку. выводит кучу информации про ответы сайта. 
- -u имя пользователя. То, что вы вводите на сайте или в приложении
- -p пароль. Оно же
- -f формат, в котором забирать книги. Список форматов разный, но для моей коллекции работают следующие 

| -f|примечание|
|fb2.zip|для андроида|
|html||
|html.zip||
|txt||
|txt.zip||
|rtf.zip||
|a4.pdf||
|a6.pdf| для читалок|
|mobi.prc||
|epub||
|ios.epub|для ios|

Скачивает в текущий каталог, никаких проверок класса "есть ли этот фаил" не производится. 

## Что должно получиться

![alt text](https://raw.githubusercontent.com/kiltum/litres-backup/master/screen.png "How it works")

