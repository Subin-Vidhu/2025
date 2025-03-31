# -*- coding: utf-8 -*-
"""
Created on Mon Mar 31 13:03:02 2025

@author: USER
"""

import os
import logging
import datetime
from pydicom import dcmread
from pydicom.uid import generate_uid, UID
from pynetdicom import AE, debug_logger, build_context
from pynetdicom.sop_class import BasicGrayscalePrintManagement
from pynetdicom.pdu_primitives import SCP_SCU_RoleSelectionNegotiation

# Constants from the Wireshark capture
CALLING_AE_TITLE = "MRAW"  # The AE Title of our application
CALLED_AE_TITLE = "AXYS"   # The AE Title of the printer
PRINT_SOP_CLASS = "1.2.840.10008.5.1.1.9"  # Basic Grayscale Print Management
IMPLEMENTATION_UID = "1.2.276.0.7230010.3.0.3.6.8"
IMPLEMENTATION_VERSION = "OFFIS_DCMTK_368"
MAX_PDU_LENGTH = 16384

# Setup directories and logging
def setup_environment():
    """
    Set up the environment by creating data and logs directories
    and configuring logging.
    """
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Create data directory if it doesn't exist
    data_dir = os.path.join(script_dir, "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Created data directory: {data_dir}")
    
    # Create logs directory if it doesn't exist
    logs_dir = os.path.join(script_dir, "logs")
    if not os.path.exists(logs_dir):
        os.makedirs(logs_dir)
        print(f"Created logs directory: {logs_dir}")
    
    # Set up logging
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(logs_dir, f"dicom_print_{timestamp}.log")
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    logger = logging.getLogger(__name__)
    logger.info("Environment setup complete")
    
    return data_dir, logs_dir, logger

def find_dicom_printers(host='127.0.0.1', port_range=(104, 110), timeout=5, logger=None):
    """
    Scan the local network for DICOM print SCP (printers)
    Args:
        host: IP address or hostname to scan (you may need to scan a range)
        port_range: Range of ports to scan
        timeout: Connection timeout in seconds
        logger: Logger object
    Returns:
        List of (host, port) tuples for available DICOM printers
    """
    printers = []
    ae = AE(ae_title=CALLING_AE_TITLE)
    ae.add_requested_context(BasicGrayscalePrintManagement)
    
    # Set implementation identifiers to match the expected values
    ae.implementation_class_uid = IMPLEMENTATION_UID
    ae.implementation_version_name = IMPLEMENTATION_VERSION
    
    log_msg = f"Scanning for DICOM printers on {host}..."
    if logger:
        logger.info(log_msg)
    else:
        print(log_msg)
    
    for port in range(port_range[0], port_range[1] + 1):
        try:
            assoc = ae.associate(host, port, ae_title=CALLED_AE_TITLE, timeout=timeout)
            if assoc.is_established:
                log_msg = f"Found DICOM printer at {host}:{port}"
                if logger:
                    logger.info(log_msg)
                else:
                    print(log_msg)
                printers.append((host, port))
                assoc.release()
        except Exception as e:
            log_msg = f"No DICOM printer at {host}:{port} - {str(e)}"
            if logger:
                logger.debug(log_msg)
            else:
                print(log_msg)
    
    return printers

