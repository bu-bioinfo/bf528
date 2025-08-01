#!/usr/bin/env python3
"""
R Markdown to Markdown Converter

This script converts R Markdown (.Rmd) files to standard Markdown (.md) files,
specifically handling:
- Conversion of anchor links from R Markdown format to standard Markdown format
- Converting reference-style links [Text] to anchor links [Text](#text)
- Removing R Markdown div blocks (:::{.class} and :::)
- Adding appropriate frontmatter
- Removing R Markdown {-} syntax from headers

Usage:
    python rmd_to_md.py input.Rmd [output.md]                    # Single file
    python rmd_to_md.py --dir /path/to/directory [--output-dir /path/to/output]  # Directory mode
    python rmd_to_md.py --dir . --recursive                      # Process directory recursively
"""

import re
import sys
import os
import argparse
from pathlib import Path
from typing import List, Optional


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


def create_anchor_id(text):
    """
    Create a URL-friendly anchor ID from header text.
    Converts to lowercase, replaces spaces/special chars with hyphens.
    """
    # Remove special characters and convert to lowercase
    anchor = re.sub(r'[^\w\s-]', '', text.lower())
    # Replace spaces and multiple hyphens with single hyphens
    anchor = re.sub(r'[\s_]+', '-', anchor)
    # Remove leading/trailing hyphens
    anchor = anchor.strip('-')
    return anchor


def remove_rmd_div_blocks(content):
    """
    Remove R Markdown div blocks (fenced divs) like:
    :::{.box .task}
    :::
    
    These are Pandoc/R Markdown specific syntax that don't render in standard Markdown.
    """
    # Remove opening div blocks: :::{.class .other-class}
    content = re.sub(r'^:::\{[^}]*\}\s*$', '', content, flags=re.MULTILINE)
    
    # Remove closing div blocks: :::
    content = re.sub(r'^:::\s*$', '', content, flags=re.MULTILINE)
    
    # Clean up multiple consecutive empty lines that might result from removals
    content = re.sub(r'\n\s*\n\s*\n', '\n\n', content)
    
    return content


def convert_rmd_links(content):
    """
    Convert R Markdown reference-style links to proper anchor links.
    
    Examples:
    [Section Name] -> [Section Name](#section-name)
    [Some Title] -> [Some Title](#some-title)
    [link text](url) -> [link text](url) (unchanged - already proper markdown)
    [text][ref] -> [text][ref] (unchanged - reference definition)
    """
    # Simple and comprehensive pattern to match [text] 
    # We'll do the filtering in the replacement function instead of the regex
    pattern = r'\[([^\]]+)\]'
    
    def replace_link(match):
        full_match = match.group(0)
        link_text = match.group(1)
        
        # Skip if it's empty or just whitespace
        if not link_text.strip():
            return full_match
            
        # Skip footnote references [^something]
        if link_text.startswith('^'):
            return full_match
        
        # Check what comes after the closing bracket to determine if it's already a proper link
        match_end = match.end()
        remaining_content = content[match_end:]
        
        # If followed by ( then it's already a proper markdown link [text](url)
        if remaining_content.startswith('('):
            return full_match
            
        # If followed by [ then it's a reference link [text][ref]  
        if remaining_content.startswith('['):
            return full_match
            
        # Skip common figure/table references but be less restrictive
        if re.match(r'^(fig|figure|img|image|table|tbl)[-_:]\w', link_text.lower()):
            return full_match
            
        # Convert to anchor link
        anchor_id = create_anchor_id(link_text)
        return f'[{link_text}](#{anchor_id})'
    
    return re.sub(pattern, replace_link, content)


def convert_rmd_headers(content, remove_first_header=True):
    """
    Convert R Markdown headers with {-} anchors to standard Markdown headers.
    Optionally remove the first # header since it becomes the title.
    Also creates a mapping of header text to anchor IDs for link conversion.
    
    Examples:
    # Title {-} -> removed (becomes frontmatter title)
    ## Section {-} -> ## Section
    ## Custom Section {#custom-id} -> ## Custom Section {#custom-id}
    """
    lines = content.split('\n')
    converted_lines = []
    first_header_removed = False
    
    for line in lines:
        # Check if this is a header with {-} anchor (R Markdown style)
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
        
        # Check if this is a header with custom anchor {#custom-id}
        elif re.match(r'^#+\s+.+\s*\{#[\w-]+\}\s*$', line):
            # Keep custom anchor headers as-is (they're already proper markdown)
            if remove_first_header and line.startswith('# ') and not first_header_removed:
                first_header_removed = True
                continue
            else:
                converted_lines.append(line)
        
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


def find_rmd_files(directory: Path, recursive: bool = False) -> List[Path]:
    """
    Find all .Rmd files in a directory.
    
    Args:
        directory: Path to search
        recursive: If True, search subdirectories recursively
    
    Returns:
        List of Path objects for .Rmd files
    """
    if recursive:
        # Use rglob for recursive search
        rmd_files = list(directory.rglob("*.Rmd")) + list(directory.rglob("*.rmd")) + list(directory.rglob("*.rmarkdown"))
    else:
        # Use glob for current directory only
        rmd_files = list(directory.glob("*.Rmd")) + list(directory.glob("*.rmd")) + list(directory.glob("*.rmarkdown"))
    
    return sorted(rmd_files)


