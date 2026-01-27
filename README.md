# gnv-django-realworld

## API Examples

### Authentication APIs

#### Create user
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"user":{"username":"gnv","email":"gnv@gmail.com","password":"12345678"}}' \
  http://localhost:8000/api/users

curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"user":{"username":"jake","email":"jake@gmail.com","password":"12345678"}}' \
  http://localhost:8000/api/users
```

#### Login
```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"user":{"email":"gnv@gmail.com","password":"12345678"}}' \
  http://localhost:8000/api/users/login
```

#### Get Current User
```bash
# Login và lưu token vào biến
TOKEN=$(curl -s -X POST \
  -H "Content-Type: application/json" \
  -d '{"user":{"email":"gnv@gmail.com","password":"12345678"}}' \
  http://localhost:8000/api/users/login | jq -r '.user.token')

# Get current user với token đó
curl -X GET \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  http://localhost:8000/api/user
```

#### Update User
```bash
# Update user bio and image
curl -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"user":{"bio":"I work at State Farm","image":"https://i.stack.imgur.com/xHWG8.jpg"}}' \
  http://localhost:8000/api/user

# Update email
curl -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"user":{"email":"newemail@gmail.com"}}' \
  http://localhost:8000/api/user

# Update password
curl -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"user":{"password":"newpassword123"}}' \
  http://localhost:8000/api/user
```

### Profile APIs

#### Get Profile
```bash
# Get profile without authentication (following = false)
curl -X GET \
  http://localhost:8000/api/profiles/gnv/

# Get profile with authentication (shows real following status)
curl -X GET \
  -H "Authorization: Bearer ${TOKEN}" \
  http://localhost:8000/api/profiles/gnv/
```

**Response:**
```json
{
  "profile": {
    "username": "gnv",
    "bio": "I work at State Farm",
    "image": "https://i.stack.imgur.com/xHWG8.jpg",
    "following": false
  }
}
```

#### Follow User
```bash
# Follow a user (authentication required)
curl -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  http://localhost:8000/api/profiles/jake/follow/
```

**Response:**
```json
{
  "profile": {
    "username": "jake",
    "bio": "I work at Jake Farm",
    "image": "https://api.realworld.io/images/demo-avatar.png",
    "following": true
  }
}
```

#### Unfollow User
```bash
# Unfollow a user (authentication required)
curl -X DELETE \
  -H "Authorization: Bearer ${TOKEN}" \
  http://localhost:8000/api/profiles/jake/follow/
```

**Response:**
```json
{
  "profile": {
    "username": "jake",
    "bio": "I work at Jake Farm",
    "image": "https://api.realworld.io/images/demo-avatar.png",
    "following": false
  }
}
```

### Tags APIs

#### Get Tags
```bash
# Get all tags (no authentication required)
curl -X GET \
  http://localhost:8000/api/tags/
```

**Response:**
```json
{
  "tags": ["reactjs", "angularjs", "dragons"]
}
```

#### Create Tag
```bash
# Create a new tag (authentication required)
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"tag":{"name":"reactjs"}}' \
  http://localhost:8000/api/tags/
```

**Response:**
```json
{
  "tag": {
    "name": "reactjs"
  }
}
```

### Articles APIs

#### List Articles
```bash
# Get all articles (no authentication required)
curl -X GET \
  http://localhost:8000/api/articles/

# Filter by tag
curl -X GET \
  "http://localhost:8000/api/articles/?tag=dragons"

# Filter by author
curl -X GET \
  "http://localhost:8000/api/articles/?author=jake"

# Filter by favorited by user
curl -X GET \
  "http://localhost:8000/api/articles/?favorited=gnv"

# Pagination with limit and offset
curl -X GET \
  "http://localhost:8000/api/articles/?limit=10&offset=0"

# Combine filters and pagination
curl -X GET \
  "http://localhost:8000/api/articles/?tag=dragons&author=jake&limit=20&offset=0"
```

**Query Parameters:**
- `tag`: Filter by tag name
- `author`: Filter by author username
- `favorited`: Filter by username who favorited
- `limit`: Number of articles to return (default: 20, max: 100)
- `offset`: Number of articles to skip (default: 0)

**Response:**
```json
{
  "articles": [
    {
      "slug": "how-to-train-your-dragon",
      "title": "How to train your dragon",
      "description": "Ever wonder how?",
      "body": "It takes a Jacobian",
      "tagList": ["dragons", "training"],
      "createdAt": "2024-01-09T12:00:00.000Z",
      "updatedAt": "2024-01-09T12:00:00.000Z",
      "favorited": false,
      "favoritesCount": 0,
      "author": {
        "username": "jake",
        "bio": "I work at statefarm",
        "image": "https://i.stack.imgur.com/xHWG8.jpg",
        "following": false
      }
    }
  ],
  "articlesCount": 1
}
```

#### Get Article
```bash
# Get single article by slug (no authentication required)
curl -X GET \
  http://localhost:8000/api/articles/how-to-train-your-dragon/
