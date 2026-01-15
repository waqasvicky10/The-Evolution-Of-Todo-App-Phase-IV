"""
Setup configuration for Phase III - The Evolution of Todo App
"""

from setuptools import setup, find_packages

setup(
    name="todo-app-phase3",
    version="3.0.0",
    description="AI-Powered Todo Chatbot - Phase III",
    author="The Evolution of Todo App Team",
    packages=find_packages(include=['phase_iii', 'phase_iii.*']),
    python_requires='>=3.9',
    install_requires=[
        'openai>=2.9.0',
        'mcp>=1.25.0',
        'fastapi==0.104.0',
        'uvicorn[standard]==0.24.0',
        'streamlit>=1.28.0',
        'python-dotenv>=1.0.0',
        'pydantic>=2.5.0',
        'sqlmodel>=0.0.14',
    ],
    extras_require={
        'dev': [
            'pytest>=7.4.3',
            'pytest-asyncio>=0.21.1',
            'pytest-cov>=4.1.0',
            'black>=23.11.0',
            'ruff>=0.1.6',
            'mypy>=1.7.0',
        ],
    },
    package_data={
        'phase_iii': ['**/*.py', '**/*.md', '**/.gitkeep'],
    },
    include_package_data=True,
)
