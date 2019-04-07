

# Splitting the django monolith

This is a demo of how I approached splitting a monolithic django system into microservices.
Its is a very dumbed down version to demo some of the concepts.
Rather than rewriting everything from scratch and then migrate, this makes it possible to keep the old system up to date.
This allows for old integrations to still function while migrations can proceed.

The main idea is that instead of having inter dependencies between apps and database models.
Each service can own their own local model allowing for loose coupling.

Each model should have a "master" service. In this case the monolith still "owns" Product.
The catalog microservice takes ownership of catalog.

Each service publishes events for changes to its public models.
Each service acts on external events based on its own business logic.

Separation of django functionality has also been started, this allows for decoupling logic from django more cleanly.
It will probably make sense to look at alternative API frameworks going forward.






To run a local rabbitmq for celery

docker run  --hostname my-rabbit -p 15672:15672 -p 5672:5672 rabbitmq:3-management 