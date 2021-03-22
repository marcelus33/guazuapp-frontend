

def get_screen_by_name(screens, name):
    screen = False
    for s in screens:
        if s.name == name:
            screen = s
            break
    return screen