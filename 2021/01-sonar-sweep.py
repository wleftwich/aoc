# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.1
#   kernelspec:
#     display_name: Python 3
#     language: python
#     name: python3
# ---

# %% [markdown]
# [https://adventofcode.com/2021/day/1](https://adventofcode.com/2021/day/1)

# %%
import itertools

# %%
with open('data/01.txt') as fh:
    depths = [int(x.strip()) for x in fh if x]

# %%
len(depths), depths[:3], depths[-3:]

# %%
sum(b > a for (a, b) in zip(depths, depths[1:]))

# %%
windows = itertools.zip_longest(depths, depths[1:], depths[2:], fillvalue=0)
window_sums = [sum(w) for w in windows]

sum(b > a for (a, b) in zip(window_sums, window_sums[1:]))