def convert_rmd_to_md(input_file: Path, output_file: Optional[Path] = None) -> Path:
    """
    Convert R Markdown file to standard Markdown file.
    
    Args:
        input_file: Path to input .Rmd file
        output_file: Path to output .md file. If None, uses input filename with .md extension
    
    Returns:
        Path to the created output file
    """
    # Validate input file
    if not input_file.exists():
        raise FileNotFoundError(f"Input file not found: {input_file}")
    
    # Determine output file path
    if output_file is None:
        output_file = input_file.with_suffix('.md')
    
    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
    except UnicodeDecodeError:
        # Try with different encoding if UTF-8 fails
        with open(input_file, 'r', encoding='latin-1') as f:
            content = f.read()
    
    # Extract title for frontmatter
    title = extract_title_from_content(content)
    
    # Convert R Markdown specific syntax (remove first header)
    converted_content = convert_rmd_headers(content, remove_first_header=True)
    
    # Remove R Markdown div blocks
    converted_content = remove_rmd_div_blocks(converted_content)
    
    # Convert R Markdown reference-style links to anchor links
    converted_content = convert_rmd_links(converted_content)
    
    # Create frontmatter
    frontmatter = create_frontmatter(title)
    
    # Combine frontmatter with converted content
    final_content = frontmatter + converted_content
    
    # Ensure output directory exists
    output_file.parent.mkdir(parents=True, exist_ok=True)
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_content)
    
    return output_file


def process_directory(input_dir: Path, output_dir: Optional[Path] = None, recursive: bool = False) -> List[Path]:
    """
    Process all .Rmd files in a directory.
    
    Args:
        input_dir: Directory containing .Rmd files
        output_dir: Directory for output files (default: same as input_dir)
        recursive: If True, process subdirectories recursively
    
    Returns:
        List of output file paths
    """
    if not input_dir.exists():
        raise FileNotFoundError(f"Input directory not found: {input_dir}")
    
    if not input_dir.is_dir():
        raise NotADirectoryError(f"Input path is not a directory: {input_dir}")
    
    # Find all .Rmd files
    rmd_files = find_rmd_files(input_dir, recursive)
    
    if not rmd_files:
        print(f"No .Rmd files found in {input_dir}")
        return []
    
    print(f"Found {len(rmd_files)} .Rmd file(s) to process")
    
    output_files = []
    successful_conversions = 0
    
    for rmd_file in rmd_files:
        try:
            # Determine output file path
            if output_dir:
                # Preserve directory structure if processing recursively
                if recursive:
                    relative_path = rmd_file.relative_to(input_dir)
                    output_file = output_dir / relative_path.with_suffix('.md')
                else:
                    output_file = output_dir / rmd_file.with_suffix('.md').name
            else:
                output_file = rmd_file.with_suffix('.md')
            
            # Convert the file
            result_file = convert_rmd_to_md(rmd_file, output_file)
            output_files.append(result_file)
            successful_conversions += 1
            print(f"✓ Converted {rmd_file.name} -> {result_file.name}")
            
        except Exception as e:
            print(f"✗ Failed to convert {rmd_file.name}: {e}")
    
    print(f"\nProcessed {successful_conversions}/{len(rmd_files)} files successfully")
    return output_files


def main():
    """Main function to handle command line arguments."""
    parser = argparse.ArgumentParser(
        description="Convert R Markdown files to standard Markdown format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s input.Rmd                           # Convert single file
  %(prog)s input.Rmd output.md                 # Convert single file with custom output
  %(prog)s --dir ./docs                        # Convert all .Rmd files in directory
  %(prog)s --dir ./docs --output-dir ./output  # Convert with different output directory
  %(prog)s --dir ./docs --recursive            # Convert recursively through subdirectories
        """
    )
    
    # Create mutually exclusive group for single file vs directory mode
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('input_file', nargs='?', help='Input .Rmd file (for single file mode)')
    group.add_argument('--dir', '--directory', dest='input_dir', 
                      help='Input directory containing .Rmd files')
    
    parser.add_argument('output_file', nargs='?', 
                       help='Output .md file (only for single file mode)')
    parser.add_argument('--output-dir', dest='output_dir',
                       help='Output directory (for directory mode)')
    parser.add_argument('--recursive', '-r', action='store_true',
                       help='Process subdirectories recursively (for directory mode)')
    
    args = parser.parse_args()
    
    try:
        if args.input_dir:
            # Directory mode
            input_dir = Path(args.input_dir)
            output_dir = Path(args.output_dir) if args.output_dir else None
            process_directory(input_dir, output_dir, args.recursive)
        else:
            # Single file mode
            if not args.input_file:
                parser.error("Input file is required when not using --dir")
            
            input_file = Path(args.input_file)
            output_file = Path(args.output_file) if args.output_file else None
            result_file = convert_rmd_to_md(input_file, output_file)
            print(f"Successfully converted {input_file} to {result_file}")
            
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()