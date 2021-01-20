from parameters_setting import get_tsumego, get_solved_tsumego_dir, get_positive_integer
from solve_tsumego import solve_tsumego


def main():
    tsumego_path = get_tsumego()
    first_page = get_positive_integer('first page', default_val=1)
    out_dir = get_solved_tsumego_dir(tsumego_path=tsumego_path)
    width = 720
    ratio = 297 / 210
    h = get_positive_integer('board height', default_val=int(width * ratio))
    w = get_positive_integer('board width', default_val=width)
    stone_size = get_positive_integer('stone size', default_val=21)
    solve_tsumego(tsumego_path=tsumego_path, first_page=first_page, out_dir=out_dir, h=h, w=w, r=stone_size)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
