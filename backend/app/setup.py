from setuptools import setup, find_packages

setup(
    name="its_app",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "pydantic",
        "pydantic-settings",
        "openai",
        "openai-agents",
        "pymysql",
        "dbutils",
        "pystun3"
    ],
)
