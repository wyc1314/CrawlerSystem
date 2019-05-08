import os
from six.moves import cPickle as pickle
import warnings

from importlib import import_module
from os.path import join, dirname, abspath, isabs, exists

from scrapy.utils.conf import closest_scrapy_cfg, get_config, init_env
from scrapy.settings import Settings
from scrapy.exceptions import NotConfigured

ENVVAR = 'SCRAPY_SETTINGS_MODULE'
DATADIR_CFG_SECTION = 'datadir'


def inside_project():
    scrapy_module = os.environ.get('SCRAPY_SETTINGS_MODULE')
    if scrapy_module is not None:
        try:
            import_module(scrapy_module)
        except ImportError as exc:
            warnings.warn("Cannot import scrapy settings module %s: %s" % (scrapy_module, exc))
        else:
            return True
    return bool(closest_scrapy_cfg())


def project_data_dir(project='default'):
    """Return the current project data dir, creating it if it doesn't exist"""
    if not inside_project():
        raise NotConfigured("Not inside a project")
    cfg = get_config()
    if cfg.has_option(DATADIR_CFG_SECTION, project):
        d = cfg.get(DATADIR_CFG_SECTION, project)
    else:
        scrapy_cfg = closest_scrapy_cfg()
        if not scrapy_cfg:
            raise NotConfigured("Unable to find scrapy.cfg file to infer project data dir")
        d = abspath(join(dirname(scrapy_cfg), '.scrapy'))
    if not exists(d):
        os.makedirs(d)
    return d


def data_path(path, createdir=False):
    """
    Return the given path joined with the .scrapy data directory.
    If given an absolute path, return it unmodified.
    """
    if not isabs(path):
        if inside_project():
            path = join(project_data_dir(), path)
        else:
            path = join('.scrapy', path)
    if createdir and not exists(path):
        os.makedirs(path)
    return path


def get_project_settings():
    # ENVVAR = 'SCRAPY_SETTINGS_MODULE'
    # os.environ环境变量
    # 当配置文件不在环境变量中时，初始化环境变量
    if ENVVAR not in os.environ:
        # project = 'default'
        project = os.environ.get('SCRAPY_PROJECT', 'default')
        # 初始化环境变量（加载scrapy.cfg，完善os.environ，获得项目所在目录）
        # os.environ['SCRAPY_SETTINGS_MODULE'] = "ScrapyTest.settings"
        init_env(project)

    settings = Settings()
    # 配置文件的路径 settings_module_path = 'ScrapyTest.settings'
    settings_module_path = os.environ.get(ENVVAR)
    if settings_module_path:
        settings.setmodule(settings_module_path, priority='project')    # 覆盖初始settings配置
    # pickled_settings = None
    pickled_settings = os.environ.get("SCRAPY_PICKLED_SETTINGS_TO_OVERRIDE")
    if pickled_settings:
        settings.setdict(pickle.loads(pickled_settings), priority='project')

    # env_overrides = {'SETTINGS_MODULE': 'ScrapyTest.settings'}
    env_overrides = {k[7:]: v for k, v in os.environ.items() if
                     k.startswith('SCRAPY_')}
    if env_overrides:
        settings.setdict(env_overrides, priority='project')    # 设置模块'SETTINGS_MODULE': 'ScrapyTest.settings',

    return settings
