import os
import cv2
import sys
from matplotlib import image
import numpy as np

sys.path.append(os.path.join(os.path.dirname(__file__), "../../../../"))

from sdks.novavision.src.media.image import Image
from sdks.novavision.src.base.component import Component
from sdks.novavision.src.helper.executor import Executor

from components.DemoThresholding.src.utils.response import build_response, build_dual_response
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
        if self.type == "GlobalThresholding":
            self.global_type = self.request.get_param("configGlobalType")
            self.max_value = int(self.request.get_param("maxvalue"))

            if self.global_type in [
                "black white",
                "black white inv",
                "color like grey",
                "blackening",
                "blackening inv"
            ]:
                self.th_value = int(self.request.get_param("thresholdvalue"))

        elif self.type == "LocalThresholding":
            self.local_type = self.request.get_param("configLocalType")
            self.max_value = int(self.request.get_param("maxvalue"))
            self.sub_block = int(self.request.get_param("subblock"))
            self.off_set = int(self.request.get_param("offset"))

    @staticmethod
    def bootstrap(config: dict) -> dict:
        return {}

    def thresholding(self, image_a, image_b):
        image_a = np.asarray(image_a).astype(np.uint8)
        image_b = np.asarray(image_b).astype(np.uint8)

        if len(image_a.shape) == 3:
            image_a = cv2.cvtColor(image_a, cv2.COLOR_BGR2GRAY)
        if len(image_b.shape) == 3:
            image_b = cv2.cvtColor(image_b, cv2.COLOR_BGR2GRAY)

        th_image_a = image_a
        th_image_b = image_b

        if self.type == "GlobalThresholding":
            if self.global_type == "black white":
                _, th_image_a = cv2.threshold(
                    image_a,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_BINARY
                )
                _, th_image_b = cv2.threshold(
                    image_b,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_BINARY
                )

            elif self.global_type == "black white inv":
                _, th_image_a = cv2.threshold(
                    image_a,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_BINARY_INV
                )
                _, th_image_b = cv2.threshold(
                    image_b,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_BINARY_INV
                )

            elif self.global_type == "color like grey":
                _, th_image_a = cv2.threshold(
                    image_a,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_TRUNC
                )
                _, th_image_b = cv2.threshold(
                    image_b,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_TRUNC
                )

            elif self.global_type == "blackening":
                _, th_image_a = cv2.threshold(
                    image_a,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_TOZERO
                )
                _, th_image_b = cv2.threshold(
                    image_b,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_TOZERO
                )

            elif self.global_type == "blackening inv":
                _, th_image_b = cv2.threshold(
                    image_b,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_TOZERO_INV
                )
                _, th_image_a = cv2.threshold(
                    image_a,
                    self.th_value,
                    self.max_value,
                    cv2.THRESH_TOZERO_INV
                )

            elif self.global_type == "auto thresholding":
                _, th_image_a = cv2.threshold(
                    image_a,
                    0,
                    self.max_value,
                    cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )
                _, th_image_b = cv2.threshold(
                    image_b,
                    0,
                    self.max_value,
                    cv2.THRESH_BINARY + cv2.THRESH_OTSU
                )

        elif self.type == "LocalThresholding":
            if self.sub_block < 3:
                self.sub_block = 3

            if self.sub_block % 2 == 0:
                self.sub_block += 1

            if self.local_type == "mean":
                th_image_a = cv2.adaptiveThreshold(
                    image_a,
                    self.max_value,
                    cv2.ADAPTIVE_THRESH_MEAN_C,
                    cv2.THRESH_BINARY,
                    self.sub_block,
                    self.off_set
                )
                th_image_b = cv2.adaptiveThreshold(
                    image_b,
                    self.max_value,
                    cv2.ADAPTIVE_THRESH_MEAN_C,
                    cv2.THRESH_BINARY,
                    self.sub_block,
                    self.off_set
                )


            elif self.local_type == "gaussian":
                th_image_b = cv2.adaptiveThreshold(
                    image_b,
                    self.max_value,
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY,
                    self.sub_block,
                    self.off_set
                )
                th_image_a = cv2.adaptiveThreshold(
                    image_a,
                    self.max_value,
                    cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
                    cv2.THRESH_BINARY,
                    self.sub_block,
                    self.off_set
                )

        return th_image_a, th_image_b

    def run(self):
        img_a = Image.get_frame(img=self.image_a, redis_db=self.redis_db)
        img_b = Image.get_frame(img=self.image_b, redis_db=self.redis_db)

        img_a.value = self.thresholding(img_a.value)
        img_b.value = self.thresholding(img_b.value)

        self.image_a = Image.set_frame(
            img=img_a,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        self.image_b = Image.set_frame(
            img=img_b,
            package_uID=self.uID,
            redis_db=self.redis_db
        )

        packageModel = build_dual_response(context=self)
        return packageModel


if __name__ == "__main__":
    Executor(sys.argv[1]).run()



# class DualThresholding(Component):
#     def __init__(self, request, bootstrap):
#         super().__init__(request, bootstrap)

#         self.request.model = PackageModel(**self.request.data)

#         self.type = self.request.get_param("configDualType")

#         self.image_a = self.request.get_param("inputImageA")
#         self.image_b = self.request.get_param("inputImageB")

#         self.load_parameters()

#     def load_parameters(self):
#         if self.type == "DualBlur":
#             self.blur_size = int(self.request.get_param("subblock"))

#         elif self.type == "DualThreshold":
#             self.threshold_value = int(self.request.get_param("thresholdvalue"))
#             self.max_value = int(self.request.get_param("maxvalue"))

#     @staticmethod
#     def bootstrap(config: dict) -> dict:
#         return {}

#     def process(self, image):
#         image = np.asarray(image).astype(np.uint8)

#         if self.type == "DualBlur":
#             k = int(self.blur_size)

#             if k < 3:
#                 k = 3

#             if k % 2 == 0:
#                 k += 1

#             return cv2.GaussianBlur(image, (k, k), 0)

#         elif self.type == "DualThreshold":
#             if len(image.shape) == 3:
#                 image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

#             _, th_image = cv2.threshold(
#                 image,
#                 self.threshold_value,
#                 self.max_value,
#                 cv2.THRESH_BINARY
#             )

#             return th_image

#         return image

#     def run(self):
#         img_a = Image.get_frame(img=self.image_a, redis_db=self.redis_db)
#         img_b = Image.get_frame(img=self.image_b, redis_db=self.redis_db)

#         img_a.value = self.process(img_a.value)
#         img_b.value = self.process(img_b.value)

#         self.output_a = Image.set_frame(
#             img=img_a,
#             package_uID=self.uID,
#             redis_db=self.redis_db
#         )

#         self.output_b = Image.set_frame(
#             img=img_b,
#             package_uID=self.uID,
#             redis_db=self.redis_db
#         )

#         # packageModel = build_dual_response(context=self)
#         return build_response(context=self) 


# if __name__ == "__main__":
#     Executor(sys.argv[1]).run()