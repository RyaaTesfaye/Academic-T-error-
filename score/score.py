import json
path = 'score/highscore.json'

def highscore(score):
    with open(path, 'r') as file:
        highscore = json.load(file)

    if score > highscore["you"]:
        highscore["you"] = score
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(highscore, file, indent=4)

        return f"NEW HIGH SCORE!: {score:.2f} detik"
    else:
        return f"Waktu Bertahan: {score:.2f} detik"
    
def listScore():
    with open(path, 'r') as file:
        score = json.load(file)
    
    return score

def scoreBoard(score):
    pass