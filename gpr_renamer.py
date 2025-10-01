import json
import re
import os
from pathlib import Path

def apply_renaming_rules(segment_name):
    """Apply the renaming rules to a segment name"""
    original = segment_name
    
    # Metal1 rules
    if segment_name.endswith('Metal1'):
        segment_name = segment_name.replace('Metal1', 'Metal1Block1')
    elif segment_name.endswith('Metal10'):
        segment_name = segment_name.replace('Metal10', 'Metal1Block1')
    elif segment_name.endswith('Metal11'):
        segment_name = segment_name.replace('Metal11', 'Metal1Block2')
    elif segment_name.endswith('Metal12'):
        segment_name = segment_name.replace('Metal12', 'Metal1Block3')
    elif segment_name.endswith('Metal13'):
        segment_name = segment_name.replace('Metal13', 'Metal1Block4')
    elif segment_name.endswith('Metal14'):
        segment_name = segment_name.replace('Metal14', 'Metal1Block5')
    elif segment_name.endswith('Metal15'):
        segment_name = segment_name.replace('Metal15', 'Metal1Block6')
    elif segment_name.endswith('Metal16'):
        segment_name = segment_name.replace('Metal16', 'Metal1Block7')
    elif segment_name.endswith('Metal17'):
        segment_name = segment_name.replace('Metal17', 'Metal1Block8')
    elif segment_name.endswith('Metal18'):
        segment_name = segment_name.replace('Metal18', 'Metal1Block9')
    elif segment_name.endswith('Metal19'):
        segment_name = segment_name.replace('Metal19', 'Metal1Block10')
    elif segment_name.endswith('BSPR'):
        segment_name = segment_name.replace('BSPR', 'Metal1Block1')
    
    # Metal2 rules
    elif segment_name.endswith('Metal2'):
        segment_name = segment_name.replace('Metal2', 'Metal2Block1')
    elif segment_name.endswith('Metal20'):
        segment_name = segment_name.replace('Metal20', 'Metal2Block1')
    elif segment_name.endswith('Metal21'):
        segment_name = segment_name.replace('Metal21', 'Metal2Block2')
    elif segment_name.endswith('Metal22'):
        segment_name = segment_name.replace('Metal22', 'Metal2Block3')
    elif segment_name.endswith('Metal23'):
        segment_name = segment_name.replace('Metal23', 'Metal2Block4')
    elif segment_name.endswith('Metal24'):
        segment_name = segment_name.replace('Metal24', 'Metal2Block5')
    elif segment_name.endswith('Metal25'):
        segment_name = segment_name.replace('Metal25', 'Metal2Block6')
    elif segment_name.endswith('Metal26'):
        segment_name = segment_name.replace('Metal26', 'Metal2Block7')
    elif segment_name.endswith('Metal27'):
        segment_name = segment_name.replace('Metal27', 'Metal2Block8')
    elif segment_name.endswith('Metal28'):
        segment_name = segment_name.replace('Metal28', 'Metal2Block9')
    elif segment_name.endswith('Metal29'):
        segment_name = segment_name.replace('Metal29', 'Metal2Block10')
    
    # Diffcon rules - ContactLower variants
    elif segment_name.endswith('ContactLower'):
        segment_name = segment_name.replace('ContactLower', 'DiffconBlock1')
    elif segment_name.endswith('ContactLowerMetal0'):
        segment_name = segment_name.replace('ContactLowerMetal0', 'DiffconBlock1')
    elif segment_name.endswith('ContactLowerMetal00'):
        segment_name = segment_name.replace('ContactLowerMetal00', 'DiffconBlock1')
    elif segment_name.endswith('ContactLowerMetal01'):
        segment_name = segment_name.replace('ContactLowerMetal01', 'DiffconBlock2')
    elif segment_name.endswith('ContactLowerMetal02'):
        segment_name = segment_name.replace('ContactLowerMetal02', 'DiffconBlock3')
    elif segment_name.endswith('ContactLowerMetal03'):
        segment_name = segment_name.replace('ContactLowerMetal03', 'DiffconBlock4')
    elif segment_name.endswith('ContactLowerMetal04'):
        segment_name = segment_name.replace('ContactLowerMetal04', 'DiffconBlock5')
    elif segment_name.endswith('ContactLowerMetal05'):
        segment_name = segment_name.replace('ContactLowerMetal05', 'DiffconBlock6')
    elif segment_name.endswith('ContactLowerMetal06'):
        segment_name = segment_name.replace('ContactLowerMetal06', 'DiffconBlock7')
    elif segment_name.endswith('ContactLowerMetal07'):
        segment_name = segment_name.replace('ContactLowerMetal07', 'DiffconBlock8')
    elif segment_name.endswith('ContactLowerMetal08'):
        segment_name = segment_name.replace('ContactLowerMetal08', 'DiffconBlock9')
    elif segment_name.endswith('ContactLowerMetal09'):
        segment_name = segment_name.replace('ContactLowerMetal09', 'DiffconBlock10')
    
    # Diffcon rules - Metal0 variants
    elif segment_name.endswith('Metal0'):
        segment_name = segment_name.replace('Metal0', 'DiffconBlock1')
    elif segment_name.endswith('Metal00'):
        segment_name = segment_name.replace('Metal00', 'DiffconBlock1')
    elif segment_name.endswith('Metal01'):
        segment_name = segment_name.replace('Metal01', 'DiffconBlock2')
    elif segment_name.endswith('Metal02'):
        segment_name = segment_name.replace('Metal02', 'DiffconBlock3')
    elif segment_name.endswith('Metal03'):
        segment_name = segment_name.replace('Metal03', 'DiffconBlock4')
    elif segment_name.endswith('Metal04'):
        segment_name = segment_name.replace('Metal04', 'DiffconBlock5')
    elif segment_name.endswith('Metal05'):
        segment_name = segment_name.replace('Metal05', 'DiffconBlock6')
    elif segment_name.endswith('Metal06'):
        segment_name = segment_name.replace('Metal06', 'DiffconBlock7')
    elif segment_name.endswith('Metal07'):
        segment_name = segment_name.replace('Metal07', 'DiffconBlock8')
    elif segment_name.endswith('Metal08'):
        segment_name = segment_name.replace('Metal08', 'DiffconBlock9')
    elif segment_name.endswith('Metal09'):
        segment_name = segment_name.replace('Metal09', 'DiffconBlock10')
    
    # GateLine rules
    elif segment_name.endswith('GateLine'):
        segment_name = segment_name.replace('GateLine', 'GateLineBlock1')
    
    # Via rules
    elif segment_name.endswith('Via'):
        segment_name = segment_name.replace('Via', 'ViaBlock1')
    elif segment_name.endswith('Via0'):
        segment_name = segment_name.replace('Via0', 'ViaBlock1')
    elif segment_name.endswith('Via1'):
        segment_name = segment_name.replace('Via1', 'ViaBlock2')
    elif segment_name.endswith('Via2'):
        segment_name = segment_name.replace('Via2', 'ViaBlock3')
    elif segment_name.endswith('Via3'):
        segment_name = segment_name.replace('Via3', 'ViaBlock4')
    elif segment_name.endswith('Via4'):
        segment_name = segment_name.replace('Via4', 'ViaBlock5')
    elif segment_name.endswith('Via5'):
        segment_name = segment_name.replace('Via5', 'ViaBlock6')
    elif segment_name.endswith('Via6'):
        segment_name = segment_name.replace('Via6', 'ViaBlock7')
    elif segment_name.endswith('Via7'):
        segment_name = segment_name.replace('Via7', 'ViaBlock8')
    elif segment_name.endswith('Via8'):
        segment_name = segment_name.replace('Via8', 'ViaBlock9')
    elif segment_name.endswith('Via9'):
        segment_name = segment_name.replace('Via9', 'ViaBlock10')
    
    # Clean up special characters
    if segment_name.endswith('BSPR'):
        segment_name = segment_name.replace('BSPR', 'Metal1Block1')
    segment_name = segment_name.replace('BSPR', 'Metal1')
    segment_name = re.sub(r'[^a-zA-Z0-9]', '', segment_name)
    
    return segment_name

