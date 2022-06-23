import os
import vtk
from vtk.util import numpy_support
import numpy as np
import time


class SphereVisualizer:
    def __init__(self, N):
        self.N = N

        self.positions = vtk.vtkPoints()
        self.diameters = vtk.vtkDoubleArray()

        for i in range(N):
            self.positions.InsertNextPoint(0.0, 0.0, 0.0)
            self.diameters.InsertNextValue(0.0)
        self.diameters.SetName("diameter")

        self.window = self._sphere_render_window()

    def add_box(self, lx, ly, lz):
        cube = vtk.vtkCubeSource()
        cube.SetXLength(lx)
        cube.SetYLength(ly)
        cube.SetZLength(lz)
        cube_mapper = vtk.vtkPolyDataMapper()
        cube_mapper.SetInputConnection(cube.GetOutputPort())
        cube_actor = vtk.vtkActor()
        cube_actor.SetMapper(cube_mapper)
        cube_actor.SetPosition(lx / 2, ly / 2, lz / 2)
        cube_actor.GetProperty().SetRepresentationToWireframe()
        self.renderer.AddActor(cube_actor)

    def _reference_sphere(self, resolution=20):
        sphere = vtk.vtkSphereSource()
        sphere.SetThetaResolution(resolution)
        sphere.SetPhiResolution(int(resolution / 2))
        sphere.SetRadius(0.5)
        return sphere

    def _sphere_render_window(self):
        grid = vtk.vtkUnstructuredGrid()
        grid.SetPoints(self.positions)
        grid.GetPointData().AddArray(self.diameters)
        grid.GetPointData().SetActiveScalars("diameter")

        sphere_source = self._reference_sphere(resolution=20)
        glyph = vtk.vtkGlyph3D()
        glyph.GeneratePointIdsOn()
        glyph.SetInputData(grid)
        glyph.SetSourceConnection(sphere_source.GetOutputPort())
        glyph.SetColorModeToColorByScalar()
        glyph.ClampingOff()
        glyph.Update()

        table = vtk.vtkLookupTable()
        lutNum = 256
        table.SetNumberOfTableValues(lutNum)
        color_transfer = vtk.vtkColorTransferFunction()
        color_transfer.SetColorSpaceToDiverging()

        def to_rgb(h):
            return [int(h[i:i+2], 16)/255 for i in (0, 2, 4)]

        color_transfer.AddRGBPoint(0.0, *to_rgb("426174"))
        color_transfer.AddRGBPoint(1.0, *to_rgb("FEED42"))
        for ii, ss in enumerate([float(xx) / float(lutNum) for xx in range(lutNum)]):
            cc = color_transfer.GetColor(ss)
            table.SetTableValue(ii, *cc, 1.0)

        self.mapper = vtk.vtkPolyDataMapper()
        self.mapper.SetInputConnection(glyph.GetOutputPort())
        self.mapper.SetLookupTable(table)
        self.mapper.ScalarVisibilityOn()
        self.mapper.SetScalarModeToUsePointData()
        self.mapper.SelectColorArray("diameter")

        actor = vtk.vtkActor()
        actor.SetMapper(self.mapper)

        # create a rendering window and renderer
        renderer = vtk.vtkRenderer()
        renderer.SetBackground(1, 1, 1)
        renderer.AddActor(actor)

        self.txt = vtk.vtkTextActor()
        self.txt.GetTextProperty().SetFontFamilyToArial()
        self.txt.GetTextProperty().SetFontSize(18)
        self.txt.GetTextProperty().SetColor(0, 0, 0)
        self.txt.SetDisplayPosition(20, 30)
        renderer.AddActor(self.txt)

        render_window = vtk.vtkRenderWindow()
        render_window.AddRenderer(renderer)
        render_window.SetSize(500, 500)

        self.renderer = renderer
        return render_window

    def update_data(self, positions, ri=None, radius_range=None):

        if ri is None:
            ri = positions[:, 3]
            positions = positions[:, :3]

        vtk_p = numpy_support.numpy_to_vtk(positions)
        self.vtk_d = numpy_support.numpy_to_vtk(
            2 * np.asarray(ri)
        )  # memory shenanigans

        if radius_range is None:
            radius_range = 2 * np.min(ri), 2 * np.max(ri)

        self.mapper.SetScalarRange(*radius_range)

        self.positions.SetData(vtk_p)
        self.diameters.SetArray(self.vtk_d, self.N, 1)

        self.positions.Modified()
        self.diameters.Modified()

    def update_txt(self, txt):
        self.txt.SetInput(txt)

    def show(self):
        interactor = vtk.vtkRenderWindowInteractor()
        interactor.SetRenderWindow(self.window)
        interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        interactor.Initialize()
        interactor.Start()
        interactor.GetRenderWindow().Finalize()

    def set_camera(self, x_camera, x_focal):
        new_camera = vtk.vtkCamera()
        new_camera.SetPosition(x_camera)
        new_camera.SetFocalPoint(x_focal)
        new_camera.SetViewUp((0, 1, 0))
        self.renderer.SetActiveCamera(new_camera)
        self.window.Render()

    def to_png(self, filename, magnification=1):
        render_image = vtk.vtkRenderLargeImage()
        image_writer = vtk.vtkJPEGWriter()
        render_image.SetInput(self.renderer)
        render_image.SetMagnification(magnification)
        image_writer.SetInputConnection(render_image.GetOutputPort())
        image_writer.SetFileName(filename)
        image_writer.Write()

        # I had a look at e.g. PIL and found nothing as convenient
        # as unix `convert`. For windows compatibility, that needs
        # to be adapted.
        os.system(f"convert -trim {filename} {filename}")


class Animation:
    def __init__(self, window, update, dt=0.02):
        self.window = window
        self.update = update
        self.interactor = vtk.vtkRenderWindowInteractor()
        self.interactor.SetRenderWindow(self.window)

        # enable user interface interactor
        self.interactor.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())
        self.interactor.Initialize()

        self.interactor.AddObserver("TimerEvent", self.update_scene)
        self.interactor.CreateRepeatingTimer(20)

        self.t = 0
        self.dt = dt
        self.timings = {"Update": 0.0, "Render": 0.0}

    def update_scene(self, *args):
        t_start = time.time()
        self.t += self.dt
        self.update(self.t)
        t_update = time.time()

        self.window.Render()
        t_render = time.time()

        self.timings["Update"] += t_update - t_start
        self.timings["Render"] += t_render - t_update

    def start(self):
        self.interactor.Start()
        self.interactor.GetRenderWindow().Finalize()


if __name__ == "__main__":
    N = 1000
    v = SphereVisualizer(N)
    v.add_box(1, 1, 1)

    x = np.random.random((N, 3))
    r = np.random.random(N) / 100

    def update(t):
        F = 0.1
        v.update_data(x + F * np.sin(t), r + 0.1 * F * (1 + np.cos(20 * t)))

    animation = Animation(v.window, update)
    animation.start()

    print(animation.timings)
