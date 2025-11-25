import json
from datetime import datetime, timezone
from dataclasses import asdict, dataclass, fields
from collections.abc import Generator, Iterator, MutableSequence
from typing import Any, Optional

META_ROW_NUM_FIELD = "meta_source_file_row_number"


@dataclass
class Metadata(dict[str, Any]):
    source_file: str
    source_file_row: int

    def to_string(self) -> str:
        """
        Returns Metadata CE header in string format
        """
        metadata_string = json.dumps(asdict(self))

        return metadata_string

@dataclass
class CloudEvent:
    ce_id: str
    ce_dataschema: str
    ce_metadata: str
    ce_specversion: str = "1.0"
    ce_time: str = datetime.now(timezone.utc).isoformat()


def meta_row_number( rows: Iterator[dict[str, Any]], row_num_start: int = 0) -> Iterator[dict[str, Any]]:
    for row_num, row in enumerate(rows, row_num_start):
        row[META_ROW_NUM_FIELD] = str(row_num)
        print(row)
        yield row
