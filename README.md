# Animal DNA Visualization 🧬

A Python application that retrieves and visualizes DNA sequences of animals using a beautiful animated double helix representation.

**Author:** Emilijus Kanapeckas

## 📋 Overview

This application allows users to search for animals by their common names and retrieve their scientific names, accession numbers, and DNA sequences from the European Nucleotide Archive (ENA) database. The DNA sequence is then visualized as an animated, color-coded double helix in a graphical user interface.

## ✨ Features

- **Animal Information Retrieval**: Search animals by common name and get scientific classification
- **DNA Sequence Visualization**: Animated double helix representation of DNA sequences
- **Color-Coded Bases**: Each nucleotide base is color-coded for easy identification:
  - **A (Adenine)**: Red
  - **T (Thymine)**: Green
  - **G (Guanine)**: Blue
  - **C (Cytosine)**: Yellow
- **Local Caching**: SQLite database stores previously searched animals for faster access
- **3D-like Animation**: Smooth rotating helix with depth effects

## 🎨 Interesting GUI Features

The GUI is built using **DearPyGui**, a modern GPU-accelerated Python GUI framework that offers several unique features:

- **Real-time Animation**: The DNA double helix continuously rotates with a smooth 3D-like effect
- **Depth Perception**: The helix uses varying line thickness and opacity to simulate depth, making parts of the helix appear closer or farther away
- **Dynamic Color Mapping**: Each DNA base pair is rendered with its corresponding color, making it easy to identify nucleotide patterns
- **Responsive Drawlist**: Uses DearPyGui's drawlist feature for efficient rendering of geometric shapes and text
- **Frame Callbacks**: Implements frame-by-frame animation updates for smooth motion
- **Split-Panel Layout**: Clean interface with input controls on the left and visualization on the right

## 🏗️ How It Works

### Architecture

The application is structured into several modular components:

1. **main.py**: Entry point that initializes the database and GUI
2. **gui.py**: Handles all graphical interface and visualization logic
3. **api.py**: Manages API calls to ENA (European Nucleotide Archive) services
4. **db.py**: SQLite database operations for caching animal data
5. **config.py**: Configuration file containing API endpoints

### Data Flow

1. User enters an animal's common name (e.g., "dog", "cat", "elephant")
2. System checks local SQLite database for cached results
3. If not found, makes API calls to ENA:
   - Retrieves scientific name and taxonomy ID from common name
   - Fetches accession number using taxonomy ID
   - Downloads DNA sequence using accession number
4. Stores results in local database for future quick access
5. Displays scientific information and animates the DNA sequence

### API Integration

The application uses three ENA (European Nucleotide Archive) API endpoints:

- **Taxonomy API**: Converts common names to scientific names and taxonomy IDs
- **Portal API**: Searches for sequence accession numbers by taxonomy
- **Browser API**: Retrieves FASTA-formatted DNA sequences

## 🚀 Installation & Setup

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Download the Project

#### Option 1: Clone with Git
```bash
git clone https://github.com/yourusername/Animal_DNA_vizualization.git
cd Animal_DNA_vizualization
```

#### Option 2: Download ZIP
1. Click the green "Code" button on GitHub
2. Select "Download ZIP"
3. Extract the ZIP file to your desired location
4. Navigate to the extracted folder

### Install Dependencies

```bash
pip install -r requirements.txt
```

The required packages are:
- **requests**: For making HTTP API calls
- **dearpygui**: For the graphical user interface
- **sqlite3**: For local database (included in Python standard library)

## 🎮 How to Run

1. Navigate to the project directory:
```bash
cd Animal_DNA_vizualization
```

2. Run the application:
```bash
python main.py
```

3. In the GUI:
   - Enter an animal's common name (e.g., "dog", "human", "whale")
   - Click the "Search" button
   - Watch the animated DNA helix visualization!

## 📊 Project Structure

```
Animal_DNA_vizualization/
│
├── main.py              # Application entry point
├── gui.py               # GUI and visualization logic
├── api.py               # API interaction functions
├── db.py                # Database operations
├── config.py            # Configuration (API URLs)
├── requirements.txt     # Python dependencies
├── data.db              # SQLite database (auto-generated)
├── README.md            # This file
└── .gitignore           # Git ignore rules
```

## 🔧 Technical Details

- **GUI Framework**: DearPyGui (GPU-accelerated immediate mode GUI)
- **Database**: SQLite3 for local caching
- **API Source**: European Nucleotide Archive (ENA)
- **Animation**: Frame-callback based rendering at ~60 FPS
- **Helix Rendering**: Mathematical sine/cosine functions for 3D projection

## 🤝 Contributing

Feel free to fork this project and submit pull requests for any improvements!


