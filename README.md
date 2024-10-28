# mini-twitter-project
This project is a simple Twitter-based API. This Django API provides endpoints for user registration/authentication, following/unfollowing users, and creating/liking/unliking posts.

## **Instalation guide**
To start this project locally, follow the steps below:

- 1 - Create a **.env** file in the backend directory. This file contains essential properties required to run the project. An example file, **env-example.txt**, is available in the same directory with all the necessary properties for executing the project.
- 2 - Inside the backend directory run **docker-compose up --build** to start the project
- 3 - Make requests to the local URL following the API documentation (e.g localhost:8000, http://127.0.0.1:8000)
  
## **Important links**:
### Production url: https://mini-twitter-3do9.onrender.com
### **API documentation Postman:** The Api documantation can be accessed in the follow link:https://documenter.getpostman.com/view/36902945/2sAY4sjja7
![image](https://github.com/user-attachments/assets/a003327b-99b6-4459-a4fe-3f0d70512b91)

## **About:**
### entity-relationship diagram (ERD)
The project includes Users and Posts as its primary entities.
![eer](https://github.com/user-attachments/assets/a2199ae6-f69d-4ea6-868e-00307b34ecbe)

## **Use cases:**
CASE 1: User Registration
- Users should be able to sign up via the API by providing an email, username, and password.
  - Steps: user registration with api/user/register/
- Use JWT to handle authentication for login and session management.
  - Steps: Login with api/token to get access token. Then pass the access token to the requests with bearer auth. 

CASE 2: Post Creation
- Authenticated users can create a post with text and one image as content
  - Steps: Create posts using api/post/
- Posts can be liked by other users.
  - Steps: Like/unlike posts with api/post/like/<post_ld>/

CASE 3: Follow/Unfollow User
- Users should be able to follow or unfollow others.
  - Steps: follow/unfollow users with api/user/follow/<user_id>/
- The feed should only show posts from users the authenticated user follows.
  - Steps: List posts feed with api/post/

CASE 4: Viewing Feed
- The user can view a paginated list of posts from the users they follow.
  - Steps: List posts feed with api/post/?page=1
- Posts should be ordered by creation time, from most recent to oldest.
  - Steps: List posts feed with api/post/ to see the ordering 
