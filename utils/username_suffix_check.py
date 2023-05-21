def check_suffix(username):
    if len(username.split("@"))==1:
            username = f"{username}@metabyte.one"
    return username
    