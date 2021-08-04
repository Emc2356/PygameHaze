# ButtonManger

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/Pygame-Widgets)

#### this is a class made for managing buttons easier with the [pygame](https://www.pygame.org)

#### arguments

| Argument | Description | Default Value |
|:----------:|:-------------:|:---------------:|
| `WIN` | the window that the buttons are going to be drawn in | - |

#### methods 
| Name | Description | Arguments |
|:----:|:-----------:|:---------:|
| `draw` | it draws the buttons in the screen | - |
| `event_handler` | it sends the event to all of the buttons so it can do the commands | pygame.event.Event |
| `get_buttons` | it returns a list with the buttons | - |
| `add_button` | it creates a new button | x, y, w, h, inactive_color, hover_inactive_color, active_color, hover_active_color, **kwargs |

#### it also can hanle some dunder(magic) methods
| Name | Description | Arguments |
|:----:|:-----------:|:---------:|
| `__getitem__` or `button = class_instance[i]` | it can get a item the same way as a list | key |
| `__setitem__` or `class_instance[i] = Button` | it can set a item same way as a list  | key, value |
| `__delitem__` or `del class_instace[i]` | it deletes a button from the stored button | key |
| `__len__` or `len()` | it returns how many buttons it has | - |
| `__next__` or ` next(class_instance)` | it returns a Button when it is called a second time it will return the second button etc | - |
| `__iadd__` or `class_instance += class_instance_2` | it adds the buttons from 2 ButtonManager objs | class_instance |
| `__add__` or `class_instance = class_instance + class_instance_2` | it adds the buttons from 2 ButtonManager objs | class_instance |
| `__iter__` or `for item in class_instance` | it returns a iterable obj | - |
| `__contains__` or `if item in class_instance` | it returns a bool wether a item is in the ButtonManager | item |
| `__del__` pr `del class_instance` | it deletes the instance of the class and the buttons stored in the Buttonmanager | - |
| `__repr__` or `repr(class_instance)` | it returns a string that represents the class | - |
| `__str__` or `str(class_instance)` | it returns a string that represents the class | - |
| `__bool__` or `bool(class_instance)` | it returns a boolian wether the ButtonManager contains any button | - |
| `__reversed__` or `reversed(class_instance)` | it reverses the list that the buttons are stored in incase you want the button to be rendered the oposite way | - |

contributions:
---
> Pull requests are welcome! For major refactors,
> please open an issue first to discuss what you would like to improve.
> Feel free to create a fork of this repository and use the code for any noncommercial purposes.