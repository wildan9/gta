#   Copyright (c) 2024 Wildan R Wijanarko
#
#   Permission is hereby granted, free of charge, to any person obtaining a copy
#   of this software and associated documentation files (the "Software"), to deal
#   in the Software without restriction, including without limitation the rights
#   to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#   copies of the Software, and to permit persons to whom the Software is
#   furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in all
#   copies or substantial portions of the Software.
#
#   THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#   IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#   FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#   AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#   LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#   OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#   SOFTWARE.

from raylibpy import *
from player import *
from camera import *
from car import *

class Engine():
    def __init__(self):
        self.in_car = False

    def run(self):
        screen_width = 640
        screen_height = 480

        set_config_flags(FLAG_MSAA_4X_HINT)
        init_window(screen_width, screen_height, "GTA")
        set_target_fps(60)

        map_model = load_model("resources/gta_2_maps.glb")
        player = Player()
        car = Car()

        map_model.transform = matrix_multiply(map_model.transform, matrix_rotate_zyx(quaternion_to_euler(quaternion_normalize(Quaternion(0.0, 7.20, 7.20, 0.0)))))

        camera = CameraTP(45, Vector3(1, 0, 1))

        def update():
            camera.update(player.pos)

            if check_collision_boxes(player.bounding_box, car.bounding_box) and is_key_pressed(KEY_ENTER):
                self.in_car = not self.in_car
                if self.in_car:
                    print("Entering")
                else:
                    print("Exiting")

            player.update(self.in_car, car)
            car.update(player.rot_radians, player.pos, self.in_car)

        def render():
            begin_drawing()
            camera.begin_mode_3d()

            clear_background(BLACK)
            player.draw()
            car.draw()

            draw_model(map_model, Vector3(0, 0, 0), 1.0, WHITE)
            draw_grid(24, 24)

            camera.end_mode_3d()
            
            camera_target_str = str(round(camera.view_camera.pos.x)) + " " + str(round(camera.view_camera.pos.y)) + " " + str(round(camera.view_camera.pos.z))
            draw_text(camera_target_str, 10, screen_height - 50, 12, WHITE)
            end_drawing()

        while not window_should_close():
            update()
            render()

        unload_model(map_model)
        close_window()

if __name__ == '__main__':
    engine = Engine()
    engine.run()