import numpy as np

def split_data():
  '''
  Script writes the all.dta dataset into base, valid, hidden, probe sets
  using the indices in all.idx.

  Outputs: None
  '''

  print("Processing \'um\' data...")
  with open("../data/um/all.dta", 'r') as all, \
  open("../data/um/all.idx", 'r') as i_file, \
  open("../data/um/base.dta", 'w+') as base, \
  open("../data/um/valid.dta", 'w+') as valid, \
  open("../data/um/hidden.dta", 'w+') as hidden, \
  open("../data/um/probe.dta", 'w+') as probe:

    print("Loading indices...")
    indices = np.loadtxt(i_file, delimiter = '\n')
    print("Finished loading indices.")

    print("Splitting dataset...")
    for i, line in enumerate(all):
        if indices[i] == 1:
            base.write(line)
        elif indices[i] == 2:
            valid.write(line)
        elif indices[i] == 3:
            hidden.write(line)
        elif indices[i] == 4:
            probe.write(line)
        else:
            pass

    print("Finished splitting dataset.")

    print("Processing \'mu\' data...")
    with open("../data/mu/all.dta", 'r') as all, \
    open("../data/mu/all.idx", 'r') as i_file, \
    open("../data/mu/base.dta", 'w+') as base, \
    open("../data/mu/valid.dta", 'w+') as valid, \
    open("../data/mu/hidden.dta", 'w+') as hidden, \
    open("../data/mu/probe.dta", 'w+') as probe:
        print("Loading indices...")
        indices = np.loadtxt(i_file, delimiter = '\n')
        print("Finished loading indices.")

        print("Splitting dataset...")
        for i, line in enumerate(all):
            if indices[i] == 1:
                base.write(line)
            elif indices[i] == 2:
                valid.write(line)
            elif indices[i] == 3:
                hidden.write(line)
            elif indices[i] == 4:
                probe.write(line)
            else:
                pass

        print("Finished splitting dataset.")

    return

# Example usage of load_data
split_data()
