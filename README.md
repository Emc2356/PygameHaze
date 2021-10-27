# PygameHelper

###### [source code](https://github.com/Emc2356/Pygame-Widgets)
###### [creator](https://github.com/Emc2356)
###### [PyGame](https://pygame.org/) 

##### this is a package created to help you with pygame functionality 

##### at this point it has the following classes:
| Class name |
|:----------:|
|[Button](./Documentation/Button.md) |
|[SimpleText](./Documentation/SimpleText.md) |
| [MultiLineText](./Documentation/MultiLineText.md) |
| [InputField](./Documentation/InputField.md) |
| [InputFieldNumbers](./Documentation/InputFieldNumbers.md) |
| [InputFieldLetters](./Documentation/InputFieldLetters.md) |
| [Particle](./Documentation/Particle.md) |
| [Animation](./Documentation/Animation.md) |
| [SpriteSheet](./Documentation/SpriteSheet.md) |
| [Font](./Documentation/Font.md) |

##### also, PygameHelper, offers functions::
| Function name | description | cached |
|:-------------:|:-----------:|:------:|
| `load_image` | it loads an image from a given path and it performs .convert() | True |
| `load_alpha_image` | it loads an image from a given path and it performs .convert_alpha() | True |
| `resize_smooth_image` | wrapper for pygame.transform.smoothscale | False |
| `resize_image` | wrapper for pygame.transform.scale | False |
| `resize_image_ratio` | - | False |
| `resizex` | it resizes a image in both axis by the same amount | False |
| `left_click` | it checks for the left-click event  | False |
| `middle_click` | it checks for the middle-click event  | False |
| `right_click` | it checks for the right-click event  | False |
| `get_font` | it returns a font | True |
| `wrap_multi_lines` |  | True |
| `blit_multiple_lines` | it blits in a surface a list of strings | False |
| `pixel_perfect_collision` | it is a wrapper for pygame.mask.overlap and it handles the offset | False |
| `get_distance` | it calculates the distance between two points | True |
| `flatten` | it takes a iterable object and it flattens the object | False |
| `get_cloth` | it returns the cloth data from a file (basically a json reader) | False |
| `clamp` | it clamps a value between two values | False |
| `remap` | it Re-maps a number from one range to another | False |
| `lerp` |  Calculates a number between two numbers at a specific increment | False |
| `quadratic_bezier` | Quadratic bezier curve (1 static, 1 control and 1 static point) | False |
| `bezier` | it creates a bezier curve based on 4 points (1 static, 2 control points an 1 static) aka a cubic bezier | False |
| `get_neighbors` | it returns the directly adjacent cells (it makes the assumption that it has rows of the same length) | False |
| `get_neighbors_index` | it returns the directly adjacent cells index (it makes the assumption that it has rows of the same length) | False |
| `pathfinding` | if finds the most efficient path from 1 point to another | False |

##### TODO list (at this point this is a joke lmao)
~~~
1. add a menu class
   * add a menu class for building menus
   * it will accept managers
2. add a dropdown class
   * dropdowns will have an animation when clicked
   * it will change color when the mouse is over an option
   * won't have support for multi-line text
   * the options will be instances of the button class
3. add sliders
~~~

# Documentation
##### Documentation for the classes can be found in [./Documentation](./Documentation)

# Examples
##### Examples of the classes and functions can be found in [./Examples](./Examples)

# NOTES
> in commit 73 I accidentally pushed everything in 1 batch, and they have wrong titles  

# contributions:
---
> Pull requests are welcome!  
> Feel free to create a fork of this repository and use the code for any purpose. Credit is appreciated but not needed.
