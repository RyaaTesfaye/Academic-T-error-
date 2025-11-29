import json
path = 'score/highscore.json'

def highscore(score):
    with open(path, 'r') as file:
        highscore = json.load(file)

    if score > highscore["you"]:
        highscore["you"] = int(score * 100) / 100
        with open(path, 'w', encoding='utf-8') as file:
            json.dump(highscore, file, indent=4)

        return highscore["you"]
    else:
        return int(score * 100) / 100
    
def listScore():
    with open(path, 'r') as file:
        score = json.load(file)
    
    return score