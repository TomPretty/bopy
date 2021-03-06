from setuptools import Distribution, setup

setup(
    name="bopy",
    author="Tom Pretty",
    author_email="tpretty@robots.ox.ac.uk",
    license="MIT",
    packages=["bopy"],
    install_requires=[
        "numpy",
        "sobol-seq",
        "pydoe",
        "scikit-learn",
        "matplotlib",
        "seaborn",
        "gpy",
        "scipydirect",
        "dppy",
    ],
    zip_safe=False,
)
