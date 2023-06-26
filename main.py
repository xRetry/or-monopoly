import numpy as np
import matplotlib.pyplot as plt

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

def create_trans_matrix_complex(dice_probs: np.ndarray, matrix_simple: np.ndarray) -> np.ndarray:
    matrix = np.zeros((SIZE+3, SIZE+3))
    matrix[:SIZE, :SIZE] = matrix_simple

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

def get_n_step_probs(matrix: np.ndarray, num_steps: float) -> np.ndarray:
    init = np.zeros(matrix.shape[1], dtype=float)
    init[0] = 1

    eig_vals, eig_vecs_right = np.linalg.eig(matrix)
    eig_vecs_left = np.linalg.inv(eig_vecs_right)
    probs_stationary = eig_vecs_left[0] / eig_vecs_left[0].sum()

    if np.isinf(num_steps):
        probs = np.real(probs_stationary @ matrix)
    else:
        matrix_n_steps = eig_vecs_right @ np.diag(eig_vals**num_steps) @ eig_vecs_left
        probs = np.real(matrix_n_steps.T @ init)

    if len(probs) > SIZE:
        probs[10] += probs[SIZE] + probs[SIZE+1] + probs[SIZE+2]
        probs = probs[:SIZE]

    return probs

def plot_matrix(matrix: np.ndarray):
    plt.figure()
    plt.imshow(matrix)
    plt.show() 

def plot_board(probs: np.ndarray, no_start_and_jail: bool=False):
    board = np.ones((13, 13)) * np.nan

    board[-1, 1:-1] = probs[:11][::-1]
    board[-2, 1:-1] = probs[:11][::-1]

    for i in range(9):
        board[-i-3, :2] = probs[11+i]
        board[-i-3, -2:] = probs[39-i]

    board[0, 1:-1] = probs[20:31]
    board[1, 1:-1] = probs[20:31]

    board[-2:, -1] = probs[0]
    board[-2:, 0] = probs[10]
    board[:2, 0] = probs[20]
    board[:2, -1] = probs[30]

    if no_start_and_jail:
        board[-2:, :2] = 0
        board[-2:, -2:] = 0

    plt.figure()
    plt.imshow(board)
    plt.xticks([])
    plt.yticks([])
    plt.show()

def print_field_probs(probs: np.ndarray, title: str, show_plot=False) -> None:
    print(title)
    print('Field\tProbability')
    for i in range(SIZE):
        p = probs[i]
        print(f'{i+1}\t{p}')
    print()

    if show_plot: 
        plot_board(probs)

def main():
    dice_probs = create_dice_probs()
    matrix_simple = create_trans_matrix_simple(dice_probs)
    matrix_cplx = create_trans_matrix_complex(dice_probs, matrix_simple)
    plot_matrix(matrix_cplx)

    probs = get_n_step_probs(matrix_simple, 1)
    print_field_probs(probs, 'One Step Probs:')
    #plot_board(probs)

    probs = get_n_step_probs(matrix_simple, 2)
    print_field_probs(probs, 'Two Step Probs:')
    #plot_board(probs)

    probs = get_n_step_probs(matrix_simple, 3)
    print_field_probs(probs, 'Three Step Probs:')
    #plot_board(probs)

    probs = get_n_step_probs(matrix_simple, 1000)
    print_field_probs(probs, 'Thousand Step Probs:')
    #plot_board(probs)

    probs = get_n_step_probs(matrix_cplx, np.inf)
    print_field_probs(probs, 'Stationary Probs:', True)
    #plot_board(probs)
    #plot_board(probs, True)

    idx_sorted = np.argsort(probs)+1
    print('Field with max probability without start and jail:', idx_sorted[-3])
    print('Field with min probability:', idx_sorted[0])

if __name__ == '__main__':
    main()
