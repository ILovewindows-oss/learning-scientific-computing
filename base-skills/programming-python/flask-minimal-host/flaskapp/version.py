# -*- coding: utf-8 -*-

version = "0.1.0"
author = "Walter Dal'Maz Silva"

install_requires = [
    "Flask==2.0.3",
    "python-dotenv==0.19.2",
]

package_data = {
    "flaskapp": [
        "templates/*.html",
        "static/favicon.ico",
        "static/*.css",
        "static/*.js"
    ]
}
