from sdks.novavision.src.helper.package import PackageHelper

from components.DemoThresholding.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,

    ThresholdingExecutor,
    ThresholdingResponse,
    ThresholdingOutputs,

    DualThresholdingExecutor,
    DualThresholdingResponse,
    DualThresholdingOutputs,

    OutputImage,
    OutputImageSecond,
)


def build_response(context):
    """
    Tek input / tek output olan Thresholding executor response'unu oluşturur.
    context.image bekler.
    """

    output_image = OutputImage(value=context.image)

    outputs = ThresholdingOutputs(
        outputImage=output_image
    )

    response = ThresholdingResponse(outputs=outputs)
    selected_executor = ThresholdingExecutor(value=response)

    executor = ConfigExecutor(value=selected_executor)
    package_configs = PackageConfigs(executor=executor)

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs
    )

    return package.build_model(context)


def build_dual_response(context):
    """
    İki input / iki output olan DualThresholding executor response'unu oluşturur.
    context.image ve context.imageSecond bekler.
    """

    output_image = OutputImage(value=context.image)
    output_image_second = OutputImageSecond(value=context.imageSecond)

    outputs = DualThresholdingOutputs(
        outputImage=output_image,
        outputImageSecond=output_image_second
    )

    response = DualThresholdingResponse(outputs=outputs)
    selected_executor = DualThresholdingExecutor(value=response)

    executor = ConfigExecutor(value=selected_executor)
    package_configs = PackageConfigs(executor=executor)

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs
    )

    return package.build_model(context)