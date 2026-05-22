from sdks.novavision.src.helper.package import PackageHelper

from components.DemoThresholding.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,

    ThresholdingExecutor,
    ThresholdingResponse,
    ThresholdingOutputs,
    OutputImage,

    DualThresholdingExecutor,
    DualThresholdingResponse,
    DualThresholdingOutputs,
    OutputImageA,
    OutputImageB,
)


def build_response(context):
    """
    Tekli veya ikili executor response'unu otomatik oluşturur.
    Thresholding için: context.image
    DualThresholding için: context.output_a, context.output_b
    """

    if hasattr(context, "output_a") and hasattr(context, "output_b"):
        output_image_a = OutputImageA(value=context.output_a)
        output_image_b = OutputImageB(value=context.output_b)

        outputs = DualThresholdingOutputs(
            outputImageA=output_image_a,
            outputImageB=output_image_b
        )

        response = DualThresholdingResponse(outputs=outputs)

        selected_executor = DualThresholdingExecutor(
            value=response
        )

    else:
        output_image = OutputImage(value=context.image)

        outputs = ThresholdingOutputs(
            outputImage=output_image
        )

        response = ThresholdingResponse(outputs=outputs)

        selected_executor = ThresholdingExecutor(
            value=response
        )

    executor = ConfigExecutor(
        value=selected_executor
    )

    package_configs = PackageConfigs(
        executor=executor
    )

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs
    )

    package_model = package.build_model(context)
    return package_model


def build_dual_response(context):
    """
    DualThresholding.py eski import yapısıyla uyumlu kalsın diye bırakıldı.
    Asıl işi build_response yapıyor.
    """
    return build_response(context)