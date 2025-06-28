# templates.py

utils_code = """
def greet(name: str):
    print(f"Hello, {name} from Python!")
"""

main_code = """
from utils import greet

def main():
    name = "Alice"
    greet(name)

if __name__ == "__main__":
    main()
"""
