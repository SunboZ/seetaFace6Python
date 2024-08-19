import os
import PyQt5

qt_designer_path = os.path.join(os.path.dirname(PyQt5.__file__), 'Qt', 'bin', 'designer.exe')
print(f"Qt Designer is located at: {qt_designer_path}")