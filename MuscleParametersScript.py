# Computes the muscle paramteres of fascicularis macaca model from a human model (optimal
#   fiber length, tendon slack length and maximum isometric force

# author : Romain Donzé (romain.donze@epfl.ch)

import opensim
import sys

generic_model_file = 'gait2392_simbody.osim'
monkey_model_file = 'MonkeyLegsMillardMuscles.osim'
# Need to change the respective heights of these models
height_generic = 1.80
model_generic = opensim.Model(generic_model_file)
state_generic = model_generic.initSystem()
mass_generic = model_generic.getTotalMass(state_generic)

model_monkey = opensim.Model(monkey_model_file)
state_monkey = model_monkey.initSystem()

# formula for total muscle volume
V_total_generic = 47.05 * mass_generic * height_generic + 1289.6
# Volume approximated from CT scan total volume without bones, assuming 10% of the volume to be soft tissues
V_total_monkey = 0.001313*0.9*(10**6)
#1.84e-5 + 2.3e-5 + 2.5e-4 + 2.7e-4 + 8.1e-5 + 6.6e-5 + 6.05e-4
generic_muscles = []

# Important : You want the name of the muscles in both models to be similar for them to be treated !
# Get all of the muscles of the generic model in a list
for i in range(0, model_generic.getMuscles().getSize()):
    muscle_generic = model_generic.updMuscles().get(i)
    name = muscle_generic.getName()
    generic_muscles.append(name)

monkey_muscles = []

# Get all of the muscles of the monkey model in a list
for j in range(0, model_monkey.getMuscles().getSize()):
    muscle_monkey = model_monkey.updMuscles().get(j)
    name = muscle_monkey.getName()
    monkey_muscles.append(name)

for k in range(len(monkey_muscles)):
    # Find the name of the wanted muscle
    muscle_name = monkey_muscles[k]
    # Go through the generic_muscles and find the corresponding muscle
    nuMuscle = False
    for l in range(len(generic_muscles)):
        if generic_muscles[l] == muscle_name :
            generic_index = l
            break
        if l == len(generic_muscles) -1:
            nuMuscle = True

            print("Generic Model has no muscle named : ", muscle_name)
    # Take the report of length between the two muscles : 
    if nuMuscle == False :
        # Get the two muscles
        muscle_monkey = model_monkey.getMuscles().get(k)
        muscle_generic = model_generic.getMuscles().get(l)
        length_scale_factor = muscle_monkey.getLength(state_monkey)/muscle_generic.getLength(state_generic)
        # Get the new OptimalFiberLength and TendonSlackLength
        newOptimalFiberLength = muscle_generic.getOptimalFiberLength()*length_scale_factor
        muscle_monkey.setOptimalFiberLength(newOptimalFiberLength)
        newTendonSlackLength = muscle_generic.getTendonSlackLength()*length_scale_factor
        muscle_monkey.setTendonSlackLength(newTendonSlackLength)
        # Set the Maximal Isometric Force
        l0_generic = muscle_generic.getOptimalFiberLength()
        l0_monkey = newOptimalFiberLength
        force_scale_factor = (V_total_monkey / V_total_generic) / (l0_monkey / l0_generic)
        muscle_monkey.setMaxIsometricForce(muscle_generic.getMaxIsometricForce()*force_scale_factor)
        # Set the rigid tendon model
        muscle_monkey.set_ignore_tendon_compliance(True)
        #print("{} & {:.4f} & {:.4f} & {:.4f} & {:.4f} & {:.4f} & {:.4f} & {:.4f} & {:.4f}".format(muscle_monkey.getName(), newOptimalFiberLength, newTendonSlackLength, 
        #        muscle_generic.getMaxIsometricForce()*force_scale_factor, muscle_generic.getOptimalFiberLength(), 
        #        muscle_generic.getTendonSlackLength(), muscle_generic.getMaxIsometricForce(), length_scale_factor, force_scale_factor))

# Print the changes to the file
model_monkey.printToXML(monkey_model_file)
print("END OF FILE")