# AutoProxy with ADSL VPS

```
/
|- opt
    |- autoproxy
        |- server.py
        |- client.py
        \- func.py
```

## Server
- Parameters
    ```
    NEED_AUTH = True
    AUTH_USER = user
    AUTH_PASSWD = passwd
    PORT = port
    ```
- Usages

| Auth | URL                                     | Return              |
|:---  | :---                                    | :--                 |
| No   | http://host:5000/status/                | True / False        |
| No   | http://host:5000/status/?act=change     | Done (Set True)     |
| No   | http://host:5000/status/?act=receive    | Done (Set False)    |
| Yes  | http://host:5000/proxy/                 | ip:port             |
| Yes  | http://host:5000/proxy/?act=set         | Done (Set ip:port)  | 

## Client
- Rent an ADSL VPS
- Parameters
    ```
    AUTH = (user, passwd)
    HOST = host
    ```
- Run: `python3 /opt/autoproxy/client.py`


## Function
- Change status & take new proxy from server
- Usage: `new_proxy = get_new_proxy()`


## Others
- Supervisord conf: `autoproxy.ini`
    ```
    # Autoproxy
    [program:autoproxy]
    command=/usr/local/bin/python3 /opt/autoproxy/server.py
    #command=/usr/local/bin/python3 /opt/autoproxy/client.py
    user=root
    autostart=false
    autorestart=true
    startsecs=10
    startretries=10
    redirect_stderr=true
    stderr_logfile=/var/log/supervisor/autoproxy.stderr.log
    stdout_logfile=/var/log/supervisor/autoproxy.stdout.log
    ```

## Ref
- [GitHub: Germey/AutoProxy](https://github.com/Germey/AutoProxy)