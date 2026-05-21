import os
import cv2
import sys
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.DemoThresholding.src.utils.response import build_dual_response
from components.DemoThresholding.src.models.PackageModel import PackageModel


class DualThresholding(Component):
    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(**self.request.data)

        self.type = self.request.get_param("configDualType")

        self.image_input = self.request.get_param("inputImage")
        self.image_second_input = self.request.get_param("inputImageSecond")

        self.load_parameters()

    def load_parameters(self):
        if self.type == "DualBlur":
            self.blur_size = int(self.request.get_param("subblock") or 11)

        elif self.type == "DualThreshold":
            self.threshold_value = int(self.request.get_param("thresholdvalue") or 127)
            self.max_value = int(self.request.get_param("maxvalue") or 255)

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def process(self, image):
        image = np.asarray(image).astype(np.uint8)

        if self.type == "DualBlur":
            k = int(self.blur_size)

            if k < 3:
                k = 3

            if k % 2 == 0:
                k += 1

            return cv2.GaussianBlur(image, (k, k), 0)

        elif self.type == "DualThreshold":
            if len(image.shape) == 3:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            _, th_image = cv2.threshold(
                image,
                self.threshold_value,
                self.max_value,
                cv2.THRESH_BINARY
            )

            return th_image

        return image

    def run(self):
        img = Image.get_frame(
            img=self.image_input,
            redis_db=self.redis_db
        )

        img_second = Image.get_frame(
            img=self.image_second_input,
            redis_db=self.redis_db
        )

        img.value = self.process(img.value)
        img_second.value = self.process(img_second.value)

        self.image = Image.set_frame(
            img=img.value,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        self.imageSecond = Image.set_frame(
            img=img_second.value,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        package_model = build_dual_response(context=self)
        return package_model


if __name__ == "__main__":
    Executor(sys.argv[1]).run()