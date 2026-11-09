Flaw 1:
Routes (delete restaurant) and (creating account)
Flaw 1 [Broken access control](https://top10.owasp.org/2021/A01_2021-Broken_Access_Control/): Deleting restaurants is currently only blocked from the frontend side by hiding the delete button, but nothing on the server side checks it. Thus a sending a simple delete requests to server side still deletes the restaurant.

Fix: Implement server side check if someone is admin or not to block frontend bypass.

Flaw 2 [Cryptographic Failures](https://top10.owasp.org/2021/A02_2021-Cryptographic_Failures/): using outdated sha-1 for hashing with one iteration round. This would allow a hacker to break the password by pure brute force.
Fix: use modern day hashing algorithms like scrypt.


Flaw 3 [ SQL Injection](https://top10.owasp.org/2021/A03_2021-Injection/): Applying text directly sent from a user on the frontend without any kind of processing allows for SQL Injection. This means that the user can try to insert their own SQL commands e.g:
        WHERE name 
        LIKE '%' || """+ search_text+ """|| '%'... <-- If search_text is now :
        "' UNION SELECT (id, username, password, is_admin,NULL, NULL) FROM users--'"
           it would allow the hacker to steal every credential from the database.

Fix: pass the frontend search_text with the ":"-prefix e.g. ":search_text". This binds the search_text for SQLalchemy to use the values as parametrized queries with bind parameters that make them safe by doing the following in SQLAlchemy:  
    t = text("SELECT * FROM users WHERE id=:user_id")
    result = connection.execute(t, {"user_id": 12}).
    SQLAlchemy builds the query without the user input, locks it and then treats the input data as just values to match against. 

        
    