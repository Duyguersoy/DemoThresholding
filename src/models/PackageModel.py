from pydantic import Field, validator
from typing import List, Optional, Union, Literal

from sdks.novavision.src.base.model import (
    Package,
    Image,
    Inputs,
    Configs,
    Outputs,
    Response,
    Request,
    Output,
    Input,
    Config,
)


class InputImage(Input):
    name: Literal["inputImage"] = "inputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Image"


class InputImageSecond(Input):
    name: Literal["inputImageSecond"] = "inputImageSecond"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Second Image"


class OutputImage(Output):
    name: Literal["outputImage"] = "outputImage"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Image"


class OutputImageSecond(Output):
    name: Literal["outputImageSecond"] = "outputImageSecond"
    value: Union[List[Image], Image]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        value = values.get("value")
        if isinstance(value, Image):
            return "object"
        elif isinstance(value, list):
            return "list"
        return "object"

    class Config:
        title = "Second Output Image"


class ConfigOffSet(Config):
    name: Literal["offset"] = "offset"
    value: int = Field(default=0, ge=-15.0, le=15.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [-15, 15]"] = "integers between [-15, 15]"

    class Config:
        title = "Offset"
        json_schema_extra = {
            "shortDescription": "Sensitivity Constant"
        }


class ConfigSubBlock(Config):
    name: Literal["subblock"] = "subblock"
    value: int = Field(default=11, ge=3.0, le=191.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["odd integers between [3, 191]"] = "odd integers between [3, 191]"

    @validator("value")
    def validate_odd_integer_range(cls, value):
        if value % 2 == 0 or value < 3 or value > 191:
            raise ValueError("Invalid value: must be an odd integer between 3 and 191")
        return value

    class Config:
        title = "SubBlock Size"
        json_schema_extra = {
            "shortDescription": "Neighborhood Area Size"
        }


class ConfigMaxVal(Config):
    name: Literal["maxvalue"] = "maxvalue"
    value: int = Field(default=255, ge=0, le=255.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [0, 255]"] = "integers between [0, 255]"

    class Config:
        title = "Max Value"
        json_schema_extra = {
            "shortDescription": "Active Pixel Color"
        }


class ConfigThresholdVal(Config):
    name: Literal["thresholdvalue"] = "thresholdvalue"
    value: int = Field(default=127, ge=0, le=255.0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["integers between [0, 255]"] = "integers between [0, 255]"

    class Config:
        title = "Threshold Value"
        json_schema_extra = {
            "shortDescription": "Cutoff Point"
        }


class ConfigTypeAutoThresholding(Config):
    name: Literal["auto thresholding"] = "auto thresholding"
    maxVal: ConfigMaxVal = ConfigMaxVal()
    value: Literal["auto thresholding"] = "auto thresholding"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "AUTO_TH"


class ConfigTypeBlackeningInv(Config):
    name: Literal["blackening inv"] = "blackening inv"
    thresholdVal: ConfigThresholdVal = ConfigThresholdVal()
    maxVal: ConfigMaxVal = ConfigMaxVal()
    value: Literal["blackening inv"] = "blackening inv"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "TOZERO_INV_TH"


class ConfigTypeBlackening(Config):
    name: Literal["blackening"] = "blackening"
    thresholdVal: ConfigThresholdVal = ConfigThresholdVal()
    maxVal: ConfigMaxVal = ConfigMaxVal()
    value: Literal["blackening"] = "blackening"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "TOZERO_TH"


class ConfigTypeColorLikeGrey(Config):
    name: Literal["color like grey"] = "color like grey"
    thresholdVal: ConfigThresholdVal = ConfigThresholdVal()
    maxVal: ConfigMaxVal = ConfigMaxVal()
    value: Literal["color like grey"] = "color like grey"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "TRUNCATED_TH"


class ConfigTypeBlackWhiteInv(Config):
    name: Literal["black white inv"] = "black white inv"
    thresholdVal: ConfigThresholdVal = ConfigThresholdVal()
    maxVal: ConfigMaxVal = ConfigMaxVal()
    value: Literal["black white inv"] = "black white inv"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "BINARY_INV_TH"


class ConfigTypeBlackWhite(Config):
    name: Literal["black white"] = "black white"
    thresholdVal: ConfigThresholdVal = ConfigThresholdVal()
    maxVal: ConfigMaxVal = ConfigMaxVal()
    value: Literal["black white"] = "black white"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "BINARY_TH"


class ConfigMean(Config):
    name: Literal["mean"] = "mean"
    maxVal: ConfigMaxVal = ConfigMaxVal()
    subBlock: ConfigSubBlock = ConfigSubBlock()
    offSet: ConfigOffSet = ConfigOffSet()
    value: Literal["mean"] = "mean"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Mean"


class ConfigGaussian(Config):
    name: Literal["gaussian"] = "gaussian"
    maxVal: ConfigMaxVal = ConfigMaxVal()
    subBlock: ConfigSubBlock = ConfigSubBlock()
    offSet: ConfigOffSet = ConfigOffSet()
    value: Literal["gaussian"] = "gaussian"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Gaussian"


class ConfigLocalType(Config):
    name: Literal["configLocalType"] = "configLocalType"
    value: Union[ConfigMean, ConfigGaussian] = ConfigMean()
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Type"
        json_schema_extra = {
            "shortDescription": "Adaptive Algorithm"
        }


class ConfigGlobalType(Config):
    name: Literal["configGlobalType"] = "configGlobalType"
    value: Union[
        ConfigTypeBlackWhite,
        ConfigTypeBlackWhiteInv,
        ConfigTypeColorLikeGrey,
        ConfigTypeBlackening,
        ConfigTypeBlackeningInv,
        ConfigTypeAutoThresholding,
    ] = ConfigTypeBlackWhite()
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Type"
        json_schema_extra = {
            "shortDescription": "Separation Logic"
        }


class ConfigTypeLocalThresholding(Config):
    configEdit: ConfigLocalType = ConfigLocalType()
    name: Literal["LocalThresholding"] = "LocalThresholding"
    value: Literal["LocalThresholding"] = "LocalThresholding"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Local Thresholding"


class ConfigTypeGlobalThresholding(Config):
    configEdit: ConfigGlobalType = ConfigGlobalType()
    name: Literal["GlobalThresholding"] = "GlobalThresholding"
    value: Literal["GlobalThresholding"] = "GlobalThresholding"
    type: Literal["string"] = "string"
    field: Literal["option"] = "option"

    class Config:
        title = "Global Thresholding"


class ConfigType(Config):
    name: Literal["configType"] = "configType"
    value: Union[ConfigTypeGlobalThresholding, ConfigTypeLocalThresholding] = ConfigTypeGlobalThresholding()
    type: Literal["object"] = "object"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Method"
        json_schema_extra = {
            "shortDescription": "Segmentation Strategy"
        }


class ThresholdingInputs(Inputs):
    inputImage: InputImage


class DualThresholdingInputs(Inputs):
    inputImage: InputImage
    inputImageSecond: InputImageSecond


class ThresholdingConfigs(Configs):
    configType: ConfigType = ConfigType()


class ThresholdingOutputs(Outputs):
    outputImage: OutputImage


class DualThresholdingOutputs(Outputs):
    outputImage: OutputImage
    outputImageSecond: OutputImageSecond


class ThresholdingRequest(Request):
    inputs: Optional[ThresholdingInputs] = None
    configs: ThresholdingConfigs = ThresholdingConfigs()

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class DualThresholdingRequest(Request):
    inputs: Optional[DualThresholdingInputs] = None
    configs: ThresholdingConfigs = ThresholdingConfigs()

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class ThresholdingResponse(Response):
    outputs: ThresholdingOutputs


class DualThresholdingResponse(Response):
    outputs: DualThresholdingOutputs


class ThresholdingExecutor(Config):
    name: Literal["Thresholding"] = "Thresholding"
    value: Union[ThresholdingRequest, ThresholdingResponse] = ThresholdingRequest()
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Thresholding Executor"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class DualThresholdingExecutor(Config):
    name: Literal["DualThresholding"] = "DualThresholding"
    value: Union[DualThresholdingRequest, DualThresholdingResponse] = DualThresholdingRequest()
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
    value: Union[ThresholdingExecutor, DualThresholdingExecutor] = ThresholdingExecutor()
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"


class PackageConfigs(Configs):
    executor: ConfigExecutor = ConfigExecutor()


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["DemoThresholding"] = "DemoThresholding"