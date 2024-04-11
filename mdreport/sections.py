from abc import ABC, abstractmethod
from mdutils.mdutils import MdUtils

class Section(ABC):
    """
    Abstract class for a section in the markdown report. All types of sections must inherit from this class.
    """

    @abstractmethod
    def render(self, md_file: MdUtils):
        """
        Render the section in the markdown file. This section should include all the pre-processing required to render
        followed by a call to some MdUtils methods to render the section.

        Example MdUtils methods: new_header, new_paragraph, new_inline_image, insert_code, etc.
        """

    @abstractmethod
    def is_valid(self) -> bool:
        """
        Is the section valid to be rendered in the markdown file. If this returns False, the section will be ignored
        during rendering.
        """


class TextSection(Section):
    """
    Single text section in the markdown report.
    """

    def __init__(self, heading, text):
        self.heading = heading
        self.text = text

    def render(self, md_file: MdUtils):
        md_file.new_header(level=1, title=self.heading)
        md_file.new_paragraph(self.text)
        md_file.new_line()

    def is_valid(self) -> bool:
        if len(self.text) == 0:
            return False
        return True


class ImageSection(Section):
    """
    Single image section in the markdown report.
    """

    def __init__(self, heading, image_path: str):
        self.heading = heading
        self.image_path = image_path

    def render(self, md_file: MdUtils):
        md_file.new_header(level=1, title=self.heading)
        md_file.new_line()
        # mdFile.new_inline_image(text=self.heading, path=str(self.image_path))
        md_file.new_line(text=rf"![{self.heading}]({self.image_path})")
        md_file.new_line()

    def is_valid(self) -> bool:
        return True


class CodeSection(Section):
    """
    Single code section in the markdown report.
    """

    def __init__(self, heading: str, code: str, language: str = ""):
        self.heading = heading
        self.code = code
        self.language = language

    def render(self, md_file: MdUtils):
        md_file.new_header(level=1, title=self.heading)
        md_file.insert_code(self.code, language=self.language)
        md_file.new_line()

    def is_valid(self) -> bool:
        if len(self.code) == 0:
            return False
        return True
