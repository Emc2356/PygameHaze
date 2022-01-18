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
