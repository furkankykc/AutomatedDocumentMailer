from pathlib import Path


def seperatedListSummoner(liste):
    try:
        liste = liste.split(".")[0][:-1]+str(int(liste.split(".")[0][-1])+1)+"."+liste.split(".")[1]
    except:
        return None
    file = Path(liste)
    if file.exists():
        return liste
    return None