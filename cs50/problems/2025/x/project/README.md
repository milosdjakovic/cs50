# Quick Note
#### Video Demo:  https://youtu.be/U8hwZpXQfDk
#### Description:
My CS50x final project is a simple web app for note taking.

It includes user account management features like registering the account, logging in, changing username and password, changing security question and answer, account recovery and deletion. Account recovery is basic and for user to recover the account, they need to provide the correct answer to the security question they chose during the registration.

Changing password, username, and security question is done through the profile page.

But password can also be changed through the account recovery page, if the user provides the correct answer to the security question.

Regarding the notes themselves, they support markdown formatting. Notes can be pinned to the top of the list, and unpinned as well. Title and content can be modified for each note and notes can be deleted.

The deletion works with a trash system, where deleted notes are not permanently removed but moved to a trash page. From there, the notes can be permanently deleted or restored back to the main notes list.

For this project I'm using Flask Python framework and SQLite as a database.

All routes and methods on that routes are defined in `app.py`. Some helper methods are stored in files located inside the `lib/` directory like the decorator function to check if the user is logged in used on protected routes inside `helpers.py` and a very basic `Database` class with simple method to handle execution of SQL queries and manage database connections inside `db.py`.

The database itself is located inside the `db/` directory alongside with 2 `.sql` files, one containing database schema and other containing seeds for security questions so that the database can be recreated.

Each time the flask app is run, the `init_db` function in `init_db.py` file which is also located inside the `/db` directory will check if the database file exists, if not it will create the database file, run `schema.sql` to create the tables and `seeds.sql` to insert the security questions.

Regarding the database design, tables `users` and `notes` are pretty straightforward. The `users` table contains the user information, while the `notes` table stores the content of the notes along with their associated user IDs.

The `user_favorite_notes` table holds the id of user and the note the user favorited. The `security_questions` table will store predefined questions for account recovery defined in `db/seeds.sql`. The `user_security_answers` will store the id of the user, the id of the security question the user selected, as well as the value of the answer the user provided.

For storing the security question answers for account recovery, I store the answers as plain text. This is not the best practice, but for this project I wanted to keep it simple. In a real world application, I would probbably use hashing to store the answers securely.

Regarding trash feature. The notes table has a `trashed_at` column of type `DATETIME` which defaults to `NULL`. If the value is not `NULL` the note will be considered trashed and be visible on the `Trash` page, otherwise it will be displayed on the `Notes` page.

To permanently delete the notes, the user needs to delete it from the `Trash` page. This will remove the note from the database.

For User Interface I used Bootstrap, some custom JavaScript to handle few interactions, like trashing and deleting the notes from a Bootstrap modal on view note papge.

The SVG icons are imported using the `include` statement directly in the Jinja templates so that the code is cleaner and easier to read. The SVG icons are stored in the `static/icons` directory.

I reused note form on create and modify pages with the help of Jinja macros and i only pass necessary values. The content form field in this template is text are with monospace font to make it easier to write markdown formatted text. Especially elements like tables.

To render note contents as markdown I found modules `markdown` which helps with translating the markdown syntax to proper HTML elements and `bleach` which is used to sanitize the HTML output. To do this, I defined template filter named `markdown` in `app.py` and I used the filter directly in my templates. In the view page there is also some custom CSS to handle the styles for the rendered markdown. For code blocks in rendered markdown, I didn't include any syntax highlighting to keep it simple.

To get pinned notes I join the `notes` and `user_favorite_notes` on user id field. And to get the notes, I select all notes and than check if the id of the note is not present in the `user_favorite_notes` table. So I could render the pinned notes first.
