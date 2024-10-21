import ROOT
import os

def split_root_file(input_file, output_prefix, events_per_file=10000):
    # Open the input ROOT file
    input_f = ROOT.TFile.Open(input_file)
    # Get the 'Events' tree from the input file
    input_tree = input_f.Get("Events")

    # Get the total number of events in the tree
    total_events = input_tree.GetEntries()
    print("Total events in {}: {}".format(input_file, total_events))

    # Initialize a counter for output file naming
    file_count = 0

    # Loop through the events in chunks of 'events_per_file'
    for start_event in range(0, total_events, events_per_file):
        # Create a new output ROOT file for each chunk
        output_file = "{}_{}.root".format(output_prefix, file_count)
        output_f = ROOT.TFile(output_file, "RECREATE")
        # Clone an empty tree structure from the original tree
        output_tree = input_tree.CloneTree(0)

        # Loop through the events in the current chunk
        for i in range(start_event, min(start_event + events_per_file, total_events)):
            # Copy the current event to the new tree
            input_tree.GetEntry(i)
            output_tree.Fill()

        # Write the new tree to the output file and close the file
        output_f.Write()
        output_f.Close()

        print("Created {} with events {} to {}".format(
            output_file, start_event, min(start_event + events_per_file, total_events) - 1))

        # Increment the file counter for the next output file
        file_count += 1

    # Close the input ROOT file
    input_f.Close()


# Base directory where the input files are located
#input_directory = "/xrootd_user/seungjun/xrootd/nano/root/0_90em/"
input_directory = "/xrootd_user/seungjun/xrootd/nano/root/1_10em/"

# Process lhe_0.root to lhe_49.root
for i in range(50):
    # Using format() instead of f-string for compatibility with older Python versions
    input_file = os.path.join(input_directory, "lhe_{}.root".format(i))  # Input file path
    output_prefix = os.path.join(input_directory, "lhe_root_{}".format(i))  # Output prefix for each file
    split_root_file(input_file, output_prefix)
    os.system("rm {}".format(input_file))

num = 0
for filename in os.listdir(input_directory):
    old_file = os.path.join(input_directory, filename)
    
    if os.path.isfile(old_file):
        new_filename = "lhe_"+str(num)+".root"
        new_file = os.path.join(input_directory, new_filename)
        
        os.rename(old_file, new_file)
        print("Renamed: {} -> {}".format(old_file, new_file))
        num +=1

