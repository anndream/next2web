(function(win, next2web){
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
})(window, window.next2web)
