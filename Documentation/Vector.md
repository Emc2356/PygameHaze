# Vector

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/PygameHelper)

#### this is a Vector class similarly to [pygame.math.Vector2](https://www.pygame.org/docs/ref/math.html#pygame.math.Vector2) [pygame](https://www.pygame.org)
> these are arguments  

| Argument | Description | Default Value |
|:--------:|:-----------:|:-------------:|
| `x` | the x value of the Vector (as it is the first argument it can be a tuple, list, another vector or a number) | 0 |
| `y` | the y value of the Vector | 0 |

> methods

| name | description | arguments |
|:-----:|:----------:|:---------:|
| `add()` | it adds a value to the Vector | x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING |
| `sub()` | it subtracts a value to the Vector | x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING |
| `mul()` | it multiplies a value to the Vector | x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING |
| `div()` | it divides a value to the Vector | x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING |
| `dot()` | it calculates the dot product of two vectors | x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING |
| `cross()` | it calculates the Z value of the cross product from 2 Vectors | x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING |
| `lerp()` | linear interpolate between 2 Vectors | x: Optional[Union[float, pygame.math.Vector2, Vector, Tuple[float, float], List[float]]], y: Optional[float]=_MISSING |
| `distance()` | it calculates the Euclidean distance between two Vectors | target: Union[pygame.math.Vector2, Vector, Tuple[Union[int, float], Union[int, float]], List[Union[int, float]]] |
| `copy()` | it returns a copy of the vector | - |
| `tostring` | it turns a Vector into string form | - |
| `staticmethod(fromstring)` | it returns a Vector from a string | string: str |
| `normalize()` | it normalizes the vector to length 1 (make it a unit vector) | - |
| `property(mag_sq)` | it returns the magnitude of the vector squared | - |
| `property(mag)` | it returns the magnitude of the vector | - |
| `property(mag).setter` | it sets the magnitude of the vector | val: Union[int, float] |
| `set_mag()` | it sets the magnitude of the vector (same as instance.mag = value but it returns self to stack chain) | val: Union[int, float] |
| `limit` | it limits the magnitude of the Vector | maxV: Union[int, float] |
| `rotate` | it rotates the vector | angle: Union[int, float] |
| `property(heading)` | it calculate the angle of rotation for the vector | - |
| `property(heading).setter` | it sets the heading of the Vector (in degrees) | Union[int, float] |
| `staticmethod(from_angle)` | it makes a Vector from a given angle in degrees or radians | angle: Union[int, float], length: Union[int, float]=1, degrees=True |
| `staticmethod(random)` | it creates a random vector | - |
| `staticmethod(from_polar)` | it creates a Vector from polar coordinates | r: Union[int, float], theta: Union[int, float], degrees=True |
| `polar()` | it sets the Vectors coordinates based on polar coordinates | r: Union[int, float], theta: Union[int, float], degrees=True |
