import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.core.window import Window

# Set window color
Window.clearcolor = (0.15, 0.15, 0.15, 1)

# KV language string for the layout
KV = '''
#:kivy 2.0.0

<CalcButton@Button>:
    font_size: '32sp'
    background_normal: ''
    background_color: (0.2, 0.2, 0.2, 1)
    size_hint: (0.25, 0.2)

<OperatorButton@CalcButton>:
    background_color: (0.98, 0.6, 0.22, 1) # Orange color for operators

<SpecialButton@CalcButton>:
    background_color: (0.6, 0.6, 0.6, 1) # Grey for C, +/-, %

<EqualsButton@CalcButton>:
    background_color: (0.2, 0.8, 0.2, 1) # Green for equals


<CalculatorLayout>:
    orientation: 'vertical'
    display: display_input

    TextInput:
        id: display_input
        text: "0"
        halign: "right"
        font_size: '72sp'
        readonly: True
        size_hint_y: 0.25
        background_color: (0.15, 0.15, 0.15, 1)
        foreground_color: (1, 1, 1, 1)
        padding: [20, 20]

    GridLayout:
        cols: 4
        spacing: 1
        size_hint_y: 0.75

        SpecialButton:
            text: "C"
            on_press: root.clear_display()
        SpecialButton:
            text: "⌫"
            on_press: root.backspace()
        SpecialButton:
            text: "%"
            on_press: root.add_operator('%')
        OperatorButton:
            text: "÷"
            on_press: root.add_operator('/')

        CalcButton:
            text: "7"
            on_press: root.add_to_display('7')
        CalcButton:
            text: "8"
            on_press: root.add_to_display('8')
        CalcButton:
            text: "9"
            on_press: root.add_to_display('9')
        OperatorButton:
            text: "×"
            on_press: root.add_operator('*')

        CalcButton:
            text: "4"
            on_press: root.add_to_display('4')
        CalcButton:
            text: "5"
            on_press: root.add_to_display('5')
        CalcButton:
            text: "6"
            on_press: root.add_to_display('6')
        OperatorButton:
            text: "-"
            on_press: root.add_operator('-')

        CalcButton:
            text: "1"
            on_press: root.add_to_display('1')
        CalcButton:
            text: "2"
            on_press: root.add_to_display('2')
        CalcButton:
            text: "3"
            on_press: root.add_to_display('3')
        OperatorButton:
            text: "+"
            on_press: root.add_operator('+')

        CalcButton:
            text: "0"
            size_hint_x: 0.5
            on_press: root.add_to_display('0')
        CalcButton:
            text: "."
            on_press: root.add_to_display('.')
        EqualsButton:
            text: "="
            on_press: root.calculate_result()
'''

Builder.load_string(KV)

class CalculatorLayout(BoxLayout):
    # Flag to check if the last action was a calculation
    is_result = False

    def clear_display(self):
        """ स्क्रीन साफ़ करें """
        self.display.text = "0"
        self.is_result = False

    def backspace(self):
        """ एक अक्षर मिटाएं """
        current_text = self.display.text
        if len(current_text) > 1 and current_text != "त्रुटि":
            self.display.text = current_text[:-1]
        else:
            self.display.text = "0"
        self.is_result = False

    def add_to_display(self, value):
        """ डिस्प्ले में अक्षर जोड़ें """
        current_text = self.display.text
        # If the last action was a calculation, start a new input
        if self.is_result:
            current_text = "0"
            self.is_result = False

        if current_text == "0" and value != ".":
            self.display.text = value
        else:
            # Prevent multiple decimal points in one number
            parts = current_text.replace('+', ' ').replace('-', ' ').replace('*', ' ').replace('/', ' ').replace('%', ' ').split()
            if value == "." and "." in parts[-1]:
                return
            self.display.text += value

    def add_operator(self, operator):
        """ ऑपरेटर जोड़ें """
        current_text = self.display.text
        self.is_result = False
        
        # Add operator if the last character is a digit
        if current_text and current_text[-1].isdigit() or current_text[-1] == '%':
            self.display.text += operator

    def calculate_result(self):
        """ गणना करें """
        try:
            expression = self.display.text.replace('÷', '/').replace('×', '*')
            
            # Basic percentage calculation: x% -> x/100
            if '%' in expression:
                # This simple logic assumes '%' is at the end of a number
                # e.g. "50%" becomes "0.5", "100+10%" becomes "100+0.1"
                import re
                expression = re.sub(r'(\d+\.?\d*)%', r'((\1)/100)', expression)
            
            result = eval(expression)
            if result == int(result):
                self.display.text = str(int(result))
            else:
                self.display.text = str(round(result, 8))
            self.is_result = True
        except Exception as e:
            self.display.text = "त्रुटि" # "Error" in Hindi
            self.is_result = True

class CalculatorApp(App):
    def build(self):
        self.title = "गणक" # "Calculator" in Hindi
        return CalculatorLayout()

if __name__ == '__main__':
    CalculatorApp().run()
