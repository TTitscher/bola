import gmsh

geo = gmsh.model.geo

gmsh.initialize()


def rectangle(xs, xe, mesh_size=0.1):
    """
    Rectangle from start point `xs` to end point `xe` with a
    given `mesh_size`.
    """
    ms = mesh_size
    p0 = geo.add_point(xs[0], xs[1], 0, ms)
    p1 = geo.add_point(xe[0], xs[1], 0, ms)
    p2 = geo.add_point(xe[0], xe[1], 0, ms)
    p3 = geo.add_point(xs[0], xe[1], 0, ms)

    l0 = geo.add_line(p0, p1)
    l1 = geo.add_line(p1, p2)
    l2 = geo.add_line(p2, p3)
    l3 = geo.add_line(p3, p0)

    loop = gmsh.model.geo.add_curve_loop([l0, l1, l2, l3])
    return loop


def cuboid(xs, xe, mesh_size=0.1):
    """
    Cuboid from start point `xs` to end point `xe` with a
    given `mesh_size`.
    """
    ms = mesh_size
    # top points: z = ze
    p0 = geo.add_point(xs[0], xs[1], xe[2], ms)
    p1 = geo.add_point(xs[0], xe[1], xe[2], ms)
    p2 = geo.add_point(xe[0], xe[1], xe[2], ms)
    p3 = geo.add_point(xe[0], xs[1], xe[2], ms)
    # bottom points z = zs
    p4 = geo.add_point(xs[0], xs[1], xs[2], ms)
    p5 = geo.add_point(xs[0], xe[1], xs[2], ms)
    p6 = geo.add_point(xe[0], xe[1], xs[2], ms)
    p7 = geo.add_point(xe[0], xs[1], xs[2], ms)

    # top lines z = zs
    lT0 = geo.add_line(p0, p1)
    lT1 = geo.add_line(p1, p2)
    lT2 = geo.add_line(p2, p3)
    lT3 = geo.add_line(p3, p0)
    # bottom lines z = ze
    lB0 = geo.add_line(p4, p5)
    lB1 = geo.add_line(p5, p6)
    lB2 = geo.add_line(p6, p7)
    lB3 = geo.add_line(p7, p4)
    # connection zs --> ze
    lC0 = geo.add_line(p0, p4)
    lC1 = geo.add_line(p1, p5)
    lC2 = geo.add_line(p2, p6)
    lC3 = geo.add_line(p3, p7)

    # lineloops and surfaces
    s0 = geo.add_plane_surface([geo.add_curve_loop([-lT3, lC3, lB3, -lC0])])
    s1 = geo.add_plane_surface([geo.add_curve_loop([-lT1, lC1, lB1, -lC2])])
    s2 = geo.add_plane_surface([geo.add_curve_loop([-lT0, lC0, lB0, -lC1])])
    s3 = geo.add_plane_surface([geo.add_curve_loop([-lT2, lC2, lB2, -lC3])])
    s4 = geo.add_plane_surface([geo.add_curve_loop([lT0, lT1, lT2, lT3])])
    s5 = geo.add_plane_surface([geo.add_curve_loop([-lB3, -lB2, -lB1, -lB0])])

    return geo.add_surface_loop([s0, s1, s2, s3, s4, s5])


def circle(xc, r, mesh_size=0.1):
    """
    geo.add_circle_arc with center `xc`, radius `r` and a given `mesh_size`.
    """
    ms = mesh_size
    p0 = gmsh.model.geo.add_point(xc[0], xc[1], 0, ms)
    p1 = gmsh.model.geo.add_point(xc[0] + r, xc[1], 0, ms)
    p2 = gmsh.model.geo.add_point(xc[0] - r, xc[1], 0, ms)

    c0 = gmsh.model.geo.add_circle_arc(p1, p0, p2)
    c1 = gmsh.model.geo.add_circle_arc(p2, p0, p1)

    loop = gmsh.model.geo.add_curve_loop([c0, c1])
    surface = gmsh.model.geo.add_plane_surface([loop])

    return loop, surface


