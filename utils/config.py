from omegaconf import OmegaConf


def load_config_from_yaml(file_path: str) -> OmegaConf:
    """Loads a configuration from a .yaml file and returns it as an OmegaConf dictionary."""
    config = OmegaConf.load(file_path)
    return config