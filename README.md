# HCleander

HCleander is a simple bot to clean messages to and from some annoying bots.

### Installation
HCleander requires Python 3 to run.

  - Get API ID and API HASH on the site https://my.telegram.org/
  - Install the dependencies
  - Create configuration file `config.py` based on example `config/config_example.py`
  - Start the service
  
```sh
$ git clone https://github.com/FreeFox/hcleaner_python.git
$ cd hcleaner_python
$ pip3 install -r requirements.txt
$ cp config/config_example.py config/config.py
$ nano config/config.py
$ python3 main.py
```

### Docker Compose

```sh
$ cp .env.example .env
$ nano .env  # fill in API_ID and API_HASH
```

First run — interactive authorization (Telethon will ask for your phone number and confirmation code):
```sh
$ docker compose run --rm hcleaner
```

Once authorized, `Cleaner.session` is saved locally. Start as a background service:
```sh
$ docker compose up -d
```

License
----

MIT
