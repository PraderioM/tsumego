from parameters_setting import get_tsumego, get_solved_tsumego_dir, get_positive_integer, get_bool
from solve_tsumego import solve_tsumego
from store_results import store_joint_images
from default_values import get_defaults, store_defaults


def main():
    default_values = get_defaults()
    tsumego_path = get_tsumego(default_path=default_values.default_path)
    first_page = get_positive_integer('first page', default_val=default_values.first_page)
    out_dir = get_solved_tsumego_dir(tsumego_path=tsumego_path)
    w = get_positive_integer('board width', default_val=default_values.width)
    h = get_positive_integer('board height', default_val=default_values.height)
    stone_size = get_positive_integer('stone size', default_val=default_values.stone_size)
    show_fairy_lights = get_bool(message='Do you want to add fairy lights to your tsumego?',
                                 default=default_values.show_fairy_lights)
    last_page = solve_tsumego(tsumego_path=tsumego_path, first_page=first_page, out_dir=out_dir, h=h, w=w, r=stone_size,
                              show_fairy_lights=show_fairy_lights)

    join_tsumego_images = True
    n_joined_images = 6
    if last_page > first_page:
        join_tsumego_images = get_bool(message='Do you want to join all tsumego images?',
                                       default=default_values.join_tsumego_images)
        if join_tsumego_images:
            n_joined_images = get_positive_integer('number of joined images',
                                                   default_val=default_values.n_joined_images)
            store_joint_images(first_page=first_page, last_page=last_page, out_dir=out_dir, n=n_joined_images)

    store_defaults(tsumego_path=tsumego_path, first_page=last_page, width=w, height=h, stone_size=stone_size,
                   show_fairy_lights=show_fairy_lights,
                   join_tsumego_images=join_tsumego_images,
                   n_joined_images=n_joined_images)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
