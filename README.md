# Auto buying stickers Standoff 2

## Описание

Эта программа автоматически покупает скины с наклейками в игре Standoff 2 за кратчайшее возможное время.
Также можно выставить цену, ниже которой надо будет купить лот (необязательно с наклейками).

! Эта программа не встраивается в код Standoff 2 и никак его не модифицирует. Скрипт работает как человек,
только в разы быстрее. Поэтому бан за это получить нельзя.

## Пример работы

https://github.com/user-attachments/assets/9b67b882-5149-426a-8515-064c9b2af197

## Требования

- Операционная система Windows 10/11 (другие не тестировались)
- ~15гб свободного дискового пространства на диске C
- Разрешение монитора 1920x1080 (иначе сами разбирайтесь в коде и настраивайте координаты обнаружения наклеек)
- Эмулятор LdPlayer 9 (другие не тестировались)
- Много времени и терпения

## Установка

1. Установите Python версии ~3.11.9. При установке **НЕ** забудьте поставить галочку напротив "Add to PATH"
2. [Скачайте](https://github.com/Leo-Proger/Auto-buying-stickers-Standoff-2/archive/refs/heads/master.zip) исходный код
   этого репозитория и распакуйте архив
3. Установите библиотеки для работы программы
    1. В консоли перейдите в папку с кодом
    2. Выполните `pip install -r requirements.txt`
4. Установите Cuda ([этот](https://github.com/chrismeunier/OpenCV-CUDA-installation) гайд в помощь)
    1. В интернете проблематично найти Visual Studio именно 2019
       года. [Вот](https://github.com/user-attachments/files/18280278/vs_Community.zip) ссылка на нее, чтобы вы не
       тратили время на поиски
5. Установите Pytesseract

## Запуск

1. В настройках эмулятора выставите: ширина - 1280, высота - 960, dpi - 240
2. Растяните окно эмулятора на весь экран (кнопка между тире и крестиком)
3. Запустите main.py

Чтобы проверить правильно ли определены координаты, запустите файл `test_sticker_detection.py`.

Если у вас другое разрешение экрана, то вам придется менять координаты наклеек (в переменной STICKER_BBOX класса
Config).

## Известные баги и ограничения

- Если медленный интернет, при 2 стикерах и более может случайно купить лот, когда обновляет список лотов (полосу
  загрузки может принять за стикер)
- Не работает со скинами с паттернами
- Функция покупки лотов ниже определенной цены работает нестабильно

## Контакты

- Telegram - [Leo Proger](https://t.me/Leo_Proger)
