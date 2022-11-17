import http.server
import json
from pathlib import Path

def get_problems():
    problems = []

    class CompanionRequestHandler(http.server.BaseHTTPRequestHandler):
        def do_POST(self):
            nonlocal problems
            problems.append(json.loads(self.rfile.read()))

    with http.server.HTTPServer(("127.0.0.1", 10043), CompanionRequestHandler) as server:
        server.handle_request()

        num_batch = problems[0]["batch"]["size"]
        for _ in range(num_batch - 1):
            server.handle_request()

    return problems

def create_dirs(problems):
    for problem in problems:
        letter = problem["name"][0]

        try:
            path = Path(".", letter)
            path.mkdir()
        except FileExistsError:
            print("Directory '{}' already exists.".format(letter))
            continue

        for idx, test in enumerate(problem["tests"]):
            with open(path / "{}.in".format(idx), 'w') as f:
                f.write(test["input"])
            with open(path / "{}.out".format(idx), 'w') as f:
                f.write(test["output"])

if __name__ == "__main__":
    problems = get_problems()
    print(problems)
    print("")
    create_dirs(problems)

