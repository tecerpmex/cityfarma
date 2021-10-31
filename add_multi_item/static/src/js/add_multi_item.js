odoo.define('add_multi_item.AddMulti',function (require) {
"use strict";
	var ViewDialog = require("web.view_dialogs");
	var core = require("web.core");
	var ListEditRenderer = require("web.EditableListRenderer");
	var ListRenderer = require('web.ListRenderer');
	var FieldReg = require("web.field_registry");
	var FieldOne2Many = FieldReg.get("one2many");
	var _t = core._t;
	var loader=function(records,renderer,fieldName,startRowIndex){
		var exector= function (resolve,reject){
			var data_context = this;
			renderer.trigger_up('add_record', {
				onSuccess:() => {
					var recordID = renderer._getRecordID(renderer.currentRow);
					var recordWidgets = renderer.allFieldWidgets[recordID];
					_.each(recordWidgets,widget　=>　{
						if(widget.name == fieldName){
							widget.reinitialize(data_context).then(resolve());
						}
					});								
			}});						
		};
		var job = function() {
			return new Promise(_.bind(exector,this));
		};
		var sequece= data => {
			var promise = Promise.resolve();
			var sequeceIndex = 0;
			// 串联promise
			_.each(data,item => {
				sequeceIndex++;
				if(_.size(data) == sequeceIndex){
					// 最后一个job完成以后，重新定位到起始行．
					promise = promise.then(item).then(()=>{
						renderer._selectRow(startRowIndex);
					})
				}else{
					promise = promise.then(item);
				}
			});
			return promise;
		}
		// 创建任务队列
		var jobs = [];
		_.each(records,item => {
			// 绑定数据
			jobs.push(_.bind(job,item));
		});
		sequece(jobs);
	}
	FieldReg.get('many2one').include({
		_getSearchCreatePopupOptions: function(view, ids, context, dynamicFilters) {
			var self=this;
			var options = this._super.apply(this,arguments);
			options = _.extend(options,{disable_multiple_selection:false,});
			if(_.has(this,'nodeOptions') && (!_.has(this.nodeOptions,'create_row') || !this.nodeOptions.create_row)){
				return options;
			}			
			return _.extend(options,{				
				on_selected: function (records) {					
					var parent=self.getParent();								
					var rowIndex= parent.currentRow;		
					parent.trigger_up("fill_batch_record",{select_data:records,batch_field:self.name,currentId:self.dataPointID,row_index:rowIndex});
	            },
			});
		}
	});
	ListRenderer.include({
		init:function(parent, state, params){
			this._super.apply(this,arguments);
			if(this.addCreateLine){
				var add_batch = false;
				var batch_field = false;
				var fieldsList = _.each(this.state.fieldsInfo.list,(field,key,list)=>{
					if (batch_field){
						return;
					}
					if(field.options && _.has(field.options,'add_batch_out') && field.options.add_batch_out){
						batch_field = key;
						return;
					}
				});
				if(batch_field){
					this.creates.unshift({
						string:_t('Add Multi Item'),
						context:JSON.stringify({add_batch:true,batch_field:batch_field})
					});
				}
			}
		},
		_onAddRecord: function (ev) {
	        ev.preventDefault();
	        ev.stopPropagation();
	        var self = this;
	        var evContext = ev.currentTarget.dataset.context && ev.currentTarget.dataset.context 
	        if(evContext && evContext.indexOf("add_batch")>=0){
	        	var context = JSON.parse(evContext);
	        	if(context.add_batch && context.batch_field){
	        		self.trigger_up('add_batch_record',{batch_field:context.batch_field});
	        	}
	        	return $.when();
	        }
	        return this._super.apply(this,arguments);
	    }
	});
	FieldOne2Many.include({
		custom_events:_.extend({},FieldOne2Many.prototype.custom_events,{
			add_batch_record:'_onAddBatchRecord',
			fill_batch_record:'_onFillBatchRecord'
		}),
		_onAddBatchRecord:function(ev){
			var self = this;
			ev.stopPropagation();
			var batch_field = ev.data.batch_field;
			var field = this.view.viewFields[batch_field];
			return new ViewDialog.SelectCreateDialog(this,{
			 	res_model: field.relation,
	            title: _t("Search: "),
	            initial_view: 'search',
	            context:self.value.getContext(),
	            disable_multiple_selection: false,
	            no_create: true,
	            on_selected: function (records) {	
	            	var renderer = self.renderer;
	            	var rowIndex=renderer.currentRow;
	            	if(rowIndex==null){
	            		rowIndex=renderer.state.count;
	            	}
					//loader(records,renderer,batch_field,rowIndex);
					renderer.trigger_up("fill_batch_record",{select_data:records,batch_field:batch_field,row_index:rowIndex});
	            },
	            on_closed: function () {
	            },
		}).open();
		},
		_onFillBatchRecord:function(ev){
			var self = this;
			ev.stopPropagation();
			if(!ev.data.select_data || this.viewType!='form' || !(this.mode === 'edit' && this.editable)){
				return $.when();
			}	
			var controller = this.getParent().getParent();
			var model = controller.model;
			var recordID = this.dataPointID;
			var recordModel = this.field.relation;
			var name = this.name;
			var records = ev.data.select_data;
			var batch_field =  ev.data.batch_field;
			var batchId =_.uniqueId();			
			var create_changes = {};
			var update_changes ={};
			var create_cmds = [];
			var update_cmds = [];
			var first_row = ev.data.currentId;
			var createIndex=0;
			var rowIndex = ev.data.row_index? ev.data.row_index:0;
			_.each(records,record=>{
				if(!(first_row && createIndex==0)){
					create_cmds.push({
						context:[_.extend({},{_addBatchID:batchId})],
						operation:'CREATE',
						position:self.editable || 'bottom'
					});
				}
				createIndex++;
			});
			create_changes[name]={commands:create_cmds,
								  operation:'MULTI'
								  };
			var event = {
					data:{
						changes:create_changes,
						dataPointID:recordID,
						viewType:this.viewType,
						notifyChange:true
					},
					stopped:true,
					name:"field_changed",
					target:self,
			};
			var update_batch = function(){
				var addRecordIDs = [];
				_.each(model.localData,function(value,key,list){
					if(value.model == recordModel && value.context && value.context._addBatchID==batchId){
						addRecordIDs.push(value.id);
					}
				})
				if(first_row){
					addRecordIDs.unshift(first_row);
				}
				if (_.size(addRecordIDs)>0){
					var index=0;
					_.each(records,record=>{
						var data = {};
						data[batch_field]=record;
						update_cmds.push({
							operation:'UPDATE',
							id:addRecordIDs[index],
							data:data,
						})
						index++;
					});
					update_changes[name]={
							  operation:'MULTI',
							  commands:update_cmds
							  };
					var update_event ={
							data:{
								changes:update_changes,
								dataPointID:recordID,
								viewType:self.viewType,
								notifyChange:true
							},
							stopped:true,
							name:"field_changed",
							target:self,
					};
					controller._applyChanges(recordID,update_changes,update_event).then(function(){
						self.renderer._selectRow(rowIndex);
					});
				}
			}
			controller._applyChanges(recordID,create_changes,event).then(function(){
				update_batch();
			});
		}
	});
});