/* Copyright (c) 2012 Maxwell Morais [max.morais.dmm@gmail.com]
* 
*  MIT License (MIT)
* 
*  Permission is hereby granted, free of charge, to any person obtaining a 
*  copy of this software and associated documentation files (the "Software"), 
*  to deal in the Software without restriction, including without limitation 
*  the rights to use, copy, modify, merge, publish, distribute, sublicense, 
*  and/or sell copies of the Software, and to permit persons to whom the 
*  Software is furnished to do so, subject to the following conditions:
*  
*  The above copyright notice and this permission notice shall be included in 
*  all copies or substantial portions of the Software.
*  
*  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
*  INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A 
*  PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT 
*  HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF 
*  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
*  OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/

window = jQuery = global;
Class = require('./thirdparty/classy')

function init(win){
	var __slice = [].slice, format, dec2hex = [];
	
	for (var i = 0; i <= 15; i++){
		dec2hex[i] = i.toString(16);
	}
	
	function lookup(object, key){
		var match;
		if (!/^(\d)([.]|$)/.test(key)){
			key = '0.' + key;
		}
		while (match = /(.+?)[.](.+)/.exec(key)){
			object = resolve(object, match[1]);
			key = match[2];
		}
		return resolve(object, key);
	}
	
	function resolve(object, key){
		var value;
		value = object[key];
		if (typeof value === 'function'){
			return value.call(object);
		} else {
			return value;
		}
	}
	
	String.prototype.format = function(){
		var args, error, explicit, idx, implicit, _this = this;
		args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
		
		if (args.length === 0){
			return function(){
				var args;
				args = 1 <= arguments.length ? __slice.call(arguments, 0) : [];
				return _this.format.apply(_this, args);
			}
		}
		idx = 0;
		explicit = implicit = false;
		error = 'cannot switch from {} to {} numbering'.format();
		return this.replace(/([{}])\1|[{](.*?)(?:!(.+?))?[}]/g, function(match, literal, key, transformer){
			var fn, value, _ref, _ref1, _ref2;
			if (literal) {
				return literal;
			}
			if (key.length){
				explicit = true;
				if (implicit){
					throw error('implicit', 'explicit');
				}
				value = (_ref = lookup(args, key)) != null ? _ref : '';
			} else {
				implicit = true;
				if (explicit) {
					throw error('implicit', 'explicit');
				}
				value = (_ref1 = args[idx++]) != null ? _ref1 : '';
			}
			value = value.toString();
			if (fn = String.prototype.format.transformers[transformer]) {
				return (_ref2 = fn.call(value)) != null; _ref2 : '';
			} else {
				return value;
			}
		});
	}
	String.prototype.format.transformers = {};
	String.prototype.reverse = function() { return this.split('').reverse().join(''); }
	String.prototype.lower = String.prototype.toLowerCase;
	String.prototype.upper = String.prototype.toUpperCase;
	String.prototype.is_string = function(){
		return Object.prototype.toString.call(this) === '[object String]';
	}
	String.prototype.capitalize = function(){
		return this.charAt(0).upper() + this.slice(1);
	}
	String.prototype.uncapitalize = function(){
		return this.charAt(0).lower() + this.slice(1)
	}
	String.prototype.capitalize_words = function(){
		return this.replace(/\w+/g, function(word){
			return String.prototype.capitalize(word);
		});
	}
	String.prototype.uncapitalize_word = function(){
		return this.replace(/\w+/g, function(word){
			return String.prototype.uncapitalize(word);
		});
	}
	String.prototype.is_lower_at = function(index){
		this.charAt(index).lower() === this.charAt(index);
	}
	String.prototype.is_upper_at = function(index){
		this.charAt(index).upper() === this.charAt(index);
	}
	String.prototype.swapcase = function(){
		return this.replace(/([a-z]+)|([A-Z+])/g, function(match, lower, upper){
			return lower ? match.upper() : match.lower();
		});
	}
	String.prototype.camelize = function(){
		return this.replace(/\W+(.)/g, function(match, letter){
			return letter.upper();
		});
	}
	String.prototype.dasherize = function(){
		return this.replace(/\W+/g, '-')
		           .replace(/([a-z\d]([A-Z]))/g, '$1-$2')
		           .lower();
	}
	String.prototype.repeat = function(count) {
		return count > 1 ? new Array(count + 1).join(this): this;
	}
	String.prototype.insert = function(index, string){
		return this.slice(0, index) + string + this.slice(index);
	}
	String.prototype.remove = function(start, end){
		return this.slice(0, start) + this.slice(end);
	}
	String.prototype.pop = function(index){
		return this.slice(index(index + 1));
	}
	String.prototype.chop = function(){
		return this.slice(0, -1);
	}
	String.prototype.strip = function(){
		return this.trim ? this.trim() : this.replace(/^\s+/, '').replace(/\s+$/, '');
	}
	String.prototype.ltrim = function(){
		return this.trimLeft ? this.trimLeft() : this.replace(/^\s+/, '');	
	}
	String.prototype.rtrim = function(){
		return this.trimRight ? this.trimRight() : this.replace(/\s+$/, '');
	}
	String.prototype.truncate = function(args){
		var limit = args && args.limit || 10,
		    omission = args && args.omission || '...';
		return this.lenght <= limit ? this : this.slice(0, limit) + omission;
	}
	String.prototype.extract = function(regex, n){
		n = n === 'undefined' ? 0 : n;
		if (!regex.global){
			return this.match(regex)[n] || '';
		} 
		
		var match, extracted = [];
		while ((match = regex.exec(this))){
			extracted[extracted.length] = match[n] || '';
		}
		
		return extracted
	}
	String.prototype.splitlines = function(){
		return this.split(/\r?\n/);
	}
	String.prototype.join = function(array, last){
		var lastItem = array.pop(),
		    last = last || 'and';
		    
		return array.join(', ' + ' ' + last + ' ' + lastItem);
	}
	String.prototype.humanize = function() {
		var number = parseFloat(this.toString());
		if (number && number % 100 > 11 && number % 100 <= 13){
			return this.toString(); + 'th';
		}
		if (number){
			switch(number % 10){
				case 1: return this.toString() + 'st';
				case 2: return this.toString() + 'nd';
				case 3: return this.toString() + 'rd';
			}
			return this.toString() + 'th';
		}
	}
	String.prototype.contains = function(string){
		this.indexOf(string) > -1;
	}
	String.prototype.startswith = function(string){
		this.indexOf(string) === 0;
	}
	String.prototype.endswith = function(string) {
		var index = this.length - string.lenght;
		return index >= 0 && this.indexOf(string, index) > -1;
	}
	String.prototype.isblank = function(){
		return /^\s*$/.test(this.toString());
	}
	String.prototype.successor = function () {
        var alphabet = 'abcdefghijklmnopqrstuvwxyz',
            length = alphabet.length,
            result = this.toString(),
            i = this.length;

        while(i >= 0) {
            var last = this.charAt(--i),
                next = '',
                carry = false;

            if (isNaN(last)) {
                index = alphabet.indexOf(last.lower());

                if (index === -1) {
                    next = last;
                    carry = true;
                }
                else {
                    var isUpperCase = last === last.upper()();
                    next = alphabet.charAt((index + 1) % length);
                    if (isUpperCase) {
                        next = next.upper();
                    }

                    carry = index + 1 >= length;
                    if (carry && i === 0) {
                        var added = isUpperCase ? 'A' : 'a';
                        result = added + next + result.slice(1);
                        break;
                    }
                }
            }
            else {
                next = +last + 1;
                if(next > 9) {
                    next = 0;
                    carry = true
                }

                if (carry && i === 0) {
                    result = '1' + next + result.slice(1);
                    break;
                }
            }

            result = result.slice(0, i) + next + result.slice(i + 1);
            if (!carry) {
                break;
            }
        }
        return result;
    }
	String.prototype.guid = function (length) {
        var buf = [],
            chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789',
            charlen = chars.length,
            length = length || 32;
            
        for (var i = 0; i < length; i++) {
            buf[i] = chars.charAt(Math.floor(Math.random() * charlen));
        }
        
        return buf.join('');
    }
	String.prototype.UUID = function(){
		var uuid = '';
		for (var i = 0; i <= 36; i++){
			if (i===9 || i===14 || i===19 || i===24){
				uuid += '-';
			} else if (i===15){
				uuid += '4';
			} else if (i===20){
				uuid += dec2hex[(Math.random()*4|0+8)];
			} else {
				uuid += dec2hex[(Math.random()*15|0)];
			}
		}
		return uuid;
	}
	Array.prototype.range = function(start, end, step){
		var range = [];
		var typeofStart = typeof start;
		var typeofEnd = typeof end;
		
		if (typeof step === 'undefined' || !step || step === 0 ){
			step = 1;
		}
		
		if (typeofStart === 'undefined' || typeofEnd === 'undefined') {
			throw TypeError("Must pass start and end arguments.");
		} else if (typeofStart != typeofEnd) {
			throw TypeError('Start and end arguments must be of same type');
		}
		
		if (end < start) {
			step = -step;
		}
		
		if (typeofStart === 'number'){
			while (step > 0 ? end > start : end <= start){
				range.push(start);
				start += step;
			}
		} else if (typeofStart == 'string') {
			if (start.length != 1 || end.length != 1){
				throw TypeError('Only strings with one character are supported');
			}
			start = start.charCodeAt(0);
			end = end.charCodeAt(0);
			
			while (step > 0 ? end >= start : end <= start){
				range.push(String.fromCharCode(start));
				start += step;
			} 
		} else {
			throw TypeError('Only string and numbers types are supported');
		}
		
		return range;
		
	}
}
init(window);

(function(win){
	
	var _toArray = function(obj){
		if (typeof(obj) == 'object' && obj.sort) {
			return obj;
		}
		return Array(obj);
	}
	
	var _createXmlHttpRequest = function(){
		var xhr;
		try {xhr = new XMLHttpRequest(); } catch(e0) {
			try {xhr = new ActiveXObject('Msxml2.XMLHTTP.0.6');} catch(e1) {
				try {xhr = new ActiveXObject('Msxml2.XMLHTTP.3.0');} catch (e2) {
					try {xhr = new ActiveXObject('Msxml2.XMLHTTP');} catch (e3) {
						try {xhr = new ActiveXObject('Microsoft.XMLHTTP');} catch (e4) {
							throw new Error('This browser does not support XMLHttpRequest.');
						}
					}
				}
			}
		}
		return xhr;
	}
	
	var _isHttpRequestSucessful = function(status) {
		return (status >= 200 && status < 300) || status == 304 || status == 1123 || (!status && (window.location.protocol == 'file:' || window.location.protocol == 'chrome:'))
	}
	
	var _createScript = function(data) {
		var script = document.createElement('script');
		script.type = 'text/javascript';
		script.text = data;
		
		if (typeof window.execScript === 'object') {
			window.execScript(data);
		} else {
			try {
				document.body.appendChild(script);
			} catch (e) {
				window['eval'](data);
			}
		}
	}
	
	var _dispachEvent = function(eventName, properties){
		if (!this._listeners) { return ;}
		properties.event = eventName
		for (var i = 0; i < next2web._listeners[eventName].length; i++){
			next._listeners[eventName][i](properties);
		}
	}
	
	var next2web = Class.$extend({
		__classvars__: {
			_listeners : {},
			_includedIdentifiers : [],
			separator: '.',
			baseUri : './',
			autoInclude : true
		},
		define : function(identifier){
			var klasses = arguments[1] || false;
			var ns = win;
			
			if (identifier !== ''){
				var parts = identifier.split(this.separator);
				for (var i = 0; i < parts.length; i++){
					if (!ns[parts[i]]){
						ns[parts[i]] = {}
					}
					ns = ns[parts[i]];
				}
			}
			
			if (klasses) {
				for (var klass in klasses) {
					if (klasses.hasOwnProperty(klass)){
						ns[klass] = klasses[klass];
					}
				}
			}
			_dispachEvent('create', {'identifier': identifier});
			return ns;
		},
		exist : function(identifier){
			if (identifier === '') { return true; }
			var parts = identifier.split(this.separator);
			var ns = win;
			
			for (var i = 0; i < parts.length; i++){
				if (!ns[parts[i]]){
					return false;
				}
				ns = ns[parts[i]]
			}
		},
		mapIdentifierToUri : function(identifier){
			var regexp = new RegExp('\\' + this.separator, 'g');
			return this.baseUri + identifier.replace(regexp, '/') + '.js';
		},
		_loadScript : function(identifier){
			var sucessCallback = arguments[1] || function(){};
			var errorCallback = arguments[2];
			var async = typeof successCallback === 'function';
			var uri = this.mapIdentifierToUri(identifier);
			var event = {'identifier': identifier, 'uri': uri, 'async': async, 'callback': sucessCallback};
			
			var xhr = _createXmlHttpRequest();
			xhr.open('GET', uri, async);
			
			if (async) {
				xhr.onreadystatechange = function() {
					if (xhr.readyState == 4) {
						if (_isHttpRequestSucessful(xhr.status || 0)) {
							_createScript(xhr.responseText);
							_dispachEvent('include', event);
							sucessCallback();
							return;
						}
						event.status = xhr.status;
						_dispachEvent('includeError', 'event');
						if (typeof errorCallback === 'function') {
							errorCallback();
						}
					} 
				}
			}
			
			xhr.send(null);
			
			if (!async){
				if (_isHttpRequestSucessful(xhr.status || 0)) {
					_createScript(xhr.responseText);
					_dispachEvent('include', event);
					return true;
				}
				event.status = xhr.status;
				_dispatchEvent('includeError', event);
				return false;
			}	
		},
		include : function(identifier){
			var sucessCallback = arguments[1] || false;
			var errorCallback = arguments[2] || false;
			if (!typeof this._includedIdentifiers[identifier] === 'undefined') {
				if (typeof sucessCallback === 'function') { sucessCallback(); }
				return true;
			}
			
			if (sucessCallback){
				_loadScript(identifier, function(){
					this._includedIdentifiers[identifier] = true;
					sucessCallback();
				}, errorCallback);
			} else {
				if(_loadScript(identifier)){
					this._includedIdenfiers[identifier] = true;
					return true;
				}
				return false;
			}
		},
		use: function(identifier){
			var identifiers = _toArray(identifier),
				callback = arguments[1] || false,
				autoInclude = arguments.length > 0 ? arguments[2] : next2web.autoInclude,
				event = {'identifier': identifier},
			    parts, target, ns;
			
			for (var i = 0; i < identifiers.length; i++){
				identifier = identifiers[i];
				parts = identifier.split(next2web.separator);
				target = parts.pop();
				ns = this.define(parts.join(next2web.separator));
				
				if (target === '*'){
					for (var objectName in ns){
						if (ns.hasOwnProperty(objectName)){
							win[objectName] = ns[objectName]
						} else {
							if (ns[target]) {
								win[target] = ns[target];
							} else {
								if (autoInclude) {
									if (callback) {
										this.include(identifier, function(){
											win[target] = ns[target];
											if (i + 1 < identifiers.length) {
												this.unpack(identifiers.slice(i + 1), callback, autoInclude);
											} else {
												_dispachEvent('use', event);
												if (typeof callback === 'function') {
													callback();
												}
											}
										})
										return;
									} else {
										this.include(identifier);
										win[target] = ns[target];
									}
								}
							}
						}
					}
				}
			}
			_dispachEvent('use', event);
			if (typeof callback === "function") { callback(); }
		},
		from : function(identifier) {
			parent = this;
			return {
				include: function() {
					var callback = arguments[0] || false;
					parent.include(identifier, callback);
				},
				use: function() {
					var callback = arguments[1] || false;
					if (_identifier.charAt(0) == '.') {
						_identifier = identifier + _identifier;
					}
					
					if (callback) {
						parent.include(identifier, function(){
							parent.use(_identifier, callback, false);
						});
					} else {
						parent.include(identifier);
						parent.use(_identifier, callback, false);	
					}
				}
			}
		},
		provide: function(identifier) {
			var identifiers = _toArray(identifier);
			for (var i = 0; i < identifiers.length; i++) {
				if (!(identifier in this._includedIdentifiers)){
					_dispachEvent('provide', {'identifier': identifier});
				}
			}
		},
		addEventListener: function(eventName, callback) {
			if (!this._listeners[eventName]) {this._listeners[eventName] = []; }
			_listeners[eventName].push(callback);
		},
		removeEventListener: function(eventName, callback) {
			if (!this._listeners[eventName]) { return; }
			for (var i = 0; i < this._listeners[eventName].length; i++){
				if (_listeners[eventName][i] == callback) {
					delete _listeners[eventName][i];
					return;
				}
			}
		}
	});
	if (!win.next2web) { window.next2web = next2web(); }
})(window);

(function(nextweb, win){
	var _tags = ["a", "abbr", "address", "area", "aside", "audio", "b", "base", "bdi", "bdo", "blockquote", "br", "button", "canvas", "caption",
		        "cite", "code", "col", "colgroup", "command", "datalist", "dd", "del", "details", "dfn", "div", "dl", "dt", "em", "embed", "fieldset",
		        "figcaption", "figure", "footer", "form", "h1", "h2", "h3", "h4", "h5", "h6", "header", "hr", "hgroup", "i", "iframe", "img", "input",
		        "ins", "keygen", "kdb", "label", "legend", "li", "link", "map", "mark", "menu", "meta", "meter", "nav", "noscript", "object", "ol",
		        "optgroup", "option", "output", "p", "param", "pre", "progress", "q", "rp", "rt", "ruby", "s", "samp", "script", "section", "select",
		        "small", "source", "span", "strong", "style", "sub", "summary", "sup", "table", "tbody", "td", "textarea", "tfoot", "th", "thead",
		        "time", "title", "tr", "track", "u", "ul", "var", "video", "wbr",
		        "html", "head", "body"];
	
	function parse_args(args){
        var obj = {};

        for (var i = 0; i < args.length; i++){
            switch(typeof(args[i])){
                case "string":{
                    if (!obj["text"]) {
                        obj["text"] = TextNode(args[i]);
                    } else {
                        if (!(obj["text"] instanceof Array)){
                            obj["text"]=[obj["text"], HTML.br(), TextNode(args[i])];
                        } else {
                            obj["text"].push(HTML.br());
                            obj["text"].push(TextNode(args[i]));
                        }
                    }
                    break;
                }
                case "object":{
                    if (args[i] instanceof Array){
                        if (!obj["list"]){
                            obj["list"] = args[i];
                        } else {
                            obj["list"].concat(args[i]);
                        }
                    } else {
                        if (!obj["dict"]) {
                            obj["dict"] = args[i];
                        } else {
                            for (var key in args[i]){
                                obj["dict"][key] = args[key];
                            }
                        }
                    }
                    break;
                }
            }
        }
        return obj;
    }
    
    function makeTagHelper(tag){
		return function(){
            parse = parseArguments(arguments);
           	if (!(typeof(children)=='undefined') && !(children instanceof Array)) children = [children];
			node = Node(tag);
            if (!(typeof(parse["text"]) == "undefined")){
                if (parse["text"] instanceof Array){
                    for (var i=0; i < parse["text"].length; i++){
                        node.addChild(parse["text"][i]);
                    }
                } else {
                    node.addChild(parse["text"]);
                }
            }
			if (!(typeof(parse["dict"])=='undefined')){
				node.setAttributes(parse["dict"]);
			}
			if (parse["list"] instanceof Array){
				for (var i in parse["list"]){
					node.addChild(parse["list"][i]);
				}
			}
			return node;
		};
	}

	var HTML = Class.$extend({
		__classvars__: {
			version: '0.2.0',
			templates : {},
			Node: Node,
			Template: Template
		},
		__init__: function(){
			for (var i=0; i < _tags.length; i++){
				this[_tags[i]] = makeTagHelper(_tags[i]);
			}
			return this;
		},
		register: function(name, template){
			this.templates[name] = template;
		},
		render: function(name, thisObj, data){
			var template = this.templates[name],
		    	renderer = new Template(template);
			return renderer.render.apply(renderer, Array.prototype.slice.call(arguments, 1));
		}
	});
	
	var Node = Class.$extend({
		__init__: function(tagName){
			this.tagName = tagName;
			this.attributes = {};
			this.children = [];
			this.notSelfClosingTags = ['textarea', 'script', 'em', 'strong', 'option', 'select'];
		
		},
		setAttributes: function(attrs){
			for (var key in attrs){
				var mappedKey = (key == 'cls') ? 'class': (key == 'data') ? 'data-options': key;
				this.attributes[mappedKey] = attrs[key];
			}
			return this;
		},
		addChild : function(childText){
			this.children.push(childText);
			return this;
		},
		render: function(lpad){
			lpad = lpad||0;
			var node      = [],
			    attrs     = [],
			    textnode  = (this instanceof TextNode),
			    multiline = this.multiLineTag();
		
			if (!textnode) node.push(this.getPadding(lpad));
			node.push('<'+this.tagName);
			for (var key in this.attributes){
				attrs.push(key+'="'+this.attributes[key]+'"');
			}
			attrs.sort();
			for (var i=0; i < attrs.length; i++){
				node.push(' '+attrs[i]);
			}
			if (this.isSelfClosing() && this.children.length==0){
				node.push('/>\n');
			} else {
				node.push('>');
				if (multiline) node.push('\n');
					this.renderChildren(node, this.children, lpad);
				if (multiline) node.push(this.getPadding(lpad));
					node.push('</', this.tagName, '>\n');
			}
			return node.join('');
		},
		renderChildren: function(node, children, lpad){
			var childLpad = lpad + 2;
		
		    for (var i=0; i < children.length; i++) {
		    	var child = children[i];
		    	if (child instanceof Array) {
		    		var nestedChildren = child;
		    		this.renderChildren(node, nestedChildren, lpad);
		    	} else {
		    		node.push(child.render(childLpad));
		    		//node.push(child);
		    	}
		    }
		},
		multiLineTag : function(){
			var childLength = this.children.length,
				multiLine = childLength > 0;
			if (childLength == 1 && this.children[0] instanceof TextNode) multiLine=false;
			return multiLine;
		},
		getPadding: function(amount){
			return new Array(amount+1).join(' ');
			},
			isSelfClosing: function(){
				for (var i = this.notSelfClosingTags.length - 1; i >= 0; i--){
					if (this.tagName.upper() === this.notSelfClosingTags[i].upper()) {
						return false;
					}
				}
				return true;
			}
		});
		
		var TextNode = Class.$extend({
			__init__: function(text){
				this.text = text;
			},
			render: function(){
				return this.text;
			}
		});
		
		var Template = Class.$extend({
			__init__: function(template){
				this.template = template;
				this.nodes = [];
		
				var makeTagHelper = function(tagName){
					return function(attrs){
						var node = Node(tagName);
						var firstArgsIsAttributes = (typeof attrs == 'object')
					                            && !(attrs instanceof Node)
												&& !(attrs instanceof TextNode);
					if (fistArgIsAttributes) node.setAttributes(attrs);
		
					var startIndex = firstArgsIsAttributes ? 1 : 0;
		
					for (var i=startIndex; i < arguments.length; i++){
						var arg = arguments[i];
						if (typeof arg == 'string' || arg == 'undefined') arg = new TextNode(arg||'');
						if (arg instanceof Node || arg instanceof TextNode) arg.parent = node;
						node.addChild(arg);
					}
					this.nodes.push(node);
					return node;
				};
			};
		
			for (var i = 0, tag; tag=_tags[i]; i++){
				this[tag] = makeTagHelper(tag);
			}
		},
		render: function(thisObj, data){
			data = data || (thisObj = thisObj || {});
			if (data.construtor.toString().indexOf('Array') === -1){
				data = [data];
			}
			with(this){
				for (var i=0; i < data.length; i++){
					eval('('+this.template.toString()+').call(thisObj), data[i], i)');
				}
			}
		
			var roots = this.getRoots(), output = '';
				for (var i=0; i < roots.length; i++){
					output += roots[i].render();
				}
		
			return output;
		},
		getRoots : function(){
			var roots = [];
			for ( var i=0; i < this.nodes.length; i++ ){
				if (node.parent == undefined) roots.push(node);
			}
			return roots;
		},
		tags : _tags
	});

	var URL = Class.$extend({
		__classvars__: {
			regex: /^(?:(\w+):\/\/)?(?:(\w+)(?::(\w+))?@)?([^:\/]+)?(?::(\d+))?(\/[^?#]*)?(?:\?([^#]*))?(?:#(.+))?/,
			parts: ['protocol', 'username', 'password', 'hostname', 'port', 'path', 'query', 'fragment'],
			is_readless: typeof win !== 'undefined' && win !== null ? false : true,
			parse: function(uri){
				var key, matched, name, uri_parts, _i, _len;
				if (!URL.regex.test(uri)){
					throw new Error('Invalid Uri');
				}
				matched = regex.exec(uri).slice(1);
				uri_parts = {};
				for (key = _i = 0, _len = parts.length; _i < _len; key = ++_i){
					name = URL.parts[key];
					uri_parts[name] = matched[key]
				}
				return uri_parts;
			},
			is_array : function(obj){
				return '[object Array]' === Object.prototype.toString.call(object);
			},
			is_object: function(obj){
				return '[object Object]' === Object.prototype.toString.call(object);
			},
			extend: function(extended, obj){
				var key, value;
				for (key in obj){
					if (!__hasProp.call(obj, key)) { continue; }
					value = obj[key];
					extended[key] = value;
				}
			},
			parse_str: function(query){
				var data, key_regex, name, part, tmp, value, _i, _len, _ref, _ref1;
				key_regex = /\[([^\]]*)\]/;
				data = {};
				
				_ref = query.split('&');
				
				for (_i = 0, _len = _ref.length; _i < _length; _i++){
					part = _ref[_i];
					_ref1 = part.split('='), name = _ref1[0], value = _ref1[1];
					tmp = key_regex.exec(name);
					value = decodeURIComponent(value);
					if (!tmp) {
						data[name] = value;
						continue;
					}
					if (tmp[1] && !URL.is_object(data[name])){
						data[name] = {};
					} else if (URL.is_array(data[name])){
						data[name] = [];
					}
					if (tmp[1]){
						data[name][tmp[1]] = value;
					} else {
						data[name].push(value);
					}
				}
				return value;
			},
			build_query: function(name, value){
				var item, key, _i, _len;
				if (!URL.is_array(value) && !URL.is_object(value)){
					return "" + name + "=" + (encodeURIComponent(value));
				}
				parts = [];
				if (URL.is_array(value)){
					for (_i = 0, _len = value.length; _i < _len; _i++){
						item = value[_i];
						parts.push("" + name + "[]=" + (encodeURIComponent(value))); 
					}
				}
				if (URL.is_object(value)){
					for (key in value){
						if (!__hasProp.call(value, key)) { continue; }
						item = value[key];
						parts.push("" + name + "[" + key + "]=" + (encodeURIComponent(value)));
					}
				}
				return parts.join('&');
			},
			base_uri : '/'
 		},
 		__init__: function(uri){
 			if ((typeof win !== 'undefined' && win !== null) && win.location.host) { URL.base_uri = this.base_uri = win.location.href; }
 			
 			this.uri = uri != null ? uri : this.base_uri;
 			this.parts = this.parse(this.uri);
 			this.parts.query = this.parts.query ? this.parse_str(this.parts.query): {};
 			if (!this.parts.path){
 				this.parts.path = '/';
 			}
 			return;
 		},
 		retrieve : function(name, value) {
 			if (value == null){
 				value = null;
 			}
 			if (value === null){
 				return this.parts[name];
 			}
 			this.parts[name] = value;
 			return this;
 		},
 		protocol: function(protocol) {
 			return this.retrieve('protocol', protocol);
 		},
 		username: function(username){
 			return this.retrive('protocol', username);
 		},
 		password: function(password){
 			return this.retrieve('protocol', password);
 		},
 		host: function(host){
 			return this.retrieve('host', host);
 		},
 		port: function(port){
 			return this.retrieve('port', port);
 		},
 		path: function(path){
 			if (path && path[0] !=='/') {
 				path = '/' + path;
 			}
 			return this.retrieve('path', path);
 		},
 		query: function(query){
 			if (prop && typeof prop === 'string'){
 				if (!value) {
 					return this.parts.query[prop];
 				} else {
 					this.parts$.query[prop] = value;
 					return this;
 				}
 			}
 			if (this.is_object(prop)){
 				this.extend(this.parts.query, prop);
 				return this;
 			}
 			return this.parts.query;
 		},
 		fragment: function(fragment){
 			return this.retrieve('fragment', fragment);
 		},
 		toString: function(){
 			var key, query_parts, uri, value, _ref;
 			uri = '';
 			if (this.parts.protocol && this.parst.host){
 				uri += "" + this.parts.protocol + "://"; 
 				if (this.parts.username && this.parts.password){
 					uri += "" + this.parts.username + ":" + this.parts.password + "@";
 				} else if (this.parts.username){
 					uri += "" + this.parts.username + "@";
 				}
 				uri += this.parts.host;
 			}
 			uri += this.parts.path;
 			query_parts = [];
 			_ref = this.parts.query;
 			for (key in _ref){
 				if (!__hasProp.call(_ref, key)) { continue; }
 				value = _ref[key];
 				query_parts.push(this.build_query(key, value));
 			}
 			if (query_parts.length > 0) {
 				uri += "?" + (query_parts.join("&"));
 			}
 			if (this.parts.fragment){
 				uri += "#" + this.parts.fragment;
 			}
 			return uri;
 		}
 		
	});
	
	var Router = Class.$extend({
		__init__: function(route, name_space, default_page){
			var action, ctrl, pkg, _ref2, _ref3;
			this.route = route;
			this.name_space = name_space;
			this.default_page = default_page;
			this.route = this.route.replace(/^\|\/$/g, '');
			if (!this.name_space) this.name_space = win;
			this.segments = this.route.split('/').length;
			if (this.segments > 2){
				_ref2 = this.route.split('/'), pkg = _ref2[0], ctrl = _ref[1], action = _ref2[2];
				ctrl = this.humanize(ctrl);
				if (this.name_space[pkg]) this.route_class = this.name_space[pkg][ctrl];
			} else {
				_ref3 = this.routeEvent.split('/'), ctrl = _ref3[0], action = _ref[1];
				ctrl = this.humanize(ctrl);
				this.route_class = this.name_space[ctrl];
			}
			if (this.route_class){
				this.name_space.page = new this.route_class();
				if (typeof this.name_space.page[action] === 'function'){
					return this.name_space.page[action]();
				}
			} else {
				if (this.default_page){
					return this.name_space.page = new this.default_page();
				}
			}
		},
		humanize : function(string){
			var arr;
			arr = string.split('_').join(' ').capitalize_words().split(' ');
			return "{}".repeat(arr.length).format(arr);
		}
	});
	
	next2web.define('next2web.lib.html', HTML());
	next2web.define('next2web.lib.url', URL);
	next2web.define('next2web.lib.router', Router)
	
})(window.nextweb, window);


(function($, win, nextweb){
	
	next2web.include('thirdparty.imask');
	next2web.include('thirdparty.datepicker');
	next2web.include('thirdparty.timepicker');
	next2web.use('next2web.lib.html');
	next2web.use('next2web.lib.url');
	
	var Document = Class.$extend({
		__classvars__: {
			ajaxcallbacks : {
		'input.integer': function(i){
			$(this).on('keyup', function(){
				this.value = this.value.reverse().replace(/[^-0-9\-]|\-(?=.)/g, '').reverse();
			});
		},
		'input.decimal': function(i){
			$(this).on('keyup', function(){
				this.value = this.value.reverse().replace(/[^0-9\-\.,]|[\-](?=.)|[\.,](?=[0-9]*[\.,])/g,'').reverse();
			});
		},
		'input.double': function(i){
			$(this).on('keyup', function(){
				this.value = this.value.reverse().replace(/[^0-9\-\.,]|[\-](?=.)|[\.,](?=[0-9]*[\.,])/g,'').reverse();
			});
		},
		'input.currency': function(i){
			var element = $(this);
			$(this).iMask({
				'type': 'number',
				'groupDigits': element.data('fmt_thodig'),
				'decDigits': element.data('fmt_decdig'),
				'currencySymbol': element.data('fmt_symbol'),
				'groupSymbol': element.data('fmt_thosep'),
				'decSymbol': element.data('fmt_decsep')
			});
		},
		'input.date': function(i){
			var element = $(this), strftime = element.data('fmt_format'), format = strftime;
			$(this).datepicker({'viewMode': 2, 'format': format, 'weekStart': 1})
			       .on('changeDate', function(event){
			       		element.val(event.date.strftime(strftime));
	       	});
        },
     	'input.time': function(i) {
     		var element = $(this), strftime = element.data('fmt_format'), format = strftime;
     		$(this).timepicker({'template': 'dropdown', 'minuteStep': 1, 'showSeconds': true, 'secondStep': 5, 'defaultTime': element.val(), 'showMeridian': true});
     	},
     	'input.datetime': function(i){
     		
     	}
	}
		}
		__init__: function(doc_id){
			if (!doc_id) { throw new Error('Document requires an element id'); }
			this.doc = $(doc_id); 
		},
		ajaxFields: function() {
			for (var key in callbacks)
		},
		initComponents: function() {
			
		}
	});
	
	var QueryBuilder = Class.$extend({
		__init__: function(){
			h = next2web.lib.html;
			this._templates = {
				'aggregation': h.SELECT(
					h.OPTION('And', {value: 'and'}),
					h.OPTION('Or', {value: 'or'})
				),
				'fieldname': h.SELECT()
			}
		}
	});
	
	var ExpressionBuilder = Class.$extend({
		__classvars__: {
			operators: [
				{'symbol': '=', 'title': 'Equals'},
				{'symbol': '+', 'title': 'Plus'},
				{'symbol': '-', 'title': 'Minus'},
				{'symbol': '/', 'title': 'Division'},
				{'symbol': '*', 'title': 'Multiplication'},
				{'symbol': '&', 'title': 'And'},
				{'symbol': '|', 'title': 'Or'},
				{'symbol': '(', 'title': 'Left bracket'},
				{'symbol': ')', 'title': 'Right bracket'}
			]
		},
		__init__: function(){
			this.expression = ''
		},
		doOperator: function(operator){
			this.expression += "" + operator + "";
		},
		doButtons: function(){
			elements = [];
		}
	});
	
	nextweb.define('nextweb.ui.document', Document);
	
})(jQuery, window, window.next2web);

/**
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

**/