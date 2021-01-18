import sys
import trimesh
# Load the mesh
mesh=trimesh.load("Parts/L_Femur_Head.stl")
# Fit a sphere using least squares
S2 = trimesh.nsphere.fit_nsphere(mesh.vertices)
S2_location = S2[0]
S2_radius = float(S2[1])
print("import bpy")
print("bpy.ops.mesh.primitive_uv_sphere_add(radius={}, enter_editmode=False, location=({},{},{}))".format(S2_radius,S2_location[0],S2_location[1],S2_location[2]))