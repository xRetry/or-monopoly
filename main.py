import numpy as np

SIZE = 40

def create_dice_probs(num_dice1: int, num_dice2: int) -> np.ndarray:
    probs = np.zeros(SIZE)
    for i in range(1, num_dice1+1):
        for j in range(1, num_dice2+1):
            probs[i+j] += 1/num_dice1 * 1/num_dice2;

    return probs;

def create_trans_matrix_simple(dice_probs: np.ndarray) -> np.ndarray:
    matrix = np.zeros((SIZE, SIZE))
    for i in range(SIZE):
        for j in range(len(dice_probs)):
            idx = (i+j) % SIZE
            matrix[i, idx] = dice_probs[j]

    return matrix

def create_trans_matrix_complex(dice_probs: np.ndarray) -> np.ndarray:
    matrix = create_trans_matrix_simple(dice_probs)

    matrix[8, :] = np.zeros(SIZE)
    matrix[8, 0] = 1

    return matrix

def get_n_step_probs_power(matrix: np.ndarray, num_steps: int) -> np.ndarray:
    init = np.zeros(SIZE, dtype=float)
    init[0] = 1

    return np.linalg.matrix_power(matrix, num_steps).T @ init

def get_n_step_probs(matrix: np.ndarray, num_steps: int) -> np.ndarray:
    init = np.zeros(SIZE, dtype=float)
    init[0] = 1

    eig_vals, eig_vecs_right = np.linalg.eig(matrix)
    eig_vecs_left = np.linalg.inv(eig_vecs_right)
    probs_stationary = eig_vecs_left[0] / eig_vecs_left[0].sum()

    if np.isinf(num_steps):
        return np.real(probs_stationary @ matrix)

    matrix_n_steps = eig_vecs_right @ np.diag(eig_vals**num_steps) @ eig_vecs_left
    return np.real(matrix_n_steps.T @ init)

def main():
    dice_probs = create_dice_probs(6, 6)
    matrix = create_trans_matrix_simple(dice_probs)

    probs = get_n_step_probs_power(matrix, 3)
    print(probs)
    probs = get_n_step_probs(matrix, 3)
    print(probs)


    

if __name__ == '__main__':
    main()
