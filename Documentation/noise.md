# perlin noise

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/PygameHazel)

#### this is a function to get a part from perlin noise [pygame](https://www.pygame.org)
#### the perlin noise module takes advantage of numba jit function, if numba isn't found then it won't use the jit function, and it will default to a normal python function

## noise3D
##### a 3 dimensional perlin noise function
| parameter | type |
|:---------:|:----:|
| `x` | float |
| `y` | float |
| `z` | float |

## noise2D
##### a 2 dimensional perlin noise function 
| parameter | type |
|:---------:|:----:|
| `x` | float |
| `y` | float |

## noise1D
##### a 1 dimensional perlin noise function 
| parameter | type |
|:---------:|:----:|
| `x` | float |

## from_array
##### it calculates the perlin noise values based on the values in the array
| parameter | type |
|:---------:|:----:|
| `arr` | np.ndarray |
| `dim` | int |
| `out` | Optional\[np.ndarray\] |

## detail
##### it sets the octave count and the falloff, the defaults are -1 
| parameter | type |
|:---------:|:----:|
| `octaves` | int |
| `falloff` | float |

## set_seed
##### it sets the seed for the random values
| parameter | type |
|:---------:|:----:|
| `seed` | int |