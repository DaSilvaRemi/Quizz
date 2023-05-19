# UI QUIZ

Front-End of the QUIZ application in Vue JS 3 and Vite

## Project Setup

### Without docker

```sh
npm install
```

```sh
npm run dev
```

The application will be available at
```
http://localhost:3000/
```

### With docker

``` sh
docker image build -t quiz-local-ui .
```

``` sh
docker container run -it --rm -p 3000:80 --name quiz-local-ui quiz-local-ui
```
