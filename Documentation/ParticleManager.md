# ParticleManager

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/PygameHazel)

#### this is a class made for managing texts easier with the [pygame](https://www.pygame.org)

#### arguments

| Argument | Description | Default Value |
|:----------:|:-------------:|:---------------:|
| `WIN` | the window that the buttons are going to be drawn in | - |

#### methods 
| Name | Description | Arguments |
|:----:|:-----------:|:---------:|
| `draw` | it draws the particle | - |
| `shrink` | it makes the particles smaller | Optional[dt] |
| `delete_particles` | it deletes particles that have a size smaller or equal than 0 | - |
| `collide_rects` | it does collisions with a given list of pygame rects | rects, Optional[dt] |
| `update_rects` | it updates the rects of the particles automatically called by shrink, activate_gravity, collide_with_rects | - |
| `randomize_vels` | it randomizes the directions and the speed | limit_x[the smallest vel allowed, the biggest vel allowed], limit_y[the smallest vel allowed, the biggest vel allowed], Optional[dt] |
| `move` | it moves the particle | Optional[dt] |
| `activate_gravity` | it applies a given gravity to the particle | Optional[dt] |
| `get_particles` | it returns a list of all the particles | - |
| `add_particle` | it adds a new particle | x, y, vel_x, vel_y, shrink_amount, size, color, collision_tolerance, gravity |

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
