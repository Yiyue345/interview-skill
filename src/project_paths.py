"""项目路径常量，所有脚本均以本文件位置确定仓库根目录。"""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_DIR = PROJECT_ROOT / "data"
KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge-base"
RESUMES_DIR = PROJECT_ROOT / "resumes"
STATE_DIR = PROJECT_ROOT / ".interview-state"
SESSION_STATE_DIR = STATE_DIR / "sessions"

PROFILE_CONFIG = CONFIG_DIR / "interview-profiles.json"
INDEX_FILE = DATA_DIR / "index.json"
GRAPH_FILE = DATA_DIR / "knowledge-graph.json"
DEFAULT_RESUME = RESUMES_DIR / "template.md"
QUESTION_HISTORY_FILE = STATE_DIR / "question-history.json"
