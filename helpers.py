from kivy.app import App


def next_prev(func):
    def wrapper(self):
        name, direction = func.__name__.split('_')
        list_ = App.get_running_app().paths.get(App.get_running_app().selected_avatar_attributes['sex']).get(name)
        curr_file = App.get_running_app().selected_avatar_attributes.get(name)
        curr_index = list_.index(curr_file)

        if direction == 'right':
            try:
                App.get_running_app().selected_avatar_attributes[name] = list_[curr_index + 1]
            except IndexError:
                App.get_running_app().selected_avatar_attributes[name] = list_[0]
        elif direction == 'left':
            try:
                App.get_running_app().selected_avatar_attributes[name] = list_[curr_index - 1]
            except IndexError:
                App.get_running_app().selected_avatar_attributes[name] = list_[-1]

        return func(self)

    return wrapper


def select_sex(func):
    def wrapper(self):
        _, name = func.__name__.split('_')

        App.get_running_app().selected_avatar_attributes['sex'], \
        previous = name, App.get_running_app().selected_avatar_attributes['sex']

        if previous != name:
            for x in ('base', 'eyes', 'mouth'):  # todo add hair
                App.get_running_app().selected_avatar_attributes[x] = App.get_running_app().paths.get(name).get(x)[
                    App.get_running_app().paths.get(previous).get(x).index(
                        App.get_running_app().selected_avatar_attributes.get(x)
                        # getattr(App.get_running_app(), f'selected_{x}')
                    )
                ]

        return func(self)

    return wrapper


def apply_element(template, element, x_offset, y_offset):
    for y in range(y_offset, y_offset + element.shape[0]):
        for x in range(x_offset, x_offset + element.shape[1]):
            if not all(element[y - y_offset, x - x_offset] == [0, 0, 0, 0]):
                template[y, x] = element[y - y_offset, x - x_offset]
    return template