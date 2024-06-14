def update_score(score):
    with open("score.txt", "w") as file:
        file.write(str(score))

def read_score():
    try:
        with open("score.txt", "r") as file:
            return int(file.read())
    except FileNotFoundError:
        return 0
