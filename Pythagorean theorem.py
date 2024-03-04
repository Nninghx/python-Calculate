import csv


def generate_pythagorean_triplet_euclid(limit):
    triplets = []
    m, n = 2, 1

    while len(triplets) < limit:
        a = m ** 2 - n ** 2
        b = 2 * m * n
        c = m ** 2 + n ** 2

        # 检查a, b, c是否满足勾股定理
        if a ** 2 + b ** 2 == c ** 2:
            triplets.append((a, b, c))

            # 更新m和n的值，这里我们使用一种简单的方法来避免重复：确保m和n互质
        m += 1
        if gcd(m, n) != 1:
            n = 1
        else:
            n += 1

            # 为了避免生成过大的数，我们可以设置一个条件来限制m和n的大小
        if m * n > limit * 10:
            break

    return triplets


def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# 生成勾股三元组
limit = 10000000000  # 设置你想要生成的三元组的数量
pythagorean_triplets = generate_pythagorean_triplet_euclid(limit)

# 验证生成的三元组是否符合勾股定理
invalid_triplets = []
for triplet in pythagorean_triplets:
    a, b, c = triplet
    if a ** 2 + b ** 2 != c ** 2:
        invalid_triplets.append(triplet)

if invalid_triplets:
    print("Invalid triplets found:", invalid_triplets)
else:
    print("All triplets satisfy the Pythagorean theorem.")

# 将结果保存到CSV文件
with open('pythagorean_triplets.csv', mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["a", "b", "c"])  # 写入表头
    writer.writerows(pythagorean_triplets)  # 写入数据

print(f"Results saved to 'pythagorean_triplets.csv'")