```

**Response:**
```json
{
  "article": {
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "createdAt": "2024-01-09T12:00:00.000Z",
    "updatedAt": "2024-01-09T12:00:00.000Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }
}
```

#### Create Article
```bash
# Create new article (authentication required)
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"article":{"title":"How to train your dragon","description":"Ever wonder how?","body":"It takes a Jacobian","tagList":["dragons","training"]}}' \
  http://localhost:8000/api/articles/
```

**Response:**
```json
{
  "article": {
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "createdAt": "2024-01-09T12:00:00.000Z",
    "updatedAt": "2024-01-09T12:00:00.000Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "gnv",
      "bio": "I love Django",
      "image": "https://example.com/avatar.jpg",
      "following": false
    }
  }
}
```

#### Update Article
```bash
# Update article (authentication required, only author can update)
curl -X PUT \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"article":{"title":"Did you train your dragon?","description":"So, it works!"}}' \
  http://localhost:8000/api/articles/how-to-train-your-dragon/
```

**Response:**
```json
{
  "article": {
    "slug": "how-to-train-your-dragon",
    "title": "Did you train your dragon?",
    "description": "So, it works!",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "createdAt": "2024-01-09T12:00:00.000Z",
    "updatedAt": "2024-01-09T12:30:00.000Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "gnv",
      "bio": "I love Django",
      "image": "https://example.com/avatar.jpg",
      "following": false
    }
  }
}
```

#### Delete Article
```bash
# Delete article (authentication required, only author can delete)
curl -X DELETE \
  -H "Authorization: Bearer ${TOKEN}" \
  http://localhost:8000/api/articles/how-to-train-your-dragon/
```

**Response:** `204 No Content`

#### Favorite Article
```bash
# Favorite an article (authentication required)
curl -X POST \
  -H "Authorization: Bearer ${TOKEN}" \
  http://localhost:8000/api/articles/how-to-train-your-dragon/favorite/
```

**Response:**
```json
{
  "article": {
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "createdAt": "2024-01-09T12:00:00.000Z",
    "updatedAt": "2024-01-09T12:00:00.000Z",
    "favorited": true,
    "favoritesCount": 1,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }
}
```

#### Unfavorite Article
```bash
# Unfavorite an article (authentication required)
curl -X DELETE \
  -H "Authorization: Bearer ${TOKEN}" \
  http://localhost:8000/api/articles/how-to-train-your-dragon/favorite/
```

**Response:**
```json
{
  "article": {
    "slug": "how-to-train-your-dragon",
    "title": "How to train your dragon",
    "description": "Ever wonder how?",
    "body": "It takes a Jacobian",
    "tagList": ["dragons", "training"],
    "createdAt": "2024-01-09T12:00:00.000Z",
    "updatedAt": "2024-01-09T12:00:00.000Z",
    "favorited": false,
    "favoritesCount": 0,
    "author": {
      "username": "jake",
      "bio": "I work at statefarm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }
}
```

### Comment APIs

#### Get Comments for Article
```bash
# Get all comments for an article (no authentication required)
curl -X GET \
  http://localhost:8000/api/articles/how-to-train-your-dragon/comments/
```

**Response:**
```json
{
  "comments": [
    {
      "id": 1,
      "body": "It takes a Jacobian",
      "createdAt": "2024-01-09T12:00:00.000Z",
      "updatedAt": "2024-01-09T12:00:00.000Z",
      "author": {
        "username": "jake",
        "bio": "I work at statefarm",
        "image": "https://i.stack.imgur.com/xHWG8.jpg",
        "following": false
      }
    }
  ]
}
```

#### Add Comment to Article
```bash
# Add a comment to an article (authentication required)
curl -X POST \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${TOKEN}" \
  -d '{"comment":{"body":"Thank you so much!"}}' \
  http://localhost:8000/api/articles/how-to-train-your-dragon/comments/
```

**Response:**
```json
{
  "comment": {
    "id": 1,
    "body": "Thank you so much!",
    "createdAt": "2024-01-09T12:00:00.000Z",
    "updatedAt": "2024-01-09T12:00:00.000Z",
    "author": {
      "username": "gnv",
      "bio": "I work at State Farm",
      "image": "https://i.stack.imgur.com/xHWG8.jpg",
      "following": false
    }
  }
}
```

#### Delete Comment
```bash
# Delete a comment (authentication required, must be comment author)
curl -X DELETE \
  -H "Authorization: Bearer ${TOKEN}" \
  http://localhost:8000/api/articles/how-to-train-your-dragon/comments/1/
```

**Response:** `204 No Content`
