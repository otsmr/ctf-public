#!/usr/bin/python3

from _thread import *
import docker
import time
import datetime
from flask import *
import string
import random
import os.path
import jwt

JWT_SECRET = "asdfh23g89uiewhfü208groiewjhfpeiqwufbwei" # change me

client = docker.from_env()

def get_pitm_containers():

    containers = client.containers.list()

    pitm_containers = []
    pitm_containers_byid = {}

    for container in containers:

        if container.attrs["Config"]["Image"] == "python_in_the_middle":
            pitm_containers.append(container)
            pitm_containers_byid[container.id] = container

    return pitm_containers, pitm_containers_byid

def get_password():
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    num = string.digits
    return "".join(random.sample(lower + upper + num, 8))

def create_container():

    pitm, _ = get_pitm_containers()

    port = 13370 + len(pitm)
    password = get_password()

    try:

        container = client.containers.run(
            image='python_in_the_middle',
            ports={'22/tcp': port},
            environment=["ENV_SSH_PASSWORD="+password],
            detach=True,
            cap_add=["NET_ADMIN", "NET_RAW"]
        )

    except Exception as e:
        print(e)
        return False, "", 0

    id = container.id
    return id, password, port


def kill_container_after_24h():

    while True:

        containers, _ = get_pitm_containers()

        for container in containers:

            created = datetime.datetime.strptime(container.attrs["Created"].split(".")[0], '%Y-%m-%dT%H:%M:%S')

            running_diff = datetime.datetime.now() - created
            # läuft seit mehr als 24h

            if running_diff.total_seconds() > (1 * 60 * 24) or \
                (container.status != "running" and \
                    container.status != "restarting"): 
                
                container.kill()
                container.remove(force=True)

        time.sleep(1 * 60 * 10) # alle 10 Minuten

start_new_thread(kill_container_after_24h, ())

app = Flask(__name__)
dirname = os.path.dirname(os.path.abspath(__file__))

@app.route("/remove")
def remove():
    
    jwt_token = request.cookies.get('jwt')
    response = {
        "error": True,
        "message": "No valid session"
    }

    try:

        data = jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"])

        remove_id = request.args.to_dict().get("id")

        new_containers = []

        _, pitm = get_pitm_containers()

        for container in data["containers"]:
            if container["id"] == remove_id and pitm.get(remove_id):

                cont = pitm.get(remove_id)

                print("KILL container")
                cont.kill()
                cont.remove(force=True)

                response["error"] = False
            else:
                new_containers.append(container)

        data["container"] = new_containers

        jwt_token = jwt.encode(data, JWT_SECRET, algorithm="HS256")

    except Exception as e:
        print(e)

    resp = make_response(jsonify(response))
    resp.set_cookie('jwt', jwt_token)

    return resp

@app.route("/create")
def create():

    jwt_token = request.cookies.get('jwt')
    response = {
        "error": True,
        "message": "No valid session"
    }

    try:

        data = jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"])

        pitm, _ = get_pitm_containers()

        if len(pitm) > 20:
            response["message"] = "Maximum 20 instances. Try again later"
        else:

            container_id, password, port = create_container()

            if container_id == False:
                response["message"] = "Container could not be created"
            else:

                data["containers"].append({
                    "id": container_id,
                    "password": password,
                    "port": port
                })

                jwt_token = jwt.encode(data, JWT_SECRET, algorithm="HS256")

                response["error"] = False 

    except Exception as e:
        print(e)

    resp = make_response(jsonify(response))
    resp.set_cookie('jwt', jwt_token)

    return resp


@app.route("/start")
def start():

    jwt_token = request.cookies.get('jwt')
    data = {
        "containers": []
    }

    if jwt_token == None:
        jwt_token = jwt.encode(data, JWT_SECRET, algorithm="HS256")

    try:
        data = jwt.decode(jwt_token, JWT_SECRET, algorithms=["HS256"])
    except:
        jwt_token = jwt.encode(data, JWT_SECRET, algorithm="HS256")

    pitm_containers, pitm_containers_by_id  = get_pitm_containers()

    html_containers = []
    for user_container in data["containers"]:
        cid = user_container["id"]
        cport = user_container["port"]
        cpass = user_container["password"]
        host = "localhost" if "localhost" in request.url else "ctf.hs-offenburg.de"

        if pitm_containers_by_id.get(cid):
            container = pitm_containers_by_id.get(cid)
            html_containers.append("".join([f"<p>{cid[:8]}... is {container.status}</p>", f"<pre>ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no user@{host} -p {cport}</pre><pre>Password: {cpass}</pre>", f"<button onclick=\"removeInstance('{cid}')\">Kill</button>"]))

    response = ""
    with open(dirname + "/index.html", "r") as f:

        response += f.read()

        response = response.replace("{{container-count}}", str(len(pitm_containers)))
        response = response.replace("{{own-container}}", "<hr />".join(html_containers))
        response = response.replace("{{session}}", jwt_token)

    resp = make_response(response)

    resp.set_cookie('jwt', jwt_token)

    return resp

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)