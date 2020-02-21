from setuptools import setup


setup(
    name="cldfbench_audersetinterrog",
    py_modules=["cldfbench_audersetinterrog"],
    include_package_data=True,
    zip_safe=False,
    entry_points={"cldfbench.dataset": ["audersetinterrog=cldfbench_audersetinterrog:Dataset"]},
    install_requires=["cldfbench", "pyglottolog"],
    extras_require={"test": ["pytest-cldf"]},
)