def print_dicom_image(image_path, printer_host, printer_port, logger=None):
    """
    Print a DICOM image to a DICOM printer using the parameters from the Wireshark capture
    Args:
        image_path: Path to the DICOM image file
        printer_host: Printer IP address or hostname
        printer_port: Printer port number
        logger: Logger object
    """
    # Load the image
    log_msg = f"Loading image: {image_path}"
    if logger:
        logger.info(log_msg)
    else:
        print(log_msg)
    
    try:
        ds = dcmread(image_path)
    except Exception as e:
        log_msg = f"Failed to load DICOM image: {str(e)}"
        if logger:
            logger.error(log_msg)
        else:
            print(log_msg)
        return False
    
    # Create an application entity with the correct AE Title
    ae = AE(ae_title=CALLING_AE_TITLE)
    
    # Set implementation identifiers to match the expected values
    ae.implementation_class_uid = IMPLEMENTATION_UID
    ae.implementation_version_name = IMPLEMENTATION_VERSION
    
    # Set the maximum PDU length to match the Wireshark capture
    ae.maximum_pdu_size = MAX_PDU_LENGTH
    
    # Add the Basic Grayscale Print Management context with all transfer syntaxes
    # from the Wireshark capture
    context = build_context(
        UID(PRINT_SOP_CLASS),
        [
            "1.2.840.10008.1.2.1",  # Explicit VR Little Endian
            "1.2.840.10008.1.2.2",  # Explicit VR Big Endian (Retired)
            "1.2.840.10008.1.2"     # Implicit VR Little Endian (Default)
        ]
    )
    ae.add_requested_context(context.abstract_syntax, context.transfer_syntax)
    
    # Associate with the printer
    log_msg = f"Connecting to printer at {printer_host}:{printer_port} as {CALLED_AE_TITLE}"
    if logger:
        logger.info(log_msg)
    else:
        print(log_msg)
    
    try:
        assoc = ae.associate(printer_host, printer_port, ae_title=CALLED_AE_TITLE)
    except Exception as e:
        log_msg = f"Failed to associate with printer: {str(e)}"
        if logger:
            logger.error(log_msg)
        else:
            print(log_msg)
        return False
    
    if not assoc.is_established:
        log_msg = "Association with printer failed"
        if logger:
            logger.error(log_msg)
        else:
            print(log_msg)
        return False
    
    log_msg = "Association established"
    if logger:
        logger.info(log_msg)
    else:
        print(log_msg)
    
    try:
        # Create a Basic Film Session
        film_session_attrs = {
            'FilmSessionLabel': 'PYTHON_TEST',
            'NumberOfCopies': '1',
            'PrintPriority': 'MEDIUM',
            'MediumType': 'PAPER'
        }
        
        film_session_instance = generate_uid()
        response = assoc.send_n_create(
            film_session_attrs,
            BasicGrayscalePrintManagement,
            class_instance=film_session_instance
        )
        
        if response.Status != 0x0000:  # 0x0000 is Success
            log_msg = f"Failed to create film session: {response.Status:04x}"
            if logger:
                logger.error(log_msg)
            else:
                print(log_msg)
            assoc.release()
            return False
            
        log_msg = f"Created film session: {film_session_instance}"
        if logger:
            logger.info(log_msg)
        else:
            print(log_msg)
        
        # Create a Basic Film Box
        film_box_attrs = {
            'ImageDisplayFormat': 'STANDARD\\1,1',
            'FilmOrientation': 'PORTRAIT',
            'FilmSizeID': '8INX10IN',
            'MagnificationType': 'NONE',
            'SmoothingType': 'NONE',
            'BorderDensity': 'BLACK',
            'EmptyImageDensity': 'BLACK',
            'MinDensity': 20,
            'MaxDensity': 300
        }
        
        film_box_instance = generate_uid()
        response = assoc.send_n_create(
            film_box_attrs,
            BasicGrayscalePrintManagement,
            class_instance=film_box_instance
        )
        
        if response.Status != 0x0000:
            log_msg = f"Failed to create film box: {response.Status:04x}"
            if logger:
                logger.error(log_msg)
            else:
                print(log_msg)
            assoc.release()
            return False
            
        log_msg = f"Created film box: {film_box_instance}"
        if logger:
            logger.info(log_msg)
        else:
            print(log_msg)
        
        # Create Basic Grayscale Image Box
        # In a real implementation, you would create image boxes for each image
        # and set the image data appropriately
        image_box_attrs = {
            'ImageBoxPosition': 1,
            'ImageBoxSize': ds.PixelData  # Simplified - in reality, you'd format this properly
        }
        
        image_box_instance = generate_uid()
        response = assoc.send_n_create(
            image_box_attrs,
            BasicGrayscalePrintManagement,
            class_instance=image_box_instance
        )
        
        if response.Status != 0x0000:
            log_msg = f"Failed to create image box: {response.Status:04x}"
            if logger:
                logger.error(log_msg)
            else:
                print(log_msg)
            assoc.release()
            return False
            
        log_msg = f"Created image box: {image_box_instance}"
        if logger:
            logger.info(log_msg)
        else:
            print(log_msg)
        
        # Send N-ACTION to print the film box
        response = assoc.send_n_action(
            film_box_instance,
            BasicGrayscalePrintManagement,
            1  # Print action
        )
        
        if response.Status != 0x0000:
            log_msg = f"Failed to print: {response.Status:04x}"
            if logger:
                logger.error(log_msg)
            else:
                print(log_msg)
            assoc.release()
            return False
            
        log_msg = "Print job submitted successfully"
        if logger:
            logger.info(log_msg)
        else:
            print(log_msg)
        
        # Clean up - delete the film box
        response = assoc.send_n_delete(film_box_instance, BasicGrayscalePrintManagement)
        
        # Clean up - delete the film session
        response = assoc.send_n_delete(film_session_instance, BasicGrayscalePrintManagement)
        
        # Release the association
        assoc.release()
        return True
        
    except Exception as e:
        log_msg = f"Error during printing: {e}"
        if logger:
            logger.error(log_msg)
        else:
            print(log_msg)
        if assoc.is_established:
            assoc.release()
        return False

