import sys
import socket
from pydantic import ValidationError
from backend.app.config.settings import settings


def mask_secret(secret: str | None) -> str:
    """
    安全脱敏函数：只显示密钥的前3位和后3位
    """
    if not secret:
        return "未配置"
    if len(secret) <= 6:
        return "******"
    return f"{secret[:3]}****{secret[-3:]} (长度:{len(secret)})"


def check_mysql_connection(host: str, port: int, timeout: int = 2):
    """
    简单的 TCP 连接测试，检查数据库端口是否开放
    """
    try:
        sock = socket.create_connection((host, port), timeout=timeout)
        sock.close()
        return "连接成功 (TCP端口开放)"
    except Exception as e:
        return f"连接失败: {str(e)}"


def main():
    print("==================================================")
    print("         系统配置加载与自检程序")
    print("==================================================")

    try:
        # 尝试导入配置，会触发 Settings 的实例化和验证器
        print("\n[1] 核心配置加载")
        print(f"配置文件路径: {settings.model_config.get('env_file')}")
        print("状态: 配置加载成功，校验通过")

    except ValidationError as e:
        print("\n 配置校验失败！程序无法启动。")
        print("错误详情:")
        for error in e.errors():
            print(f" - 字段: {error['loc']} | 错误: {error['msg']}")
        sys.exit(1)  # 立即终止程序
    except ImportError:
        print("\n 错误: 找不到 settings.py 文件，请确认文件名正确。")
        sys.exit(1)

    print("\n[2] AI 服务配置检查")
    print(f"{'SiliconFlow   Key':<20}: {mask_secret(settings.SF_API_KEY)}") # 左对齐 占 20 个字符宽度。
    print(f"{'SiliconFlow   URL':<20}: {settings.SF_BASE_URL or '未配置'}")
    print(f"{'Ali  Bailian  Key':<20}: {mask_secret(settings.AL_BAILIAN_API_KEY)}")
    print(f"{'Ali  Bailian  URL':<20}: {settings.AL_BAILIAN_BASE_URL or '未配置'}")

    print("\n[3] 模型参数")
    print(f"{'主模型 (Main)':<20}: {settings.MAIN_MODEL_NAME}")
    print(f"{'子模型 (Sub)':<20}: {settings.SUB_MODEL_NAME}")

    print("\n[4] 数据库配置")
    print(f"{'MySQL Host':<20}: {settings.MYSQL_HOST}")
    print(f"{'MySQL Connection':<20}: {settings.MYSQL_USER}@**SECRET**:{settings.MYSQL_PORT}/{settings.MYSQL_DATABASE}")

    # 执行简单的连接检查
    conn_status = check_mysql_connection(settings.MYSQL_HOST, settings.MYSQL_PORT)
    print(f"{'连通性检查':<20}: {conn_status}")

    # -----------------------------------------------------------------
    # 新增部分：知识库与 MCP 配置
    # -----------------------------------------------------------------

    print("\n[5] 知识库配置")
    print(f"{'Knowledge Base URL':<20}: {settings.KNOWLEDGE_BASE_URL or '未配置'}")

    print("\n[6] MCP 服务配置")
    print(f"{'DashScope URL':<20}: {settings.DASHSCOPE_BASE_URL or '未配置'}")
    print(f"{'Baidu Map AK':<20}: {mask_secret(settings.BAIDUMAP_AK)}")

    print("\n==================================================")
    print("自检完成，配置对象 `settings` 可供全局使用")
    print("==================================================")


if __name__ == "__main__":
    main()