from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLineEdit, QLabel, QTextEdit, QApplication, QHBoxLayout
from PyQt5.QtCore import Qt
from groq import Groq
import sys
import os
from dotenv import load_dotenv

class CalculatorGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        load_dotenv()  # Load environment variables from .env file
        self.api_key = os.getenv("GROQ_API_KEY")
        if not self.api_key:
            print("API key is not set in the .env file.")
            sys.exit(1)
        
        self.client = Groq(api_key=self.api_key)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Math Genie')
        self.setGeometry(100, 100, 600, 400)  # Adjust size for better usability
        self.setStyleSheet("background-color: #2e2e2e;")  # Dark background for the main window

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()

        # Chat area
        self.chat_area = QTextEdit(self)
        self.chat_area.setReadOnly(True)
        self.chat_area.setStyleSheet("background-color: #ffffff; color: #000000; border-radius: 5px; padding: 10px;")
        layout.addWidget(self.chat_area)

        # Input field for user messages
        self.input_box = QLineEdit(self)
        self.input_box.setPlaceholderText("Type a message...")
        self.input_box.setClearButtonEnabled(True)
        self.input_box.setStyleSheet("background-color: #ffffff; color: #000000; border-radius: 5px; padding: 10px;")
        layout.addWidget(self.input_box)

        # Button to send message
        send_button = QPushButton('Send', self)
        send_button.clicked.connect(self.send_message)
        send_button.setStyleSheet("background-color: #4caf50; color: #ffffff; border-radius: 5px; padding: 10px;")
        layout.addWidget(send_button, alignment=Qt.AlignRight)

        # Button layout for additional functionality (if needed)
        button_layout = QHBoxLayout()

        # Button to clear input
        clear_button = QPushButton('Clear', self)
        clear_button.clicked.connect(self.clear_input)
        clear_button.setStyleSheet("background-color: #f44336; color: #ffffff; border-radius: 5px; padding: 10px;")
        button_layout.addWidget(clear_button)

        layout.addLayout(button_layout)

        central_widget.setLayout(layout)

    def send_message(self):
        user_input = self.input_box.text()
        if not user_input:
            return
        
        # Add user message to chat area
        self.add_user_message(user_input)

        # Get response from the AI
        response = self.get_ai_response(user_input)
        self.add_app_message(response)

        # Clear input box
        self.input_box.clear()

    def add_user_message(self, msg):
        self.chat_area.append(f'<p style="color: blue; text-align: right;">You: {msg}</p>')
        
    def add_app_message(self, msg):
        self.chat_area.append(f'<p style="color: black; text-align: left;">Math Genie: {msg}</p>')

    def clear_input(self):
        self.input_box.clear()

    def get_ai_response(self, user_input):
        try:
            completion = self.client.chat.completions.create(
                model="llama3-70b-8192",
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "In the realm of calculations, I am Math Genie, your faithful companion. My purpose is to assist and serve, showing utmost precision and reliability. Address your queries with clarity, and I shall navigate the labyrinth of numbers and functions with unwavering expertise. Together, we shall unravel the mysteries of mathematics."
                        )
                    },
                    {
                        "role": "user",
                        "content": user_input
                    }
                ],
                temperature=0.7,
                max_tokens=1024,
                top_p=1,
                stream=True,
                stop=None,
            )
            response = ""
            for chunk in completion:
                response += chunk.choices[0].delta.content or ""
            return response.strip()
        except Exception as e:
            return f"Error: {str(e)}"

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CalculatorGUI()
    window.show()
    sys.exit(app.exec_())
