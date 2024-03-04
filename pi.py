from tqdm import tqdm
import decimal
import concurrent.futures
import os
import pickle


def load_checkpoint(checkpoint_file):
    """从检查点文件中加载数据"""
    if os.path.exists(checkpoint_file):
        with open(checkpoint_file, 'rb') as f:
            return pickle.load(f)
    return None, None


def save_checkpoint(checkpoint_file, k, pi_estimate):
    """将当前状态保存到检查点文件"""
    with open(checkpoint_file, 'wb') as f:
        pickle.dump((k, pi_estimate), f)


def pi_to_n_decimal_places(n, checkpoint_file='checkpoint.pkl'):
    decimal.getcontext().prec = n + 1

    # 尝试从检查点加载
    k, pi_estimate = load_checkpoint(checkpoint_file)
    if k is None:
        pi_estimate = decimal.Decimal(0)
        k = 0
    else:
        print(f"Resuming calculation from checkpoint at k = {k}")

    with tqdm(total=n + 1, desc="Processing pi calculation", leave=True, initial=k) as progress:
        while True:
            term = 1 / decimal.Decimal(16) ** k * (
                    decimal.Decimal(4) / (8 * k + 1) -
                    decimal.Decimal(2) / (8 * k + 4) -
                    decimal.Decimal(1) / (8 * k + 5) -
                    decimal.Decimal(1) / (8 * k + 6))
            if abs(term) < decimal.Decimal("1e-{}".format(n)):
                break
            pi_estimate += term
            k += 1
            progress.update(1)

            # 保存检查点
            save_checkpoint(checkpoint_file, k, pi_estimate)

    return pi_estimate


if __name__ == '__main__':
    n = 90000  # 注意：计算1000000000位可能需要非常长的时间和大量的内存
    checkpoint_file = 'pi_checkpoint.pkl'

    # 使用单个进程计算圆周率
    result = pi_to_n_decimal_places(n, checkpoint_file)

    # 将计算结果保存到文件中
    with open('圆周率.txt', 'w') as f:
        f.write(str(result) + '\n')
