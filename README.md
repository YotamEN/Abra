[![Build Status](https://travis-ci.org/YotamEN/abra.svg?branch=master)](https://travis-ci.org/github/YotamEN/abra)
[![codecov](https://codecov.io/gh/YotamEN/abra/branch/master/graph/badge.svg)](https://codecov.io/gh/YotamEN/abra)

# Abra: Advanced System Design course project (Tel Aviv University)

This project assumes you have the following installed on your device:
* **docker, docker-compose** 

At this point the only DB and MessageQueue supported:
* **Postgres** (DB)
* **Rabbitmq** (MQ)

## Installation

1. Clone the repository:

    ```console
    $ git clone https://github.com/YotamEN/abra.git
    $ cd abra/
    ```

2. Install:

    ```console
    $ ./scripts/run-pipeline.sh
    [abra] $
    ```
   
   or 
   
   ```console
    $ ./scripts/install.sh
    $ source .env/bin/activate
    [abra] $
    ```
   

## Interfaces

**1. Client** - send mind samples to the server

```python
python API:

>>> from abra.client import upload_sample
>>> upload_sample(host='127.0.0.1', port=8000, path='sample.mind.gzip')
```
```bash
CLI:

$ python -m abra.client upload-sample   \
      -h/--host '127.0.0.1'             \
      -p/--port 8000                    \
      'snapshot.mind.gz'
```

**2. Server** - receive mind samples (snapshots) and forward to parsers via message queue OR 
activates a function on the received samples if "publish" is a callable function
   
```python
python API:

>>> from abra.server import run_server
>>> run_server(host='127.0.0.1', port=8000, publish="rabbitmq://127.0.0.1:5672")
>>> run_server(host='127.0.0.1', port=8000, publish=print)
```
```bash
CLI:

$ python -m abra.server run-server \
      -h/--host '127.0.0.1'          \
      -p/--port 8000                 \
      'rabbitmq://127.0.0.1:5672/'
```
**3. Parsers** - parses snapshot in to usable data such as images, numbers, etc.

    Avaliable parsers:
        * pose
        * color-image
        * depth-image
        * feelings
```python
python API:

>>> parser = 'pose'
>>> data_path = '../some_path/snapshot.raw'

>>> from abra.parsers import parse
>>> parse(parser=parser, data_path=data_path)
```
```bash
CLI:

# to parse raw data and save the result:
$ python -m abra.parsers parse 'pose' 'snapshot.raw' > 'pose.result'

# to run a parser consuming from a publisher:
$ python -m abra.parsers run-parser 'pose' 'rabbitmq://127.0.0.1:5672/'
```
```
In order for you to add your own parser, follow the following steps:
    1. Go to abra/parsers.
    2. Give it a name! add it's name as a string to the list 'PARSER_NAMES' located in "parsers.py".
    3. Create a class in the marked section in "parsers.py", look for the "CREATE YOUR OWN PARSER" zone.
        (If you really want to write it in a new file instead, that's ok.. just make sure to import it in __init__.py
        and put your file in the "parsers" directory)
    3. Inherit from BaseParser and override the "parse" method.
            The "parse" method must be implemented as follows:
            :input:  a Snapshot object as defined in abra.proto
            :output: a dict object with the parsed fields - 
                keys to be set according to the "field names" described in "common.py" file
                + a key and value for the parser name
                + a key and value for datetime
            If your parser saves data to disk - override the "write" method to be implemented as follows:
            :input: path
            :output: full path to saved file
    4. You're good to go!
```

**4. Saver** - saves parsed sata to Database
```python
python API:

>>> db_url = 'postgresql://127.0.0.1:5432'
>>> mq_url = 'rabbitmq://127.0.0.1:5672'
>>> topic = 'pose'
>>> data_path = '/data/pose.result'

>>> from abra.saver import run_saver
>>> run_saver(db_url=db_url, mq_url=mq_url)

>>> from abra.saver import Saver
>>> saver = Saver(db_url)
>>> saver.save(topic=topic, data=data_path)
```
```bash
CLI:

# to save one result to the database
$ python -m abra.saver save                       \
      -d/--database 'postgresql://127.0.0.1:5432' \
     'pose'                                       \
     'pose.result'

# to run the saver to consume from all parsers and saves all results to the DB
$ python -m abra.saver run-saver  \
      'postgresql://127.0.0.1:5432' \
      'rabbitmq://127.0.0.1:5672/'

```

**5. API** - abra's RestAPI.

```python
python API:

>>> from abra.api import run_server
>>> run_server(host='127.0.0.1', port=5000, database='postgresql://127.0.0.1:5432')
```
```bash
CLI:

$ python -m abra.api run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 5000              \
      -d/--database 'postgresql://127.0.0.1:5432'
```
RestfulAPI:
* **`GET /users`**

        returns a jsonified list of users
    
* **`GET /users/<user_id>`**

        returns json of user information:
            * user.id
            * user.name
            * user.birthday
            * user.gender
    
* **`GET /users/<user_id>/snapshots`**

        returns a jsonified list of snapshots
    
* **`GET /users/<user_id>/snapshots/<snapshot_id>`**

        returns a json holding the available results, current result types:
            * pose
            * color-image
            * depth-image
            * feelings
    
* **`GET /users/<user_id>/snapshots/<user_id>/<result_name>`**

        returns a json holding:
            * relevant data to be presented to user 
            * result_url to image if result is not "pose"
        

**6. CLI**

The following command-line commands are supported:
```bash

    $ python -m abra.cli get-users
    
    $ python -m abra.cli get-user <user-id> 
    
    $ python -m abra.cli get-snapshots <user-id> 
    
    $ python -m abra.cli get-snapshot <user-id> <snapshot_id>
    
    $ python -m abra.cli get-result <user-id> <snapshot_id> <result_type>
```
  

**7. GUI** - abra's GUI.

NOTICE: The GUI only works if the API server is up!

```python
python API:

>>> from abra.gui import run_server
>>> run_server(host='127.0.0.1', port=8080, api_host='127.0.0.1', api_port=5000)
```
```bash
CLI:

$ python -m abra.gui run-server \
      -h/--host '127.0.0.1'       \
      -p/--port 8080              \
      -H/--api-host '127.0.0.1'   \
      -P/--api-port 5000
```
  
## Website


    Default host = 0.0.0.0
    Default port = 8080
            
    Go to 0.0.0.0:8080 and enjoy!


## Testing

Run tests:
```bash
[abra] $ pytest tests/
```


## Reset

After running abra through docker, use this to reset volumes and data:
```bash
[abra] $ ./scripts/reset.sh
```