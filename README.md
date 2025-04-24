# Inventory &amp; Purchase Order Workflow

A complete setup for a Django REST API service using Docker Compose, including PostgreSQL database to create and Inventry management

## Table of Contents
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)


## Prerequisites
- Docker (version 20.10.0+)
- Docker Compose (version 1.27.0+)

## Setup
```
git clone https://github.com/mdahaduzzaman/pos-django.git
```

Change directory to pos-django
```
cd pos-django
```
## Running the Application
```
docker compose up -d
```
It will run the application on [localhost](http://localhost)

You'll be see the basic html template showing the list of Pending and Completed Purchase Order (PO)

You already have a default user. Here is the credential

### Username
```
admin
```
### Password
```
admin
```

You'll be see all the data from this admin panel

## API Endpoints

Create two users: one regular user and another user with the group "manager".

Now click the [swagger](http://localhost/swagger/) to see the all API endpoints.

Create some suppliers and products from [admin panel](http://localhost/admin)

Then, copy some product IDs and a supplier ID and try to create a Purchase Order.

You can find a sample JSON in the swagger documentation. Authenticate the regular user with their username and password and try to create a Purchase Order. Copy the created ID and try to approve it. You will receive an error response indicating that you do not have the necessary permissions. Try the same approval request with the manager user; you will be able to approve it. After approval, you will be able to use the receive endpoint to receive the products.
