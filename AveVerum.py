import tkinter as tk
from tkinter import ttk
from mido import MidiFile, MidiTrack, Message

MIDI_INSTRUMENTS = [
    "Acoustic Grand Piano", "Bright Acoustic Piano", "Electric Grand Piano", "Honky-Tonk Piano", 
    "Electric Piano 1", "Electric Piano 2", "Harpsichord", "Clavinet", "Celesta", "Glockenspiel", 
    "Music Box", "Vibraphone", "Marimba", "Xylophone", "Tubular Bells", "Dulcimer", "Drawbar Organ", 
    "Percussive Organ", "Rock Organ", "Church Organ", "Reed Organ", "Accordion", "Harmonica", 
    "Tango Accordion", "Acoustic Guitar (nylon)", "Acoustic Guitar (steel)", "Electric Guitar (jazz)", 
    "Electric Guitar (clean)", "Electric Guitar (muted)", "Overdriven Guitar", "Distortion Guitar", 
    "Guitar Harmonics", "Acoustic Bass", "Electric Bass (finger)", "Electric Bass (pick)", "Fretless Bass", 
    "Slap Bass 1", "Slap Bass 2", "Synth Bass 1", "Synth Bass 2", "Violin", "Viola", "Cello", 
    "Contrabass", "Tremolo Strings", "Pizzicato Strings", "Orchestral Harp", "Timpani", "String Ensemble 1", 
    "String Ensemble 2", "SynthStrings 1", "SynthStrings 2", "Choir Aahs", "Voice Oohs", "Synth Voice", 
    "Orchestra Hit", "Trumpet", "Trombone", "Tuba", "Muted Trumpet", "French Horn", "Brass Section", 
    "SynthBrass 1", "SynthBrass 2", "Soprano Sax", "Alto Sax", "Tenor Sax", "Baritone Sax", "Oboe", 
    "English Horn", "Bassoon", "Clarinet", "Piccolo", "Flute", "Recorder", "Pan Flute", "Blown Bottle", 
    "Shakuhachi", "Whistle", "Ocarina", "Square Lead", "Saw Lead", "Calliope Lead", "Chiff Lead", 
    "Charang Lead", "Voice Lead", "Fifths Lead", "Bass + Lead", "New Age Pad", "Warm Pad", "Polysynth Pad", 
    "Choir Pad", "Bowed Pad", "Metallic Pad", "Halo Pad", "Sweep Pad", "Rain", "Soundtrack", "Crystal", 
    "Atmosphere", "Brightness", "Goblins", "Echoes", "Sci-Fi", "Sitar", "Banjo", "Shamisen", "Koto", 
    "Kalimba", "Bagpipe", "Fiddle", "Shanai", "Tinkle Bell", "Agogo", "Steel Drums", "Woodblock", 
    "Taiko Drum", "Melodic Tom", "Synth Drum", "Reverse Cymbal", "Guitar Fret Noise", "Breath Noise", 
    "Seashore", "Bird Tweet", "Telephone Ring", "Helicopter", "Applause", "Gunshot"
]

INSTRUMENT_MAP = {name: idx for idx, name in enumerate(MIDI_INSTRUMENTS)}

