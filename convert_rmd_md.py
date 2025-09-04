#!/usr/bin/env python3
"""
R Markdown to Markdown Converter

This script converts R Markdown (.Rmd) files to standard Markdown (.md) files,
specifically handling the conversion of anchor links from R Markdown format
to standard Markdown format and adding appropriate frontmatter.

Usage:
    python rmd_to_md.py input.Rmd [output.md]
"""

import re
import sys
import os
from pathlib import Path


def extract_title_from_content(content):
    """
    Extract title from the first heading in the content.
    Returns the title without the heading marker and anchor link.
    """
    # Look for the first heading (# Title {-})
    title_match = re.search(r'^#\s+(.+?)\s*\{-\}', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    
    # Fallback: look for any first heading
    title_match = re.search(r'^#\s+(.+?)$', content, re.MULTILINE)
    if title_match:
        return title_match.group(1).strip()
    
    return "Untitled"


def convert_rmd_headers(content, remove_first_header=True):
    """
    Convert R Markdown headers with {-} anchors to standard Markdown headers.
    Optionally remove the first # header since it becomes the title.
    
    Examples:
    # Title {-} -> removed (becomes frontmatter title)
    ## Section {-} -> ## Section
    """
    lines = content.split('\n')
    converted_lines = []
    first_header_removed = False
    
    for line in lines:
        # Check if this is a header with {-} anchor
        header_match = re.match(r'^(#+)\s+(.+?)\s*\{-\}\s*$', line)
        if header_match:
            header_level = header_match.group(1)
            header_text = header_match.group(2).strip()
            
            # Remove first # header if requested
            if remove_first_header and len(header_level) == 1 and not first_header_removed:
                first_header_removed = True
                continue  # Skip this line (don't add to output)
            else:
                converted_lines.append(f"{header_level} {header_text}")
        else:
            converted_lines.append(line)
    
    return '\n'.join(converted_lines)


def create_frontmatter(title):
    """
    Create YAML frontmatter for the markdown file.
    """
    frontmatter = f"""---
title: "{title}"
layout: single
---

"""
    return frontmatter


def convert_rmd_to_md(input_file, output_file=None):
    """
    Convert R Markdown file to standard Markdown file.
    
    Args:
        input_file (str): Path to input .Rmd file
        output_file (str, optional): Path to output .md file. 
                                   If None, uses input filename with .md extension
    """
    input_path = Path(input_file)
    
    # Validate input file
    if not input_path.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    if not input_path.suffix.lower() in ['.rmd', '.rmarkdown']:
        print(f"Warning: Input file doesn't have .Rmd extension: {input_file}")
    
    # Determine output file path
    if output_file is None:
        output_path = input_path.with_suffix('.md')
    else:
        output_path = Path(output_file)
    
    # Read input file
    try:
        with open(input_path, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with open(input_path, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Extract title for frontmatter
    title = extract_title_from_content(content)
    
    # Convert R Markdown specific syntax (remove first header)
    converted_content = convert_rmd_headers(content, remove_first_header=True)
    
    # Create frontmatter
    frontmatter = create_frontmatter(title)
    
    # Combine frontmatter with converted content
    final_content = frontmatter + converted_content
    
    # Write output file
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    print(f"Successfully converted {input_path} to {output_path}")
    return output_path


def main():
    """Main function to handle command line arguments."""
    if len(sys.argv) < 2:
        print("Usage: python rmd_to_md.py input.Rmd [output.md]")
        print("\nConverts R Markdown files to standard Markdown format")
        print("- Removes {-} anchor links from headers")
        print("- Removes first # header and uses it as frontmatter title")
        print("- Adds YAML frontmatter with title and layout")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        convert_rmd_to_md(input_file, output_file)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()