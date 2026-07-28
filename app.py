import random
import numpy as np
import matplotlib.pyplot as plt

def run_simulation(n_iters):
    old_stones_list = np.zeros(n_iters, dtype=int)
    new_stones_list = np.zeros(n_iters, dtype=int)

    for i in range(n_iters):
        stones = 0
        points = 0
        got_A = False
        got_B = False

        while not (got_A and got_B):
            stones += 1200
            target_A_this_pull = not got_A
            
            for _ in range(10):
                points += 1
                if random.random() < 0.007:
                    if target_A_this_pull:
                        got_A = True
                    else:
                        got_B = True

            while points >= 200:
                if not got_A:
                    got_A = True
                    points -= 200
                elif not got_B:
                    got_B = True
                    points -= 200
                else:
                    break
        old_stones_list[i] = stones

        stones_new = 0
        charge = 0
        total_pulls = 0
        tickets = 0
        got_A_new = False
        got_B_new = False
        claimed_tickets = set()

        while not (got_A_new and got_B_new):
            if tickets > 0:
                tickets -= 1
            else:
                stones_new += 1200

            target_A_this_pull = not got_A_new

            for _ in range(10):
                total_pulls += 1
                charge += 1
                is_target = False

                if random.random() < 0.007:
                    is_target = True
                elif not is_target:
                    if charge == 200:
                        is_target = True
                    elif charge == 100:
                        if random.random() < 0.5:
                            is_target = True

                if is_target:
                    if target_A_this_pull:
                        got_A_new = True
                    else:
                        got_B_new = True
                    charge = 0

                if total_pulls in (70, 130, 150, 170, 270, 330, 350, 370) and total_pulls not in claimed_tickets:
                    tickets += 1
                    claimed_tickets.add(total_pulls)

        new_stones_list[i] = stones_new

    return old_stones_list, new_stones_list

def print_stats(name, data):
    print(f"--- {name} ---")
    print(f"Mean: {np.mean(data):.1f}")
    print(f"Std Dev: {np.std(data):.1f}")
    print(f"Variance: {np.var(data):.1f}")
    print(f"Min: {np.min(data)}")
    print(f"Q1 (25%): {np.percentile(data, 25)}")
    print(f"Median: {np.percentile(data, 50)}")
    print(f"Q3 (75%): {np.percentile(data, 75)}")
    print(f"90%ile: {np.percentile(data, 90)}")
    print(f"95%ile: {np.percentile(data, 95)}")
    print(f"99%ile: {np.percentile(data, 99)}")
    print(f"Max: {np.max(data)}")
    print()

N_ITERS = 6
old_data, new_data = run_simulation(N_ITERS)

print_stats("Old Specs", old_data)
print_stats("New Specs", new_data)

plt.figure(figsize=(10, 6))
plt.hist(old_data, bins=50, alpha=0.5, label='Old Specs', color='cornflowerblue', density=True)
plt.hist(new_data, bins=50, alpha=0.5, label='New Specs', color='lightpink', density=True)
plt.title(f'Distribution of Required Stones (N={N_ITERS})')
plt.xlabel('Required Stones')
plt.ylabel('Probability Density')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

plt.figure(figsize=(10, 6))
bplot = plt.boxplot([old_data, new_data], labels=['Old Specs', 'New Specs'], patch_artist=True, medianprops=dict(color='red', linewidth=2))
colors = ['cornflowerblue', 'lightpink']
for patch, color in zip(bplot['boxes'], colors):
    patch.set_facecolor(color)
plt.title(f'Boxplot of Required Stones (N={N_ITERS})')
plt.ylabel('Required Stones')
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()

plt.figure(figsize=(10, 6))
x_old = np.sort(old_data)
y_old = np.arange(1, len(x_old) + 1) / len(x_old)
x_new = np.sort(new_data)
y_new = np.arange(1, len(x_new) + 1) / len(x_new)
plt.plot(x_old, y_old, label='Old Specs', color='cornflowerblue', linewidth=2)
plt.plot(x_new, y_new, label='New Specs', color='lightpink', linewidth=2)
plt.title(f'Cumulative Distribution Function (N={N_ITERS})')
plt.xlabel('Required Stones')
plt.ylabel('Cumulative Probability')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.7)
plt.show()
