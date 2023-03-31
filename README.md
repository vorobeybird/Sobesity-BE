# Sobesity

## Start the application:
To run the app:
```
make run
```

API Documentation: <a href="http://localhost:5150/openapi/" target="_blank">http://localhost:5150/openapi/</a>

## Useful dev commands
To build the app:
```
make build
```

Run migration
```
make migrate
```

Create migration
```
make create-migration message='create skill table'
```

## Pull of updates
The app support code reload. When you change python code in most cases it will be reloaded automatically.
But OpenAPI generation doesn't support code reload. So when you pull updates from the git it's recommended to reload 
the app. To do this run next command:
```
make restart-app
```

## Install library

For example how to install `alembic` as library.
```
make add-lib lib="alembic"
```

## How to debug the app
Set `breakpoint()` in particular place then run the command. It will stop the app and rerun it with attached tty
```
make debug-app
```


## How to generate JWT token
Open [jwt.io](jwt.io). In `payload` set `iat`("Issue at") to your current time in unix style [(human time to unix)](https://www.epochconverter.com/).
Then set `exp`("Expiration time") to time when you what to expire. For example after a week and set date in unix style.
