import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="Main Window", width=1000, height=600):
    with dpg.group(horizontal=True):

        # Left Window
        with dpg.child_window(width=320):
            dpg.add_text("Input the common name of the animal to get its scientific name, accession number, and DNA sequence.", wrap=300)
            dpg.add_spacer(height=10)
            dpg.add_text("Input the animal: ")
            animal_input = dpg.add_input_text(default_value="Input your common animal name here...")
            dpg.add_button(label="Search", callback=lambda: print("Button Clicked!"))

            dpg.add_separator()

            scientific_name_text = dpg.add_text("Scientific Name: ")
            dna_sequence_text = dpg.add_text("DNA Sequence: ")


        # Right Window
        with dpg.child_window():
            dpg.add_text("Vizualization of the DNA sequence will be shown here.")



dpg.create_viewport(title='Animal DNA', width=1000, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()