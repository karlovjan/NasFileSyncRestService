class FileItem:
    """A file info class"""

    def __init__(self, file_name, last_modified):
        self.name = file_name
        self.mtime = last_modified

    def serialize(self):
        return {
            'name': self.name,
            'mtime': self.mtime
        }
