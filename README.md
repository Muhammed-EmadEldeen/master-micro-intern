# Python Function Plotter

### Overview
![Main Image](./imgs/1721583182.png)
This project involves creating a Python GUI application that allows users to input a mathematical function and plot it over a specified range of x-values. The application is built using PySide2 for the GUI and Matplotlib for plotting. It supports basic mathematical operations and functions, including basic arithmetic, logarithms of 10 only, and square roots.

### Features
- User Input: Enter Mathematical function with support of the following operators ['+', '-', '*', '/', '^', 'log10', 'sqrt']
![]
- Plot: Plot the function over a specified range of x-values
- Validation: Validate the input function if correct, else shows an error message
- Testing: Automated testing of the application using pytest and pytest-qt

### Installation
1. Clone the repository by typing the following command in terminal
```
git clone https://github.com/Muhammed-EmadEldeen/master-micro-intern.git
```
2. Make sure you have all Pre-requisites installed

#### Pre-requisites
- Python 3.6 or higher
- Pip

##### Dependencies in Python
- PySide2
- Matplotlib
- Sympy
- Numpy
- Pytest
- Pytest-qt

### Usage
1. Run the Application:
Execute the following command to start the GUI Application
```
python3 app.py
```
2. Enter your Math formula and make sure it's correct
3. Enter X minimum and maximum values
4. Hit Submit

### Examples
- Working Example
```
Function: 5*x^3 + 2*x

Range: -10 to 10
```


- Error Example
```
Function: 5*x^3 + 2*x+

Range: -10 to 10
```



