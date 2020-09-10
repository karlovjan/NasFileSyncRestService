class FileItem:
    """A file info class"""

    def __init__(self, file_name, modified_at):
        self.name = file_name
        self.mtime = modified_at

    def serialize(self):
        return {
            'name': self.name,
            'mtime': self.mtime
        }