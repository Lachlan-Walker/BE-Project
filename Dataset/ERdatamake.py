import random
import os
import math

def generate_er_graph_fast(n, lam, seed, filepath, buffer_lines=200_000):
    """
    Fast Erdős Rényi G(n, p) generator using the edge-skipping method.

    Inputs:
      - n: number of nodes (0..n-1)
      - lam: expected degree (lambda)
      - seed: RNG seed
      - filepath: where to write the edge list
      - buffer_lines: number of lines to buffer before writing (I/O speed)

    Output file format (one edge per line):
      i j
    Undirected simple graph (no self-loops, no duplicates). All implicit weights = 1.
    """

    random.seed(seed)
    p = lam / (n - 1)


    if p >= 1.0:
        # Complete graph: write all edges
        with open(filepath, "w") as f:
            buf = []
            for i in range(n):
                for j in range(i + 1, n):
                    buf.append(f"{i} {j}\n")
                    if len(buf) >= buffer_lines:
                        f.writelines(buf)
                        buf.clear()
            if buf:
                f.writelines(buf)
        return

    # Precompute log(1-p) once (negative number)
    log_q = math.log(1.0 - p)

    # Batagelj–Brandes style generation for undirected graph:
    # Generates edges (w, v) with 0 <= w < v < n
    v = 1
    w = -1

    with open(filepath, "w") as f:
        buf = []
        while v < n:
            r = random.random()
            # Number of non-edges to skip is geometric; compute jump length via logs
            w = w + 1 + int(math.log(1.0 - r) / log_q)

            while w >= v and v < n:
                w -= v
                v += 1

            if v < n:
                buf.append(f"{w} {v}\n")
                if len(buf) >= buffer_lines:
                    f.writelines(buf)
                    buf.clear()

        if buf:
            f.writelines(buf)


def create_er_dataset(node_list, lambda_list, instances_per_setting=10, base_seed=37):
    """
    Create an ER dataset across node counts and expected degrees.
    For each (n, lam), generates `instances_per_setting` instances with different seeds.

    Output directory: ER_dataset/
    Filenames: n_lam_instanceid.txt
    """
    output_dir = "ER_dataset_mini"
    os.makedirs(output_dir, exist_ok=True)

    for n in node_list:
        print("starting:", n)
        for lam in lambda_list:
            print("starting:", lam)
            for instance_id in range(instances_per_setting):
                seed = base_seed + instance_id
                filename = f"{n}_{lam}_{instance_id}.txt"
                filepath = os.path.join(output_dir, filename)

                generate_er_graph_fast(
                    n=n,
                    lam=lam,
                    seed=seed,
                    filepath=filepath,
                )

node_list = [100, 1000, 10_000, 100_000, 1_000_000]
lambda_list = [0.6, 0.8, 1.0, 1.6, 2.0, 3, 5, 8, 13, 20]

create_er_dataset(node_list, lambda_list)