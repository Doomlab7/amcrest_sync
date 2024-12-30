from main import main

def watcher():
    while True:
        main()
        time.sleep(300)

if __name__ == "__main__":
    watcher()

