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
    output_image = OutputImage(value=context.image)

    outputs = ThresholdingOutputs(
        outputImage=output_image
    )

    response = ThresholdingResponse(
        outputs=outputs
    )

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

    return package.build_model(context)


def build_dual_response(context):
    output_image_a = OutputImageA(value=context.output_a)
    output_image_b = OutputImageB(value=context.output_b)

    outputs = DualThresholdingOutputs(
        outputImageA=output_image_a,
        outputImageB=output_image_b
    )

    response = DualThresholdingResponse(
        outputs=outputs
    )

    selected_executor = DualThresholdingExecutor(
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

    return package.build_model(context)