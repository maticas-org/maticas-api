# Maticas API

Welcome to the Maticas API repository! This is the database and API branch of the Maticas project. We are using the Django framework for the database and REST technology for the API structure.

##  Getting Started

To get started with the Maticas API, you'll need to follow these steps:

1. Clone this repository to your local machine using git clone https://github.com/maticas-org/maticas-api.git
2. Install Docker and docker-compose on your machine by following the instructions on the official Docker website.
3. Open a terminal and navigate to the root directory of the project.
4. Start the app with docker-compose up. This command will create and start the containers for the API and database services defined in the docker-compose.yml file.
5. Open a web browser and go to http://localhost:8000/. You should see the API homepage.
5. Start making API requests!

Note: If you make changes to the code and want to see them reflected in the running app, simply stop the running containers with docker-compose down and start them again with docker-compose up.

## License

The Maticas API is released under the MIT License. Please see the LICENSE file for more details.
