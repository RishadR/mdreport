"""
Generate a report as a markdown file for future reference. Useful for storing expreiment results.
"""

from pathlib import Path
from typing import List
from mdutils.mdutils import MdUtils
from matplotlib.figure import Figure
from .sections import Section, TextSection, ImageSection, CodeSection


class MarkdownReport:
    """
    Create a Markdown report with text and image sections.

    Example Usage:
    -------------
    ```python
    from report_generator import MarkdownReport
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
    """

    FIG_FOLDER = "figures"

    def __init__(self, save_directory: Path, file_name: str, title: str, dpi: int = 300, author: str = "Unknown"):
        """
        Args:
            save_directory: Base directory to save the markdown file along with any related images.
            file_name: Name of the markdown file (without the .md extension)
            title: Title that goes at the top of the markdown file.
            dpi: DPI of the images to be saved in the report. Default is 300.
        """
        self.save_directory = save_directory
        # Create the save directory if it doesn't exist
        self.save_directory.mkdir(exist_ok=True)
        self.file_name = file_name
        self.title = title
        self.dpi = dpi
        markdown_save_path = save_directory / f"{file_name}.md"
        self.md_file = MdUtils(str(markdown_save_path), title=title, author=author)
        self.sections: List[Section] = []

    def add_text_report(self, heading, text) -> None:
        """
        Add a text section to the report.
        """
        self.sections.append(TextSection(heading, text))

    def add_image_report(self, heading, matplotlib_figure: Figure) -> None:
        """
        Add an image section to the report.
        """
        # Create a unique name and save the image
        image_save_path = self.save_directory / MarkdownReport.FIG_FOLDER / f"{self.file_name}_{len(self.sections)}.png"
        if image_save_path.parent.exists() is False:  # Create the figures folder if it doesn't exist
            self._create_figures_folder()
        matplotlib_figure.savefig(str(image_save_path), dpi=self.dpi)
        # The image link in the markdown file should be relative to the markdown file
        image_section = ImageSection(heading, str(image_save_path.relative_to(self.save_directory)))
        self.sections.append(image_section)

    def add_code_report(self, heading, code, language="") -> None:
        """
        Add a code section to the report.
        """
        code_section = CodeSection(heading, code, language)
        self.sections.append(code_section)

    def save_report(self):
        """
        Render and Save the report
        """
        for section in self.sections:
            if section.is_valid():
                section.render(self.md_file)

        self.md_file.create_md_file()

    def _create_figures_folder(self):
        """
        Create a folder to store the figures.
        """
        figures_folder = self.save_directory / MarkdownReport.FIG_FOLDER
        figures_folder.mkdir(exist_ok=True)
