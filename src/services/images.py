import shutil

from src.services.base import BaseService
from src.tasks.tasks import resize_image
from src.adapters.protocols import UploadFileProtocol


class ImageService(BaseService):
    def upload_image(self, file: UploadFileProtocol):
        image_path = f"/app/src/static/images/{file.filename}"
        with open(image_path, "wb+") as new_file:
            shutil.copyfileobj(file.file, new_file)

        resize_image.delay(image_path)
