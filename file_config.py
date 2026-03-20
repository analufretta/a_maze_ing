
from mazegen import MazeConfig


class FileConfig:
    def __init__(self, filepath: str) -> None:
        """Initialize FileConfig by parsing and validating a config file."""
        raw = self._parse_file(filepath)
        self.output_file: str = raw["OUTPUT_FILE"]
        if "/" in self.output_file or "\\" in self.output_file:
            raise ValueError("output_file should be a filename, not a path")
        self.config = self._build_config(raw)

    @staticmethod
    def _build_config(raw: dict[str, str]) -> MazeConfig:
        """Parse config raw dict and return validated Config instance."""

        # Convert types to create the object
        try:
            width = int(raw["WIDTH"])
            height = int(raw["HEIGHT"])
        except ValueError:
            raise ValueError("WIDTH and HEIGHT must be integers")

        try:
            entry_x, entry_y = raw["ENTRY"].split(",")
            entry = (int(entry_x), int(entry_y))
            exit_x, exit_y = raw["EXIT"].split(",")
            exit_ = (int(exit_x), int(exit_y))
        except ValueError:
            raise ValueError(
                "ENTRY and EXIT must be int format 'x,y'"
            )

        perfect_raw = raw["PERFECT"].lower()
        if perfect_raw not in ("true", "false"):
            raise ValueError(
                "PERFECT must be 'True' or 'False'"
            )
        perfect_bool: bool = perfect_raw == "true"

        seed: int | None = None
        if "SEED" in raw:
            try:
                seed = int(raw["SEED"])
            except ValueError:
                raise ValueError(
                    "SEED must be an integer"
                )

        return MazeConfig(
            width=width,
            height=height,
            entry=entry,
            exit_=exit_,
            perfect=perfect_bool,
            seed=seed,
        )

    @staticmethod
    def _parse_file(filepath: str) -> dict[str, str]:
        """Read config file and return raw key-value pairs."""
        raw: dict[str, str] = {}
        try:
            with open(filepath, "r") as f:
                lines = f.readlines()
            for line_num, line in enumerate(lines, 1):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                if "=" not in line:
                    raise ValueError(
                        f"Line {line_num}: expected KEY=VALUE, got '{line}'"
                    )
                key, _, value = line.partition("=")
                raw[key.strip()] = value.strip()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {filepath}")
        except PermissionError:
            raise PermissionError(f"Cannot read file '{filepath}'.")
        except OSError as e:
            raise OSError(f"Failed to read file: {e}")
        required = {
            "WIDTH", "HEIGHT", "ENTRY", "EXIT", "OUTPUT_FILE", "PERFECT"
            }
        missing = required - raw.keys()
        if missing:
            raise ValueError(
                f"Missing required keys: {missing}"
            )
        for key in required:
            if not raw[key]:
                raise ValueError(f"Empty value for key: {key}")
        return raw
