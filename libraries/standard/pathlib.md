
## 获取绝对路径

```python
from pathlib import Path

print(Path('~/.chia/mainnet').expanduser().resolve().as_posix())
```