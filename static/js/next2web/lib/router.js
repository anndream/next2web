(function(win, next2web){
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
	next2web.define('next2web.lib.router', Router)	
})(window, window.next2web)
