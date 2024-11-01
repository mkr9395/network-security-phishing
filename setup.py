'''
The setup.py file is an essential part of packaging and 
distributing Python projects. It is used by setuptools 
(or distutils in older Python versions) to define the configuration 
of your project, such as its metadata, dependencies, and more
'''


from setuptools import find_packages, setup # it will consider all folders with __init__.py as packages

def get_requirements() -> list[str]:
    """
    This function will return list of requirements
    """
    requirement_lst:list[str] = []
        
    try:
        with open('requirements.txt','r') as file:
            # read all the lines and save inside a variable
            lines = file.readlines()
            # process each line
            for line in lines:
                requirement = line.strip() # remove empty spaces
                # ignore empty lines and -e .
                if (requirement) and (not requirement.startswith('-e')):
                    requirement_lst.append(requirement)
    except FileNotFoundError:
        print("Requirements.txt file not found")
        
    return requirement_lst


# print(get_requirements())
                
setup(
    name = "network-security-phising",
    version = "0.0.1",
    author="Mohit Kumar",
    author_email="mkr9395@gmail.com",
    packages = find_packages(),
    install_requires = get_requirements()
    
)

