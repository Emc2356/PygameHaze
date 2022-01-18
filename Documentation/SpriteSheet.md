# SpriteSheet

#### [creator](https://github.com/Emc2356)
#### [source code](https://github.com/Emc2356/PygameHazel)

#### this is a class made for creating spritesheets with the [pygame](https://www.pygame.org)

| Argument | Description | Default Value |
|:--------:|:-----------:|:-------------:|
| `path` | the path for the image that is going to be used | - |
| `colorkey_for_char` | the colorkey for the sheet -1 sets the colorkey as the pixel color of [0, 0] | None |

> methods

| name | description | arguments |
|:--------:|:-----------:|:-------------:|
| `get_sheet` | it returns the sheet | - |
| `clip` | it returns the image in a specified location | [x, y, w, h], colorkey |
