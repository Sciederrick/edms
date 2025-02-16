import os

class Utils:
    ALLOWED_EXTENSIONS = {'pdf'}

    @classmethod
    def allowed_file(cls, filename):
        return '.' in filename and filename.rsplit('.', )