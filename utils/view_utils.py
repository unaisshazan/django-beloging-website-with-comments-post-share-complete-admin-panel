import datetime
from django.core.paginator import Paginator
from django.conf import settings
from django.utils.safestring import mark_safe


class PaginationContextMixin(object):
    
    def update_pagination_context(self,context):
        if len(self.object_list) > settings.MAX_PAGINATION_ITEMS_PER_PAGE:
            context['paginate'] = True
            p = Paginator(self.object_list,settings.MAX_PAGINATION_ITEMS_PER_PAGE)
            page = p.page(int(self.request.GET.get('page',1)))
            context['page'] = page
            context['pages'] = p.page_range
            context['object_list'] = page.object_list
        
        return




class ModelToHtml(object):
    """ html output for fields by verbose name, in the order provided"""
    
    simple_row_template =  "{row_start} {label} {divider} {value} {row_end} \n"
    styled_row_template = '{row_start}<span class="label label-info p-r-10"> {label} </span> {divider}  <span class="panel panel-default" style="border:none;padding-left:10px;">{value}</span> {row_end} \n'
    obj = None
    
    def __init__(self,model,fields):
        
        self.model = model
        self.Lfields = fields
        s = set(model._meta.get_all_field_names())
        assert set(fields).issubset(s)
             
    def _row(self,row_template,field_name,value,row_start,row_end, divider="    "):
        
        label = self.model._meta.get_field(field_name).verbose_name
        return row_template.format(row_start=row_start,label=label,row_end=row_end,divider=divider,value=value)
        
    def _output_html(self,tag,row_template):
        
        html_output = ""
        for field_name in self.Lfields:
            value = getattr(self.obj,field_name)
            if isinstance(value,datetime.datetime):
                value = value.strftime(settings.DATETIME_FULL_STRFTIME)
            else:
                value = str(value)
            
            html_output = html_output + self._row(row_template,field_name,value,"<%s>"%tag,"</%s>"%tag)
            
        return mark_safe(html_output)
    
    def as_p(self):
        
        return self._output_html("p",self.simple_row_template)
    
    def styled(self):
        
        return self._output_html("h4",self.styled_row_template)
    
    
class ModelToHtmlMixin(object):
    
    model_to_html_fields = None
    model_to_html = None
    
    def __init__(self,*args,**kwargs):
        
        model = self.model_to_html if self.model_to_html != None else self.model
        self.model_html = ModelToHtml(model, self.model_to_html_fields)
    
    def get_context_data(self,*args,**kwargs):
        
        context = super(ModelToHtmlMixin,self).get_context_data(*args,**kwargs)
        self.model_html.obj = self.object
        context ['model_html'] = self.model_html
        return context
        
            
            
            
        
        
            
        
        
        
        
        
        