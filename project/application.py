from project.config import DefaultConfig as base_config
from flask import Flask
from project.extentions import sqldb, login_manager

DEFAULT_APP_NAME = 'project'



def create_app(app_name=DEFAULT_APP_NAME , config = None):
    
    app = Flask(
        app_name,
        static_folder='media/statics/',
        template_folder='media/templates',
    )
    configure_app(app, config)
    configure_blueprints(app)
    configure_extentions(app)
    
    return app


def configure_app(app, config):
    """
    tanzimate kolli app ke mamolan dar yek file zakhore mishavat tavasote in tabe
    megdar dehi va load mishavad
    """

    # config default ro dakhele app load mikone
    app.config.from_object(base_config())
    # sys.path.append(os.path.dirname(os.path.realpath(__file__)))
    if config is not None:
        # agar config degari be create_app ersal shode bashe dar in bakhsh load mishe
        # agar tanzimate in bakhsh gablan va dakhele defalt config tanzim shode
        # bashe dobare nevisi mishe
        app.config.from_object(config)

    # dar sorati ke environment variable baraye tanzimat set shode bashe ham
    # load mishe
    app.config.from_envvar('project_CONFIG', silent=True)

def configure_blueprints(app):

    app.config.setdefault('INSTALLED_BLUEPRINTS', [])
    blueprints = app.config['INSTALLED_BLUEPRINTS']
    for blueprint_name in blueprints:
        bp = __import__('project.apps.%s' % blueprint_name, fromlist=['views'])

        try:
            mod = __import__('project.%s' % blueprint_name, fromlist=['urls'])
        except ImportError:
            pass
        else:
            mod.urls.add_url_rules(bp.views.mod)
        try:
            app.register_blueprint(bp.views.mod)
        except:
            # report has no views
            pass

def configure_extentions(app):
    sqldb.init_app(app)
    login_manager.init_app(app)
