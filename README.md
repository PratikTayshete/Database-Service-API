# Database-Service-API
Implementing REST API as a service to access a mongodb database

In this API:

  - A User registers with username and password 
  - A User logs in with username and password

<b>User Register Functionalities</b>:

  - A user can register with username(unique) and password.
  - The username and password fields are required.
  - Each user should have unique username.
  - With successful registration, each user get default 10 chances(coins) to log in into their account

<b>User Log In Functionalities</b>:

  - A user can log in with it's username and password.
  - The username and password fields are required.
  - Access denied if both or either username and password are incorrect.
  - With each successful Log In, 1 chance(1 coin) from the total chances(coins) is reduced.
  - A user with it's username and password won't be allowed to log in after the total chances(coins) are zero.

<b>Prerequisites</b>:
 
  - Install Docker and Docker-Compose
    
    https://docs.docker.com/install/linux/docker-ce/ubuntu/

    https://docs.docker.com/docker-for-windows/install/

    https://docs.docker.com/compose/install/
 
<b> Run </b>:

    [Inside the parent directory]
    
    sudo docker-compose build
    
    sudo docker-compose up
 
 NOTE: You can use Postman to test the REST-API [https://www.getpostman.com/]
