# Intro
Front end using ViteJS + ReactJS + ReactQuery + Zustand + Tailwind ...
A rough UI design, which i actually really spend some time, borrowed some ideas and template
## Install Dependencies
`yarn install`

## Run
`yarn run dev`
## After backend API change
you need generate the openapi code again: 
- download opanapi from http://localhost:8080/api/docs
- replace openapi.json
`npx  openapi -i ./openapi.json -o src/generated --client axios`

there is miltipal choiced other than axios, the generated code is quite abstract high level.
go https://github.com/ferdikoomen/openapi-typescript-codegen to learn more.

## After backend URL change
please modify .env accordingly