def print_dicom_with_dcmtk(dicom_file, printer_host, printer_port=104, logger=None):
    """
    Alternative implementation using DCMTK's dcmprscu tool
    Based on the Wireshark capture information
    
    Args:
        dicom_file: Path to DICOM file
        printer_host: Hostname/IP of the DICOM printer
        printer_port: Port of the DICOM printer
        logger: Logger object
    """
    # Ensure DCMTK is installed and in PATH
    try:
        cmd = [
            "dcmprscu",
            "-aec", CALLED_AE_TITLE,       # Called AE title (printer)
            "-aet", CALLING_AE_TITLE,      # Calling AE title (us)
            "+P", str(printer_port),       # Remote port
            printer_host,                  # Remote host
            # Parameters matching the Wireshark capture
            "-xf", "1.2.840.10008.5.1.1.9", # Basic Grayscale Print Management
            "-k", "FilmDestination=PROCESSOR", 
            "-k", "FilmSessionLabel=PYTHON_TEST",
            "-k", "NumberOfCopies=1",
            "-k", "PrintPriority=MEDIUM",
            "-k", "MediumType=PAPER",
            "-k", "FilmOrientation=PORTRAIT", 
            "-k", "FilmSizeID=8INX10IN",
            "-k", "MagnificationType=NONE",
            "-k", "SmoothingType=NONE",
            "-k", "BorderDensity=BLACK",
            "-k", "EmptyImageDensity=BLACK",
            "-k", "MinDensity=20",
            "-k", "MaxDensity=300",
            "-k", "ImageDisplayFormat=STANDARD\\1,1",
            # Match the implementation version from Wireshark
            "-ic", IMPLEMENTATION_UID,
            "-iv", IMPLEMENTATION_VERSION,
            "-pdu", str(MAX_PDU_LENGTH),   # Max PDU length
            "+Ka",                         # Keep association open
            dicom_file                     # Input DICOM file
        ]
        
        log_msg = f"Sending print job to {printer_host}:{printer_port}"
        if logger:
            logger.info(log_msg)
        else:
            print(log_msg)
            
        import subprocess
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        log_msg = f"Success: {result.stdout}"
        if logger:
            logger.info(log_msg)
        else:
            print(log_msg)
        return True
        
    except subprocess.CalledProcessError as e:
        log_msg = f"DCMTK printing failed: {e}\nError output: {e.stderr}"
        if logger:
            logger.error(log_msg)
        else:
            print(log_msg)
        return False
    except FileNotFoundError:
        log_msg = "Error: dcmprscu not found. Make sure DCMTK is installed and in your PATH."
        if logger:
            logger.error(log_msg)
        else:
            print(log_msg)
        return False

def find_dicom_files(data_dir):
    """
    Find all DICOM files in the data directory
    
    Args:
        data_dir: Path to the data directory
    
    Returns:
        List of paths to DICOM files
    """
    dicom_files = []
    for root, _, files in os.walk(data_dir):
        for file in files:
            if file.lower().endswith(('.dcm', '.dicom')) or '.' not in file:  # DICOM files often have no extension
                dicom_files.append(os.path.join(root, file))
    return dicom_files

if __name__ == "__main__":
    # Setup environment (creates data and logs directories)
    data_dir, logs_dir, logger = setup_environment()
    
    # Enable PyNetDICOM debug logging to our log file if needed
    # debug_logger(logs_dir)
    
    logger.info("Starting DICOM print application")
    
    # Find DICOM files in the data directory
    dicom_files = find_dicom_files(data_dir)
    if dicom_files:
        logger.info(f"Found {len(dicom_files)} DICOM files in {data_dir}")
    else:
        logger.warning(f"No DICOM files found in {data_dir}")
        logger.info(f"Please place DICOM files in the {data_dir} directory")
    
    # Find printers on the local network
    # You may need to scan your specific network range
    available_printers = find_dicom_printers('192.168.1.1', (104, 110), logger=logger)
    
    if available_printers:
        logger.info(f"Found {len(available_printers)} DICOM printer(s)")
        for host, port in available_printers:
            logger.info(f"Printer at {host}:{port}")
            
        # Print DICOM images to the first available printer
        if dicom_files:
            printer_host, printer_port = available_printers[0]
            
            for dicom_file in dicom_files:
                logger.info(f"Processing file: {dicom_file}")
                
                # Method 1: Use pynetdicom
                success = print_dicom_image(dicom_file, printer_host, printer_port, logger=logger)
                
                # Method 2: Use DCMTK (usually more reliable)
                # success = print_dicom_with_dcmtk(dicom_file, printer_host, printer_port, logger=logger)
                
                if success:
                    logger.info(f"Successfully printed {dicom_file}")
                else:
                    logger.error(f"Failed to print {dicom_file}")
    else:
        logger.warning("No DICOM printers found")
        
    # If you already know the printer address, you can call directly:
    # Example with known printer (uncomment to use)
    # known_printer_host = "192.168.1.100"
    # known_printer_port = 104
    # if dicom_files:
    #     for dicom_file in dicom_files:
    #         logger.info(f"Printing {dicom_file} to known printer at {known_printer_host}:{known_printer_port}")
    #         print_dicom_image(dicom_file, known_printer_host, known_printer_port, logger=logger)
    #         # Or use DCMTK:
    #         # print_dicom_with_dcmtk(dicom_file, known_printer_host, known_printer_port, logger=logger)
    
    logger.info("DICOM print application finished")