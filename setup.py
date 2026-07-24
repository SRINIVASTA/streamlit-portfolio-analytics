from setuptools import setup, find_packages

setup(
    name="streamlit-portfolio-analytics",
    version="0.1",
    packages=find_packages(),
    py_modules=["tracker"], # Links directly to your tracker.py file
    install_requests=["requests", "streamlit"]
)
