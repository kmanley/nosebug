nosebug
=======

A Mustache-template-to-native-language compiler


Differences to other Mustache implementations
----------------------------------------------
* Tag variables can include path syntax including / to descend a level and ../ to go up a level. Note that we don't support dot syntax
  for nested variables, instead use path, e.g. foo.bar => foo/bar
* There is no implicit looking up values in higher-level contexts because there is no need to given that we support path syntax in variables
* We don't support {{{}}} because this is just syntactic sugar for {{&}}
* Like mustache.js, we support {{.}} to indicate the current loop value in a section iterating over a list
* Callables are passed a reference to the entire context stack

TODO: what else...

 