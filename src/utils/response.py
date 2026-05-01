from sdks.novavision.src.helper.package import PackageHelper
from components.Thresholding.src.models.PackageModel import (
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
    outputImage = OutputImage(value=context.image)
    outputs = ThresholdingOutputs(outputImage=outputImage)
    response = ThresholdingResponse(outputs=outputs)
    thresholdingExecutor = ThresholdingExecutor(value=response)
    executor = ConfigExecutor(value=thresholdingExecutor)
    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel


def build_dual_response(context):
    outputImageA = OutputImageA(value=context.output_a)
    outputImageB = OutputImageB(value=context.output_b)

    outputs = DualThresholdingOutputs(
        outputImageA=outputImageA,
        outputImageB=outputImageB
    )

    response = DualThresholdingResponse(outputs=outputs)
    dualExecutor = DualThresholdingExecutor(value=response)
    executor = ConfigExecutor(value=dualExecutor)

    packageConfigs = PackageConfigs(executor=executor)
    package = PackageHelper(packageModel=PackageModel, packageConfigs=packageConfigs)
    packageModel = package.build_model(context)
    return packageModel