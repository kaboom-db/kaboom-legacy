## Developer Guidelines

Before creating your client, you must read through these simple rules and guidelines:
1. When testing API requests please use the staging server available here: https://staging-kaboom.herokuapp.com/v1. This will allow data uploads and supplies a test user for requests that need a user to be logged in. The [Postman Collection]() also includes the users accesstoken.
2. Do not abuse the API. The current rate limit is 60 requests per 60 seconds.
3. Do not post test data to the production server.

For ease, there is a pre-made [Postman collection]() available for use that utilises the staging server and a demo accesstoken.

This document was published on Sunday 30th, 2022.

## Client Guidelines

If you are a client developer you must credit Kaboom. For GUI applications, please include the Kaboom logo in the about section of your application. You can find high quality logos in the [brand assets](https://github.com/kaboom-db/kaboom-api/tree/master/brand%20assets) folder. If it's a TUI/CLI application, include something like `Developed with Kaboom` as part as the help or about command.