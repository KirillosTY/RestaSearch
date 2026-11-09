Flaw 1:
Routes (delete restaurant) and (creating account)
Flaw [Broken access control](https://top10.owasp.org/2021/A01_2021-Broken_Access_Control/): Deleting restaurants is currently only blocked from the frontend side by hiding the delete button, but nothing on the server side checks it. Thus a sending a simple delete requests to server side still deletes the restaurant.

Fix: Implement server side check if someone is admin or not to block frontend bypass.

