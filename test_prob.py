import argparse
import sys
import subprocess
import pyperclip
from pathlib import Path

if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument("problem")
    parser.add_argument("-e")

    args = parser.parse_args()
    if args.e is None:
        args.e = args.problem.lower()

    path = Path(".", args.problem)
    if not path.exists():
        print("Problem not found.")
        sys.exit(1)

    correct = True

    for in_file in path.glob("*.in"):
        out_file = in_file.with_suffix(".out")
        print("Test {}".format(in_file.parts[-1][0]))

        with open(in_file, "r") as f:
            data = f.read()
            process = subprocess.run("./{}".format(args.e), input = data.encode(), capture_output = True)
            solution = process.stdout.decode()

        if process.returncode != 0:
            correct = False
            print("Process exited with nonzero code.")
            continue

        with open(out_file, "r") as f:
            expected = f.read()
            if solution == expected:
                print("\033[92mCorrect\033[m")
            else:
                correct = False
                print("\033[91mWrong\033[m\n")

                print("Your output")
                print("\033[94m", end = '')
                print(solution)
                print("\033[m", end = '')

                print("Expected")
                print("\033[35m", end = '')
                print(expected)
                print("\033[m", end = '')
                
    if correct:
        with open("{}.cpp".format(args.e), "r", encoding = "utf-8") as f:
            pyperclip.copy(f.read())

