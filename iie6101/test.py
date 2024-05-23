a = [{"a": 1, "b": 2}, {"a": 3, "b": 4}, {"a": 5, "b": 6}]
b = a.copy()

b[0]["a"] = 10
del b[0]

print(a)
