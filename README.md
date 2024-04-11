# Markdown Report
A very simple report generator to save your experiment comments, figures and codes onto a markdown for future references.

## Installation
On the terminal, cd to the base directory for this project and run pip install
```
pip install .
```

## Usage
For most usecases, import and create a new MarkdownReport. Add whatever sections you want to save on to this object sequentially. Finally, call **save_report()** to generate the markdown file.

## Example
```python
from mdreport import MarkdownReport
from pathlib import Path
import matplotlib.pyplot as plt

plt.plot([1, 2, 3, 4])
plt.ylabel('some numbers')
fig = plt.gcf()
report = MarkdownReport(save_directory=Path("reports"), file_name="example_report", title="Example Report")
report.add_text_report("Heading 1", "This is a text section.")
report.add_image_report("Heading 2", fig)
report.add_code_report("Heading 3", "print('Hello World!')")
report.save_report()    # Saves to reports/example_report.md
```