# Frontend

## Docker setup
From frontend folder use this commands
```
docker build -t vuejs-cookbook/dockerize-vuejs-app .
```
```
docker run -it -p 8080:8080 --rm --name dockerize-vuejs-app-1 vuejs-cookbook/dockerize-vuejs-app
```

## Project setup
```
npm install
```

### Compiles and hot-reloads for development
```
npm run serve
```

### Compiles and minifies for production
```
npm run build
```

### Lints and fixes files
```
npm run lint
```

### Customize configuration
See [Configuration Reference](https://cli.vuejs.org/config/).

## TODO

- refactor FE for better code style []
- add .env vars []
- validation for asset adding []
- token validation [x]