# python-memcached-dump
Export data from memcache server,just for backup data<br />
For help
```python
[root@localhost~]# python memcached-dump.py --help
usage: memcached-dump.py [-h] [--host HOST] [--port PORT] [--path PATH]

optional arguments:
  -h, --help   show this help message and exit
  --host HOST  memcached server host,default[127.0.0.1]
  --port PORT  memcached server port,default[11211]
  --path PATH  File path,default[/tmp/memcached.json]
  ```
  Export data
  ```python
  [root@localhost]# python memcached-dump.py --path /tmp/memcached.json
  ```
