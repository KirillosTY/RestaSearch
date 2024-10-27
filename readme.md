### This is a practice project for a course.

# RestaSearch
This application is meant to allow users to create,review and search restauraunts with some minor additional features.


## Documentation


[Functional requirements](pythonFlaskBackend/documentation/FunctionalRequirements.md)


## Basic info and functionalities explained
There are 2 types of users: Basic and Admin.
Basic users can create restaurant requests. Requests can be viewed on a separate page and can be accepted as official by an admin.
Basic users can review restaurants and them as favourites. Favourite restaurants are shown in a separate list.
Basic users can also delete their own reviews.

Admin users have all of the above and extra: 
Admin created restaurants are automatically added to the official list and they can approve user created restaurants. 
Admins can create other admin accounts.
Admins can remove restaurants or reviews from any user account.

## Getting started
    1. Make sure you have Python3 installed.
    2. Make sure you have PostreSQL installed and access to it.
    3. Download this repository to your computer.
    4. Create a file named .env into the pythonFlaskBackend folder and insert the following:
       ``` SQL_AlCHEMY_DBURL = "Insert here your local PSQL address"
            SECRET = "Insert here a proper hex_token "
    ```
    
    5. Open a cli in the python pythonFlaskBackend folder an run:
        1. ```python3 -m venv venv```
        2.  ```source venv/bin/activate```
        3. ```pip install -r ./requirements.txt```
        4. ```psql < schemas/Start.sql```
        5. ```psql``` and run the following line:
            ```INSERT INTO users (username,password,is_admin) VALUES ('admin','admin1K',true);```
        6.```flask run```
        7. You can login with the admin account with: admin as username and admin1K as password or create a default user account

   
