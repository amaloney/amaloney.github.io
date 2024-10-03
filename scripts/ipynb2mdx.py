import re
from typing import TypedDict

import mdformat
import nbformat


class Preamble(TypedDict):
    source: str
    preamble: str


def handle_preamble(cell_source: str) -> Preamble:
    mdx = ""
    pattern = re.compile(r"\n*(<!--(?:[^-]+|-(?!->))*-->)\s*")
    matches = re.match(pattern, cell_source)
    if matches is not None:
        match = matches.group()
        mdx += match.replace("<!--", "").replace("\n-->", "").strip()
        # Add KaTeX CSS.
        mdx += "\nimport 'katex/dist/katex.min.css'\n\n"
        cell_source = cell_source.replace(match, "")
    return {"source": cell_source, "preamble": mdx}


def handle_markdown_cell_type(cell: nbformat.NotebookNode) -> str:
    mdx = ""
    source = cell["source"]

    # Check if the cell has a preamble. If it does, then we will remove the HTML comment
    # around it.
    preamble = handle_preamble(cell_source=source)
    mdx += preamble["preamble"]
    source = preamble["source"]

    # Format the markdown.
    mdx += mdformat.text(source, options={"wrap": 88}, extensions={"myst"})
    mdx += "\n"
    return mdx


def handle_code_cell_source(cell_source: str) -> str:
    mdx = "```"
    # If we have an empty cell, then ignore it.
    if not cell_source:
        return ""
    # Determine what language is being used in the code cell. We assume Python, but
    # there are others thanks to cell magics.
    cell_language = "python"
    lines = cell_source.splitlines()
    if lines:
        if lines[0].startswith("%%"):
            cell_language = lines[0].replace("%%", "")
            lines.pop(0)
    mdx += f"{cell_language} showLineNumbers\n"
    for line in lines:
        mdx += f"{line}\n"
    mdx += "```\n\n"
    return mdx


def sanitize_text(s: str) -> str:
    return s.replace("<", "\\<").replace(">", "\\>")


def handle_code_cell_outputs(cell_outputs: list[dict]) -> str:
    mdx = ""
    for cell_output in cell_outputs:
        if "data" in cell_output:
            data = cell_output["data"]
            for key, value in data.items():
                if key == "text/plain":
                    mdx += f"{sanitize_text(value)}\n\n"
                if key == "image/png":
                    mdx += f"![](data:image/png;base64,{value})\n"
        elif "data" not in cell_output:
            output_type = cell_output["output_type"]
            if output_type == "stream":
                data = cell_output["text"]
                if "WARNING" in data:
                    mdx += f":::warning\n\n{data}\n:::\n\n"
    return mdx


def handle_code_cell_type(cell: nbformat.NotebookNode) -> str:
    source_mdx = handle_code_cell_source(cell_source=cell["source"])
    output_mdx = handle_code_cell_outputs(cell_outputs=cell["outputs"])
    mdx = source_mdx + output_mdx

    return mdx


def convert(nb: nbformat.NotebookNode) -> str:
    mdx = ""
    for cell in nb["cells"]:
        cell_type = cell["cell_type"]

        if cell_type == "markdown":
            mdx += handle_markdown_cell_type(cell=cell)

        if cell_type == "code":
            mdx += handle_code_cell_type(cell=cell)
    return mdx
