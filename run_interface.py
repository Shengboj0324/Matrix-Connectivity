#!/usr/bin/env python3

import sys
import subprocess
import webbrowser
import time
from pathlib import Path

def show_interface_menu():
    print("=== Matrix Connectivity Investigation ===")
    print("Choose your interface:")
    print()
    print("1. Web Interface (Recommended)")
    print("   - Interactive graph editor with visual canvas")
    print("   - Real-time discovery experiments")
    print("   - Performance benchmarking with results display")
    print("   - Matrix powers visualization")
    print()
    print("2. Command Line Interface")
    print("   - Text-based menu system")
    print("   - Full access to all experiments")
    print("   - Detailed mathematical output")
    print("   - Suitable for headless environments")
    print()
    print("3. Exit")
    print()

def launch_web_interface():
    print("Starting web interface...")
    print("This will:")
    print("- Start a local web server")
    print("- Open your default browser")
    print("- Provide full interactive capabilities")
    print()
    
    try:
        import webbrowser
        
        server_script = Path(__file__).parent / 'editor' / 'server.py'
        
        print("Starting server on http://localhost:8000")
        print("Press Ctrl+C to stop the server when done.")
        print()
        
        subprocess.run([sys.executable, str(server_script)], cwd=Path(__file__).parent)
        
    except KeyboardInterrupt:
        print("\nWeb interface stopped.")
    except Exception as e:
        print(f"Error starting web interface: {e}")
        print("Please ensure you have Python 3.7+ installed.")

def launch_cli_interface():
    print("Starting command line interface...")
    print()
    
    try:
        cli_script = Path(__file__).parent / 'cli_interface.py'
        subprocess.run([sys.executable, str(cli_script)], cwd=Path(__file__).parent)
    except Exception as e:
        print(f"Error starting CLI interface: {e}")

def main():
    while True:
        show_interface_menu()
        
        try:
            choice = input("Enter your choice (1-3): ").strip()
            
            if choice == '1':
                launch_web_interface()
            elif choice == '2':
                launch_cli_interface()
            elif choice == '3':
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
                print()
        
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()
