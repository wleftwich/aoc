# https://www.reddit.com/r/adventofcode/comments/18ge41g/comment/kefgbn7/?utm_source=share&utm_medium=web2x&context=3

ls = [*open("data/12.txt")]
import re
from tqdm import tqdm
from functools import lru_cache

games = [(x, (*map(int, y.split(",")),)) for x, y in (l.strip().split(" ") for l in ls)]
games2 = [("?".join([x] * 5), y * 5) for x, y in games]


@lru_cache(maxsize=None)
def count_poss(g):
    pos, hints = g
    if "?" not in pos:
        return (*map(len, re.findall(r"#+", pos)),) == hints
    i, p = pos.index("?"), re.compile(r"#+\.")
    y = [(m.start(), m.end()) for m in p.finditer(pos[:i + 1])]
    x = [y - x - 1 for x, y in y]
    if len(hints) < len(x) or any(x != y for x, y in zip(x, hints)): return 0
    j, nh = 0 if len(y) == 0 else y[-1][1], hints[len(x):]
    return sum(count_poss(((pos[j:i] + x + pos[i + 1:]).strip("."), nh)) for x in ".#")


print([sum(map(count_poss, gs)) for gs in [games, tqdm(games2)]])


