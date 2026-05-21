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

        self.type = self.request.get_param("configType") or "GlobalThresholding"

        self.image_input = self.request.get_param("inputImage")
        self.image_second_input = self.request.get_param("inputImageSecond")

        self.load_parameters()

    def load_parameters(self):
        if self.type == "GlobalThresholding":
            self.global_type = self.request.get_param("configGlobalType") or "black white"

            if self.global_type in [
                "black white",
                "black white inv",
                "color like grey",
                "blackening",
                "blackening inv",
            ]:
                self.th_value = int(self.request.get_param("thresholdvalue") or 127)

            self.max_value = int(self.request.get_param("maxvalue") or 255)

        elif self.type == "LocalThresholding":
            self.local_type = self.request.get_param("configLocalType") or "mean"
            self.max_value = int(self.request.get_param("maxvalue") or 255)
            self.sub_block = int(self.request.get_param("subblock") or 11)
            self.off_set = int(self.request.get_param("offset") or 0)

            if self.sub_block < 3:
                self.sub_block = 3

            if self.sub_block % 2 == 0:
                self.sub_block += 1

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def thresholding(self, image):
        image = np.asarray(image).astype(np.uint8)

        if len(image.shape) == 3:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        th_image = image

        if self.type == "GlobalThresholding":
            if self.global_type == "black white":
                _, th_image = cv2.threshold(
                    image,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_BINARY
                )

            elif self.global_type == "black white inv":
                _, th_image = cv2.threshold(
                    image,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_BINARY_INV
                )

            elif self.global_type == "color like grey":
                _, th_image = cv2.threshold(
                    image,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_TRUNC
                )

            elif self.global_type == "blackening":
                _, th_image = cv2.threshold(
                    image,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_TOZERO
                )

            elif self.global_type == "blackening inv":
                _, th_image = cv2.threshold(
                    image,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_TOZERO_INV
                )

            elif self.global_type == "auto thresholding":
                _, th_image = cv2.threshold(
                    image,
                    0,
                    self.max_value,
                    cv2.THRESH_OTSU + cv2.THRESH_BINARY
                )

        elif self.type == "LocalThresholding":
            if self.local_type == "mean":
                th_image = cv2.adaptiveThreshold(
                    image,
                    self.max_value,
                    cv2.ADAPTIVE_THRESH_MEAN_C,
                    cv2.THRESH_BINARY,
                    self.sub_block,
                    self.off_set
                )

            elif self.local_type == "gaussian":
                th_image = cv2.adaptiveThreshold(
                    image,
                    self.max_value,
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY,
                    self.sub_block,
                    self.off_set
                )

        return th_image

    def run(self):
        img = Image.get_frame(
            img=self.image_input,
            redis_db=self.redis_db
        )

        img_second = Image.get_frame(
            img=self.image_second_input,
            redis_db=self.redis_db
        )

        img.value = self.thresholding(img.value)
        img_second.value = self.thresholding(img_second.value)

        self.image = Image.set_frame(
            img=img,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        self.imageSecond = Image.set_frame(
            img=img_second,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        package_model = build_dual_response(context=self)
        return package_model


if __name__ == "__main__":
    Executor(sys.argv[1]).run()