def process_gpr_file(file_path):
    """Process a single .gpr file and apply renaming rules"""
    try:
        # Read the file
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Navigate to Parasitics -> Capacitances
        if 'Parasitics' in data and 'Capacitances' in data['Parasitics']:
            capacitances = data['Parasitics']['Capacitances']
            
            # Process each dictionary in the Capacitances list
            for cap_dict in capacitances:
                if 'SegmentGroup1' in cap_dict:
                    cap_dict['SegmentGroup1'] = apply_renaming_rules(cap_dict['SegmentGroup1'])
                
                if 'SegmentGroup2' in cap_dict:
                    cap_dict['SegmentGroup2'] = apply_renaming_rules(cap_dict['SegmentGroup2'])
        
        # Write the modified data back to the file
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4)
        
        return True, None
        
    except json.JSONDecodeError as e:
        return False, f"JSON decode error: {str(e)}"
    except FileNotFoundError as e:
        return False, f"File not found: {str(e)}"
    except PermissionError as e:
        return False, f"Permission denied: {str(e)}"
    except Exception as e:
        return False, f"Unexpected error: {str(e)}"

def process_folder_with_error_tracking(folder_path):
    """Process all .gpr files in a folder and track errors"""
    folder_path = Path(folder_path)
    
    if not folder_path.exists():
        print(f"Folder does not exist: {folder_path}")
        return
    
    gpr_files = list(folder_path.glob("*.gpr"))
    
    if not gpr_files:
        print(f"No .gpr files found in: {folder_path}")
        return
    
    print(f"Found {len(gpr_files)} .gpr files in {folder_path}")
    
    success_count = 0
    failed_files = []
    
    for gpr_file in gpr_files:
        success, error_msg = process_gpr_file(gpr_file)
        if success:
            success_count += 1
            print(f"✓ Processed: {gpr_file.name}")
        else:
            failed_files.append({
                'file': gpr_file.name,
                'path': str(gpr_file),
                'error': error_msg
            })
            print(f"✗ Failed: {gpr_file.name} - {error_msg}")
    
    print(f"\n{'='*50}")
    print(f"PROCESSING SUMMARY")
    print(f"{'='*50}")
    print(f"Successfully processed: {success_count} out of {len(gpr_files)} files")
    
    if failed_files:
        print(f"\nFAILED FILES ({len(failed_files)}):")
        print("-" * 30)
        for i, failed in enumerate(failed_files, 1):
            print(f"{i:2d}. {failed['file']}")
            print(f"    Path: {failed['path']}")
            print(f"    Error: {failed['error']}")
            print()
        
        # Create a summary file with failed files
        failed_files_path = folder_path / "failed_files_report.txt"
        with open(failed_files_path, 'w') as f:
            f.write(f"Failed Files Report - {len(failed_files)} files\n")
            f.write("=" * 50 + "\n\n")
            for i, failed in enumerate(failed_files, 1):
                f.write(f"{i:2d}. {failed['file']}\n")
                f.write(f"    Path: {failed['path']}\n")
                f.write(f"    Error: {failed['error']}\n\n")
        
        print(f"Failed files report saved to: {failed_files_path}")
    
    return failed_files

# Main execution
if __name__ == "__main__":
    # Replace this path with your actual folder path containing .gpr files
    # folder_path = input("Enter the path to your folder containing .gpr files: ")
    # failed_files = process_folder_with_error_tracking(folder_path)
    
    # Alternative: You can directly set the path here instead of input
    failed_files = process_folder_with_error_tracking("/home/ubuntu/sivista_users/hritik/sivista_pro/gpr_renaming_analysis/all_gpr_files")