notes_with_rhythm = [
    #Intro
    (60, 1440),  # C (3/4 Note)
    (62, 480),   # D (Quarter Note)
    (64, 480),   # E (Quarter Note)
    (60, 480),   # C (Quarter Note)
    (64, 480),   # E (Quarter Note)
    (65, 480),   # F (Quarter Note)

    # Ave
    (67, 960),  # G (Half Note)    AA
    (72, 480),  # C (Quarter Note) VE
    (64, 480),  # E (Quarter Note) EE
    (67, 480),  # G (Quarter Note) AA
    (65, 480),  # F (Quarter Note) AA
    (65, 960),  # F (Half Note)    VE

    # Verum corpus
    (65, 480),   # F (Quarter Note) VE
    (69, 480),   # A (Quarter Note) EE
    (67, 480),   # G (Quarter Note) RU
    (65, 480),   # F (Quarter Note) UM
    (65, 480),   # F (Quarter Note) CO
    (64, 480),   # E (Quarter Note) OR
    (64, 960),   # E (Half Note)    PUS

    # Natum de Maria virgine
    (62, 1440),  # D (3/4 Note)     NA
    (62, 480),   # D (Quarter Note) TUM
    (64, 480),   # E (Quarter Note) DE
    (64, 480),   # E (Quarter Note) MA
    (65, 480),   # F (Quarter Note) RI
    (65, 480),   # F (Quarter Note) AA
    (65, 960),   # F (Half Note)    VI
    (64, 480),   # E (Quarter Note) IR
    (64, 480),   # E (Quarter Note) GI
    (62, 1920),  # D (Whole Note)   NE

    # Vere Passum Immolatum
    (62, 1440),  # D (3/4 Note)     VE
    (67, 480),   # G (Quarter Note) RE
    (67, 480),   # G (Quarter Note) PA
    (66, 480),  # F# (Quarter Note) AA
    (66, 960),   # F# (Half Note)   SUM
    (62, 480),   # D (Quarter Note) IM
    (66, 960),   # F# (Half Note)   IM
    (69, 480),   # A (Quarter Note) MO
    (69, 480),   # A (Quarter Note) LA
    (67, 480),   # G (Quarter Note) AA
    (67, 480),   # G (Quarter Note) TUM

    #Im Cruce Pro Homine
    (67, 480),   # G (Quarter Note) IM
    (72, 1920),  # C (Full Note)    CRU
    (72, 480),   # C (Quarter Note) UU
    (71, 480),   # B (Quarter Note) UU
    (69, 480),   # A (Quarter Note) CE
    (67, 480),   # G (Quarter Note) PRO
    (67, 960),   # G (Half Note)    HO
    (66, 480),   # F# (Quarter Note)OO
    (66, 480),   # F# (Quarter Note)MI
    (67, 1920),   # G (Full Note)   NE

    # Filler music
    (79, 960),   # G (Half Note)
    (79, 960),   # G (Half Note)
    (79, 480),   # G (Quarter Note)
    (77, 480),   # F (Quarter Note)
    (79, 480),   # G (Quarter Note)
    (81, 480),   # A (Quarter Note)
    (72, 960),   # Lower C (Half Note)
    (76, 480),   # E (Quarter Note)
    (74, 480),   # D (Quarter Note)
    (72, 1920),  # C (Full Note)

    # Cuius latus perforatum
    (67, 1440),  # G (3/4 Note)     CU
    (67, 480),   # G (Quarter Note) IUS
    (67, 480),   # G (Quarter Note) LA
    (68, 480),   # G# (Quarter Note)AA
    (68, 960),   # G# (Half Note)   TUS
    (68, 480),   # G# (Quarter Note)PE
    (72, 480),   # C (Quarter Note) EE
    (70, 480),  # A# (Quarter Note) ER
    (68, 480),  # G# (Quarter Note) FO
    (68, 480),  # G# (Quarter Note) RA
    (67, 480),  # G (Quarter Note)  AA
    (67, 960),   # G (Half Note)    TUM

    # Unda fluxit et sanguine
    (65, 1440),  # F (3/4 Note)     UN
    (65, 480),   # F (Quarter Note) DA
    (65, 480),   # F (Quarter Note) FLU
    (68, 480),   # G# (Quarter Note)UU
    (67, 480),   # G (Quarter Note) XIT
    (65, 480),   # F (Quarter Note) ET
    (65, 960),   # F (Half Note)    SA
    (63, 240),   # D# (1/8th Note)  ANG
    (62, 240),   # D (1/8th Note)   ANG
    (63, 480),   # D# (Quarter Note)GUI
    (62, 1920),   # D (Full Note)   NE

    #Esto nobis praegustatum
    (64, 1440),  # E (3/4 Note)    EE
    (64, 480),   # E (Quarter Note)STO
    (64, 480),   # E (Quarter Note)NO
    (62, 480),   # D (Quarter Note)OO
    (60, 480),   # C (Quarter Note)BIS
    (65, 480),   # F (Quarter Note)PRA
    (65, 1440),  # F (3/4 Note)    AE
    (65, 480),   # F (Quarter Note)GUS
    (65, 480),   # F (Quarter Note)STA
    (64, 480),   # E (Quarter Note)AA
    (62, 480),   # D (Quarter Note)TUM

    # In mortis examine
    (67, 480),   # G (Quarter Note) IN
    (67, 1920),  # G (Half Note)    MO
    (67, 480),   # G (Quarter Note) OO
    (65, 480),   # F (Quarter Note) OR
    (67, 480),   # G (Quarter Note) TIS
    (69, 480),   # A (Quarter Note) EX
    (64, 960),   # E (Half Note)    SA
    (62, 480),   # D (Quarter Note) AA
    (64, 480),   # E (Quarter Note) MI
    (65, 960),   # F (Half Note)    NE

    (65, 960),    # F (Half Note)   IN
    (72, 2880),   # C (3/2 Note)    MO
    (73, 960),    # C# (Half Note)  OO
    (74, 480),    # D (Quarter Note) OO
    (69, 480),    # A (Quarter Note) OO
    (71, 480),    # B (Quarter Note) O0
    (72, 480),    # C (Quarter Note) 0O
    (71, 480),    # B (Quarter Note) OO
    (69, 240),    # A (1/8th Note)   OO
    (67, 240),    # G (1/8th Note)   OR
    (72, 480),    # C (Quarter Note) TIS
    (65, 480),    # F (Quarter Note) EX
    (64, 960),    # E (Half Note)    SAMI
    (62, 60),    # D (1/32th Note)
    (64, 60),    # E (1/32th Note)
    (62, 60),    # D (1/32th Note)
    (64, 60),    # E (1/32th Note)
    (62, 60),    # D (1/32th Note)
    (64, 60),    # E (1/32th Note)
    (62, 60),    # D (1/32th Note)
    (64, 60),    # E (1/32th Note)
    (62, 60),    # D (1/32th Note)
    (64, 60),    # E (1/32th Note)
    (62, 60),    # D (1/32th Note)
    (64, 60),    # E (1/32th Note)
    (62, 120),   # D (1/16th Note)
    (64, 120),   # E (1/16th Note)
    (60, 1920),  # C (Full Note)    NE

    # Filler music
    (67, 960),   # G (Half Note)
    (67, 960),   # G (Half Note)
    (67, 480),   # G (Quarter Note)
    (65, 480),   # F (Quarter Note)
    (67, 480),   # G (Quarter Note)
    (69, 480),   # A (Quarter Note)
    (60, 960),   # Lower C (Half Note)
    (64, 480),   # E (Quarter Note)
    (62, 160),   # D (Quarter Note)
    (64, 160),   # E (Quarter Note)
    (62, 160),   # D (Quarter Note)
    (60, 1920),  # C (Full Note)
]

