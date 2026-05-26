#!/usr/bin/env python3

"""
Intentionally vulnerable Python program for Bandit testing.

DO NOT USE IN PRODUCTION.
This file contains multiple insecure coding patterns
meant for static analysis practice.
"""

import os
import subprocess
import pickle
import hashlib
import random
import tempfile
import yaml
from flask import Flask, request

app = Flask(__name__)

# Hardcoded password (Bandit: B105)
ADMIN_PASSWORD = "SuperSecret123"

# Weak cryptography (Bandit: B303)
def insecure_hash(data):
    return hashlib.md5(data.encode()).hexdigest()


# Predictable random numbers (Bandit: B311)
def generate_token():
    return str(random.random())


# Unsafe pickle deserialization (Bandit: B301)
def load_user_profile(filename):
    with open(filename, "rb") as f:
        return pickle.load(f)


# Unsafe YAML loading (Bandit: B506)
def load_yaml_config(filename):
    with open(filename, "r") as f:
        return yaml.load(f, Loader=yaml.Loader)


# Command injection vulnerability (Bandit: B602)
def ping_host(host):
    cmd = f"ping -c 1 {host}"
    return subprocess.check_output(cmd, shell=True)


# Dangerous use of eval (Bandit: B307)
def calculate(expression):
    return eval(expression)


# Insecure temp file usage (Bandit: B108)
def write_temp_data(data):
    temp_path = "/tmp/mytempfile.txt"
    with open(temp_path, "w") as f:
        f.write(data)


# SQL injection example
def build_query(username):
    query = f"SELECT * FROM users WHERE username = '{username}'"
    return query


# Flask debug enabled (Bandit may warn)
@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")

    if password == ADMIN_PASSWORD:
        return f"Welcome {username}"
    return "Access denied"


@app.route("/run")
def run_command():
    user_cmd = request.args.get("cmd")
    output = subprocess.check_output(user_cmd, shell=True)
    return output.decode()


@app.route("/calc")
def calc():
    expr = request.args.get("expr")
    return str(eval(expr))


def main():
    print("Weak hash:", insecure_hash("password"))
    print("Token:", generate_token())

    user_input = input("Enter expression: ")
    print("Result:", calculate(user_input))

    host = input("Enter host to ping: ")
    print(ping_host(host))


if __name__ == "__main__":
    app.run(debug=True)