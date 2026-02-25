"""
This module creates a GUI using DearPyGui to visualize the DNA sequence of an animal.
The GUI allows users to input the common name of an animal, retrieves its scientific name and DNA sequence using an API, and visualizes the DNA sequence as a double helix.
The module also includes caching functionality using a SQLite database to store previously retrieved animal data for faster access.

Functions:
- draw_helix(draw_tag, dna): Draws a double helix representation of the DNA sequence on a DearPyGui drawlist.
- on_frame(): Updates the animation phase and redraws the helix on each frame.
- search_animal(): Handles the search button click event, retrieves animal information from the database or API, and updates the GUI with the retrieved data.
- gui_init(): Initializes the DearPyGui context, creates the main window and its components, and starts the DearPyGui event loop.
"""

import dearpygui.dearpygui as dpg
import api
import math
import db


W, H = 650, 520
phase = 0.0
is_animating = False

BASE_COLORS = {
    'A': (255, 100, 100),   # red
    'T': (100, 200, 100),   # green
    'G': (100, 100, 255),   # blue
    'C': (255, 200, 50),    # yellow
}

def draw_helix(draw_tag, dna="ATGCGTATGCGTATGCGT"):
    """
    Draws a double helix representation of the DNA sequence on a DearPyGui drawlist.

    :param:
        - draw_tag: The tag of the DearPyGui drawlist where the helix will be drawn.
        - dna: A string representing the DNA sequence to visualize. The default value is "ATGCGTATGCGTATGCGT".
    """

    dpg.delete_item(draw_tag, children_only=True)

    cx, cy = W/2, H/2
    amp = 130      # width of helix
    pitch = 14     # vertical spacing
    n = 32         # rungs visible

    for i in range(n):
        y = cy - (n/2)*pitch + i*pitch
        t = i*0.35 + phase

        x1 = cx + amp * math.cos(t)
        x2 = cx + amp * math.cos(t + math.pi)

        # simple “3D-ish” depth effect
        depth = (math.sin(t) + 1) / 2  # 0..1
        thick = 1 + 3*depth
        r = 2 + 4*depth
        a = int(80 + 175*depth)

        # Pick a color based on the DNA base, cycling through the sequence
        base = dna[i % len(dna)]
        color = BASE_COLORS.get(base, (200, 200, 200))

        dpg.draw_line((x1, y), (x2, y), color=(120, 200, 255, a), thickness=thick, parent=draw_tag)
        dpg.draw_circle((x1, y), r, fill=(230,230,230,a), color=(*color, a), parent=draw_tag)
        dpg.draw_circle((x2, y), r, fill=(230,230,230,a), color=(*color, a), parent=draw_tag)

        # draw the base letter in the middle of the rung
        mid_x = (x1 + x2) / 2
        dpg.draw_text((mid_x - 5, y - 7), base, color=(255,255,255, a), size=13, parent=draw_tag)

def on_frame():
    """Updates the animation phase and redraws the helix on each frame."""

    global phase
    phase += 0.005  # speed
    draw_helix("dna_draw", dpg.get_value("dna_str"))
    dpg.set_frame_callback(dpg.get_frame_count() + 1, on_frame)


def search_animal():
    """Handles the search button click event, retrieves animal information from the database or API, and updates the GUI with the retrieved data."""

    global is_animating
    common_name = dpg.get_value("animal_input")

    if db.db_find(common_name) is not None:
        animal_data = db.db_find(common_name)
    else:
        animal_data = api.get_animal_info(common_name)
        if animal_data is None:
            dpg.set_value("scientific_name_text", "Scientific Name: not found try a more specific name")
            dpg.set_value("dna_sequence_text", "DNA Sequence: N/A")
            dpg.set_value("dna_str", "")
            return
        else:
            db.db_insert(animal_data)

        dpg.set_value("scientific_name_text", f"Scientific Name: {animal_data['scientific_name']}")
        dpg.set_value("dna_sequence_text", f"DNA Sequence: {animal_data['dna_sequence']}")
        dpg.set_value("dna_str", animal_data['dna_sequence'])

        if not is_animating:
            is_animating = True
            dpg.set_frame_callback(dpg.get_frame_count() + 1, on_frame)


def gui_init():
    """Initializes the DearPyGui context, creates the main window and its components, and starts the DearPyGui event loop."""

    dpg.create_context()

    with dpg.window(label="Main Window", width=1000, height=600):

        with dpg.value_registry():
            dpg.add_string_value(tag="dna_str", default_value="ATGCGTATGCGT")

        with dpg.group(horizontal=True):

            # Left Window
            with dpg.child_window(width=320):
                dpg.add_text("Input the common name of the animal to get its scientific name, accession number, and DNA sequence.", wrap=300)
                dpg.add_spacer(height=10)
                dpg.add_text("Input the animal:")
                dpg.add_input_text(hint="Input your common animal name here...", width=300, tag="animal_input")
                dpg.add_button(label="Search", callback=search_animal)

                dpg.add_separator()

                dpg.add_text("Scientific Name: ", tag="scientific_name_text", wrap=300)
                dpg.add_text("DNA Sequence: ", tag="dna_sequence_text")


            # Right Window
            with dpg.child_window():
                dpg.add_text("Vizualization of the DNA sequence will be shown here.")

                dpg.add_drawlist(width=W, height=H, tag="dna_draw")




    dpg.create_viewport(title='Animal DNA', width=1000, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()

    dpg.start_dearpygui()
    dpg.destroy_context()