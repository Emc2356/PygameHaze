# PygameHaze

links:
  - [source code](https://github.com/Emc2356/PygameHaze)
  - [creator](https://github.com/Emc2356)
  - [PyGame](https://pygame.org/)

PygameHaze is a package that is designed to help with game dev using pygame
it offers some gui elements that are used a lot a, also it has some function that are handy with pygame

PygameHaze is designed to have minimal dependencies, (only pygame & numpy) but to get some extra performance there is 
optional [numba](https://numba.pydata.org/) dependency

##### some functions:
| Function name | description | cached | Numba jit capability |
|:-------------:|:-----------:|:------:|:------------:|
| `load_image` | it loads an image from a given path and it performs .convert() | True | False |
| `load_alpha_image` | it loads an image from a given path and it performs .convert_alpha() | True | False |
| `resize_smooth_image` | wrapper for pygame.transform.smoothscale | False | False |
| `resize_image` | wrapper for pygame.transform.scale | False | False |
| `resize_image_ratio` | - | False | False |
| `resizex` | it resizes a image in both axis by the same amount | False | False |
| `left_click` | it checks for the left-click event  | False | False |
| `middle_click` | it checks for the middle-click event  | False | False |
| `right_click` | it checks for the right-click event  | False | False |
| `get_font` | it returns a font | True | False |
| `wrap_multi_lines` |  | True | False |
| `blit_list` | it blits in a surface a list of strings | False | False |
| `pixel_perfect_collision` | it is a wrapper for pygame.mask.overlap and it handles the offset | False | False |
| `flatten` | it takes a iterable object and it flattens the object | False | False |
| `get_cloth` | it returns the cloth data from a file (basically a json reader) | False | False |
| `get_neighbors` | it returns the directly adjacent cells (it makes the assumption that it has rows of the same length) | False | False |
| `get_neighbors_index` | it returns the directly adjacent cells index (it makes the assumption that it has rows of the same length) | False | False |
| `pathfinding` | if finds the most efficient path from 1 point to another | False | False |
| `combine_rects` | it creates the smallest possible rect that contains all of the rects | False | False |
| `save_frame` | it saves the pixels from a pygame surface into a specified file, if unspecified it defaults to the pygame window | False | False |
| `lerp` | Calculates a number between two numbers at a specific increment |  False | True |
| `clamp` | it clamps a value between mini and maxi | False | True |
| `remap` | it Re-maps a number from one range to another (nothing to do with regex it is just the name) | False | True |
| `get_distance` | it returns the distance between two points | False | True |
| `get_distance_squared` | it returns the distance squared between two points | False | True |

##### some drawing utils  
##### they are wrapping `pygame.draw` but with some extra functionality
| Function name | description |
|:-------------:|:-----------:|
| `draw.push` | it saves the current draw location |
| `draw.translate` | it moves the current draw location |
| `draw.pop` | it goes to the previous draw location |
| `draw.quadratic_bezier` | Quadratic bezier curve (1 static, 1 control and 1 static point) |
| `draw.bezier` | it creates a bezier curve based on 4 points (1 static, 2 control points an 1 static) aka a cubic bezier |
| `draw.beginShape` | it begins tracing the vertices |
| `draw.vertex` | it adds a new vertex |
| `draw.endShape` | it stops tracing the vertices and draw the shape |
| `draw.rect` | a wrapper for `pygame.draw.rect` but it takes advantage of the position from translate |
| `draw.polygon` | a wrapper for `pygame.draw.polygon` but it takes advantage of the position from translate |
| `draw.circle` | a wrapper for `pygame.draw.circle` but it takes advantage of the position from translate |
| `draw.ellipse` | a wrapper for `pygame.draw.ellipse` but it takes advantage of the position from translate |
| `draw.arc` | a wrapper for `pygame.draw.arc` but it takes advantage of the position from translate |
| `draw.line` | a wrapper for `pygame.draw.line` but it takes advantage of the position from translate |
| `draw.lines` | a wrapper for `pygame.draw.lines` but it takes advantage of the position from translate |
| `draw.aaline` | a wrapper for `pygame.draw.aaline` but it takes advantage of the position from translate |
| `draw.aalines` | a wrapper for `pygame.draw.aalines` but it takes advantage of the position from translate |

# Documentation
##### Documentation for the classes can be found in [./Documentation](./Documentation)

# Examples
##### Examples of the classes and functions can be found in [./Examples](./Examples)

contributions:
---
> Pull requests are welcome!  
> Feel free to create a fork of this repository and use the code for any purpose. Credit is appreciated but not needed.
