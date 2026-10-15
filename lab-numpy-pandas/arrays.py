import numpy as np

# portions of pizza sold, Monday to Sunday
week = np.array([18, 15, 17, 19, 24, 27, 21])
print(week.dtype, week.shape)

# one maths line for the whole array: no loop
print(week * 14)
print(week.mean())

# one dtype: one string turns everything into text
print(np.array([18, "pizza"]))

# two branches: one row each, one column per day
both = np.array([[18, 15, 17, 19, 24, 27, 21],
                 [12, 11, 13, 12, 16, 19, 14]])
print(both.shape)
print(both.sum(axis=0))   # down: each day
print(both.sum(axis=1))   # across: each branch

# a slice is a view: it shares the numbers
weekend = week[5:7]
weekend[0] = 0
print(week)
