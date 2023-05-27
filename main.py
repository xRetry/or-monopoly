import numpy as np

SIZE = 40
NUM_DICE1 = 6
NUM_DICE2 = 6

def create_dice_probs() -> np.ndarray:
    probs = np.zeros(NUM_DICE1 + NUM_DICE2 + 1)
    for i in range(1, NUM_DICE1+1):
        for j in range(1, NUM_DICE2+1):
            probs[i+j] += 1/NUM_DICE1 * 1/NUM_DICE2;

    return probs;

def create_trans_matrix_simple(dice_probs: np.ndarray) -> np.ndarray:
    matrix = np.zeros((SIZE, SIZE))
    for i in range(SIZE):
        for j in range(len(dice_probs)):
            idx = (i+j) % SIZE
            matrix[i, idx] = dice_probs[j]

    return matrix

def create_trans_matrix_complex(dice_probs: np.ndarray) -> np.ndarray:
    matrix = np.zeros((SIZE+3, SIZE+3))
    matrix[:SIZE, :SIZE] = create_trans_matrix_simple(dice_probs)

    # Go to start
    matrix[7, :] = np.zeros(SIZE+3)
    matrix[7, 0] = 1
    matrix[17, :] = np.zeros(SIZE+3)
    matrix[17, 0] = 1
    matrix[33, :] = np.zeros(SIZE+3)
    matrix[33, 0] = 1

    # Go to jail
    matrix[22, SIZE] = 1
    matrix[30, SIZE] = 1

    # Leave jail
    prob_equal = 1/NUM_DICE1 * 1/NUM_DICE2

    idxs_leave = 10+2*np.arange(1, 7)
    matrix[SIZE, idxs_leave] = prob_equal
    matrix[SIZE+1, idxs_leave] = prob_equal
    matrix[SIZE+2, 10:10+len(dice_probs)] = dice_probs

    # Stay in jail
    matrix[SIZE, SIZE+1] = 1 - matrix[SIZE, :].sum()
    matrix[SIZE+1, SIZE+2] = 1 - matrix[SIZE+1, :].sum()

    return matrix

def get_n_step_probs_power(matrix: np.ndarray, num_steps: int) -> np.ndarray:
    init = np.zeros(matrix.shape[1], dtype=float)
    init[0] = 1

    return np.linalg.matrix_power(matrix, num_steps).T @ init

def get_n_step_probs(matrix: np.ndarray, num_steps: int) -> np.ndarray:
    init = np.zeros(matrix.shape[1], dtype=float)
    init[0] = 1

    eig_vals, eig_vecs_right = np.linalg.eig(matrix)
    eig_vecs_left = np.linalg.inv(eig_vecs_right)
    probs_stationary = eig_vecs_left[0] / eig_vecs_left[0].sum()

    if np.isinf(num_steps):
        return np.real(probs_stationary @ matrix)

    matrix_n_steps = eig_vecs_right @ np.diag(eig_vals**num_steps) @ eig_vecs_left
    return np.real(matrix_n_steps.T @ init)

def main():
    dice_probs = create_dice_probs()
    matrix = create_trans_matrix_simple(dice_probs)
    matrix = create_trans_matrix_complex(dice_probs)

    probs = get_n_step_probs_power(matrix, 3)
    print(probs)
    probs = get_n_step_probs(matrix, 3)
    print(probs)

if __name__ == '__main__':
    main()
