def parse_XYZ(filename):
    #Check that filename ends in .xyz
    if filename[-4:] != ".xyz":
        print("Error: File must have .xyz file extension")
        return
    
    #Open file
    file = open(filename, "r")

    #Read first line
    numAtoms = file.readline()
    numAtoms = int(numAtoms)

    #Read lines of file
    atoms = []
    atomicSpecies = []
    for line in file:
        #Split line into list
        line = line.split()

        if len(line) == 0:
            continue
        elif len(line) != 4:
            continue

        atom = {
            "element": line[0],
            "x": float(line[1]),
            "y": float(line[2]),
            "z": float(line[3])
        }

        if atom['element'] not in atomicSpecies:
            atomicSpecies.append(atom['element'])
        atoms.append(atom)

    #Close file
    file.close()

    if len(atoms) != numAtoms:
        print("Error: Number of atoms does not match number of atoms in file")
        return

    return atoms, atomicSpecies