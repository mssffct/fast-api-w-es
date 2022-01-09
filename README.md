# fast-api-w-es
tiny web service for saving and organizing text pieces and searching among already saved results
#### Created on base of [FastAPI](https://fastapi.tiangolo.com/)
#### For search and store operation [ElasticSearch](https://www.elastic.co/elasticsearch/) is used.
## installation:
#### Clone repository as usual
#### In order to create containers for api use:
`$ docker-compose build`
#### To start them up use:
`$ docker-compose up`
## Getting started:
:rocket: main script-file will run automatically after the start of the app container 
## Usage: 
- The app container will be running on ***localhost:80***
- Use ***/docs*** to see progect's documentation and to try out application scope
## Searching:
- There are four modes to search: 
    - Search text pieces on definite page of the definite document:
      - specify search option as ***definite*** and point out document's name and page number
    - Search by text piece type among all the documents:
      - specify search option as ***by_type*** and choose which type of text piece you want to find
    - Search by text sample closely similar text pieces:
      - specify search option as ***similar*** and type in text sample you want to find
    - Mixed search:
      - there are two ways with different parameters specified:
          - you can search in definite document by text piece type:  
            specify search option as ***mixed*** and choose text piece type you want
          - also search text sample in definite document by text piece type awailable:  
            specify search option as ***mixed*** and choose text piece type you want and type in text sample
          
