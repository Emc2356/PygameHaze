# QuadTree

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/PygameHelper)

#### this is a QuadTree data structure with the [pygame](https://www.pygame.org)
> these are the mandatory arguments

| Argument | Description | Type |
|:--------:|:-----------:|:----:|
| `space` | the location of the QuadTree | pygame.Rect |
| `capacity` | how many objects can it handle | int |

> methods

| name | description | arguments |
|:-----:|:----------:|:---------:|
| `get_items` | it returns all of the objects of the QuadTree | - |
| `list_insert` | it inserts a list of objects in the QuadTree | objs: List[Any] |
| `insert` | it inserts a object on the QuadTree (it needs to have a .pos attribute) | obj: Any |
| `query` | it returns all of the objects that can be found in a given area | rectangle: pygame.Rect |
