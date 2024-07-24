from PyQt5.QtWidgets import QApplication
from gui import CalculatorGUI
import sys

def main():
    # Initialize the application
    app = QApplication(sys.argv)
    
    try:
        # Create an instance of the CalculatorGUI
        calculator_window = CalculatorGUI()
        
        # Show the GUI window
        calculator_window.show()
        
        # Execute the application
        sys.exit(app.exec_())
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
