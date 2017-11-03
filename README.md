# PyPelt

This is a framework for a configurable fuzzy inference system (FIS) influenced by the 
[Tsukamoto model](http://researchhubs.com/post/engineering/fuzzy-system/tsukamoto-fuzzy-model.html) for 
fuzzy-rule-based systems, but has been adapted to support non-monotonic membership functions. 


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
The *FuzzyKB* class will be a singleton used to keep all linguistic variables accessible throughout the process. 

### Step 2: Fuzzification

Now that everything has been parsed and loaded, we take the inputs in the *input_vals* dictionary and map them
convert them to fuzzy values (hence the name pelt) in the domains of their respective variables. In practice, 
this is roughly the equivalent of plugging the inputs into every membership function in the domain of the 
variable. 


### Step 3: Inference into Consequent Domain

This is where the rules actually fire. In the fuzzification process, we mapped our crisp inputs into fuzzy 
degrees of membership. Now we take those fuzzy degrees of membership and perform some fuzzy logic operations to 
map from the domain of the antecedent to the domain of the consequent. In simpler terms, we've turned hard numbers into abstract "judgements" about our input, and now we need to know 
what to do with those "judgements" based on our rules. 

In PyPelt, rules can use the following operations:
* and: take the minimum membership value from antecedent variables 
* or: take the maximum of all the antecedent variables, cannot be combined with AND
* then: begins consequent
* is: used to specify which set is being used for the fuzzy variable in the rule
* if: begins antecedent

The mapping process takes the calculated weight of the fired rule, truncates the consequent membership function, 
and calculates the midpoint between the values on the membership function that produce the weight. 


### Step 4: De-fuzzification
There are a lot of different ways to "de-fuzzify" values, and at the end of the day, research has yet to prove 
there's a single design that suits every need perfectly. In PyPelt, I use a weighted average that 
in my opinion does a fair job of letting every part of the rule affect the output in a manner that's relatively 
intuitive. Rules that fired with little weight will have little impact on the outcome, and consequent sets that 
resemble discrete sets will express less variance in their output. 

## Performance

*Section not yet written*
