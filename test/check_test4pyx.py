import sys
from test4cmod import test4
from timeit import Timer

d = {'header': "My Post Comments",
     'comments': [
         {'name': "Joe", 'body': "Thanks for this post!"},
         {'name': "Sam", 'body': "Thanks for this post!"},
         {'name': "Heather", 'body': "Thanks for this post!"},
         {'name': "Kathy", 'body': "Thanks for this post!"},
         {'name': "George", 'body': "Thanks for this post!"}]}

#print test4(d)
expected = """\
<div class="comments">
<h3>My Post Comments</h3>
<ul>
<li class="comment">
<h5>Joe</h5><p>Thanks for this post!</p>
</li><li class="comment">
<h5>Sam</h5><p>Thanks for this post!</p>
</li><li class="comment">
<h5>Heather</h5><p>Thanks for this post!</p>
</li><li class="comment">
<h5>Kathy</h5><p>Thanks for this post!</p>
</li><li class="comment">
<h5>George</h5><p>Thanks for this post!</p>
</li>
</ul>
</div>"""

def run():
    actual = test4(d)
    if actual != expected:
        raise Exception("Benchmark mismatch: \n%s\n*** != ***\n%s" % (expected, actual))

count = int(sys.argv[1])
print "benchmarking %d times" % count

t = Timer(run,)
print min(t.repeat(repeat=3, number=count))

#result = test4(d)
#assert result == expected
#open(r"c:\temp\actual.txt", "wb").write(result)
#open(r"c:\temp\expected.txt", "wb").write(expected)


