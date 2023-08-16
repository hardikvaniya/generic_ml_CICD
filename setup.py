from setuptools import setup, find_packages

HYPHEN_E_DOT = "-e ."
def get_requirements(file_name: str) -> list:
    """Get requirements from file."""
    with open(file_name) as f:
        requirements = f.readlines()
        requirements = [r.replace("\n", "") for r in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)
        return requirements
    
setup(
    name="genericMLcicd",
    version="0.0.1",
    author="Hardik",
    author_email="hardikvaniya3800@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt")

)