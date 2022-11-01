# 오라클클라우드-장고

- [http://141.147.169.203:8080](http://141.147.169.203:8080/) for poll
- [http://141.147.169.203:8000](http://141.147.169.203:8000/) for viewer
- [http://141.147.169.203:8080/admin](http://141.147.169.203:8080/admin) for db editing

# Forked From
https://github.com/devmahmud/Django-Poll-App

# Installation

- pip설치
- 장고설치

- 포트열기
    
    ```
    iptables -P INPUT ACCEPT
    iptables -P OUTPUT ACCEPT
    iptables -P FORWARD ACCEPT
    iptables -F
    ```

- Git clone

- Migrate the database

    ```
    python manage.py makemigrations
    python manage.py migrate
    ```

- Create Superuser

    ```
    python manage.py createsuperuser
    ```

- [settings.py](http://settings.py) 에서 
ALLOWED_HOSTS = ['*']

- 서버시작
    
    ```jsx
    python manage.py runserver 0:8000
    ```
    
-  Add class and choices for each classes from 0 to 10 at admin site

- Run Flask viewer
    
    ```jsx
    cd db_viewer_flask
    python app.py
    ```
    
- Make service

   ```
   sudo nano /etc/systemd/system/vote_system.service
   sudo nano /etc/systemd/system/vote_viewer.service

   sudo systemctl daemon-reload
   sudo systemctl enable vote_system.service
   sudo systemctl enable vote_viewer.service
   sudo systemctl start vote_system.service
   sudo systemctl start vote_viewer.service
   ```
