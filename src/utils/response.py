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

    package_model = package.build_model(context)
    return package_model


def build_dual_response(context):
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

    package_model = package.build_model(context)
    return package_model