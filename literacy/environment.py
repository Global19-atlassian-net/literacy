from jinja2 import (
    Environment,
    DictLoader,
)
from IPython import (
    get_ipython,
)
from mistune import (
    Markdown,
    Renderer,
)
class LiterateEnvironment( Environment ):
    """A Jinja Environment that can """
    ip = get_ipython()
    def __init__(self,default_lang='python',lang_prefix='lang-', render_template=True,*args,**kwargs):
        self.renderer=Markdown(renderer=Renderer(escape=False))
        super(LiterateEnvironment,self).__init__(loader=DictLoader({}))
        self.loader.mapping['weave_code'] = """<hr><pre><code>{{code}}</code></pre>"""
        self.loader.mapping['weave_template'] = """
        {% if css %}<style>{{css}}</style>{% endif %}
        {% if html %}{{html}}<hr>{% endif %}
        {% if js %}<script>{{js}}</script>{% endif %}
        """
        self.globals["default_lang"]=default_lang
        self.globals["lang_prefix"]=lang_prefix
        self.globals["render_template"]=render_template
        self.globals['callback']={
            'python': lambda code: {
                'python': self.ip.run_cell(code),
            },
            'js': lambda code: {
                'js': code,
            },
            'css': lambda code: {
                'css': code,
            },
        }
