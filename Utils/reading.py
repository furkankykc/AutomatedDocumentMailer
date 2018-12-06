from pathlib import Path


def seperatedListSummoner(liste):
    liste = liste.split(".")[0][:-1]+str(int(liste.split(".")[0][-1])+1)+"."+liste.split(".")[1]
    file = Path(liste)
    if file.exists():
        return liste
    return None