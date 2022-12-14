#calculate pos for mouse click
def click_pos(win, obj):
    click_x = win[0] + obj[0]
    click_y = win[1] + obj[1]

    return click_x, click_y