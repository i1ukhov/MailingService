## Стэк используемых технологий
Frontend: HTML, CSS, Bootstrap, JavaScript

Backend: Python, Django, PostgreSQL, Git, Docker, Redis, Django-apscheduler


## Сервис для email-рассылок
![coursework main page](https://github.com/i1ukhov/DjangoCoursework/assets/96483139/dd587dd7-6b88-4a60-aac7-da79e4e50034)

### Запуск:
1. Переименуйте файл .env.sample в .env и заполните необходимые данные
2. Запустите Redis: sudo service redis-server start; redis-cli
3. Запустите проект

### Работа с командами рассылки из командой строки:
1. Запуск проверки периодических рассылок - python manage.py start_schedule_mailing
   Запускает проверку необходимости отправки рассылок, отправляет активные рассылки
2. Мгновенный запуск рассылки - python manage.py permanent_mailing
   В терминале отобразится список рассылок и программа попросит выбрать нужную рассылку, указав номер
   ![django_permanent_mailing_demo](https://github.com/i1ukhov/DjangoCoursework/assets/96483139/fadb44fc-a8df-49d3-9b03-5eb53d7ba727)
   Результат:
   
   ![django_permanent_mailing_demo_result](https://github.com/i1ukhov/DjangoCoursework/assets/96483139/1bab9319-28fc-45df-8a7c-b2b0fc230aa1)

### Особенности работы менеджера рассылок
Менеджер может деактивировать рассылку, нажав "Редактировать" на нужной рассылке и сняв чекбокс, нажать кнопку "Изменить":
![moderator blocks newsletter](https://github.com/i1ukhov/DjangoCoursework/assets/96483139/212f1ee9-e738-47bb-aa5b-771708f36cc4)
Рассылка без этого чекбокса не будет отправлена, несмотря на статус рассылки
