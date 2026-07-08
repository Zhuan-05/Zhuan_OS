$ErrorActionPreference = "Stop"

python -m unittest discover D:\Zhuan_OS\tests
python D:\Zhuan_OS\scripts\validate_events.py
python D:\Zhuan_OS\scripts\rebuild_index.py
python D:\Zhuan_OS\scripts\health_check.py
