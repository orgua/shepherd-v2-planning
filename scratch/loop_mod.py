interval_n = 10
interval_step1 = 0
interval_step2 = 0

for _ in range(30):
    interval_step1 = (interval_step1 + 1) % interval_n
    interval_step2 = 0 if (interval_step2 >= interval_n) else interval_step2 + 1
    print(f"{interval_step1} {interval_step2}")
