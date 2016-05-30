#!/usr/bin/env python

from setuptools import setup

ENTRY_POINTS = {
    # Entry point used to specify packages containing tutorials accessible
    # from welcome screen. Tutorials are saved Orange Workflows (.ows files).
    'orange.widgets.tutorials': (
        # Syntax: any_text = path.to.package.containing.tutorials
        'exampletutorials = orangecontrib.educational.tutorials',
    ),

    # Entry point used to specify packages containing widgets.
    'orange.widgets': (
        # Syntax: category name = path.to.package.containing.widgets
        # Widget category specification can be seen in
        #    orangecontrib/example/widgets/__init__.py
        'Education = orangecontrib.educational.widgets',
    ),

    # Register widget help
    "orange.canvas.help": (
        'html-index = orangecontrib.educational.widgets:WIDGET_HELP_PATH',)
}

KEYWORDS = (
    # [PyPi](https://pypi.python.org) packages with keyword "orange3 add-on"
    # can be installed using the Orange Add-on Manager
    'orange3 add-on',
)

if __name__ == '__main__':
    setup(
        name="Orange3 Educational Add-on",
        packages=['orangecontrib',
                  'orangecontrib.educational',
                  'orangecontrib.educational.tutorials',
                  'orangecontrib.educational.widgets'],
        package_data={
            'orangecontrib.educational': ['tutorials/*.ows'],
            'orangecontrib.educational.widgets': ['icons/*'],
        },
        install_requires=['Orange'],
        entry_points=ENTRY_POINTS,
        keywords=KEYWORDS,
        namespace_packages=['orangecontrib'],
        include_package_data=True,
        zip_safe=False,
    )
