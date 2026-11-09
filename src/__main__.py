import bm25s
from src.cli import CLI
import src.parser
import fire



def main():
    fire.Fire(CLI)


if __name__ == "__main__":
    main()
