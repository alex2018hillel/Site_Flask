def json_reader():
    with open("resourses/response.json") as f:
        user_data = (json.loads(f.read()).get("payload"))
    return user_data