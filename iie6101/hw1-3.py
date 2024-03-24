import random, math

random.seed(486)

seq_dep = [[0, 3, 5, 9], [4, 0, 2, 8], [3, 3, 0, 6], [2, 7, 1, 0]]
initial_schedule = [0, 1, 2, 3]
initial_makespan = 20
for i in range(3):
    initial_makespan += seq_dep[initial_schedule[i]][initial_schedule[i + 1]]

sapi_schedule_greedy = [(initial_schedule, initial_makespan)]
sapi_schedule_random = [(initial_schedule, initial_makespan)]
spi_schedule_greedy = [(initial_schedule, initial_makespan)]
spi_schedule_random = [(initial_schedule, initial_makespan)]

sapi_greedy_best_schedule = sapi_schedule_greedy[-1]
sapi_random_best_schedule = sapi_schedule_random[-1]
spi_greedy_best_schedule = spi_schedule_greedy[-1]
spi_random_best_schedule = spi_schedule_random[-1]

for _ in range(5):
    sapi_schedule_greedy_new = []
    sapi_schedule_random_new = []
    spi_schedule_greedy_new = []
    spi_schedule_random_new = []

    for i in range(3):
        sapi_greedy_new_schedule = sapi_schedule_greedy[-1][0].copy()
        sapi_greedy_new_schedule[i], sapi_greedy_new_schedule[i + 1] = (
            sapi_greedy_new_schedule[i + 1],
            sapi_greedy_new_schedule[i],
        )

        sapi_random_new_schedule = sapi_schedule_random[-1][0].copy()
        sapi_random_new_schedule[i], sapi_random_new_schedule[i + 1] = (
            sapi_random_new_schedule[i + 1],
            sapi_random_new_schedule[i],
        )

        sapi_greedy_makespan = 20
        sapi_random_makespan = 20
        for j in range(3):
            sapi_greedy_makespan += seq_dep[sapi_greedy_new_schedule[j]][
                sapi_greedy_new_schedule[j + 1]
            ]
            sapi_random_makespan += seq_dep[sapi_random_new_schedule[j]][
                sapi_random_new_schedule[j + 1]
            ]

        sapi_schedule_greedy_new.append(
            (sapi_greedy_new_schedule, sapi_greedy_makespan)
        )
        sapi_schedule_random_new.append(
            (sapi_random_new_schedule, sapi_random_makespan)
        )
    for i in range(3):
        for j in range(i + 1, 4):
            spi_greedy_new_schedule = spi_schedule_greedy[-1][0].copy()
            spi_greedy_new_schedule[i], spi_greedy_new_schedule[j] = (
                spi_greedy_new_schedule[j],
                spi_greedy_new_schedule[i],
            )

            spi_random_new_schedule = spi_schedule_random[-1][0].copy()
            spi_random_new_schedule[i], spi_random_new_schedule[j] = (
                spi_random_new_schedule[j],
                spi_random_new_schedule[i],
            )
            spi_greedy_makespan = 20
            spi_random_makespan = 20
            for k in range(3):
                spi_greedy_makespan += seq_dep[spi_greedy_new_schedule[k]][
                    spi_greedy_new_schedule[k + 1]
                ]
                spi_random_makespan += seq_dep[spi_random_new_schedule[k]][
                    spi_random_new_schedule[k + 1]
                ]

            spi_schedule_greedy_new.append(
                (spi_greedy_new_schedule, spi_greedy_makespan)
            )
            spi_schedule_random_new.append(
                (spi_random_new_schedule, spi_random_makespan)
            )
    new_sapi_schedule_greedy = min(sapi_schedule_greedy_new, key=lambda x: x[1])
    new_sapi_schedule_random = random.choice(sapi_schedule_random_new)
    new_spi_schedule_greedy = min(spi_schedule_greedy_new, key=lambda x: x[1])
    new_spi_schedule_random = random.choice(spi_schedule_random_new)
    sapi_schedule_greedy.append(new_sapi_schedule_greedy)
    sapi_schedule_random.append(new_sapi_schedule_random)
    spi_schedule_greedy.append(new_spi_schedule_greedy)
    spi_schedule_random.append(new_spi_schedule_random)
    if new_sapi_schedule_greedy[1] < sapi_greedy_best_schedule[1]:
        sapi_greedy_best_schedule = new_sapi_schedule_greedy
    if new_sapi_schedule_random[1] < sapi_random_best_schedule[1]:
        sapi_random_best_schedule = new_sapi_schedule_random
    if new_spi_schedule_greedy[1] < spi_greedy_best_schedule[1]:
        spi_greedy_best_schedule = new_spi_schedule_greedy
    if new_spi_schedule_random[1] < spi_random_best_schedule[1]:
        spi_random_best_schedule = new_spi_schedule_random


print(f"SAPI Greedy: {sapi_schedule_greedy}")
print(f"SAPI Random: {sapi_schedule_random}")
print(f"SPI Greedy: {spi_schedule_greedy}")
print(f"SPI Random: {spi_schedule_random}")
print(f"SAPI Greedy Best: {sapi_greedy_best_schedule}")
print(f"SAPI Random Best: {sapi_random_best_schedule}")
print(f"SPI Greedy Best: {spi_greedy_best_schedule}")
print(f"SPI Random Best: {spi_random_best_schedule}")
