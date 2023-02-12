#!/usr/bin/python3
import math
import pathlib
import sys

from py3d.effects.additive_blend import AdditiveBlendEffect
from py3d.effects.horizontal_blur import HorizontalBlurEffect
from py3d.effects.vertical_blur import VerticalBlurEffect
from py3d.extras.postprocessor import Postprocessor
from py3d.light.ambient import AmbientLight
from py3d.light.directional import DirectionalLight
from py3d.light.point import PointLight
from py3d.material.flat import FlatMaterial
from py3d.material.lambert import LambertMaterial
from py3d.material.phong import PhongMaterial

# Get the package directory
package_dir = str(pathlib.Path(__file__).resolve().parents[2])
# Add the package directory into sys.path if necessary
if package_dir not in sys.path:
    sys.path.insert(0, package_dir)

from py3d.core.base import Base
from py3d.core_ext.camera import Camera
from py3d.core_ext.mesh import Mesh
from py3d.core_ext.render_target import RenderTarget
from py3d.core_ext.renderer import Renderer
from py3d.core_ext.scene import Scene
from py3d.core_ext.texture import Texture
from py3d.geometry.box import BoxGeometry
from py3d.geometry.rectangle import RectangleGeometry
from py3d.geometry.sphere import SphereGeometry
from py3d.material.surface import SurfaceMaterial
from py3d.material.texture import TextureMaterial
from py3d.extras.movement_rig import MovementRig


class Example(Base):

    def __init__(self, screen_size=(512, 512)):
        super().__init__(screen_size)

    def initialize(self):
        print("Initializing program...")
        self.renderer = Renderer()
        self.scene = Scene()
        self.camera = Camera(aspect_ratio=800/600)
        self.rig = MovementRig()
        self.rig.add(self.camera)
        self.scene.add(self.rig)
        self.rig.set_position([0, 1, 4])
        sky_geometry = SphereGeometry(radius=50)
        sky_material = TextureMaterial(texture=Texture(file_name="images/dark_sky.jpg"))
        sky = Mesh(sky_geometry, sky_material)
        self.scene.add(sky)

        # The Sun's lighting effect
        point_light1 = PointLight(color=[0.9, 0.9, 0], position=[1.5, 0, 1.5], attenuation=[0.1,0,0.1])
        self.scene.add(point_light1)
        point_light2 = PointLight(color=[0.9, 0.9, 0], position=[-1.5, 0, 1.5], attenuation=[0.1,0,0.1])
        self.scene.add(point_light2)
        point_light3 = PointLight(color=[0.9, 0.9, 0], position=[-1.5, 0, -1.5], attenuation=[0.1,0,0.1])
        self.scene.add(point_light3)
        point_light4 = PointLight(color=[0.9, 0.9, 0], position=[1.5, 0, -1.5], attenuation=[0.1,0,0.1])
        self.scene.add(point_light4)
        point_light5 = PointLight(color=[0.9, 0.9, 0], position=[0, 2,0], attenuation=[0.1,0,0.1])
        self.scene.add(point_light5)
        point_light6 = PointLight(color=[0.9, 0.9, 0], position=[0, -2,0], attenuation=[0.1,0,0.1])
        self.scene.add(point_light6)

        # textures materials
        textured_flat_earth = FlatMaterial(
            texture=Texture("images/earth.jpg"),
            number_of_light_sources=6
        )
        textured_lambert_earth = LambertMaterial(
            texture=Texture("images/earth.jpg"),
            number_of_light_sources=6
        )
        textured_phong_earth = PhongMaterial(
            texture=Texture("images/earth.jpg"),
            number_of_light_sources=6
        )
        textured_phong_sun = PhongMaterial(
            texture=Texture("images/sun.jpg"),
            number_of_light_sources=6

        )

        #Sun Object
        sun = SphereGeometry()
        self.sun = Mesh(sun, textured_phong_sun)
        self.sun.set_position([0, 0, 0])
        self.scene.add(self.sun)

        #Earth Object
        Earth = SphereGeometry()
        self.earth = Mesh(Earth, textured_flat_earth)
        self.earth.set_position([8, 0, 0])
        self.scene.add(self.earth)

        # # Uncomment for glow effect
        #
        # self.postprocessor = Postprocessor(self.renderer, self.scene, self.camera)
        #
        # # glow scene.
        # self.glow_scene = Scene()
        # yellow_material = SurfaceMaterial(property_dict={"baseColor": [1, 1, 0]})
        # glow_sphere = Mesh(sun, yellow_material)
        # glow_sphere.local_matrix = self.sun.local_matrix
        # self.glow_scene.add(glow_sphere)
        #
        # # glow postprocessing
        # glow_target = RenderTarget(resolution=[800, 600])
        # self.glow_pass = Postprocessor(self.renderer, self.glow_scene, self.camera, glow_target)
        # self.glow_pass.add_effect(HorizontalBlurEffect(texture_size=[800, 600], blur_radius=50))
        # self.glow_pass.add_effect(VerticalBlurEffect(texture_size=[800, 600], blur_radius=50))
        #
        # # combining results of glow effect with main scene
        # self.combo_pass = Postprocessor(self.renderer, self.scene, self.camera)
        # self.combo_pass.add_effect(
        #     AdditiveBlendEffect(
        #         blend_texture=glow_target.texture,
        #         original_strength=1,
        #         blend_strength=3
        #     )
        # )


    def update(self):
        self.sun.rotate_y(0.00233) # Sun rotation around itself

        # Earth rotation around itself and around the sun
        self.earth.translate(-0.01, 0, -0.08)
        self.earth.rotate_y(0.01337)

        self.rig.update(self.input, self.delta_time)
        self.renderer.render(self.scene, self.camera)

        ## Uncomment for glow effect
        # self.glow_pass.render()
        # self.combo_pass.render()

# Instantiate this class and run the program
Example(screen_size=[800, 600]).run()
