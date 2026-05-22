class ThresholdingInputs(Inputs):
    inputImage: InputImage


class DemoSecondInputs(Inputs):
    inputImage: InputImage
    inputImageSecond: InputImageSecond


class ThresholdingConfigs(Configs):
    configType: ConfigType


class ThresholdingOutputs(Outputs):
    outputImage: OutputImage


class DemoSecondOutputs(Outputs):
    outputImage: OutputImage
    outputImageSecond: OutputImageSecond


class ThresholdingRequest(Request):
    inputs: ThresholdingInputs
    configs: ThresholdingConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class DemoSecondRequest(Request):
    inputs: DemoSecondInputs
    configs: ThresholdingConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class ThresholdingResponse(Response):
    outputs: ThresholdingOutputs


class DemoSecondResponse(Response):
    outputs: DemoSecondOutputs


class ThresholdingExecutor(Config):
    name: Literal["Thresholding"] = "Thresholding"
    value: Union[ThresholdingRequest, ThresholdingResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Thresholding Executor"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class DemoSecondExecutor(Config):
    name: Literal["DemoSecondExecutor"] = "DemoSecondExecutor"
    value: Union[DemoSecondRequest, DemoSecondResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Dual Thresholding Executor"
        json_schema_extra = {
            "target": {
                "value": 1
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[ThresholdingExecutor, DemoSecondExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoThresholding"] = "DemoThresholding"