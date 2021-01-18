from parameters_setting import get_tsumego, get_solved_tsumego_path, get_size
from store_results import store_results
from solve_tsumego import solve_tsumego


def main():
    tsumego, in_tsumego_path = get_tsumego()
    out_path = get_solved_tsumego_path(in_tsumego_path=in_tsumego_path)
    width = 720
    ratio = 297 / 210
    h = get_size('board height', default_val=int(width * ratio))
    w = get_size('board width', default_val=width)
    stone_size = get_size('stone size', default_val=22)
    solutions = solve_tsumego(tsumego=tsumego, h=h, w=w, r=stone_size)
    store_results(tsumego=tsumego, path=out_path, solutions=solutions, stone_size=stone_size)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
