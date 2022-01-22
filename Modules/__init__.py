from pathlib import Path

Modules_dir = Path(__file__,'..')
files = Modules_dir.glob('*.py')

__all__ = [x.name[:-3] for x in files if x.is_file() and x!='__init__.py']
