comp_dirs = {"up": "down", "down": "up", "right": "left", "left": "right"}


def get_ovr_dir(snake):
    head_x, head_y = snake.blocks[0]
    tail_x, tail_y = snake.blocks[-1]

    if abs(head_x - tail_x) > abs(head_y - tail_y):

        if head_x - tail_x > 0:

            return "right"

        else:

            return "left"

    else:

        if head_y - tail_y > 0:

            return "down"

        else:

            return "up"
