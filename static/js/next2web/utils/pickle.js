(function(next2web){
	
	var arg0,
		MARK = "(", 
	    STOP = ".", 
	    INT = "I",	
	    FLOAT = "F", 
	    NONE = "N",
		STRING = "S",
		APPEND = "a",
		DICT = "d",
		GET = "g",
		LIST = "l",
		PUT = "p",
		SETITEM = "s",
		TUPLE = "t",
		TRUE = "I01\n",
		FALSE = "I00\n",
		NEWLINE = "\n",
		MARK_OBJECT = null,
		SQUO = "'";

	function process_op(op, memo, stack) {
        if (op.length === 0) { return; }
    
        switch (op[0]) {
            case MARK:
                // TODO: when we support POP_MARK AND POP, we need real marks
                // ...we need this for tuple, as well
                //stack.push(MARK_OBJECT)
                process_op(op.slice(1), memo, stack)
                break
            case STOP:
                //console.log("stop")
                break
            case INT:
                // booleans are a special case of integers
                if (op[1] === "0") {
                    arg0 = (op[2] === "1")
                    stack.push(arg0)
                    break
                }
            
                arg0 = parseInt(op.slice(1))
                //console.log("int", arg0)
                stack.push(arg0)
                break
            case FLOAT:
                arg0 = parseFloat(op.slice(1))
                //console.log("int", arg0)
                stack.push(arg0)
                break
            case STRING:
                arg0 = eval(op.slice(1))
                stack.push(arg0)
                //console.log("string", arg0)
                break
            case NONE:
                stack.push(null)
                process_op(op.slice(1), memo, stack)
                break
            case APPEND:
                arg0 = stack.pop()
                //console.log("appending to", stack[stack.length-1])
                stack[stack.length-1].push(arg0)
                process_op(op.slice(1), memo, stack)
                break
            case DICT:
                stack.push({})
                process_op(op.slice(1), memo, stack)
                break
            case GET:
                arg0 = parseInt(op.slice(-1))
                arg1 = memo[arg0]
                stack.push(arg1)
                //console.log("getting", arg1)
                break
            case LIST:            
                stack.push([])
                process_op(op.slice(1), memo, stack)
                break
            case PUT:
                arg0 = parseInt(op.slice(-1))
                arg1 = stack[stack.length-1]
                memo[arg0] = arg1
                //console.log("memo", arg0, arg1)
                break
            case SETITEM:
                arg1 = stack.pop()
                arg0 = stack.pop()
                stack[stack.length-1][arg0] = [arg1]
                //console.log("current before set", stack)
                process_op(op.slice(1), memo, stack)
                break
            case TUPLE:
                //console.log("tuple")
                stack.push([])
                // TODO: tuples
                
                process_op(op.slice(1))
                break    
            default:
                throw new Error("unknown opcode " + op[0])
        }
        
    function _check_memo(obj, memo) {
        for (var i=0; i<memo.length; i++) {
            if (memo[i] === obj) {
                return i
            }
        }
        return -1
    }
    
    function _dumps(obj, memo) {
        memo = memo || []
        if (obj === null) {
            return NONE
        }

        if (typeof(obj) === "object") {
            var p = _check_memo(obj, memo)
            if (p !== -1) {
                return GET + p + NEWLINE
            }
            
            var t = obj.constructor.name
            switch (t) {
                case Array().constructor.name:
                    var s = MARK + LIST + PUT + memo.length + NEWLINE
                    memo.push(obj)

                    for (var i=0; i<obj.length; i++) {
                        s += _dumps(obj[i], memo) + APPEND
                    }
                    return s
                    break
                case Object().constructor.name:
                    var s = MARK + DICT + PUT + memo.length + NEWLINE
                    memo.push(obj)
                    
                    for (var key in obj) {
                        //console.log(key)
                        //push the value, then the key, then 'set'
                        s += _dumps(obj[key], memo)
                        s += _dumps(key, memo)
                        s += SETITEM
                    }                    
                    return s
                    break
                default:
                    throw new Error("Cannot pickle this object: " + t)
            
            }
        } else if (typeof(obj) === "string") {
            var p = _check_memo(obj, memo)
            if (p !== -1) {
                return GET + p + NEWLINE
            }
            
            var escaped = obj.replace("\\","\\\\","g")
                            .replace("'", "\\'", "g")
                            .replace("\n", "\\n", "g")

            var s = STRING + SQUO + escaped + SQUO + NEWLINE
                    + PUT + memo.length + NEWLINE
            memo.push(obj)
            return s
        } else if (typeof(obj) === "number") {
            return FLOAT + obj + NEWLINE
        } else if (typeof(obj) === "boolean") {
            return obj ? TRUE : FALSE
        } else {
            throw new Error("Cannot pickle this type: " + typeof(obj))
        }
    }

	var Pickle = Class.$extend({
		__classvars__: {
			loads: function(pickle) {
		        stack = []
		        memo = []
		    
		        var ops = pickle.split(NEWLINE)
		        var op
		    
		        for (var i=0; i<ops.length; i++) {
		            op = ops[i]
		            process_op(op, memo, stack)
		        }
		        return stack.pop()
		   },
		   dumps: function(obj) {
		        // pickles always end with a stop
		        return _dumps(obj) + STOP
		    } 
		}
	});

	next2web.provide('next2web.lib.pickle', Pickle);

})(next2web);