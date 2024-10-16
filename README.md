# Introduction
The Shopping Cart project is a Python-based system
designed to manage a collection of items, allowing 
for operations such as adding, removing, and listing
items. The project was developed as part of an evaluation
process to demonstrate proficiency in software design, 
data structures, and design patterns.


# Setup Instructions

To set up the project and run the tests, please follow these steps:

### 1. Install Python 3.7 or Higher

Ensure that Python 3.7 or a newer version is installed on your system.

### 2. Create a Virtual Environment

Open a terminal in the project directory and create a virtual environment:


    python3 -m venv venv

    source venv/bin/activate

    pip3 install -e .

    python3 -m unittest discover -s tests

    python3 main.py



# ShoppingCart Class
## Location
The ShoppingCart class is located in the shopping_cart/shopping_cart.py file within the project directory.

## Features
### The ShoppingCart class offers the following features:

**Add Items**: 

Ability to add unique Item instances to the cart.

**Remove Items**: 

Remove specific item instances from the cart individually.

**Preserve Item Instances**: 

Each item is treated as a unique instance, even if multiple items share the same name.

**Track Quantities and Prices**: 

Maintains total quantities and prices both for individual item names and the entire cart.

**List Items**: 

Provides methods to list all items or filter items by name.

**Generate Receipts**: 

Supports generating receipts in multiple formats (JSON, CSV, text, YAML) using a scalable and expandable pattern.

**Error Handling**: 

Implements robust error handling to manage invalid operations gracefully.

### Innovative Aspects

The clever aspects of the ShoppingCart class include:

**Custom Data Structure**: 

The class uses a nested dictionary to manage items. Each item name maps to a dictionary containing:

**instances**:

A list of Item instances with that name.

**total_quantity**:

The total number of instances of that item.

**total_price**:

The cumulative price of all instances.

This structure allows for efficient tracking and manipulation of items, even when multiple items share the same name but are distinct instances.

**Unique Item Handling**:

By treating each Item instance as unique (with its own UID), the cart can handle items individually. This is particularly useful when items have unique attributes beyond name and price (e.g., serial numbers, expiration dates).

**Consistent State Management**:

The class ensures that total quantities and prices are always updated correctly after any operation, maintaining the integrity of the cart's state.


# Receipt Generation
## Design Pattern Used
The receipt generation functionality is implemented using the Strategy Factory Pattern combined with an abstract base class. This approach involves:

**Abstract Base Class (ReceiptStrategy)**:

Defines a common interface for all receipt generation strategies.

**Concrete Strategy Classes**:

Implement the generate method for different formats (JSON, CSV, text, YAML).


**Factory Function (get_receipt_strategy)**: 

Returns an instance of the appropriate strategy based on the requested format.
Benefits

**Scalability**:

New receipt formats can be added easily by creating new strategy classes that implement the ReceiptStrategy interface.

**Maintainability**:

Encapsulating receipt generation logic within separate classes adheres to the Single Responsibility Principle, making the codebase easier to maintain and extend.


**Flexibility**:

The ShoppingCart class remains agnostic of the receipt formats, relying on the strategy pattern to handle specifics.


**Personal Preference**:

The decision to use the Strategy Factory Pattern reflects a preference for design patterns that promote clean architecture and extensibility.



# Conclusion
The Shopping Cart project showcases a robust and well-thought-out
implementation of a cart system that handles items as unique 
instances while providing comprehensive functionality for 
managing and tracking items. The use of the Strategy Factory 
Pattern for receipt generation demonstrates a commitment to 
scalable and maintainable code design.