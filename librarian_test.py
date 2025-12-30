
import sys
from pathlib import Path

# Add trinity to the python path
trinity_path = Path('/srv/janus/trinity/')
sys.path.insert(0, str(trinity_path))

from master_librarian_adapter import MasterLibrarianAdapter

def main():
    """Tests the MasterLibrarianAdapter functionality."""
    try:
        print("Initializing MasterLibrarianAdapter...")
        adapter = MasterLibrarianAdapter()

        # 1. Test reading a file
        # We need a file that is guaranteed to exist. Let's use a log file.
        # First, find a log file to read.
        log_dir = Path("/srv/janus/logs/")
        log_files = list(log_dir.glob("*.log"))
        if not log_files:
            print("⚠️ Could not find a log file to test reading. Skipping read test.")
            # Create a dummy file to test search
            dummy_log = log_dir / "dummy_test_log.log"
            dummy_log.write_text("This is a test log for MasterLibrarian.")
            target_log_for_search = "logs/dummy_test_log.log"
            search_pattern = "MasterLibrarian"
        else:
            target_log_for_read = f"logs/{log_files[0].name}"
            print(f"Testing read_file() on '{target_log_for_read}'...")
            content = adapter.read_file(target_log_for_read)
            if content:
                print("✅ read_file() test passed.")
            else:
                print(f"❌ read_file() test FAILED. Read empty content from {target_log_for_read}")
            target_log_for_search = "logs" # search the whole dir
            search_pattern = "error" # A common term in logs


        # 2. Test searching content
        print(f"Testing search_content() in '{target_log_for_search}' for pattern '{search_pattern}'...")
        search_results = adapter.search_content(search_pattern, target_log_for_search)

        # We don't know if there will be results, so we just check if it runs without error.
        # The result should be a dict.
        if isinstance(search_results, dict):
            print("✅ search_content() executed successfully.")
            print(f"Found {len(search_results)} files with matches.")
        else:
            print(f"❌ search_content() test FAILED. Expected a dict, got {type(search_results)}")

        # Clean up dummy file if created
        if 'dummy_log' in locals() and dummy_log.exists():
            dummy_log.unlink()
            print("Cleaned up dummy log file.")


    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
