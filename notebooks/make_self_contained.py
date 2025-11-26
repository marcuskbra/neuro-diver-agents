#!/usr/bin/env python3
"""
make_self_contained.py - Generate a self-contained Kaggle notebook

This script takes the main demo notebook and injects all source code as
%%writefile cells, creating a fully self-contained notebook that Kaggle
reviewers can run without uploading any additional files.

Usage:
    python make_self_contained.py

Output:
    kaggle_capstone_self_contained.ipynb
"""

import json
from pathlib import Path


def get_source_files() -> list[tuple[str, str]]:
    """Get all source files in the correct order for imports."""
    src_dir = Path(__file__).parent.parent / "src" / "capstone"

    # Order matters for imports - models first, then tools, then agents, then infrastructure
    file_order = [
        # Models (no internal dependencies)
        "models/__init__.py",
        "models/behavior.py",
        "models/activity.py",
        "models/memory.py",
        "models/results.py",
        "models/strategy.py",
        # Tools (depend on models)
        "tools/__init__.py",
        "tools/behavior_classifier.py",
        "tools/activity_planner.py",
        "tools/pattern_analyzer.py",
        # Agents (depend on models and tools)
        "agents/__init__.py",
        "agents/retry_config.py",
        "agents/agent_configs.py",
        "agents/tool_formatters.py",
        "agents/specialist_helpers.py",
        "agents/tool_wrappers.py",
        "agents/specialist_factory.py",
        "agents/coordinator.py",
        # Infrastructure (depends on agents)
        "infrastructure/__init__.py",
        "infrastructure/agent_factory.py",
        # Package root
        "__init__.py",
    ]

    files = []
    for rel_path in file_order:
        file_path = src_dir / rel_path
        if file_path.exists():
            content = file_path.read_text()
            files.append((rel_path, content))
        else:
            print(f"Warning: {rel_path} not found")

    return files


def create_markdown_cell(content: str) -> dict:
    """Create a markdown cell."""
    return {"cell_type": "markdown", "metadata": {}, "source": content.split("\n")}


def create_code_cell(content: str) -> dict:
    """Create a code cell."""
    # Ensure content ends with newline and split properly
    lines = content.rstrip("\n").split("\n")
    # Add newline to each line except the last
    source = [line + "\n" for line in lines[:-1]] + [lines[-1]] if lines else []
    return {
        "cell_type": "code",
        "metadata": {},
        "outputs": [],
        "execution_count": None,
        "source": source,
    }


def create_writefile_cell(filepath: str, content: str) -> dict:
    """Create a %%writefile cell for a source file."""
    # Build the cell content
    cell_content = f"%%writefile src/capstone/{filepath}\n{content}"
    return create_code_cell(cell_content)


def create_directory_setup_cell() -> dict:
    """Create a cell that sets up the directory structure."""
    content = """# Create directory structure for source files
import os

directories = [
    "src/capstone/models",
    "src/capstone/tools",
    "src/capstone/agents",
    "src/capstone/infrastructure",
]

for d in directories:
    os.makedirs(d, exist_ok=True)

print("Directory structure created successfully!")"""
    return create_code_cell(content)


def create_source_files_header() -> dict:
    """Create a markdown header for the source files section."""
    content = """## Source Code Files

The following cells create all the source code files needed by this notebook.
This makes the notebook fully self-contained - no external file uploads required!

Run these cells to create the `src/capstone/` directory structure with all modules."""
    return create_markdown_cell(content)


def create_source_section_header(section: str) -> dict:
    """Create a markdown header for a source section."""
    section_names = {
        "models": "Models - Data Structures & Validation",
        "tools": "Tools - Custom Function Tools",
        "agents": "Agents - Specialist Agents & Coordinator",
        "infrastructure": "Infrastructure - Factory & Dependencies",
    }
    name = section_names.get(section, section.title())
    return create_markdown_cell(f"### {name}\n")


def find_insertion_point(notebook: dict) -> int:
    """Find the cell index where source files should be inserted.

    Looks for the cell that mentions uploading src/ directory or
    the first code cell after setup/installation.
    """
    cells = notebook["cells"]

    # Look for the cell that talks about uploading files
    for i, cell in enumerate(cells):
        if cell["cell_type"] == "markdown":
            source = "".join(cell.get("source", []))
            # Find the cell that instructs manual file upload
            if "Upload Project Files" in source or "upload the `src/` directory" in source.lower():
                return i

    # Fallback: insert after installation cells (look for pip install)
    for i, cell in enumerate(cells):
        if cell["cell_type"] == "code":
            source = "".join(cell.get("source", []))
            if "pip install" in source:
                return i + 1

    # Default: after first few cells
    return 3


def remove_manual_upload_instructions(notebook: dict) -> dict:
    """Remove or update cells that mention manual file upload."""
    new_cells = []
    skip_next = False

    for cell in notebook["cells"]:
        if skip_next:
            skip_next = False
            continue

        if cell["cell_type"] == "markdown":
            source = "".join(cell.get("source", []))

            # Skip cells about manual upload
            if "Upload Project Files" in source or "upload the `src/` directory" in source.lower():
                continue

            # Skip cells about extracting zip files
            if "unzip" in source.lower() and "kaggle/input" in source.lower():
                continue

        new_cells.append(cell)

    notebook["cells"] = new_cells
    return notebook


def generate_self_contained_notebook():
    """Main function to generate the self-contained notebook."""
    notebook_path = Path(__file__).parent / "kaggle_capstone_demo.ipynb"
    output_path = Path(__file__).parent / "kaggle_capstone_self_contained.ipynb"

    print(f"Reading notebook: {notebook_path}")

    # Read the original notebook
    with open(notebook_path) as f:
        notebook = json.load(f)

    # Remove manual upload instructions
    notebook = remove_manual_upload_instructions(notebook)

    # Find where to insert source files
    insertion_point = find_insertion_point(notebook)
    print(f"Inserting source files at cell index: {insertion_point}")

    # Get all source files
    source_files = get_source_files()
    print(f"Found {len(source_files)} source files")

    # Create cells for source files
    source_cells = []

    # Add header
    source_cells.append(create_source_files_header())

    # Add directory setup
    source_cells.append(create_directory_setup_cell())

    # Group files by section and add cells
    current_section = None
    for rel_path, content in source_files:
        section = rel_path.split("/")[0] if "/" in rel_path else "root"

        # Add section header if new section
        if section != current_section and section != "root":
            source_cells.append(create_source_section_header(section))
            current_section = section

        # Add writefile cell
        source_cells.append(create_writefile_cell(rel_path, content))

    # Add confirmation cell
    confirm_cell = create_code_cell("""# Verify all files were created
import os

def count_files(directory):
    count = 0
    for root, dirs, files in os.walk(directory):
        count += len([f for f in files if f.endswith('.py')])
    return count

file_count = count_files("src/capstone")
print(f"Created {file_count} Python files in src/capstone/")
print("Source code setup complete!")""")
    source_cells.append(confirm_cell)

    # Insert source cells into notebook
    cells_before = notebook["cells"][:insertion_point]
    cells_after = notebook["cells"][insertion_point:]
    notebook["cells"] = cells_before + source_cells + cells_after

    # Write the output notebook
    with open(output_path, "w") as f:
        json.dump(notebook, f, indent=1)

    print(f"\nGenerated: {output_path}")
    print(f"Total cells: {len(notebook['cells'])}")
    print(f"Source file cells added: {len(source_cells)}")
    print("\nThe notebook is now self-contained!")
    print("Kaggle reviewers can run it without uploading any additional files.")


if __name__ == "__main__":
    generate_self_contained_notebook()
