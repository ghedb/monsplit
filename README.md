

# Splitting a django monolith

This is a demo of how I approached splitting a monolithic django system into microservices.
Its is a very dumbed down version to demo some of the concepts.
Rather than rewriting everything from scratch and then migrate, this makes it possible to keep the old system up to date.
This allows for old integrations to still function while migrations can proceed.

The main idea is that instead of having inter dependencies between apps and database models.
Each service can own their own local model allowing for loose coupling.

Each model should have a "master" service. In this case the monolith still "owns" Product.
The catalog microservice takes ownership of catalog. Each service is unaware of the other.

Each service publishes events to kafka for changes to its public models.
Each service acts on external events based on its own business logic.

Separation of django functionality has also been started, this allows for decoupling logic from django more cleanly.
It will probably make sense to look at alternative API frameworks going forward.




## Data consistency

Event object are created alongside anytime a database object is created/updated.
When working with db transactions it is unsafe to send the event immediately, we must wait for a successful commit.
Otherwise we risk sending an event for a db entry that never got committed.
The event is created with a 'sent' boolean that indicates if it has been processed.

A celery task is ran after commit that will pusblish the event.
If the publish fails, the sent boolean remains false. 
A periodic task can come back and 
reprocess any events that are still unsent. 
This allows for fairly high consistency distributed transactions.




### Trying it out

`docker-compose up`

Note that no volumes are mounted so data is not persistent

docker entrypoint will automatically create an admin user: admin/pass

monolith urls:

http://localhost:8000/admin

http://localhost:8000/api/v1/catalog

http://localhost:8000/api/v1/product

catalog service urls:

http://localhost:8001/catalog/admin

http://localhost:8001/catalog/api/v1


An example of functionality is to create a product in the monolith system (admin)
The event will get created, sent and consumed by the catalog service making it available there within seconds.




### TODO:


* tests
* sample data to import
  * Create sample data
  * Import on startup
* gateway/nginx
    * static files


 
