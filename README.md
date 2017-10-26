# PyPelt

This is a framework for a configurable fuzzy inference system (FIS) influenced by the 
[Tsukamoto model](http://researchhubs.com/post/engineering/fuzzy-system/tsukamoto-fuzzy-model.html) for 
fuzzy-rule-based systems.


## Design

PyPelt models a simple FIS in three phases:
1. File Parsing and Data Representation
2. Fuzzification of input data
3. Translation to Solution Domain
4. De-fuzzification of fuzzy solution values


### Step 1: File Parsing and Instantiation 

First, PyPelt uses the *InputParser* class to read a text file that specifies the structure of the FIS. The 
*InputParser* will have the following formatted data structures pulled from the file after successful initialization:

* A two-layer dictionary called *fuzzy_vars_dict*. The outer layer of the dictionary maps each linguistic variable name 
to an inner dictionary. This inner dictionary maps the name of each fuzzy set the variable's domain to its respective 
membership function (MF).
* A simple dictionary called *input_vals* mapping the names of linguistic variables to input values quantifying each 
variable.
* A list of stacks called *rule_stacks*. Each stack is a rule that has been reformatted from the original structure to 
a new structure that resembles reverse polish notation.

After the parser is instantiated with the input file, the next step is to generate an instance of the *FuzzyKB* class.
The *FuzzyKB* class will be a singleton used to keep all linguistic variables accessible throughout the inference 
process. 

### Step 2: Fuzzification

*TBD*


### Step 3: Translation to Consequent Domain

*TBD*


### Step 4: De-fuzzification

*TBD*
## Performance

*TBD*
