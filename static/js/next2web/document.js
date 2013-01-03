(function($, win, nextweb){
	
	next2web.include('thirdparty.imask');
	next2web.include('thirdparty.datelib');
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
		     	'div.datetime-control': function(i){
		     		var element = $(this), 
		     		    dateelement = $('input[name^="datepart_for"]', element),
		     		    timeelement = $('input[name^="timepart_for"]', element),
		     		    date_format = dateelement.data('fmt_format'),
		     		    time_format = timeelement.data('time_format'),
		     		    date;
		     		function onchange(event){
		     			date = dateelement.val() + ' ' + timelement.val();
		     			date = new Date().strptime(date, date_format + ' ' + time_format);
		     			element.val(date);
		     		}
		     		dateelement.on('onchange', onchange);
		     		timeelement.on('onchange', onchange);
		     	}
		    }
		},
		__init__: function(doc_id){
			if (!doc_id) { throw new Error('Document requires an element id'); }
			this.doc = $(doc_id); 
			this.ajaxFields();
		},		
		ajaxFields: function() {
			for (var key in this.ajaxcallbacks){
				$(key, this.doc).each(this.ajaxcallbacks[key]);
			}
		},
	});
	
	var SimpleComponent = Class.$extend({
		__init__: function(target){
			if (!target) {throw new Error('SimpleComponent requires an name.')}
			this.element = $(target);
			this.target = target;
		},
		build: function(){
			throw new Error('NotImplementedError')
		}
	})
	
	var ManyChilds = SimpleComponent.$extend({
		build: function(){
			next2web.include('thirdparty.Grid.Grid')
			
			this.childs = new Grid(this.target + "_grid", {
				srcType: 'dom',
				srcData: this.target,
				fixedCols: 1
			});
			
			this.doActions();
			
		},
		doActions: function(){
			$class = this;
			$('a[data-target="new"]', $(this.target + '_grid')).on('click', function(event){
				$.get($(this).data('url'), function(data){
					$class.doDialog(data)
				});
			});
		},
	})
	
	nextweb.define('nextweb.ui.document', Document);
	
})(jQuery, window, window.next2web);
