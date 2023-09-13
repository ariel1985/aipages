# Rasa Info

## Basic run

```bash
cd ./rasabot # folder rasa was installed

python -m rasa run --enable-api --cors "*"

python -m rasa shell --debug

```

## Run with actions: 

```bash

cd ./rasabot # folder rasa was installed

rasa run actions
```
Actions will run on a seperate process/server:

```mermaid
graph LR
    User-->|Message| RasaCore
    RasaCore-->|Action| RasaActions
    RasaActions-->|Response| User
```

This is the flow chart

```mermaid
sequenceDiagram
    participant User
    participant RasaCore as Rasa Core Server
    participant RasaActions as Rasa Action Server

    User->>RasaCore: Sends a message
    RasaCore->>RasaCore: Processes message and decides next action
    RasaCore->>RasaActions: Requests custom action execution (if needed)
    RasaActions->>RasaActions: Executes custom action
    RasaActions->>RasaCore: Sends back the result
    RasaCore->>User: Responds to user based on action result
```


## Remove models 

P.S we may need to version the dataset

(rasa cli)[https://rasa.com/docs/rasa/command-line-interface]

rasa visualize to see the chatflow