def sphere(xc, r, mesh_size=0.1):
    """
    Sphere with center `xc`, radius `r` and a given `mesh_size`.
    """
    ms = mesh_size
    p0 = geo.add_point(xc[0], xc[1], xc[2], ms)
    p1 = geo.add_point(xc[0] + r, xc[1], xc[2], ms)
    p2 = geo.add_point(xc[0], xc[1] + r, xc[2], ms)
    p3 = geo.add_point(xc[0], xc[1], xc[2] + r, ms)
    p4 = geo.add_point(xc[0] - r, xc[1], xc[2], ms)
    p5 = geo.add_point(xc[0], xc[1] - r, xc[2], ms)
    p6 = geo.add_point(xc[0], xc[1], xc[2] - r, ms)

    c0 = geo.add_circle_arc(p1, p0, p6)
    c1 = geo.add_circle_arc(p6, p0, p4)
    c2 = geo.add_circle_arc(p4, p0, p3)
    c3 = geo.add_circle_arc(p3, p0, p1)
    c4 = geo.add_circle_arc(p1, p0, p2)
    c5 = geo.add_circle_arc(p2, p0, p4)
    c6 = geo.add_circle_arc(p4, p0, p5)
    c7 = geo.add_circle_arc(p5, p0, p1)
    c8 = geo.add_circle_arc(p6, p0, p2)
    c9 = geo.add_circle_arc(p2, p0, p3)
    c10 = geo.add_circle_arc(p3, p0, p5)
    c11 = geo.add_circle_arc(p5, p0, p6)

    s0 = geo.add_plane_surface([geo.add_curve_loop([c4, c9, c3])])
    s1 = geo.add_plane_surface([geo.add_curve_loop([c8, -c4, c0])])
    s2 = geo.add_plane_surface([geo.add_curve_loop([c11, -c7, -c0])])
    s3 = geo.add_plane_surface([geo.add_curve_loop([c7, -c3, c10])])
    s4 = geo.add_plane_surface([geo.add_curve_loop([-c9, c5, c2])])
    s5 = geo.add_plane_surface([geo.add_curve_loop([-c10, -c2, c6])])
    s6 = geo.add_plane_surface([geo.add_curve_loop([-c1, -c6, -c11])])
    s7 = geo.add_plane_surface([geo.add_curve_loop([-c5, -c8, c1])])

    loop = geo.add_surface_loop([s0, s1, s2, s3, s4, s5, s6, s7])
    volume = geo.add_volume([loop])

    return loop, volume

def in2D():
    centers = [(0.25, 0.25), (0.25, 0.75), (0.75, 0.75), (0.75, 0.25)]
    r = 0.1

    loops = []
    surfaces = []

    box = rectangle((0, 0), (1, 1))

    for c in centers:
        loop, surface = circle(c, r)
        loops.append(loop)
        surfaces.append(surface)

    matrix_surface = gmsh.model.geo.add_plane_surface([box] + loops)

    gmsh.model.geo.add_physical_group(dim=2, tags=[matrix_surface], name="matrix")
    gmsh.model.geo.add_physical_group(dim=2, tags=surfaces, name="aggregates")


def in3D():
    centers = [
        (0.25, 0.25, 0.5),
        (0.25, 0.75, 0.5),
        (0.75, 0.75, 0.5),
        (0.75, 0.25, 0.5),
    ]
    r = 0.1

    loops = []
    surfaces = []

    box = cuboid((0, 0, 0), (1, 1, 1))

    for c in centers:
        loop, surface = sphere(c, r)
        loops.append(loop)
        surfaces.append(surface)

    matrix_volume = gmsh.model.geo.add_volume([box] + loops)

    gmsh.model.geo.add_physical_group(dim=3, tags=[matrix_volume], name="matrix")
    # gmsh.model.geo.add_physical_group(dim=3, tags=surfaces, name="aggregates")


in3D()

gmsh.model.geo.synchronize()

gmsh.option.set_number("Mesh.ElementOrder", 2)

gmsh.model.mesh.generate(3)
gmsh.write("out.msh")

gmsh.fltk.run()

gmsh.finalize()