def generate_midi(instrument_name):
    program_number = INSTRUMENT_MAP[instrument_name]
    midi = MidiFile()
    track = MidiTrack()
    midi.tracks.append(track)

    track.append(Message('program_change', program=program_number))

    for note, duration in notes_with_rhythm:
        if note is None:
            track.append(Message('note_off', velocity=0, time=duration))
        else:
            track.append(Message('note_on', note=note, velocity=64, time=0))
            track.append(Message('note_off', note=note, velocity=64, time=duration))

    # Save the MIDI file
    midi.save(f"AveVerum_{instrument_name.replace(' ', '_')}.mid")

# GUI for selecting an instrument
def create_gui():
    def on_generate():
        selected_instrument = instrument_combobox.get()
        generate_midi(selected_instrument)
        status_label.config(text=f"Generated MIDI file with {selected_instrument}")

    root = tk.Tk()
    root.title("MIDI Instrument Selector")

    label = tk.Label(root, text="Select an instrument:")
    label.pack(pady=5)

    instrument_combobox = ttk.Combobox(root, values=MIDI_INSTRUMENTS, width=50)
    instrument_combobox.pack(pady=5)
    instrument_combobox.set("Acoustic Grand Piano")  # Default selection

    generate_button = tk.Button(root, text="Generate MIDI", command=on_generate)
    generate_button.pack(pady=10)

    status_label = tk.Label(root, text="")
    status_label.pack(pady=5)

    root.mainloop()

create_gui()
