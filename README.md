# qr-code-gen
![](https://badgen.net/badge/python/3.9/green)
![](https://badgen.net/badge/docker/compose?icon=docker)
![](https://badgen.net/badge/flask/2.2.2/yellow)

qr-code-gene is a simple web app for generating Qr-Codes written in Python with the flask Framework

## Installation

Make shure [docker](https://docs.docker.com/get-docker "Docker Docs") and [docker-compose](https://docs.docker.com/compose/install/ "Docker-Compose Docs") is installed  
Clone the Repository and start the stack

```bash
docker-compose up -d
```

You can now acces the web-app via

```
http://hostname:5432
```

If you plann on making the Application publicly available I recommend running behind a proxy, since the connection wont be secured otherwise

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License
[MIT](https://choosealicense.com/licenses/mit/)
