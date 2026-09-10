from setuptools import find_packages, setup

package_name = 'turtle_controller'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/config', ['../../config/params.yaml']),
        ('share/' + package_name + '/launch', ['../../launch/task_3.launch.py']),
  ],
  
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Lenovo',
    maintainer_email='yahiaelshenawy51@gmail.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            'go_to_goal = turtle_controller.go_to_goal:main',
            'toggle_client = turtle_controller.toggle_client:main',
        ],
    },
)
