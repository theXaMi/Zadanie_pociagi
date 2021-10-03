from random import choice, randrange
from requests import get


def generatestation():
    url = "http://bazakolejowa.pl/index.php?dzial=stacje&st="
    alphabet = "ABCDEFGHIJKLMNOPRSTUVWZ"
    strtofind = "class='woj"
    secondstr = 'okno=start">'
    url = url + choice(list(alphabet))
    res = get(url)
    last, ix, ix2 = 0, 0, 0
    if res.ok:
        res = res.text
        ix = randrange(0, res.count(strtofind)) - 1
        for i in range(ix):
            last = res.find(strtofind, last + 1)
        ix = res.find(secondstr, last) + len(secondstr)
        ix2 = res.find("\n", ix + 1)
        return res[ix:ix2]
