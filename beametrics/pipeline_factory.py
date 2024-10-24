from abc import ABC, abstractmethod
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam import Pipeline
from typing import Optional
from dataclasses import dataclass


@dataclass
class DataflowPipelineConfig:
    """Configuration for Google Cloud Dataflow pipeline."""

    project_id: str
    region: str
    temp_location: str
    streaming: bool = True
    runner: str = "DataflowRunner"
    setup_file: str = "./setup.py"

    def to_pipeline_options(self) -> PipelineOptions:
        """Convert config to PipelineOptions."""
        return PipelineOptions(
            [
                f"--project={self.project_id}",
                f"--region={self.region}",
                f"--temp_location={self.temp_location}",
                f"--runner={self.runner}",
                f"--setup_file={self.setup_file}",
                "--streaming",
            ]
        )


class MetricsPipelineFactory(ABC):
    """Abstract factory for creating beam pipelines with specific configurations."""

    @abstractmethod
    def create_pipeline_options(self) -> PipelineOptions:
        """Create pipeline options specific to the implementation."""
        pass

    @abstractmethod
    def create_pipeline(self, options: Optional[PipelineOptions] = None) -> Pipeline:
        """Create a pipeline with the given options or default options."""
        pass


class GoogleCloudPipelineFactory(MetricsPipelineFactory):
    """Factory for creating pipelines that run on Google Cloud Dataflow."""

    def __init__(self, config: DataflowPipelineConfig):
        self.config = config

    def create_pipeline_options(self) -> PipelineOptions:
        return self.config.to_pipeline_options()

    def create_pipeline(self, options: Optional[PipelineOptions] = None) -> Pipeline:
        if options is None:
            options = self.create_pipeline_options()
        return Pipeline(options=options)
