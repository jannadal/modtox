import random

lst = [random.randint(0, 100) for _ in range(100)]
print(lst)


a = [lst[i : i + 10] for i in range(0, len(lst), 10)]
print(a)
