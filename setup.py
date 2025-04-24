from setuptools import setup, find_packages

setup(
    name='chatbot-be',
    version='1.0.0',
    description='Backend API for AI-powered chatbot built with FastAPI',
    author='Nguyen Nguyen',
    url='https://github.com/NguyenNguyen0/chatbot-be',
    packages=find_packages(),
    include_package_data=True,
    license='SEE LICENSE IN LICENSE',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Framework :: FastAPI',
        'License :: Other/Proprietary License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: APIs'
    ],
    python_requires='>=3.10',
)
