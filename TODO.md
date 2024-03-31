# Features and Requirements Engineering

The goal of the app is to provide an API for a simple chatbot API.
To keep things simple, this will sort of wrap LLM api like the Openai or Anthropic one with any bells and whistle added.

- [X] Users shall be able to start conversations with a chatbot
- [X] Users shall be able to send messages to a conversation and receive a reply
- [X] Users shall be able to execute standard CRUD on their conversations
- [X] Users shall be able to edit the system prompt of a conversation at any time
- [X] Users shall be able to create and save system prompts
- [X] Users shall be restricted to only seeing the resources that belong to them, except for specific all-to-see resources
- [ ] Users shall be able to create notes that the LLM can reference during conversations
  
Some of the learning questions I want to answer:

- [X] How to customise the primary key to be a cuid2?
  - How to do this for the default classes like users or groups?
    - [X] user
    - [ ] groups -> same as user
- [X] How to add created_at and updated_at to all models?
- [X] How to run django ORM from a lambda?
- [X] How to manage background jobs via AWS Lambda and SQS?
- [X] How to have social auth?
- [X] How to have more granular or advanced type of permissions?
- [X] Write a production docker for Django?
- [ ] How to integrate the API with a frontend?
- [X] How to add logging?
  - [ ] BONUS POINT: OTel integration
- [ ] How to use Django or DRF filters?
- [X] How to leverage nested routes?
- [/] How to add caching using Momento?
- [X] How to use environment variables?
- [X] How to restrict actions to the owner of an object?
- [X] How to ensure the user id is carried properly when requests are sent?

## Features

- [X] On user created a default system prompt shall be added to their account.

## Bugs

- [X] DJ-REST-AUTH registration clashes with camelCase JSON formatter on the fields password1 and password2. See: [StackOverflow discussion](https://stackoverflow.com/questions/63768825/get-this-field-is-required-in-django-auth-registration)
    Changing settings doesnt work
    Bug was caused by issue with ORJSON. Disabling orjson fixes it. Might need PR to owners to resolve.
