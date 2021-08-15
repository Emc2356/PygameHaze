# AnimateManager

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/PygameHelper)

#### this is a class made for managing animations with the [pygame](https://www.pygame.org)

#### arguments

| Argument | Description | Default Value |
|:--------:|:-----------:|:-------------:|
| `WIN` | the window that the buttons are going to be drawn in | - |

#### methods 
| Name | Description | Arguments |
|:----:|:-----------:|:---------:|
| `draw` | it draws the animations in the screen | - |
| `animate` | it animates all of the stored animations | - |
| `get_animations` | it returns a list of the animations stored | - |
| `add_animation` | it adds a new animation | x, y, images, frames_per_image |

#### it also can handle some dunder(magic) methods
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

# contributions:
---
> Pull requests are welcome!
> Feel free to create a fork of this repository and use the code for any noncommercial purposes.
