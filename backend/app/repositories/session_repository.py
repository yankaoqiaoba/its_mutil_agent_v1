import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from infrastructure.logging.logger import logger


class SessionRepository:
    """会话数据仓储类。

    负责处理底层的会话文件存储、读取和文件系统操作。
    使用 pathlib 进行现代化的路径管理。
    """

    # 存储目录名称常量
    STORAGE_DIR_NAME = "user_memories"

    def __init__(self):
        """初始化 SessionRepository。

        自动定位并创建存储根目录。
        """

        current_file = Path(__file__).resolve()

        self._base_dir = current_file.parent.parent

        # 拼接存储路径: backend/app/user_memories
        self._storage_root = self._base_dir / self.STORAGE_DIR_NAME

        # 确保存储根目录存在
        self._storage_root.mkdir(parents=True, exist_ok=True)


    def load_session(
            self, user_id: str, session_id: str
    ) -> Optional[List[Dict[str, Any]]]:
        """从文件加载会话数据。

        Args:
            user_id: 用户ID。
            session_id: 会话ID。

        Returns:
            List[Dict]: 解析后的会话数据。
            None: 如果文件不存在。

        Raises:
            json.JSONDecodeError: 如果文件内容损坏。
        """
        file_path = self._get_file_path(user_id, session_id)

        if not file_path.exists():
            return None

        with file_path.open("r", encoding="utf-8") as f:
            return json.load(f)

    def save_session(
            self, user_id: str, session_id: str, data: List[Dict[str, Any]]
    ) -> None:
        """保存会话数据到文件。

        Args:
            user_id: 用户ID。
            session_id: 会话ID。
            data: 要保存的数据列表。
        """
        file_path = self._get_file_path(user_id, session_id)

        # 确保用户的个人目录存在 (懒加载模式)
        if not file_path.parent.exists():
            file_path.parent.mkdir(parents=True, exist_ok=True)

        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_all_sessions_metadata(
            self, user_id: str
    ) -> List[Tuple[str, str, Union[List, Exception]]]:
        """获取用户所有会话的元数据和内容。

        Args:
            user_id: 用户ID。

        Returns:
            List[Tuple]: 包含 (session_id, create_time, data_or_error) 的列表。
        """
        user_dir = self._get_user_directory(user_id)

        if not user_dir.exists():
            logger.warning(f"用户目录不存在: {user_id}")
            return []

        results = []

        try:
            # 遍历目录下所有 .json 文件
            for file_path in user_dir.glob("*.json"):
                session_id = file_path.stem  # 获取文件名不带后缀部分

                # 获取文件创建时间
                stat = file_path.stat()
                create_time = datetime.fromtimestamp(stat.st_ctime).strftime(
                    "%Y-%m-%d %H:%M:%S"
                )

                try:
                    with file_path.open("r", encoding="utf-8") as f:
                        data = json.load(f)
                    results.append((session_id, create_time, data))
                except Exception as e:
                    # 读取或解析失败，返回异常对象
                    logger.error(f"读取会话文件 {file_path.name} 失败: {e}")
                    results.append((session_id, create_time, e))

        except Exception as e:
            logger.error(f"遍历用户 {user_id} 会话目录失败: {e}")
            return []

        return results

    def _get_user_directory(self, user_id: str) -> Path:
        """获取用户的记忆文件夹路径对象。"""
        return self._storage_root / user_id

    def _get_file_path(self, user_id: str, session_id: str) -> Path:
        """获取具体会话文件的路径对象。"""
        return self._get_user_directory(user_id) / f"{session_id}.json"


# 全局单例
session_repository = SessionRepository()

