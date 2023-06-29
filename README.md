Math Master
Math Master is a Flask web application developed by Caleb Rebar. It is a simple app that allows users to practice math problems and earn points to redeem for titles displayed on a leaderboard.

Installation
To run the Math Master app locally, follow these steps:

Clone the repository: git clone https://github.com/cmrebar/solo_project
Navigate to the project directory: cd math-master
Install the dependencies: pip install [package](Check requirements.txt for dependencies) 
## Database Setup

1. Install MySQL: If you don't have MySQL installed, download and install it from the official MySQL website (https://dev.mysql.com/downloads/).

2. Start MySQL Server: Start the MySQL server on your local machine. Refer to the documentation or instructions specific to your operating system for details on starting the MySQL server.

3. Connect to MySQL: Connect to the MySQL server using a MySQL client such as MySQL Workbench, phpMyAdmin, or the MySQL command-line client.

4. Create Database: Create a new database for your Math Master application. Choose a suitable name for the database.

5. Use Database: Use the newly created database. This will ensure that any subsequent operations are performed within the context of this database.

6. Table Creation: Execute the following SQL query to create the 'users' table with the specified columns:

```sql
CREATE TABLE users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(255) NOT NULL,
  last_name VARCHAR(255) NOT NULL,
  email VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  tracked_points INT DEFAULT 0,
  hidden_points INT DEFAULT 0,
  milestones VARCHAR(255),
  title VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
```

This query will create the 'users' table with the defined column names, data types, and constraints.

7. Verify Table Creation: You can verify that the 'users' table was created successfully by running the following query:

```sql
DESCRIBE users;
```

This query will display the table structure, including the column names, data types, and other attributes.

With these instructions, users can set up the MySQL database and create the necessary 'users' table to use with your Math Master application. Be sure to provide any additional details or considerations that may be specific to your project's database configuration or usage.

## Running the App

1. Prerequisites: Ensure that you have Python and pip installed on your machine.

2. Install Pipenv: If you don't have Pipenv installed, run the following command to install it globally:

   ```
   pip install pipenv
   ```

3. Install Dependencies: Navigate to the project directory in your terminal and run the following command to install the project dependencies specified in the `Pipfile`:

   ```
   pipenv install
   ```

4. Activate Virtual Environment: Activate the project's virtual environment by running the following command:

   ```
   pipenv shell
   ```

   This will activate the virtual environment and allow you to run the app with the installed dependencies.

5. Start the Server: Once you are in the virtual environment, run the following command to start the Flask server:

   ```
   python server.py
   ```

   This command will launch the Flask app and start the server.

6. Access the App: Open your web browser and visit `http://localhost:5000` to access the Math Master app.

   Note: If you need to use a different port, you can modify the `server.py` file to specify a different port number.

With these instructions, users can set up and run your Math Master Flask app on their local machines. Make sure to provide any additional details or considerations specific to your app's configuration or requirements.

## Usage

Once you have the app running, follow these steps to use Math Master:

1. Open your web browser and go to `http://localhost:5000`.
2. You will be greeted with the Math Master dashboard.
3. The dashboard is organized by math topics separated by grade.
4. Click on a topic to navigate to the problems page for that topic.
5. On the problems page, a math problem will be randomly generated.
6. Solve the problem and click the submit button.
7. If your answer is correct, you will earn 1 point.
8. Accumulate points to redeem for titles displayed on the leaderboard.

## Contributing

Math Master is an open-source project, and contributions are welcome! If you would like to contribute to the project, please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b my-new-feature`
3. Make your changes and test thoroughly.
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push the branch to your forked repository: `git push origin my-new-feature`
6. Submit a pull request detailing your changes.

Please make sure to follow the code style and conventions used in the project.

License
This project is licensed under the MIT License.

Contact
If you have any questions, suggestions, or feedback regarding Math Master, please feel free to reach out to Caleb Rebar at cmrebar1715@gmail.com.

Thank you for using Math Master and happy problem-solving!
