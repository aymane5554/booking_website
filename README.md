a ticketing website where users can create , rate and search events and buy and create tickets.

youtube : https://youtu.be/G-uDlGgryGY?si=shRO1tN3VzLp0x7w

# Views.py 
1. **`index(request)`**:
   - Renders the `index.html` template and passes all events (`Event.objects.all().order_by("-created_at")`) to the template.

2. **`result(request)`**:
   - Handles a GET request to filter events and users based on a search query (`s`). 
   - Filters events with titles containing the search term (`s`) and users with usernames containing the same.
   - Renders the `result.html` template with the filtered events (`events`) and users (`users`).

3. **`profile(request, username)`**:
   - Retrieves a user by `username`.
   - Calculates a rating (`rate`) for the user based on event rankings associated with events the user is linked to (`user.events.all()`).
   - Fetches user bookings (`bookings`) and events (`events`).
   - Renders the `profile.html` template with user-related data (`rate`, `user`, `bookings`, `events`).

4. **`ticket_valid(type, price, number)`**:
   - Checks if ticket information (`type`, `price`, `number`) is valid.
   - Validates that `type` is not empty, and both `price` and `number` are positive integers.

5. **`event_page(request, id)`**:
   - Retrieves an `Event` object by `id`.
   - Computes event details like `percentage` of tickets sold.
   - Manages ticket booking and event rating functionalities based on user authentication.
   - Renders the `event.html` or `fevent.html` template based on event state and user actions.

6. **`is_event_valid(title, description, address, type)`**:
   - Checks if event information (`title`, `description`, `address`, `type`) is valid.
   - Ensures that all fields are non-empty strings.

7. **`create_event_view(request)`**:
   - Manages creation of new events via POST requests.
   - Validates event data (`title`, `description`, `address`, `type`) and creates a new `Event` object if valid.
   - Redirects to the event details page (`/event/{id}`) after successful event creation.

8. **`login_view(request)`**:
   - Handles user authentication and login attempts.
   - Authenticates user credentials (`username`, `password`) and redirects to the index upon successful login.

9. **`logout_view(request)`**:
   - Logs out the authenticated user and redirects to the index page.

10. **`register(request)`**:
    - Manages user registration process.
    - Validates registration data (`username`, `email`, `password`) and creates a new `User` object if valid.
    - Logs in the user after successful registration.

11. **`password()`**:
    - Generates a random password string using ASCII characters, digits, and punctuation.

12. **`booking(request)`**:
    - Handles ticket booking for authenticated users via POST requests.
    - Creates a new `Booking` object for a selected ticket.
    - Calculates ticket selling details (`percentage`, `capacity`, `sold`) after successful booking.

13. **`check(request)`**:
    - Validates a booking by checking the password against the booked ticket's event and user.
    - Updates the booking status (`is_used`) upon successful validation.

Each function is responsible for specific functionalities within this Django application, such as user authentication, event management, booking handling, and template rendering. Some functions also handle validations to ensure data integrity and security.

# Models.py
1. **User**: contains username ,email,password
2. **Event Model**:
   - Represents an event with attributes like `title`, `description`, `address`, `created_at`, `start_at`, `type`, `user`, and `selling`.
   - `title`, `description`, `address`, and `type` are textual fields (`CharField` and `TextField`).
   - `created_at` and `start_at` are `DateTimeField` instances.
   - `user` is a foreign key linking to the `User` model (assuming `from django.contrib.auth.models import User`).
   - `selling` is a boolean field indicating whether the event is available for selling tickets.

   The `serializer()` method in this class is used to serialize the object into a dictionary format suitable for JSON serialization. However, the `capacity` attribute is missing in the serializer method, assuming it might have been intended to be part of the model.

3. **Ticket Model**:
   - Represents a ticket type for an event with attributes like `type`, `price`, `event`, and `number`.
   - `type` is the type of ticket (`CharField`).
   - `price` is the price of the ticket (`IntegerField`).
   - `event` is a foreign key linking to the `Event` model.
   - `number` represents the number of tickets available for this type.

   The `serializer()` method in this class is used to serialize the ticket object into a dictionary format.

4. **Bookings Model**:
   - Represents a booking made by a user for a ticket with attributes `ticket`, `user`, `password`, and `is_used`.
   - `ticket` is a foreign key linking to the `Ticket` model.
   - `user` is a foreign key linking to the `User` model.
   - `password` is a string field to store a password related to the booking.
   - `is_used` is a boolean field indicating whether the booking has been used.

   The `serializer()` method in this class is used to serialize the booking object into a dictionary format.

5. **Rank Model**:
   - Represents a ranking (or rating) given by a user to an event with attributes `user`, `event`, `score`, and `cmnt`.
   - `user` is a foreign key linking to the `User` model.
   - `event` is a foreign key linking to the `Event` model.
   - `score` is an integer field representing the ranking score.
   - `cmnt` is a string field representing a comment related to the ranking.

The `__str__()` method in the `Event` model specifies how instances of the `Event` class should be displayed as a string (in this case, by their `title`).

Overall, these models define a system where users can create events, sell tickets for those events, make bookings for tickets, and rank events with associated comments and scores. The 
`serializer()` methods are used to convert instances of these models into dictionary representations for serialization, such as for API responses or other data interchange formats.

# Webapp pages
* **/login**
* **/register** page where user create signup
* **/** it's the home page diplays events and a search bar to search events and users
* **/Profile** page that displays user's username , event that he created , tickets that he bought , and his rate(sum of events rates / number of events) 
* **/event/<int:id>** if the event date didnt pass users can buy and see event details on this page
  if the date passed users can buy tickets but  if they bought a ticket they can rate the event and leave a comment
* **/new_event** create form event
* **/result** display search result
* **check** every tickets has a id and password(generated with password function in views.py) and boolean field called is_used
  this page check if ticket is valid which means if it's still not used and the password is valid and if the visitor of this page is the creator of the event
  the ticket mark a used
