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

        self.image_a = self.request.get_param("inputImageA")
        self.image_b = self.request.get_param("inputImageB")

        self.load_parameters()

    def load_parameters(self):
        if self.type == "DualBlur":
            self.blur_size = int(self.request.get_param("subblock"))

        elif self.type == "DualThreshold":
            self.threshold_value = int(self.request.get_param("thresholdvalue"))
            self.max_value = int(self.request.get_param("maxvalue"))

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

        if self.type == "DualThreshold":
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
        img_a = Image.get_frame(
            img=self.image_a,
            redis_db=self.redis_db
        )

        img_b = Image.get_frame(
            img=self.image_b,
            redis_db=self.redis_db
        )

        img_a.value = self.process(img_a.value)
        img_b.value = self.process(img_b.value)

        self.output_a = Image.set_frame(
            img=img_a,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        self.output_b = Image.set_frame(
            img=img_b,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        return build_dual_response(context=self)


if __name__ == "__main__":
    Executor(sys.argv[1]).run()