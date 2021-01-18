import numpy as np
import trimesh
import math

# Method according to: Slabaugh, Gregory G. « Computing Euler Angles from a Rotation Matrix »
def Rotation_Matrix_To_Euler_Angles(R):
    if abs(abs(R[2,0])-1) < 1e-6:
        Rz = 0
        if R[2,0]+1 < 1e-6:
            Ry = math.pi/2
            Rx = math.atan2(R[0,1],R[0,2])
        else:
            Ry = -math.pi/2
            Rx = math.atan2(-R[0,1],-R[0,2])
    else:
        Ry = -math.asin(R[2,0])
        Rx = math.atan2(R[2,1]/math.cos(Ry), R[2,2]/math.cos(Ry))
        Rz = math.atan2(R[1,0]/math.cos(Ry), R[0,0]/math.cos(Ry))
    return np.array([Rx, Ry, Rz])

def Get_location_and_orientation_in_parent(mesh_processed, mesh_goal):
    # ---
    # Mesh_processed: mesh with its center in the center of the world, with correct axes (processed)
    # Mesh_goal: mesh positionned correctly to the parent body (as if attached).
    #            The parent body must be without transformation and resting at the center of the world
    # ---
    World_Matrix = mesh_processed.register(mesh_goal)[0]
    # Location_in_parent
    Location = World_Matrix[0:3,3]
    print("<Location_in_parent>", Location)
    # Orientation_in_parent
    Rotation_Matrix = World_Matrix[0:3,0:3].T
    Euler_Angles = Rotation_Matrix_To_Euler_Angles(Rotation_Matrix)
    print("<Orientation_in_parent>", -Euler_Angles)

# This is the axis along the bone. It should be (0 1 0) (if made correct for opensim)
y = np.array([0, 1, 0])
print(y)
print("norm =", np.linalg.norm(y))

# This is the axis found with the two points along an edge of the cylinder
# make sure to select global reference frame to get coordinates!
# To ensure it is perpendicular to the first axis, make sure at least one coordinate is zero....
front = np.array([0.003202, 0.000631, 0.006042]) #Location of the first sphere
back = np.array([-0.003202, 0.000631, -0.006042]) #Location of the second sphere

#x = back-front # !!!!!! Either one of those depending on where you want to X axis to point
x = front-back # !!!!!!

x = x / np.linalg.norm(x)
print(x)
print("norm =", np.linalg.norm(x))

# This is the third axis found with the cross product. Careful with the order of operation
# The sign on the Z axis may have to be changed if it actually corresponds to the X axis in reality
z = np.cross(x,y)
z = z / np.linalg.norm(z)
print(z)
print("norm =", np.linalg.norm(z))

# Making sure base is orthogonal
print(np.dot(y,x))
print(np.dot(y,z))
print(np.dot(x,z))

# MAY NEED CHANGE HERE (in the order)
New_Bo = np.array([z, y, x])
print(New_Bo)

Bo = np.identity(4)
Bo[0:3,0:3] = New_Bo.T
print(Bo)

# Print this to the console to check if the rotation is ok, If you wish to exchange X and Z:
# change the order in New_Bo
print("import bpy")
print("Transform = (( {},{},{},{}),({},{},{},{}),({},{},{},{}),({},{},{},{}))".format(Bo[0,0],Bo[1,0],Bo[2,0],Bo[3,0],Bo[0,1],Bo[1,1],Bo[2,1],Bo[3,1],Bo[0,2],Bo[1,2],Bo[2,2],Bo[3,2],Bo[0,3],Bo[1,3],Bo[2,3],Bo[3,3]))
print("bpy.ops.object.empty_add(type='ARROWS', location=(0, 0, 0))")
print("bpy.context.object.matrix_world = Transform")

# When ready, copy paste this while having the bone selected.
Bo[0,2] *= -1
Bo[2,0] *= -1
print("Transform = (( {},{},{},{}),({},{},{},{}),({},{},{},{}),({},{},{},{}))".format(Bo[0,0],Bo[1,0],Bo[2,0],Bo[3,0],Bo[0,1],Bo[1,1],Bo[2,1],Bo[3,1],Bo[0,2],Bo[1,2],Bo[2,2],Bo[3,2],Bo[0,3],Bo[1,3],Bo[2,3],Bo[3,3]))
print("bpy.context.object.matrix_world = Transform")