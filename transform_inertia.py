import sys
import trimesh

def transform(mesh):
    T = mesh.principal_inertia_transform
    print("Transform = ((",T[0,0],",",T[1,0],",",T[2,0],",",T[3,0],"),",
    "(",T[0,1],",",T[1,1],",",T[2,1],",",T[3,1],"),",
    "(",T[0,2],",",T[1,2],",",T[2,2],",",T[3,2],"),",
    "(",T[0,3],",",T[1,3],",",T[2,3],",",T[3,3],"))")
    print("import bpy")
    print("bpy.context.object.matrix_world = Transform")

if __name__ == "__main__":
    mesh = trimesh.load(sys.argv[1])
    transform(mesh)