** First simple Flask API - Bookstore **

- People can sell a book to the store (API receives JSON and only stores it in memory).

- Anyone can list what’s currently in the store (API returns JSON list).

- People can purchase a book by id (API checks if it exists then removes it then returns ok/not found).

- Includes a separate script that auto-feeds 100 random books into the API using HTTP requests.

- Some constraints as it's the first one I make: no database, so data lives only in RAM. If Flask is restarted, the inventory resets.

