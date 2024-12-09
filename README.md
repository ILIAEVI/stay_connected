# Stay Connected API

### The project on the main branch is ready for deployment. It includes all the necessary configurations for a production environment.

## Features

### Posts
- **Create, Read, Update, Delete (CRUD)** operations for posts.
- Filter posts with `django-filter`.
- Permissions:
  - Only post owners can modify or delete their posts.
  - Read-only access for anonymous users.

### Answers
- **CRUD operations** for answers related to posts.
- Mark an answer as accepted for a post (post owner only).
- Vote on answers (like/dislike) by authenticated users.
- Permissions:
  - Post owners or answer authors can modify or delete their answers.
  - Read-only access for anonymous users.

### User Authentication
- **Signup**: Create an account and verify via email.
- **Login**: Obtain JWT tokens for authenticated access.
- **Logout**: Invalidate refresh tokens.
- **Password Reset**: Request and confirm password reset via email.
- **Profile Management**: View and update user profiles.

### Leaderboard
- Displays the top 10 users ranked by their scores based on accepted answers.

### Celery Task
- Periodically calculates and updates user scores based on the number of accepted answers.


## Endpoints

### Post Endpoints
- `GET api/forum/posts/`: List all posts (supports filtering).
- `POST api/forum/posts/`: Create a new post (authenticated users only).
- `GET api/forum/posts/<id>/`: Retrieve a specific post.
- `PATCH api/forum/posts/<id>/`: Update a post (post owner only).
- `DELETE api/forum/posts/<id>/`: Delete a post (post owner only).

### Answer Endpoints
- `GET api/forum/posts/<post_id>/answers/`: List all answers for a post.
- `POST api/forum/posts/<post_id>/answers/`: Add an answer to a post.
- `PATCH api/forum/posts/<post_id>/answers/<id>/`: Update an answer (author only).
- `DELETE api/forum/posts/<post_id>/answers/<id>/`: Delete an answer (author or post owner only).
- `PATCH api/forum/posts/<post_id>/answers/<id>/mark-answer/`: Mark an answer as accepted.
- `PATCH api/forum/posts/<post_id>/answers/vote_answer/`: Vote on an answer.


### User Endpoints
- `POST api/auth/signup/`: Register a new user.
- `GET api/auth/verify_email/<token>/`: Verify email after registration.
- `POST api/auth/login/`: Authenticate and retrieve tokens.
- `POST api/auth/refresh_token/`: Refresh JWT tokens.
- `POST api/auth/logout/`: Logout and blacklist tokens.
- `POST api/auth/password-reset/`: Request a password reset.
- `POST api/auth/password-reset-confirm/`: Confirm a password reset.
- `GET api/auth/profile/`: Retrieve the logged-in user's profile.
- `PATCH api/auth/profile/`: Update the logged-in user's profile.
- `GET api/auth/profiles/`: Retrieve the all user's profile.
- `GET api/auth/leaderboard/`: View the top 10 users by score.
