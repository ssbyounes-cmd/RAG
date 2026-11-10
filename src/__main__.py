from src.cli import CLI
import fire



def main():
    fire.Fire(CLI)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")