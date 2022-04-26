import gmsh

gmsh.initialize()


def rectangle(xs, ys, xe, ye, mesh_size=0.1):
    """
    Rectangle from start point (xs, ys) to end point (xe, ye) with a
    given `mesh_size`.
    """
    ms = mesh_size
    p0 = gmsh.model.geo.add_point(xs, ys, 0, ms)
    p1 = gmsh.model.geo.add_point(xe, ys, 0, ms)
    p2 = gmsh.model.geo.add_point(xe, ye, 0, ms)
    p3 = gmsh.model.geo.add_point(xs, ye, 0, ms)

    l0 = gmsh.model.geo.add_line(p0, p1)
    l1 = gmsh.model.geo.add_line(p1, p2)
    l2 = gmsh.model.geo.add_line(p2, p3)
    l3 = gmsh.model.geo.add_line(p3, p0)

    loop = gmsh.model.geo.add_curve_loop([l0, l1, l2, l3])
    return loop


def circle(xc, yc, r, mesh_size=0.1):
    """
    Circle with center (xc, yc), radius `r` and a given `mesh_size`.
    """
    ms = mesh_size
    p0 = gmsh.model.geo.add_point(xc, yc, 0, ms)
    p1 = gmsh.model.geo.add_point(xc + r, yc, 0, ms)
    p2 = gmsh.model.geo.add_point(xc - r, yc, 0, ms)

    c0 = gmsh.model.geo.add_circle_arc(p1, p0, p2)
    c1 = gmsh.model.geo.add_circle_arc(p2, p0, p1)

    loop = gmsh.model.geo.add_curve_loop([c0, c1])
    surface = gmsh.model.geo.add_plane_surface([loop])

    return loop, surface



centers = [(0.25, 0.25), (0.25, 0.75), (0.75, 0.75), (0.75, 0.25)]
r = 0.1

loops = []
surfaces = []

box = rectangle(0, 0, 1, 1)

for c in centers:
    loop, surface = circle(*c, r)
    loops.append(loop)
    surfaces.append(surface)

matrix_surface = gmsh.model.geo.add_plane_surface([box] + loops)

gmsh.model.geo.add_physical_group(dim=2, tags=[matrix_surface], name="matrix")
gmsh.model.geo.add_physical_group(dim=2, tags=surfaces, name="aggregates")

gmsh.model.geo.synchronize()

gmsh.option.set_number("Mesh.ElementOrder", 2)

gmsh.model.mesh.generate(2)
gmsh.write("out.msh")

gmsh.fltk.run()

gmsh.finalize()





