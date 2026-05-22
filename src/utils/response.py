from sdks.novavision.src.helper.package import PackageHelper

from components.DemoThresholding.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,

    ThresholdingExecutor,
    ThresholdingResponse,
    ThresholdingOutputs,

    DemoSecondExecutor,
    DemoSecondResponse,
    DemoSecondOutputs,

    OutputImage,
    OutputImageSecond,
)


def build_response(context):
    if hasattr(context, "imageSecond"):
        output_image = OutputImage(value=context.image)
        output_image_second = OutputImageSecond(value=context.imageSecond)

        outputs = DemoSecondOutputs(
            outputImage=output_image,
            outputImageSecond=output_image_second
        )

        response = DemoSecondResponse(outputs=outputs)
        selected_executor = DemoSecondExecutor(value=response)

    else:
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
    return build_response(context)