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
