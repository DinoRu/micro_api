import random
from string import ascii_lowercase
from typing import List, Dict, Optional
from uuid import UUID

import uvicorn
from bcrypt import checkpw, hashpw, gensalt
from fastapi import FastAPI

app = FastAPI(title="Micro_api")

#Global variables
valid_users = dict()
valid_profiles = dict()
pending_users = dict()
discussion_posts = dict()
request_headers = dict()
cookies = dict()


@app.get("/index")
async def index() -> dict:
    return {"message": "Welcome FastApi nerds"}


@app.get("/login")
async def login(username: str, password: str) -> dict:
    if valid_users.get(username) is None:
        return {"message": "User doesn't exists"}
    else:
        user = valid_users.get(username)
        if checkpw(password.encode(), user.passphrase.encode()):
            return user
        else:
            return {"message": "Password invalid"}


@app.get("/login/details/info")
async def login_info() -> dict:
    return {"message": "Username and password are needed"}


@app.delete("/login/remove/all")
async def delete_users(usernames: List[str]) -> dict:
    for username in usernames:
        del valid_users[username]
        return {"message": "delete users"}


@app.delete("/delete/users/pending")
async def delete_pending_users(accounts: List[str] = []):
    for user in accounts:
        del delete_users[user]
    return {"message": "deleting pending users"}


@app.get("/login/password/change")
async def change_password(username: str, old_password: str = "Strong password ", new_password: str= " ") -> dict:
    password_len = 8
    if valid_users[username] is None:
        return {"message": "user does not exist"}
    elif old_password == '' and new_password == '':
        characters = ascii_lowercase
        temp_password = "".join(random.choice(characters) for i in range(password_len))
        user = valid_users[username]
        user.password = temp_password
        user.passphrase = hashpw(temp_password.encode(), gensalt())
        return user
    else:
        user = valid_users[username]
        if user.password == old_password:
            user.password = new_password
            user.passphrase = hashpw(new_password.encode(), gensalt())
            return user
        else:
            return {"message": "user does not exist"}
        

@app.post("/login/username/unlock")
async def unlock_username(id: Optional[UUID] = None):
    if id is None:
        return {"message": "token is needed"}
    else:
        for k, v in valid_users.items():
            if v.id == id:
                return {"username": v.username}
        return {"message": "user does not exist"}

@app.post("/login/password/unlock")
async def unlock_password(username: Optional[str] = None, id: Optional[UUID] = None) -> dict:
    if username is None:
        return {"message": "username is required"}
    elif valid_users.get(username) is None:
        return {"message": "user does not exist"}
    else:
        if id is None:
            return {"message": "token needed"}
        else:
            user = valid_users.get(username)
            if user.id == id:
                return {"password": user.password}
            else:
                return {"message": "Invalid token"}


@app.patch("/account/profile/names/update/{username}")
async def update_profile_names(username: str, new_name: Dict[str, str], id: UUID):
    if new_name is None:
        return {"message": "New name is required"}
    elif valid_users.get(username) is None:
        return {"message": "user does not exists!"}
    else:
        user = valid_users.get(username)
        if user.id == id:
            profile = valid_profiles[username]
            profile.firstname = new_name['fname']
            profile.lastname = new_name['lname']
            profile.middle_initial = new_name['mi']
            valid_profiles[username] = profile
            return {"message": "successfully updated"}
        else:
            return {"message": "user doe not exist"}


@app.delete("/login/remove/{username}")
async def delete_user(username: str) -> dict:
    if username is None:
        return {"message": "Invalid user"}
    else:
        del valid_users[username]
        return {"message": "deleted user"}


@app.get("/login/{username}/{password}")
async def login_with_token(username:str, password: str, id: UUID) -> dict:
    if valid_users.get(username) is None:
        return {"message": "User does not exists"}
    else:
        user = valid_users[username]
        if user.id == id and checkpw(password.encode(), user.passphrase):
            return user
        else:
            return {"message": "Invalid user"}



if __name__ == '__main__':
    uvicorn.run("main:app", host='0.0.0.0', port=8000, reload=True)