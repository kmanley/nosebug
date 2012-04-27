// auto-generated by nosebug (https://github.com/kmanley/nosebug.git)
function get_ctx_value(stack, path) {
    // current context is at stack[stack.length-1]
    var parts = path.split("/");
    var idx = stack.length - 1;
    var curr = stack[idx];
    for (var idx in parts) {
        var part = parts[idx];
        if (part == "..") {
            idx -= 1;
            curr = stack[idx];
        } else {
            curr = curr[part] || "";
        }
    }
    return curr;
}    

function start_section(stack, path) {
    var temp = get_ctx_value(stack, path) || [];
    if (! (temp instanceof Array)) { 
        temp = [temp];
    }
    return temp;
} 

function html_escape(s) {
    s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
    return s;
}

function test4(d){
    var res = [];
    var stack = [d]
    res.push('<div class="comments">\n<h3>');
    res.push(html_escape((stack[stack.length-1]['header'] || '').toString()));
    res.push('</h3>\n<ul>\n');
    var l1 = start_section(stack, 'comments');
    if (l1 instanceof Object) {
        stack.push(l1);
    }
    for (var ill1 in l1) {
        var ll1 = l1[ill1];
        if (ll1 instanceof Object) {
            stack.push(ll1);
        }
        res.push('<li class="comment">\n<h5>');
        res.push(html_escape((stack[stack.length-1]['name'] || '').toString()));
        res.push('</h5><p>');
        res.push(html_escape((stack[stack.length-1]['body'] || '').toString()));
        res.push('</p>\n</li>');
        if (ll1 instanceof Object) {
            stack.pop();
        }
    }
    if (l1 instanceof Object) {
        stack.pop();
    }
    res.push('\n</ul>\n</div>');
    return res.join('');
}