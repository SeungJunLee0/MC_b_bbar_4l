import ROOT

def split_root_file(input_file, output_prefix, events_per_file=10000):
    # Open the input ROOT file
    input_f = ROOT.TFile.Open(input_file)
    # Get the 'Events' tree from the input file
    input_tree = input_f.Get("Events")

    # Get the total number of events in the tree
    total_events = input_tree.GetEntries()
    print("Total events: {}".format(total_events))

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

# Example of how to call the function
input_file = "lhe_0.root"  
output_prefix = "lhe_root" 
split_root_file(input_file, output_prefix)

