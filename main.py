import sys
import argparse
import os
import glob
from pathlib import Path
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.generic import DictionaryObject, ArrayObject


def remove_links_from_page(page):
    if '/Annots' in page:
        annotations = page['/Annots']
        
        filtered_annotations = []
        
        for annot_ref in annotations:
            annot = annot_ref.get_object()
            if isinstance(annot, DictionaryObject):
                if '/Subtype' in annot and annot['/Subtype'] == '/Link':
                    continue 
                else:
                    filtered_annotations.append(annot_ref)
            else:
                filtered_annotations.append(annot_ref)
        
        if filtered_annotations:
            page['/Annots'] = ArrayObject(filtered_annotations)
        else:
            del page['/Annots']
    
    return page


def process_directory(input_dir, output_dir, verbose=False):
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    
    if not input_path.exists():
        print(f"Error: Input directory '{input_dir}' does not exist.")
        return False
    
    if not input_path.is_dir():
        print(f"Error: '{input_dir}' is not a directory.")
        return False
    
    try:
        output_path.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        print(f"Error creating output directory '{output_dir}': {str(e)}")
        return False
    
    pdf_files = list(input_path.glob('*.pdf')) + list(input_path.glob('*.PDF'))
    
    if not pdf_files:
        print(f"No PDF files found in '{input_dir}'.")
        return True
    
    print(f"Found {len(pdf_files)} PDF file(s) to process.")
    
    success_count = 0
    failed_count = 0
    
    for pdf_file in pdf_files:
        if verbose:
            print(f"\n--- Processing: {pdf_file.name} ---")
        else:
            print(f"Processing: {pdf_file.name}")
        
        output_file = output_path / pdf_file.name
        
        if remove_links_from_pdf(str(pdf_file), str(output_file)):
            success_count += 1
            if verbose:
                print(f"✓ Successfully processed: {pdf_file.name}")
        else:
            failed_count += 1
            if verbose:
                print(f"✗ Failed to process: {pdf_file.name}")
    
    print(f"\n--- Processing Summary ---")
    print(f"Successfully processed: {success_count} files")
    print(f"Failed to process: {failed_count} files")
    print(f"Total files: {len(pdf_files)}")
    
    return failed_count == 0


def remove_links_from_pdf(input_path, output_path):
    try:
        reader = PdfReader(input_path)
        writer = PdfWriter()
        
        for page_num, page in enumerate(reader.pages):
            cleaned_page = remove_links_from_page(page)
            
            writer.add_page(cleaned_page)
        
        if reader.metadata:
            writer.add_metadata(reader.metadata)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        return True
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_path}' not found.")
        return False
    except PermissionError:
        print(f"Error: Permission denied. Check file permissions for '{input_path}' or '{output_path}'.")
        return False
    except Exception as e:
        print(f"Error processing PDF: {str(e)}")
        return False


def main():
    parser = argparse.ArgumentParser(
        description="Remove all links from PDF file(s)",
        usage="%(prog)s input output [options]\n       %(prog)s --dir input_directory output_directory [options]"
    )
    
    parser.add_argument('--dir', action='store_true',
                      help='Process all PDFs in a directory')
    
    parser.add_argument('input', help='Input PDF file or directory path')
    parser.add_argument('output', help='Output PDF file or directory path')
    parser.add_argument('-v', '--verbose', action='store_true', 
                       help='Enable verbose output')
    
    if len(sys.argv) < 3:
        parser.print_help()
        sys.exit(1)
    
    args = parser.parse_args()
    
    if args.verbose:
        if args.dir:
            print(f"Input directory: {args.input}")
            print(f"Output directory: {args.output}")
            print("Starting directory processing...")
        else:
            print(f"Input file: {args.input}")
            print(f"Output file: {args.output}")
            print("Starting single file processing...")
    
    if args.dir:
        success = process_directory(args.input, args.output, args.verbose)
    else:
        if not args.input.lower().endswith('.pdf'):
            print("Warning: Input file doesn't have a .pdf extension")
        
        if not args.output.lower().endswith('.pdf'):
            print("Warning: Output file doesn't have a .pdf extension")
        
        success = remove_links_from_pdf(args.input, args.output)
        if success:
            print(f"Successfully removed links from PDF. Output saved to: {args.output}")
    
    if success:
        print("Link removal completed successfully!")
        sys.exit(0)
    else:
        print("Link removal failed!")
        sys.exit(1)


if __name__ == "__main__":
    main()