# StayConnected

**StayConnected** is a dynamic Q&A platform, inspired by Stack Overflow, designed to enable seamless knowledge sharing. It empowers users to ask questions, provide answers, engage with posts, and gain reputation within an active developer community.

---

## Features

- **Authentication and Authorization**: Secure user registration, login, logout, and password reset.
- **Interactive Q&A System**: Create and engage with posts and comments.
- **Reaction System**: Like, dislike, and update reactions on posts and comments.
- **Leaderboard**: Track top contributors.
- **User Profiles**: View user posts, answered questions, and profile information.
- **Tagging System**: Efficiently organize posts with tags for easy categorization.
- **Health Monitoring**: Built-in endpoints for system and database health checks.

---

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/lukagoguadze2/StayConnected.git
   cd StayConnected
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure .env variables:
   ```.env
   SECRET_KEY='SECRET_KEY'
   MYSQL_DB_NAME='MYSQL_DB_NAME'
   MYSQL_ROOT_USER='MYSQL_ROOT_USER'
   MYSQL_ROOT_PASSWORD='MYSQL_ROOT_PASSWORD'
   MYSQL_HOST='MYSQL_HOST'
   MYSQL_PORT=3306
   ALLOWED_HOST='*'
   ```

4. Set up the database:
   ```bash
   python manage.py migrate
   ```

5. Collect static files:
   ```bash
   python manage.py collectstatic
   ```

6. Run the development server:
   ```bash
   python manage.py runserver
   ```

---

## API Endpoints

### **Authentication**
| Endpoint                          | Method | Description                                   |
|-----------------------------------|--------|-----------------------------------------------|
| `/auth/login/`                    | POST   | Log in with an existing account.             |
| `/auth/logout/`                   | POST   | Log out and invalidate tokens.               |
| `/auth/reset-password-request/`   | POST   | Request a password reset via email.          |
| `/auth/reset-password/`           | PUT    | Reset the password.                          |
| `/auth/signup/`                   | POST   | Register a new user account.                 |

### **Health and Database Checks**
| Endpoint                          | Method | Description                                   |
|-----------------------------------|--------|-----------------------------------------------|
| `/check/db-connection/`           | GET    | Check the database connection.               |
| `/check/health/`                  | GET    | Check the application health status.         |

### **Comments**
| Endpoint                          | Method | Description                                   |
|-----------------------------------|--------|-----------------------------------------------|
| `/comments/create/`               | POST   | Create a comment.                            |
| `/comments/{id}/`                 | DELETE | Delete a comment.                            |
| `/comments/{id}/dislike/`         | POST   | Dislike a comment.                           |
| `/comments/{id}/like/`            | POST   | Like a comment.                              |
| `/comments/{id}/mark_correct/`    | PUT    | Mark a comment as the correct answer.        |
| `/comments/{id}/unmark_correct/`  | PUT    | Unmark a correct answer.                     |
| `/comments/{id}/update_reaction/` | PUT    | Update reaction (like ↔ dislike).            |
| `/comments/{id}/remove_reaction/` | DELETE | Remove a reaction.                           |
| `/comments/{post_id}/post`        | GET    | Get comments for a post.                     |

### **Leaderboard**
| Endpoint                          | Method | Description                                   |
|-----------------------------------|--------|-----------------------------------------------|
| `/leaderboard/`                   | GET    | Get the leaderboard of top contributors.     |

### **Posts**
| Endpoint                          | Method | Description                                   |
|-----------------------------------|--------|-----------------------------------------------|
| `/posts/`                         | GET    | Get a list of posts.                         |
| `/posts/create/`                  | POST   | Create a new post (requires authentication). |
| `/posts/filter/`                  | GET    | Filter posts.                                |
| `/posts/{id}/`                    | GET    | Get post details.                            |
| `/posts/{id}/`                    | PUT    | Update a post.                               |
| `/posts/{id}/`                    | DELETE | Delete a post.                               |
| `/posts/{id}/like/`               | POST   | Like a post.                                 |
| `/posts/{id}/dislike/`            | POST   | Dislike a post.                              |
| `/posts/{id}/update_reaction/`    | PUT    | Update reaction (like ↔ dislike).            |
| `/posts/{id}/remove_reaction/`    | DELETE | Remove a reaction.                           |

### **Profiles**
| Endpoint                          | Method | Description                                   |
|-----------------------------------|--------|-----------------------------------------------|
| `/profile/`                       | GET    | Get the user's profile information.          |
| `/profile/answered/`              | GET    | Get posts with correct answers by the user.  |
| `/profile/posts/`                 | GET    | Get the user's posts.                        |

### **Tags**
| Endpoint                          | Method | Description                                   |
|-----------------------------------|--------|-----------------------------------------------|
| `/tags/`                          | GET    | Get all tags.                                |
| `/tags/create/`                   | POST   | Create a new tag.                            |

### **Tokens**
| Endpoint                          | Method | Description                                   |
|-----------------------------------|--------|-----------------------------------------------|
| `/token/refresh/`                 | POST   | Refresh the authentication token.            |

---

## Contributors

1. Back-end: [Luka Goguadze](https://github.com/lukagoguadze2)
2. Back-end: [CodeVnebula](https://github.com/CodeVnebula)
3. Devops: [Saba Dvali](https://gitlab.com/dvali.saba)

## Contributing

Contributions are welcome! To contribute:

1. Fork the repository.
2. Create a new branch for your feature:
   ```bash
   git checkout -b feature-name
   ```
3. Commit and push your changes:
   ```bash
   git commit -m "Add feature"
   git push origin feature-name
   ```
4. Submit a pull request.

