(function init(win){
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
	String.prototype.index = String.prototype.indexOf;
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
	String.prototype.chop = function(){
		return this.slice(0, this.length-2);
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
		if (!start && typeof this[0] !== 'undefined'){ start = this[0]; }
		if (!end && typeof this[1] !== 'undefined'){ end =  this[1]; } 
		if (!step && typeof this[2] !== 'undefined'){ step = this[2]}
		
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
	Array.prototype.count = function(){ return this.length };
	Array.prototype.sum = function(start, end){
		var sum = 0, 
		    start = start ? start : 0,
		    end = end ? end : this.count() - start;
		end = start ? end + 2 : end;
		for (var i = start; i < end; i++) { sum += this[i] }
		return sum;
	}
	
})(window);

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

	var _createStyle = function(data){
		var style = document.createElement('style');
		style.type='text/css'
		style.text=data;
		
		document.body.appendChild(style)
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
		mapIdentifierToUri : function(identifier, ext){
			var regexp = new RegExp('\\' + this.separator, 'g');
			return this.baseUri + identifier.replace(regexp, '/') + (!ext) ? '.js' : ext;
		},
		_loadScript : function(identifier){
			var sucessCallback = arguments[2] || function(){};
			var errorCallback = arguments[3];
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
		_loadStyle: function(identifier){
		    var sucessCallback = arguments[2] || function(){};
			var errorCallback = arguments[3];
			var async = typeof successCallback === 'function';
			var uri = this.mapIdentifierToUri(identifier, '.css');
			var event = {'identifier': identifier, 'uri': uri, 'async': async, 'callback': sucessCallback};
			
			var xhr = _createXmlHttpRequest();
			xhr.open('GET', uri, async);
			
			if (async) {
				xhr.onreadystatechange = function() {
					if (xhr.readyState == 4) {
						if (_isHttpRequestSucessful(xhr.status || 0)) {
							_createStyle(xhr.responseText);
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
		include : function(identifier, css){
			var sucessCallback = arguments[2] || false;
			var errorCallback = arguments[2] || false;
			if (!typeof this._includedIdentifiers[identifier] === 'undefined') {
				if (typeof sucessCallback === 'function') { sucessCallback(); }
				return true;
			}
			
			if (css){
				this._loadStyle(identifier);
			}
			
			if (sucessCallback){
				this._loadScript(identifier, function(){
					this._includedIdentifiers[identifier] = true;
					sucessCallback();
				}, errorCallback);
			} else {
				if(this._loadScript(identifier)){
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
