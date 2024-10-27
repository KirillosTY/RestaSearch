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

## Getting Started

### Prerequisites
1. **Python 3** - Make sure Python 3 is installed on your system.
2. **PostgreSQL** - Install PostgreSQL and ensure you have access to it.

### Steps

1. **Clone this repository**  
   Download or clone this repository to your computer.

2. **Create an `.env` file**  
   Inside the `pythonFlaskBackend` folder, create a file named `.env` and add the following:
   ```env
   SQL_ALCHEMY_DBURL="Insert your local PostgreSQL address here"
   SECRET="Insert a proper hex token here"
   ```

3. **Set up the Python environment**
   - Open a command-line interface in the `pythonFlaskBackend` folder and run:
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     pip install -r requirements.txt
     ```

4. **Initialize the Database**
   - Run the following command to create the necessary tables and initial schema:
     ```bash
     psql < schemas/Start.sql
     ```
   - Then, access PostgreSQL:
     ```bash
     psql
     ```
   - Once inside PostgreSQL, run the following command to insert an admin user:
     ```sql
     INSERT INTO users (username, password, is_admin) VALUES ('admin', 'admin1K', true);
     ```

5. **Start the Application**
   - Start the Flask server with:
     ```bash
     flask run
     ```

### Login Information
- **Admin Account**  
  You can log in using:
  - **Username**: `admin`
  - **Password**: `admin1K`

- **Create a User Account**  
  Alternatively, you can create a new user account with default privileges.
