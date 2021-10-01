# PygameHelper

###### [source code](https://github.com/Emc2356/Pygame-Widgets)
###### [creator](https://github.com/Emc2356)
###### [PyGame](https://pygame.org/) 

##### this is a package created to help you with pygame functionality 

##### at this point it has the following classes:
| Class name |
|:----------:|
|`Button` |
|`SimpleText` |
|`MultiLineText` |
|`InputField` |
|`InputFieldNumbers` |
|`InputFieldLetters` |
|`Particle` |
|`Animation` |
|`SpriteSheet` |
|`Font` |
|`ButtonManager` |
|`TextManager` |
|`ParticleManager` |
|`AnimationManager` |
|`InputFieldManager` |

##### also, PygameHelper, offers functions to help with every day use:
| Function name | description |
|:-------------:|:-----------:|
| `load_image` | it loads an image and it does .convert() |
| `load_alpha_image` | it loads an image and it does .convert_alpha() |
| `resize_smooth_image` | wrapper for pygame.transform.smoothscale |
| `resize_image` | wrapper for pygame.transform.scale |
| `resize_image_ratio` | - |
| `resizex` | it resizes a image in both axis by the same amount |
| `left_click` | checks for left-click event the screen |
| `middle_click` | checks for middle-click event the screen |
| `right_click` | checks for right-click event the screen |
| `get_font` | it returns a font |
| `wrap_multi_lines` |  |
| `blit_multiple_lines` | it blits in a surface a list of strings |
| `pixel_perfect_collision` | it is a wrapper for pygame.mask.overlap and it handles the offset |
| `get_distance` | it returns the distance between two points |
| `flatten` | it takes a iterable object and it flattens the object |
| `get_cloth` | it returns the cloth data from a file |
| `map_num` | it Re-maps a number from one range to another |
| `clamp` | it clamps a value between mini and maxi

##### TODO list 
~~~
1. add a menu class
   * add a menu class for building menus
   * it will accept managers
2. add a dropdown class
   * dropdowns will have an animation when clicked
   * it will change color when the mouse is over an option
   * won't have support for multi-line text
   * the options will be instances of the button class
~~~

# Documentation
##### Documentation for the classes can be found in `./Documentation`

# Examples
##### Examples of the classes and functions can be found in `./Examples`

# contributions:
---
> Pull requests are welcome!
> Feel free to create a fork of this repository and use the code for any purpose.
